using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Text;
using UnityEngine.Networking;

/// <summary>
/// Gestiona el flujo de inicio de la aplicación:
///   1. El usuario elige cuántas clases (2 ó 3).
///   2. Se desbloquea el dropdown de clase para generar nubes manualmente.
///   3. Por cada clase el usuario ingresa media, desviación, cantidad y distribución.
///   4. Al completar TODAS las nubes requeridas se habilita el botón "Entrenar".
///   5. "Crear Objetos Entrenamiento" empieza deshabilitado.
/// </summary>
public class GestorPerceptrpon : MonoBehaviour
{
    // ─── Configuración ────────────────────────────────────────────────────────
    [Header("URL del servidor Flask")]
    public string urlBase = "http://localhost:5000";

    // ─── Referencias UI ───────────────────────────────────────────────────────
    [Header("Selección de clases")]
    public TMP_Dropdown dropdownNumClases;      // Opciones: "2 clases", "3 clases"

    [Header("Parámetros de la nube")]
    public TMP_Dropdown dropdownClaseActual;    // Opciones: "Clase 1", "Clase 2", "Clase 3"
    public TMP_InputField inputMedia;
    public TMP_InputField inputDesviacion;
    public TMP_InputField inputCantidad;
    public TMP_Dropdown dropdownDistribucion;   // Opciones: "normal", "uniforme", "exponencial"

    [Header("Botones")]
    public Button botonGenerarNube;
    public Button botonEntrenar;
    public Button botonCrearObjetosEntrenamiento;

    [Header("Feedback (opcional)")]
    public TextMeshProUGUI textoEstado;

    // ─── Estado interno ───────────────────────────────────────────────────────
    private int numClasesRequeridas = 2;
    private HashSet<int> clasesConNube = new HashSet<int>();

    // ─────────────────────────────────────────────────────────────────────────
    void Start()
    {
        // Estado inicial: sólo el selector de número de clases está habilitado
        dropdownClaseActual.interactable = false;
        botonGenerarNube.interactable = false;
        botonEntrenar.interactable = false;
        botonCrearObjetosEntrenamiento.interactable = false;

        dropdownNumClases.onValueChanged.AddListener(OnNumClasesChanged);

        ActualizarTextoEstado("Selecciona el número de clases para comenzar.");
    }

    // ─── Selección del número de clases ──────────────────────────────────────
    /// <summary>Llamado cuando el usuario cambia el dropdown de número de clases.</summary>
    public void OnNumClasesChanged(int index)
    {
        numClasesRequeridas = index + 2; // índice 0 → 2 clases, índice 1 → 3 clases
        clasesConNube.Clear();

        ActualizarDropdownClases();

        dropdownClaseActual.interactable = true;
        botonGenerarNube.interactable = true;
        botonEntrenar.interactable = false;

        ActualizarTextoEstado($"Clases requeridas: {numClasesRequeridas}. Genera una nube por cada clase.");

        StartCoroutine(PostSetNumClases(numClasesRequeridas));
    }

    /// <summary>Rellena el dropdown de clase según cuántas clases se requieren.</summary>
    private void ActualizarDropdownClases()
    {
        dropdownClaseActual.ClearOptions();

        var opciones = new List<TMP_Dropdown.OptionData>
        {
            new TMP_Dropdown.OptionData("Clase 1"),
            new TMP_Dropdown.OptionData("Clase 2")
        };

        if (numClasesRequeridas == 3)
            opciones.Add(new TMP_Dropdown.OptionData("Clase 3"));

        dropdownClaseActual.AddOptions(opciones);
        dropdownClaseActual.value = 0;
        dropdownClaseActual.RefreshShownValue();
    }

    // ─── Generar nube ─────────────────────────────────────────────────────────
    /// <summary>Llamado al pulsar el botón "Generar Nube".</summary>
    public void BotonGenerarNube()
    {
        // Leer y normalizar entradas (soporta tanto ',' como '.')
        string mediaStr      = inputMedia.text.Replace(',', '.');
        string desviacionStr = inputDesviacion.text.Replace(',', '.');
        string cantidadStr   = inputCantidad.text.Trim();
        string distribucion  = dropdownDistribucion.options[dropdownDistribucion.value].text.ToLower();

        // Validar que los campos no estén vacíos
        if (string.IsNullOrEmpty(mediaStr) || string.IsNullOrEmpty(desviacionStr) || string.IsNullOrEmpty(cantidadStr))
        {
            ActualizarTextoEstado("Por favor completa todos los campos antes de generar la nube.");
            return;
        }

        if (!float.TryParse(mediaStr,      System.Globalization.NumberStyles.Float,
                            System.Globalization.CultureInfo.InvariantCulture, out float media) ||
            !float.TryParse(desviacionStr, System.Globalization.NumberStyles.Float,
                            System.Globalization.CultureInfo.InvariantCulture, out float desviacion) ||
            !int.TryParse(cantidadStr, out int cantidad) || cantidad <= 0)
        {
            ActualizarTextoEstado("Valores inválidos. Verifica media, desviación y cantidad.");
            return;
        }

        // La clase en el backend es 0-based igual que el índice del dropdown
        int claseSeleccionada = dropdownClaseActual.value;

        StartCoroutine(PostGenerarNube(media, desviacion, cantidad, distribucion, claseSeleccionada));
    }

    // ─── Verificación de nubes completadas ───────────────────────────────────
    /// <summary>Devuelve true cuando se han generado nubes para todas las clases requeridas.</summary>
    private bool TodasNubesCreadas()
    {
        return clasesConNube.Count >= numClasesRequeridas;
    }

    // ─── Corrutinas HTTP ──────────────────────────────────────────────────────
    private IEnumerator PostSetNumClases(int numClases)
    {
        string json = $"{{\"num_clases\": {numClases}}}";
        using (UnityWebRequest req = new UnityWebRequest(urlBase + "/set_num_clases", "POST"))
        {
            byte[] bodyRaw = Encoding.UTF8.GetBytes(json);
            req.uploadHandler   = new UploadHandlerRaw(bodyRaw);
            req.downloadHandler = new DownloadHandlerBuffer();
            req.SetRequestHeader("Content-Type", "application/json");
            yield return req.SendWebRequest();

            if (req.result != UnityWebRequest.Result.Success)
                Debug.LogWarning($"set_num_clases error: {req.error}");
        }
    }

    private IEnumerator PostGenerarNube(float media, float desviacion, int cantidad, string distribucion, int clase)
    {
        // Formatear con punto decimal para el servidor
        string mediaFmt      = media.ToString(System.Globalization.CultureInfo.InvariantCulture);
        string desviacionFmt = desviacion.ToString(System.Globalization.CultureInfo.InvariantCulture);

        string json = $"{{\"media\": {mediaFmt}, \"desviacion\": {desviacionFmt}, " +
                      $"\"cantidad\": {cantidad}, \"distribucion\": \"{distribucion}\", \"clase\": {clase}}}";

        using (UnityWebRequest req = new UnityWebRequest(urlBase + "/generar_nube", "POST"))
        {
            byte[] bodyRaw = Encoding.UTF8.GetBytes(json);
            req.uploadHandler   = new UploadHandlerRaw(bodyRaw);
            req.downloadHandler = new DownloadHandlerBuffer();
            req.SetRequestHeader("Content-Type", "application/json");
            yield return req.SendWebRequest();

            if (req.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"generar_nube error: {req.error}");
                ActualizarTextoEstado("Error al conectar con el servidor.");
                yield break;
            }

            // Registrar la clase como generada
            clasesConNube.Add(clase);

            if (TodasNubesCreadas())
            {
                botonEntrenar.interactable = true;
                ActualizarTextoEstado("¡Todas las nubes generadas! Puedes entrenar el perceptrón.");
            }
            else
            {
                int faltantes = numClasesRequeridas - clasesConNube.Count;
                ActualizarTextoEstado($"Nube de clase {clase + 1} generada. Faltan {faltantes} nube(s).");
            }

            // Notificar para que otra parte del sistema (visualizador) procese los objetos
            OnNubeGenerada(req.downloadHandler.text, clase);
        }
    }

    // ─── Punto de extensión para la visualización ─────────────────────────────
    /// <summary>
    /// Sobrescribir o suscribirse desde otro script para procesar la respuesta JSON
    /// y renderizar los objetos 3D en la escena.
    /// </summary>
    protected virtual void OnNubeGenerada(string responseJson, int clase)
    {
        // Implementar en subclase o conectar mediante UnityEvent/delegate según el proyecto
        Debug.Log($"Nube clase {clase} generada. Respuesta: {responseJson}");
    }

    // ─── Helpers ──────────────────────────────────────────────────────────────
    private void ActualizarTextoEstado(string mensaje)
    {
        if (textoEstado != null)
            textoEstado.text = mensaje;
        Debug.Log("[GestorPerceptrpon] " + mensaje);
    }
}

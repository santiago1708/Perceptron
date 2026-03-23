class objeto:

    def __init__(self, x, y, z, clase, color):
        self.posX = x
        self.posY = y 
        self.posZ = z
        self.clase = clase
        self.color = color
        self.sumatoria = (x + y + z)
        

    def informacion(self):
        return f"Pos: ({self.posX}, {self.posY}, {self.posZ}) | Clase: {self.clase} | Color: {self.color} | Sumatoria: {self.sumatoria}"

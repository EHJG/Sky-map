filename = 'C:\Users\Enrique\Documents\Carpeta de trabajo\IAU-CSN.txt'  # Reemplaza "ruta_del_archivo.txt" con la ubicación real de tu archivo
position = 16337

with open(filename, 'rb') as file:
    file.seek(position)
    byte = file.read(1)

print("El byte en la posición 16337 es:", byte)
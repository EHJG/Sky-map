import json
import csv

def leer_archivo_texto(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            contenido = archivo.read()
        return contenido
    except FileNotFoundError:
        print(f"Error: Archivo '{nombre_archivo}' no encontrado.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def leer_archivo_json(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf8') as archivo:
            datos = json.load(archivo)
        return datos
    except FileNotFoundError:
        print(f"Error: Archivo '{nombre_archivo}' no encontrado.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Error al decodificar JSON - {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def leer_archivo_csv(nombre_archivo, delimitador=','):
    try:
        with open(nombre_archivo, 'r', newline='') as archivo:
            lector = csv.DictReader(archivo, delimiter=delimitador)
            datos = [fila for fila in lector]
        return datos
    except FileNotFoundError:
        print(f"Error: Archivo '{nombre_archivo}' no encontrado.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def exportar_archivo_texto(nombre_archivo, contenido):
    try:
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(contenido)
        print(f"Contenido exportado exitosamente a '{nombre_archivo}'.")
    except Exception as e:
        print(f"Error: {e}")

def exportar_archivo_json(nombre_archivo, datos):
    try:
        with open(nombre_archivo, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
        print(f"Datos exportados exitosamente a '{nombre_archivo}'.")
    except Exception as e:
        print(f"Error: {e}")

def exportar_archivo_csv(nombre_archivo, datos, nombres_campos, delimitador=','):
    """
    Exporta los datos a un archivo CSV con los nombres de campos proporcionados.

    :param nombre_archivo: Nombre del archivo CSV de destino.
    :type nombre_archivo: str
    :param datos: Lista de diccionarios que contienen los datos a exportar.
    :type datos: list of dict
    :param nombres_campos: Lista de nombres de campos para las columnas del CSV.
    :type nombres_campos: list of str
    :param delimitador: Carácter delimitador para el CSV (por defecto: ',').
    :type delimitador: str, optional
    """
    try:
        with open(nombre_archivo, 'w', newline='') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=nombres_campos, delimiter=delimitador)
            escritor.writeheader()
            escritor.writerows(datos)
        print(f"Datos exportados exitosamente a '{nombre_archivo}'.")
    except Exception as e:
        print(f"Error: {e}")

def exportar_lista_csv(nombre_archivo, lista_datos, delimitador=','):
    """
    Exporta una lista de datos a un archivo CSV.

    :param nombre_archivo: Nombre del archivo CSV de destino.
    :type nombre_archivo: str
    :param lista_datos: Lista de datos a exportar.
    :type lista_datos: list
    :param delimitador: Carácter delimitador para el CSV (por defecto: ',').
    :type delimitador: str, optional
    """
    try:
        with open(nombre_archivo, 'w', newline='') as archivo:
            escritor = csv.writer(archivo, delimiter=delimitador)
            for fila in lista_datos:
                escritor.writerow(fila)
        print(f"Datos exportados exitosamente a '{nombre_archivo}'.")
    except Exception as e:
        print(f"Error: {e}")
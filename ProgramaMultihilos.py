import os
import time
import pyautogui
from shutil import copy2
from mutagen import File
from mutagen.easyid3 import EasyID3

# Directorios de origen
desktop_dir = os.path.expanduser("\\Users\\ismad\\OneDrive\\Desktop")
documents_dir = os.path.expanduser("\\Users\\ismad\\OneDrive\\Documentos\\Music")

# Directorio de destino
destination_dir = os.path.expanduser("\\Users\\ismad\\OneDrive\\Desktop\\Organized_Music")

# Directorio de destino para las capturas de pantalla
screenshot_dir = os.path.expanduser("\\Users\\ismad\\OneDrive\\Desktop\\Screenshots")

# Función para obtener la información de metadata de un archivo MP3
def get_metadata(file_path):
    try:
        audio = EasyID3(file_path)
        print(f"Encontro el archivo mp3 {file_path}")
        return audio
    except Exception as e:
        print(f"Error al leer la metadata de {file_path}: {str(e)}")
        return None

# Función para copiar y organizar los archivos
def organize_music():
    # Crear el directorio de destino para las capturas de pantalla si no existe
    os.makedirs(screenshot_dir, exist_ok=True)
    # Crear el directorio de destino si no existe
    os.makedirs(destination_dir, exist_ok=True)

    # Recorrer los directorios de origen
    for directory in [desktop_dir, documents_dir]:
        # Obtener todos los archivos del directorio
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # Comprobar si es un archivo MP3
                if file.endswith(".mp3"):
                    metadata = get_metadata(file_path)
                    if metadata:
                        # Obtener los atributos de la metadata
                        year = metadata.get('date', ['Unknown Year'])[0]
                        album = metadata.get('album', ['Unknown Album'])[0]

                        # Crear los directorios para el año y álbum si no existen
                        year_dir = os.path.join(destination_dir, year)
                        os.makedirs(year_dir, exist_ok=True)
                        album_dir = os.path.join(year_dir, album)
                        os.makedirs(album_dir, exist_ok=True)

                        # Copiar el archivo al directorio correspondiente
                        destination_file = os.path.join(album_dir, file)
                        copy2(file_path, destination_file)
    # Capturar y guardar capturas de pantalla cada 5 milisegundos
    counter = 1
    total_files = sum([len(files) for _, _, files in os.walk(destination_dir)])
    while counter <= total_files:
        screenshot_path = os.path.join(screenshot_dir, f"screenshot{counter}.png")
        pyautogui.screenshot(screenshot_path)
        print(f"Captura de pantalla {counter} guardada: {screenshot_path}")
        counter += 1
        time.sleep(0.005)

# Ejecutar la función principal
organize_music()

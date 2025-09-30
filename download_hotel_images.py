import os
import json
import requests
import re
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image
import io

# Configuración de optimización de imágenes
MAX_WIDTH_LARGE = 1200  # Para imágenes principales
MAX_WIDTH_MEDIUM = 800   # Para galería
MAX_WIDTH_SMALL = 400    # Para miniaturas
WEBP_QUALITY = 85       # Calidad WebP (0-100)

# Función para limpiar nombres de archivos
def sanitize_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = filename.replace(" ", "_")
    return filename

# Función para descargar una imagen
def download_image(url):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error al descargar {url}: {e}")
        return None

# Función para optimizar y convertir a WebP
def optimize_image(image_data, max_width, output_path):
    try:
        # Abrir la imagen desde los datos descargados
        img = Image.open(io.BytesIO(image_data))
        
        # Convertir a RGB si es necesario (WebP no soporta RGBA con transparencia en algunos casos)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Calcular nuevas dimensiones manteniendo la proporción
        original_width, original_height = img.size
        if original_width > max_width:
            new_height = int(original_height * (max_width / original_width))
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Guardar como WebP con la calidad especificada
        img.save(output_path, 'WEBP', quality=WEBP_QUALITY, optimize=True)
        print(f"Optimizada: {output_path}")
        return True
    except Exception as e:
        print(f"Error al optimizar imagen: {e}")
        return False

# Cargar el archivo JSON
def load_hotels_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Guardar el JSON actualizado
def save_hotels_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Procesar cada hotel
def process_hotels(hotels_data, base_dir):
    updated_hotels = []
    
    for hotel in hotels_data:
        hotel_id = hotel['id']
        hotel_name = sanitize_filename(hotel['nombre'])
        
        # Crear directorio para el hotel en static/images/hotels/
        hotel_dir = os.path.join(base_dir, 'hotels', hotel_id)
        os.makedirs(hotel_dir, exist_ok=True)
        
        print(f"\nProcesando hotel: {hotel['nombre']} ({hotel_id})")
        print(f"Directorio: {hotel_dir}")
        
        # Procesar imagen principal del hotel
        if 'imagenes' in hotel and 'hotel' in hotel['imagenes']:
            hotel_img_url = hotel['imagenes']['hotel']
            image_data = download_image(hotel_img_url)
            
            if image_data:
                output_path = os.path.join(hotel_dir, "hotel.webp")
                if optimize_image(image_data, MAX_WIDTH_LARGE, output_path):
                    # Actualizar la ruta en el JSON para usar la nueva estructura
                    hotel['imagenes']['hotel'] = f"static/images/hotels/{hotel_id}/hotel.webp"
        
        # Procesar imágenes de la película
        if 'imagenes' in hotel and 'pelicula' in hotel['imagenes']:
            pelicula_imgs = hotel['imagenes']['pelicula']
            if isinstance(pelicula_imgs, list):
                updated_pelicula_imgs = []
                for i, img_url in enumerate(pelicula_imgs):
                    image_data = download_image(img_url)
                    if image_data:
                        output_path = os.path.join(hotel_dir, f"pelicula_{i+1}.webp")
                        if optimize_image(image_data, MAX_WIDTH_MEDIUM, output_path):
                            updated_pelicula_imgs.append(f"static/images/hotels/{hotel_id}/pelicula_{i+1}.webp")
                hotel['imagenes']['pelicula'] = updated_pelicula_imgs
            else:
                image_data = download_image(pelicula_imgs)
                if image_data:
                    output_path = os.path.join(hotel_dir, "pelicula.webp")
                    if optimize_image(image_data, MAX_WIDTH_MEDIUM, output_path):
                        hotel['imagenes']['pelicula'] = f"static/images/hotels/{hotel_id}/pelicula.webp"
        
        # Procesar imágenes de la galería
        if 'imagenes' in hotel and 'galeria' in hotel['imagenes']:
            updated_galeria_imgs = []
            for i, img_url in enumerate(hotel['imagenes']['galeria']):
                image_data = download_image(img_url)
                if image_data:
                    output_path = os.path.join(hotel_dir, f"galeria_{i+1}.webp")
                    if optimize_image(image_data, MAX_WIDTH_MEDIUM, output_path):
                        updated_galeria_imgs.append(f"static/images/hotels/{hotel_id}/galeria_{i+1}.webp")
            hotel['imagenes']['galeria'] = updated_galeria_imgs
        
        updated_hotels.append(hotel)
    
    return updated_hotels

# Función principal
def main():
    # Rutas
    current_dir = Path(__file__).parent
    json_path = os.path.join(current_dir, 'data', 'hotels.json')
    img_base_dir = os.path.join(current_dir, 'static', 'images')
    
    # Crear directorio base para imágenes si no existe
    os.makedirs(img_base_dir, exist_ok=True)
    
    # Cargar datos de hoteles
    print("Cargando datos de hoteles...")
    hotels_data = load_hotels_json(json_path)
    
    # Procesar hoteles y descargar imágenes
    print("\nProcesando hoteles y descargando imágenes...")
    updated_hotels = process_hotels(hotels_data, img_base_dir)
    
    # Guardar JSON actualizado
    print("\nGuardando JSON actualizado...")
    save_hotels_json(updated_hotels, json_path)
    
    print("\n¡Proceso completado!")

if __name__ == "__main__":
    main()
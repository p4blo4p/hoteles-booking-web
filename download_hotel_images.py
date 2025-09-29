import os
import json
import requests
import re
from pathlib import Path
from urllib.parse import urlparse

# Función para limpiar nombres de archivos
def sanitize_filename(filename):
    # Eliminar caracteres inválidos y reemplazar espacios
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = filename.replace(" ", "_")
    return filename

# Función para descargar una imagen
def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Descargada: {save_path}")
        return True
    except Exception as e:
        print(f"Error al descargar {url}: {e}")
        return False

# Función para obtener la extensión de una URL
def get_extension(url):
    parsed = urlparse(url)
    path = parsed.path
    ext = os.path.splitext(path)[1]
    if not ext:
        # Si no hay extensión, intentar obtenerla del content-type
        try:
            response = requests.head(url, timeout=5)
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                return '.jpg'
            elif 'png' in content_type:
                return '.png'
            elif 'gif' in content_type:
                return '.gif'
            elif 'webp' in content_type:
                return '.webp'
        except:
            pass
        return '.jpg'  # Extensión por defecto
    return ext

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
        
        # Crear directorio para el hotel
        hotel_dir = os.path.join(base_dir, hotel_id)
        os.makedirs(hotel_dir, exist_ok=True)
        
        print(f"\nProcesando hotel: {hotel['nombre']} ({hotel_id})")
        print(f"Directorio: {hotel_dir}")
        
        # Procesar imagen principal del hotel
        if 'imagenes' in hotel and 'hotel' in hotel['imagenes']:
            hotel_img_url = hotel['imagenes']['hotel']
            ext = get_extension(hotel_img_url)
            hotel_img_path = os.path.join(hotel_dir, f"hotel{ext}")
            
            if download_image(hotel_img_url, hotel_img_path):
                # Actualizar la ruta en el JSON
                hotel['imagenes']['hotel'] = f"data/img/{hotel_id}/hotel{ext}"
        
        # Procesar imágenes de la película
        if 'imagenes' in hotel and 'pelicula' in hotel['imagenes']:
            pelicula_imgs = hotel['imagenes']['pelicula']
            if isinstance(pelicula_imgs, list):
                updated_pelicula_imgs = []
                for i, img_url in enumerate(pelicula_imgs):
                    ext = get_extension(img_url)
                    img_path = os.path.join(hotel_dir, f"pelicula_{i+1}{ext}")
                    if download_image(img_url, img_path):
                        updated_pelicula_imgs.append(f"data/img/{hotel_id}/pelicula_{i+1}{ext}")
                hotel['imagenes']['pelicula'] = updated_pelicula_imgs
            else:
                ext = get_extension(pelicula_imgs)
                img_path = os.path.join(hotel_dir, f"pelicula{ext}")
                if download_image(pelicula_imgs, img_path):
                    hotel['imagenes']['pelicula'] = f"data/img/{hotel_id}/pelicula{ext}"
        
        # Procesar imágenes de la galería
        if 'imagenes' in hotel and 'galeria' in hotel['imagenes']:
            updated_galeria_imgs = []
            for i, img_url in enumerate(hotel['imagenes']['galeria']):
                ext = get_extension(img_url)
                img_path = os.path.join(hotel_dir, f"galeria_{i+1}{ext}")
                if download_image(img_url, img_path):
                    updated_galeria_imgs.append(f"data/img/{hotel_id}/galeria_{i+1}{ext}")
            hotel['imagenes']['galeria'] = updated_galeria_imgs
        
        updated_hotels.append(hotel)
    
    return updated_hotels

# Función principal
def main():
    # Rutas
    current_dir = Path(__file__).parent
    json_path = os.path.join(current_dir, 'data', 'hotels.json')
    img_base_dir = os.path.join(current_dir, 'data', 'img')
    
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

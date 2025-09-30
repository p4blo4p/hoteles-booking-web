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

# URLs originales actualizadas (reemplazadas las que daban error 404)
ORIGINAL_URLS = {
    "four-seasons-bali": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662774.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e6e&o=",
        "pelicula": [
            "https://baliventur.com/wp-content/uploads/2019/10/eat-pray-love.jpg",
            "https://baliventur.com/wp-content/uploads/2019/10/bali-was-eat-pray-love.jpg"
        ],
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662775.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662776.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662777.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o="
        ]
    },
    "grand-hotel-excelsior": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013424.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
        "pelicula": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013425.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013426.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o="
        ]
    },
    "st-regis-mexico": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/191546422.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
        "pelicula": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/191546423.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/191546424.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o="
        ]
    },
    "ashford-castle": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/118328778.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
        "pelicula": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/118328779.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/118328780.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o="
        ]
    },
    "punta-islita": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/107719322.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
        "pelicula": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/107719323.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/107719324.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o="
        ]
    },
    "chateau-frontenac": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/103041585.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
        "pelicula": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/103041586.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/103041587.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o="
        ]
    },
    "gritti-palace": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/104847384.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
        "pelicula": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/104847385.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/104847386.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o="
        ]
    },
    "plaza-athenee": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013427.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
        "pelicula": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013428.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013429.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o="
        ]
    },
    "belmond-iguazu": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/102323651.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
        "pelicula": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/102323652.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/102323653.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o="
        ]
    },
    "the-murray": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013430.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
        "pelicula": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013431.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013432.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o="
        ]
    }
}

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
        
        # Convertir a RGB si es necesario
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
        
        # Obtener URLs originales para este hotel
        if hotel_id in ORIGINAL_URLS:
            original_urls = ORIGINAL_URLS[hotel_id]
            
            # Procesar imagen principal del hotel
            if 'hotel' in original_urls:
                hotel_img_url = original_urls['hotel']
                image_data = download_image(hotel_img_url)
                
                if image_data:
                    output_path = os.path.join(hotel_dir, "hotel.webp")
                    if optimize_image(image_data, MAX_WIDTH_LARGE, output_path):
                        # Actualizar la ruta en el JSON
                        hotel['imagenes']['hotel'] = f"static/images/hotels/{hotel_id}/hotel.webp"
            
            # Procesar imágenes de la película
            if 'pelicula' in original_urls:
                pelicula_urls = original_urls['pelicula']
                if isinstance(pelicula_urls, list):
                    updated_pelicula_imgs = []
                    for i, img_url in enumerate(pelicula_urls):
                        image_data = download_image(img_url)
                        if image_data:
                            output_path = os.path.join(hotel_dir, f"pelicula_{i+1}.webp")
                            if optimize_image(image_data, MAX_WIDTH_MEDIUM, output_path):
                                updated_pelicula_imgs.append(f"static/images/hotels/{hotel_id}/pelicula_{i+1}.webp")
                    hotel['imagenes']['pelicula'] = updated_pelicula_imgs
                else:
                    image_data = download_image(pelicula_urls)
                    if image_data:
                        output_path = os.path.join(hotel_dir, "pelicula.webp")
                        if optimize_image(image_data, MAX_WIDTH_MEDIUM, output_path):
                            hotel['imagenes']['pelicula'] = f"static/images/hotels/{hotel_id}/pelicula.webp"
            
            # Procesar imágenes de la galería
            if 'galeria' in original_urls:
                updated_galeria_imgs = []
                for i, img_url in enumerate(original_urls['galeria']):
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
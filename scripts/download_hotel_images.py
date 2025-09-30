import os
import json
import requests
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image
import io

# Añadir el directorio src al path de Python
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Configuración de optimización de imágenes
MAX_WIDTH_LARGE = 1200  # Para imágenes principales
MAX_WIDTH_MEDIUM = 800   # Para galería
MAX_WIDTH_SMALL = 400    # Para miniaturas
WEBP_QUALITY = 85       # Calidad WebP (0-100)

# URLs originales actualizadas
ORIGINAL_URLS = {
    "four-seasons-bali": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662774.jpg",
        "pelicula": [
            "https://baliventur.com/wp-content/uploads/2019/10/eat-pray-love.jpg",
            "https://baliventur.com/wp-content/uploads/2019/10/bali-was-eat-pray-love.jpg"
        ],
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662775.jpg",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662776.jpg",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662777.jpg"
        ]
    },
    # ... (resto de los hoteles igual que antes)
}

def sanitize_filename(filename):
    """Limpiar nombres de archivos"""
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = filename.replace(" ", "_")
    return filename

def download_image(url):
    """Descargar una imagen"""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"❌ Error al descargar {url}: {e}")
        return None

def optimize_image(image_data, max_width, output_path):
    """Optimizar y convertir a WebP"""
    try:
        img = Image.open(io.BytesIO(image_data))
        
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        original_width, original_height = img.size
        if original_width > max_width:
            new_height = int(original_height * (max_width / original_width))
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        img.save(output_path, 'WEBP', quality=WEBP_QUALITY, optimize=True)
        print(f"✅ Optimizada: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error al optimizar imagen: {e}")
        return False

def load_hotels_json(file_path):
    """Cargar el archivo JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: JSON inválido en {file_path}: {e}")
        sys.exit(1)

def save_hotels_json(data, file_path):
    """Guardar el JSON actualizado"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON guardado en {file_path}")
    except Exception as e:
        print(f"❌ Error al guardar JSON: {e}")

def process_hotels(hotels_data, base_dir):
    """Procesar cada hotel"""
    updated_hotels = []
    
    for hotel in hotels_data:
        hotel_id = hotel['id']
        hotel_name = sanitize_filename(hotel['nombre'])
        
        hotel_dir = os.path.join(base_dir, 'hotels', hotel_id)
        os.makedirs(hotel_dir, exist_ok=True)
        
        print(f"\n🏨 Procesando hotel: {hotel['nombre']} ({hotel_id})")
        
        if hotel_id in ORIGINAL_URLS:
            original_urls = ORIGINAL_URLS[hotel_id]
            
            # Procesar imagen principal
            if 'hotel' in original_urls:
                hotel_img_url = original_urls['hotel']
                image_data = download_image(hotel_img_url)
                
                if image_data:
                    output_path = os.path.join(hotel_dir, "hotel.webp")
                    if optimize_image(image_data, MAX_WIDTH_LARGE, output_path):
                        hotel['imagenes']['hotel'] = f"static/images/hotels/{hotel_id}/hotel.webp"
            
            # Procesar imágenes de película
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
            
            # Procesar imágenes de galería
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

def main():
    """Función principal"""
    print("🚀 Iniciando descarga y optimización de imágenes...")
    
    PROJECT_ROOT = Path(__file__).parent.parent
    json_path = PROJECT_ROOT / "src" / "data" / "hotels.json"
    img_base_dir = PROJECT_ROOT / "src" / "static" / "images"
    
    os.makedirs(img_base_dir, exist_ok=True)
    
    print("📖 Cargando datos de hoteles...")
    hotels_data = load_hotels_json(json_path)
    
    print("\n🖼️ Procesando hoteles y descargando imágenes...")
    updated_hotels = process_hotels(hotels_data, img_base_dir)
    
    print("\n💾 Guardando JSON actualizado...")
    save_hotels_json(updated_hotels, json_path)
    
    print("\n🎉 Proceso completado!")

if __name__ == "__main__":
    main()
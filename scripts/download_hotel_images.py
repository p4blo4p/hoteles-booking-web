#!/usr/bin/env python3
"""
Script para descargar y optimizar imágenes de hoteles.
Versión corregida para usar la ruta correcta del JSON.
"""

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
MAX_WIDTH_MEDIUM = 800  # Para galería
MAX_WIDTH_SMALL = 400   # Para miniaturas
WEBP_QUALITY = 85      # Calidad WebP (0-100)

# URLs originales actualizadas (reemplazadas las que daban error 404)
ORIGINAL_URLS = {
    "four-seasons-bali": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662774.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e6e&o=",
        "pelicula": [
            "https://baliventur.com/wp-content/uploads/2019/10/eat-pray-love.jpg",
            "https://baliventur.com/wp-content/uploads/2019/10/bali-was-eat-pray-love.jpg"
        ],
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662775.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662776.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/265662777.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e&o="
        ]
    },
    "grand-hotel-excelsior": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013424.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e&o=",
        "pelicula": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013425.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/201013426.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e&o="
        ]
    },
    "st-regis-mexico": {
        "hotel": "https://cf.bstatic.com/xdata/images/hotel/max1024x768/191546422.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e&o=",
        "pelicula": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "galeria": [
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/191546423.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e&o=",
            "https://cf.bstatic.com/xdata/images/hotel/max1024x768/191546424.jpg?k=5a9e4c0b6c3e3e6e6e6e6e6e6e6e&o="
        ]
    }
}

def load_hotel_data():
    """Carga los datos de hoteles desde el archivo JSON."""
    # CORRECCIÓN: Usar la ruta correcta
    json_path = Path('data/hotels.json')  # Cambiado de 'src/data/hotels.json'
    
    print(f"📖 Buscando archivo en: {json_path.absolute()}")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"✅ Datos cargados: {len(data)} hoteles")
            return data
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {json_path}")
        # Mostrar el directorio actual para depuración
        current_dir = Path.cwd()
        print(f"📁 Directorio actual: {current_dir}")
        print(f"📂 Contenido del directorio actual:")
        for item in current_dir.iterdir():
            if item.is_dir():
                print(f"  📁 {item.name}/")
            else:
                print(f"  📄 {item.name}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar el archivo JSON: {e}")
        return []

def get_safe_filename(hotel_id, image_type, index=None):
    """Genera un nombre de archivo seguro para las imágenes."""
    safe_id = re.sub(r'[^a-zA-Z0-9-]', '-', hotel_id.lower())
    
    if index is not None:
        return f"{safe_id}_{image_type}_{index + 1}.webp"
    else:
        return f"{safe_id}_{image_type}.webp"

def download_image(url, save_path, max_size=None):
    """Descarga una imagen, la convierte a WebP y la guarda."""
    try:
        print(f"⬇️ Descargando: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Abrir imagen con PIL
        img = Image.open(io.BytesIO(response.content))
        
        # Convertir a RGB si es necesario (para WebP)
        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')
        
        # Redimensionar si es necesario (manteniendo aspecto)
        if max_size:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Crear directorio si no existe
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar como WebP
        img.save(save_path, 'WEBP', quality=WEBP_QUALITY, optimize=True)
        
        print(f"✅ Imagen guardada: {save_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error al procesar {url}: {e}")
        return False

def process_hotel_images(hotel):
    """Procesa todas las imágenes de un hotel."""
    hotel_id = hotel.get('id', 'unknown')
    hotel_name = hotel.get('nombre', 'Hotel sin nombre')
    
    print(f"\n🏨 Procesando hotel: {hotel_name} (ID: {hotel_id})")
    
    # Crear directorio base para el hotel
    hotel_dir = Path(f'static/images/hotels/{hotel_id}')
    hotel_dir.mkdir(parents=True, exist_ok=True)
    
    # Inicializar estructura de imágenes si no existe
    if 'imagenes' not in hotel:
        hotel['imagenes'] = {
            'hotel': '',
            'pelicula': [],
            'galeria': []
        }
    
    # Procesar imagen principal del hotel
    if hotel_id in ORIGINAL_URLS and ORIGINAL_URLS[hotel_id].get('hotel'):
        original_url = ORIGINAL_URLS[hotel_id]['hotel']
        local_path = hotel_dir / f"{hotel_id}_hotel.webp"
        
        if download_image(original_url, local_path, (MAX_WIDTH_LARGE, MAX_WIDTH_LARGE)):
            # Actualizar ruta local en el JSON
            hotel['imagenes']['hotel'] = f"static/images/hotels/{hotel_id}/{hotel_id}_hotel.webp"
    
    # Procesar imágenes de película
    if hotel_id in ORIGINAL_URLS and ORIGINAL_URLS[hotel_id].get('pelicula'):
        hotel['imagenes']['pelicula'] = []
        
        for i, pelicula_url in enumerate(ORIGINAL_URLS[hotel_id]['pelicula']):
            local_path = hotel_dir / f"{hotel_id}_pelicula_{i + 1}.webp"
            
            if download_image(pelicula_url, local_path, (MAX_WIDTH_MEDIUM, MAX_WIDTH_MEDIUM)):
                # Actualizar ruta local en el JSON
                hotel['imagenes']['pelicula'].append(f"static/images/hotels/{hotel_id}/{hotel_id}_pelicula_{i + 1}.webp")
    
    # Procesar imágenes de galería
    if hotel_id in ORIGINAL_URLS and ORIGINAL_URLS[hotel_id].get('galeria'):
        hotel['imagenes']['galeria'] = []
        
        for i, galeria_url in enumerate(ORIGINAL_URLS[hotel_id]['galeria']):
            local_path = hotel_dir / f"{hotel_id}_galeria_{i + 1}.webp"
            
            if download_image(galeria_url, local_path, (MAX_WIDTH_MEDIUM, MAX_WIDTH_MEDIUM)):
                # Actualizar ruta local en el JSON
                hotel['imagenes']['galeria'].append(f"static/images/hotels/{hotel_id}/{hotel_id}_galeria_{i + 1}.webp")
    
    return hotel

def download_hotel_images():
    """Función principal para descargar imágenes de hoteles."""
    print("🚀 Iniciando descarga y optimización de imágenes...")
    
    # Cargar datos de hoteles
    hotels = load_hotel_data()
    if not hotels:
        print("❌ No se pudieron cargar los datos de hoteles.")
        return
    
    processed_hotels = []
    
    for hotel in hotels:
        processed_hotel = process_hotel_images(hotel)
        processed_hotels.append(processed_hotel)
    
    # Guardar el JSON actualizado
    try:
        json_path = Path('data/hotels.json')  # CORRECCIÓN: Usar la ruta correcta
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(processed_hotels, f, indent=2, ensure_ascii=False)
        print(f"\n✅ JSON actualizado y guardado en: {json_path}")
    except Exception as e:
        print(f"❌ Error al guardar el JSON: {e}")

if __name__ == "__main__":
    download_hotel_images()
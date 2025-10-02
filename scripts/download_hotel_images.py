#!/usr/bin/env python3
"""
Script para descargar y optimizar imágenes de hoteles.
Versión mejorada que respeta la estructura JSON existente y llena correctamente la galería.
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

def load_hotel_data():
    """Carga los datos de hoteles desde el archivo JSON."""
    json_path = Path('data/hotels.json')
    
    print(f"📖 Buscando archivo en: {json_path.absolute()}")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"✅ Datos cargados: {len(data)} hoteles")
            
            # Mostrar estructura de imágenes del primer hotel para depuración
            if data and len(data) > 0:
                first_hotel = data[0]
                if 'imagenes' in first_hotel:
                    print("🔍 Estructura de imágenes del primer hotel:")
                    for key, value in first_hotel['imagenes'].items():
                        print(f"  {key}: {type(value).__name__} = {value}")
            
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

def download_and_convert_image(url, save_path, max_size=None):
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
        return save_path  # Devolver la ruta para usarla en el JSON
        
    except Exception as e:
        print(f"❌ Error al procesar {url}: {e}")
        return None

def process_hotel_images(hotel):
    """Procesa todas las imágenes de un hotel."""
    hotel_id = hotel.get('id', 'unknown')
    hotel_name = hotel.get('nombre', 'Hotel sin nombre')
    
    print(f"\n🏨 Procesando hotel: {hotel_name} (ID: {hotel_id})")
    
    # Crear directorio base para el hotel
    hotel_dir = Path(f'static/images/hotels/{hotel_id}')
    hotel_dir.mkdir(parents=True, exist_ok=True)
    
    # Asegurar que existe la estructura de imágenes
    if 'imagenes' not in hotel:
        hotel['imagenes'] = {
            'hotel': '',
            'pelicula': [],
            'galeria': []
        }
    
    # 1. Procesar imagen principal del hotel
    if hotel['imagenes'].get('hotel'):
        hotel_url = hotel['imagenes']['hotel']
        if hotel_url.startswith('http'):
            # Es una URL externa, descargarla y convertirla
            local_path = hotel_dir / f"{hotel_id}_hotel.webp"
            converted_path = download_and_convert_image(hotel_url, local_path, (MAX_WIDTH_LARGE, MAX_WIDTH_LARGE))
            
            if converted_path:
                # Actualizar ruta local en el JSON
                relative_path = str(converted_path).replace('\\', '/')  # Para Windows
                hotel['imagenes']['hotel'] = relative_path
                print(f"📝 Actualizada ruta de hotel: {relative_path}")
    
    # 2. Procesar imágenes de película
    if hotel['imagenes'].get('pelicula') and isinstance(hotel['imagenes']['pelicula'], list):
        pelicula_paths = []
        
        for i, pelicula_url in enumerate(hotel['imagenes']['pelicula']):
            if pelicula_url.startswith('http'):
                # Es una URL externa, descargarla y convertirla
                local_path = hotel_dir / f"{hotel_id}_pelicula_{i + 1}.webp"
                converted_path = download_and_convert_image(pelicula_url, local_path, (MAX_WIDTH_MEDIUM, MAX_WIDTH_MEDIUM))
                
                if converted_path:
                    relative_path = str(converted_path).replace('\\', '/')  # Para Windows
                    pelicula_paths.append(relative_path)
                    print(f"📝 Añadida ruta de película: {relative_path}")
            else:
                # Ya es una ruta local, mantenerla
                pelicula_paths.append(pelicula_url)
        
        # Actualizar la lista de imágenes de película
        hotel['imagenes']['pelicula'] = pelicula_paths
    
    # 3. PROCESAR IMÁGENES DE GALERÍA - ¡ESTA ES LA PARTE CLAVE!
    if 'imagenes' not in hotel:
        hotel['imagenes'] = {}
    if 'galeria' not in hotel['imagenes']:
        hotel['imagenes']['galeria'] = []
    
    galeria_paths = []
    
    # Si hay URLs de galería en el JSON, procesarlas
    if hotel['imagenes']['galeria'] and isinstance(hotel['imagenes']['galeria'], list):
        for i, galeria_url in enumerate(hotel['imagenes']['galeria']):
            if galeria_url.startswith('http'):
                # Es una URL externa, descargarla y convertirla
                local_path = hotel_dir / f"{hotel_id}_galeria_{i + 1}.webp"
                converted_path = download_and_convert_image(galeria_url, local_path, (MAX_WIDTH_MEDIUM, MAX_WIDTH_MEDIUM))
                
                if converted_path:
                    relative_path = str(converted_path).replace('\\', '/')  # Para Windows
                    galeria_paths.append(relative_path)
                    print(f"📝 Añadida ruta de galería: {relative_path}")
            else:
                # Ya es una ruta local, mantenerla
                galeria_paths.append(galeria_url)
    else:
        # Si la galería está vacía, crear imágenes de galería a partir de la imagen principal
        print("🖼️ Galería vacía, creando imágenes de galería...")
        
        # Usar la imagen principal o crear imágenes de galería genéricas
        if hotel['imagenes']['hotel']:
            if hotel['imagenes']['hotel'].startswith('http'):
                # Crear 3 imágenes de galería basadas en la imagen principal
                for i in range(3):
                    local_path = hotel_dir / f"{hotel_id}_galeria_{i + 1}.webp"
                    converted_path = download_and_convert_image(
                        hotel['imagenes']['hotel'], 
                        local_path, 
                        (MAX_WIDTH_MEDIUM, MAX_WIDTH_MEDIUM)
                    )
                    
                    if converted_path:
                        relative_path = str(converted_path).replace('\\', '/')  # Para Windows
                        galeria_paths.append(relative_path)
                        print(f"📝 Creada ruta de galería: {relative_path}")
            else:
                # La imagen principal ya es local, usarla como base
                main_image_path = Path(hotel['imagenes']['hotel'])
                if main_image_path.exists():
                    for i in range(3):
                        local_path = hotel_dir / f"{hotel_id}_galeria_{i + 1}.webp"
                        # Copiar y redimensionar la imagen principal
                        try:
                            img = Image.open(main_image_path)
                            img.thumbnail((MAX_WIDTH_MEDIUM, MAX_WIDTH_MEDIUM), Image.Resampling.LANCZOS)
                            img.save(local_path, 'WEBP', quality=WEBP_QUALITY, optimize=True)
                            
                            relative_path = str(local_path).replace('\\', '/')  # Para Windows
                            galeria_paths.append(relative_path)
                            print(f"📝 Creada ruta de galería desde imagen principal: {relative_path}")
                        except Exception as e:
                            print(f"❌ Error al crear imagen de galería: {e}")
    
    # Actualizar la lista de imágenes de galería
    hotel['imagenes']['galeria'] = galeria_paths
    print(f"📊 Total de imágenes en galería: {len(galeria_paths)}")
    
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
        json_path = Path('data/hotels.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(processed_hotels, f, indent=2, ensure_ascii=False)
        print(f"\n✅ JSON actualizado y guardado en: {json_path}")
        
        # Mostrar resumen final
        total_galeria_images = sum(len(hotel.get('imagenes', {}).get('galeria', [])) for hotel in processed_hotels)
        print(f"📊 Total de imágenes de galería creadas: {total_galeria_images}")
        
    except Exception as e:
        print(f"❌ Error al guardar el JSON: {e}")

if __name__ == "__main__":
    download_hotel_images()
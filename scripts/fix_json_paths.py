#!/usr/bin/env python3
"""
Script para corregir rutas en el archivo JSON de hoteles.
"""

import json
import os
import re
from pathlib import Path

def load_hotel_data():
    """Carga los datos de hoteles desde el archivo JSON."""
    try:
        with open('src/data/hotels.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró el archivo src/data/hotels.json")
        return []
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el archivo JSON: {e}")
        return []

def normalize_path(path):
    """Normaliza una ruta de archivo."""
    # Eliminar barras duplicadas
    path = re.sub(r'/+', '/', path)
    
    # Asegurar que comience con /
    if not path.startswith('/'):
        path = '/' + path
    
    return path

def fix_image_paths(hotels):
    """Corrige las rutas de imágenes en los datos de hoteles."""
    print("Corrigiendo rutas de imágenes...")
    
    for hotel in hotels:
        if 'images' not in hotel:
            continue
            
        original_images = hotel['images'].copy() if isinstance(hotel['images'], list) else []
        fixed_images = []
        
        for image_path in original_images:
            if isinstance(image_path, str):
                # Normalizar la ruta
                fixed_path = normalize_path(image_path)
                
                # Si es una URL externa, dejarla como está
                if fixed_path.startswith(('http://', 'https://')):
                    fixed_images.append(fixed_path)
                else:
                    # Asegurar que las rutas locales comiencen con /static/images/hotels/
                    if not fixed_path.startswith('/static/images/hotels/'):
                        # Extraer solo el nombre del archivo
                        filename = os.path.basename(fixed_path)
                        if filename:
                            fixed_path = f"/static/images/hotels/{filename}"
                        else:
                            fixed_path = f"/static/images/hotels/{hotel['name'].replace(' ', '_').lower()}.jpg"
                    
                    fixed_images.append(fixed_path)
        
        hotel['images'] = fixed_images
        print(f"  Hotel: {hotel['name']} - {len(fixed_images)} imágenes procesadas")

def fix_other_paths(hotels):
    """Corrige otras rutas que puedan existir en los datos de hoteles."""
    print("Corrigiendo otras rutas...")
    
    for hotel in hotels:
        # Corregir ruta de logo si existe
        if 'logo' in hotel and isinstance(hotel['logo'], str):
            if not hotel['logo'].startswith(('http://', 'https://')):
                hotel['logo'] = normalize_path(hotel['logo'])
        
        # Corregir rutas en amenities si existen
        if 'amenities' in hotel and isinstance(hotel['amenities'], list):
            for i, amenity in enumerate(hotel['amenities']):
                if isinstance(amenity, dict) and 'icon' in amenity:
                    if not amenity['icon'].startswith(('http://', 'https://')):
                        amenity['icon'] = normalize_path(amenity['icon'])

def verify_image_existence(hotels):
    """Verifica si las imágenes locales existen."""
    print("Verificando existencia de imágenes...")
    
    base_path = Path('src/static/images/hotels')
    
    for hotel in hotels:
        if 'images' not in hotel:
            continue
            
        existing_images = []
        
        for image_path in hotel['images']:
            if image_path.startswith(('http://', 'https://')):
                # URLs externas se consideran válidas
                existing_images.append(image_path)
            else:
                # Verificar si el archivo local existe
                filename = os.path.basename(image_path)
                file_path = base_path / filename
                
                if file_path.exists():
                    existing_images.append(image_path)
                else:
                    print(f"  Advertencia: Imagen no encontrada - {image_path}")
        
        hotel['images'] = existing_images

def save_hotel_data(hotels):
    """Guarda los datos de hoteles corregidos."""
    try:
        with open('src/data/hotels.json', 'w', encoding='utf-8') as f:
            json.dump(hotels, f, indent=2, ensure_ascii=False)
        print("Datos de hoteles guardados exitosamente.")
        return True
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return False

def fix_json_paths():
    """Función principal para corregir rutas en el JSON."""
    print("Iniciando corrección de rutas en JSON...")
    
    hotels = load_hotel_data()
    if not hotels:
        print("No se pudieron cargar los datos de hoteles.")
        return False
    
    print(f"Procesando {len(hotels)} hoteles...")
    
    # Corregir rutas
    fix_image_paths(hotels)
    fix_other_paths(hotels)
    
    # Verificar existencia de imágenes
    verify_image_existence(hotels)
    
    # Guardar datos corregidos
    if save_hotel_data(hotels):
        print("✓ Corrección de rutas completada exitosamente.")
        return True
    else:
        print("✗ Error al guardar los datos corregidos.")
        return False

if __name__ == "__main__":
    fix_json_paths()
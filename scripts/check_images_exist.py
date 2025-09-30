#!/usr/bin/env python3
"""
Script para verificar si las imágenes de hoteles existen en el sistema de archivos.
"""

import json
import os
from pathlib import Path
from urllib.parse import urlparse

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

def is_url(path):
    """Verifica si una ruta es una URL."""
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except:
        return False

def check_image_exists(image_path, base_dir='src/static/images/hotels'):
    """Verifica si una imagen existe."""
    if is_url(image_path):
        # Para URLs, asumimos que existen (no verificamos red)
        return True, "URL externa"
    
    # Para rutas locales
    if image_path.startswith('/'):
        # Quitar la barra inicial
        relative_path = image_path.lstrip('/')
    else:
        relative_path = image_path
    
    # Construir ruta completa
    full_path = Path(base_dir) / os.path.basename(relative_path)
    
    if full_path.exists():
        return True, str(full_path)
    else:
        return False, str(full_path)

def check_hotel_images():
    """Verifica todas las imágenes de todos los hoteles."""
    print("Verificando existencia de imágenes de hoteles...\n")
    
    hotels = load_hotel_data()
    if not hotels:
        print("No se pudieron cargar los datos de hoteles.")
        return
    
    total_images = 0
    existing_images = 0
    missing_images = 0
    
    for hotel in hotels:
        print(f"Hotel: {hotel['name']}")
        
        if 'images' not in hotel or not hotel['images']:
            print("  No hay imágenes definidas.")
            continue
        
        hotel_existing = 0
        hotel_missing = 0
        
        for i, image_path in enumerate(hotel['images']):
            total_images += 1
            
            exists, location = check_image_exists(image_path)
            
            if exists:
                existing_images += 1
                hotel_existing += 1
                print(f"  ✓ Imagen {i+1}: {location}")
            else:
                missing_images += 1
                hotel_missing += 1
                print(f"  ✗ Imagen {i+1}: {location} - NO ENCONTRADA")
        
        print(f"  Resumen: {hotel_existing} existentes, {hotel_missing} faltantes\n")
    
    # Resumen final
    print("=== RESUMEN FINAL ===")
    print(f"Total de imágenes verificadas: {total_images}")
    print(f"Imágenes existentes: {existing_images}")
    print(f"Imágenes faltantes: {missing_images}")
    
    if missing_images > 0:
        print(f"\n⚠️  Advertencia: {missing_images} imágenes no encontradas.")
        print("   Puede necesitar ejecutar el script de descarga de imágenes.")
        return False
    else:
        print("✓ Todas las imágenes existen.")
        return True

def list_missing_images():
    """Lista todas las imágenes faltantes con detalles."""
    print("\n=== DETALLE DE IMÁGENES FALTANTES ===")
    
    hotels = load_hotel_data()
    if not hotels:
        return
    
    missing_list = []
    
    for hotel in hotels:
        if 'images' not in hotel or not hotel['images']:
            continue
        
        for i, image_path in enumerate(hotel['images']):
            exists, location = check_image_exists(image_path)
            
            if not exists:
                missing_list.append({
                    'hotel': hotel['name'],
                    'image_index': i + 1,
                    'image_path': image_path,
                    'expected_location': location
                })
    
    if missing_list:
        print(f"Se encontraron {len(missing_list)} imágenes faltantes:\n")
        
        for missing in missing_list:
            print(f"Hotel: {missing['hotel']}")
            print(f"  Imagen #{missing['image_index']}")
            print(f"  Ruta en JSON: {missing['image_path']}")
            print(f"  Ubicación esperada: {missing['expected_location']}")
            print()
    else:
        print("No se encontraron imágenes faltantes.")

if __name__ == "__main__":
    success = check_hotel_images()
    
    if not success:
        response = input("\n¿Desea ver el detalle de las imágenes faltantes? (s/n): ")
        if response.lower() == 's':
            list_missing_images()
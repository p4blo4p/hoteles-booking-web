#!/usr/bin/env python3
"""
Script para organizar imágenes de hoteles en la estructura de directorios adecuada.
"""

import json
import os
import shutil
from pathlib import Path
import re

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

def get_safe_filename(hotel_name, original_filename=""):
    """Genera un nombre de archivo seguro para un hotel."""
    # Limpiar nombre del hotel
    safe_name = re.sub(r'[^\w\s-]', '', hotel_name.strip())
    safe_name = re.sub(r'[-\s]+', '-', safe_name)
    
    if original_filename:
        # Mantener la extensión original
        if '.' in original_filename:
            extension = original_filename.split('.')[-1].lower()
            if extension in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']:
                return f"{safe_name}.{extension}"
    
    return f"{safe_name}.jpg"

def find_image_files(source_dir="src/static/images/hotels"):
    """Encuentra todos los archivos de imagen en el directorio fuente."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'}
    image_files = []
    
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"Directorio fuente no encontrado: {source_dir}")
        return image_files
    
    for file_path in source_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    return image_files

def organize_images_by_hotel(hotels):
    """Organiza imágenes basándose en los datos de hoteles."""
    print("Organizando imágenes por hotel...")
    
    images_dir = Path('src/static/images/hotels')
    if not images_dir.exists():
        images_dir.mkdir(parents=True, exist_ok=True)
    
    # Crear un diccionario para mapear nombres de hotel a imágenes
    hotel_images = {}
    
    for hotel in hotels:
        hotel_name = hotel.get('name', '').strip()
        if not hotel_name:
            continue
            
        safe_name = get_safe_filename(hotel_name)
        hotel_images[hotel_name] = {
            'safe_name': safe_name,
            'expected_files': [],
            'images': hotel.get('images', [])
        }
    
    # Encontrar archivos de imagen existentes
    existing_files = find_image_files()
    
    # Organizar archivos existentes
    organized_count = 0
    for file_path in existing_files:
        filename = file_path.name
        
        # Buscar hotel correspondiente
        matched_hotel = None
        for hotel_name, hotel_data in hotel_images.items():
            # Buscar coincidencias en el nombre del archivo
            safe_name = hotel_data['safe_name']
            if (safe_name.lower() in filename.lower() or 
                hotel_name.lower().replace(' ', '_') in filename.lower() or
                hotel_name.lower().replace('-', '_') in filename.lower()):
                matched_hotel = hotel_name
                break
        
        if matched_hotel:
            # El archivo ya está en el lugar correcto o necesita ser renombrado
            expected_filename = f"{hotel_images[matched_hotel]['safe_name']}{file_path.suffix.lower()}"
            expected_path = images_dir / expected_filename
            
            if file_path != expected_path:
                # Renombrar o mover archivo
                try:
                    shutil.move(str(file_path), str(expected_path))
                    print(f"  Movido/Renombrado: {file_path.name} -> {expected_filename}")
                    organized_count += 1
                except Exception as e:
                    print(f"  Error al mover {file_path.name}: {e}")
        else:
            print(f"  Archivo sin hotel coincidente: {filename}")
    
    return organized_count

def create_missing_image_placeholders(hotels):
    """Crea archivos placeholder para imágenes faltantes."""
    print("\nCreando placeholders para imágenes faltantes...")
    
    images_dir = Path('src/static/images/hotels')
    placeholder_created = 0
    
    for hotel in hotels:
        hotel_name = hotel.get('name', '').strip()
        if not hotel_name:
            continue
            
        safe_name = get_safe_filename(hotel_name)
        placeholder_path = images_dir / f"{safe_name}.jpg"
        
        if not placeholder_path.exists():
            # Crear un archivo placeholder simple
            try:
                # Crear una imagen placeholder de 1x1 pixel (archivo vacío)
                placeholder_path.touch()
                print(f"  Placeholder creado: {safe_name}.jpg")
                placeholder_created += 1
            except Exception as e:
                print(f"  Error al crear placeholder para {hotel_name}: {e}")
    
    return placeholder_created

def update_json_with_local_paths(hotels):
    """Actualiza el JSON con rutas locales correctas."""
    print("\nActualizando rutas en JSON...")
    
    updated_count = 0
    
    for hotel in hotels:
        hotel_name = hotel.get('name', '').strip()
        if not hotel_name or 'images' not in hotel:
            continue
            
        safe_name = get_safe_filename(hotel_name)
        local_path = f"/static/images/hotels/{safe_name}.jpg"
        
        # Reemplazar rutas con la ruta local
        original_images = hotel['images']
        new_images = []
        
        for image_path in original_images:
            if isinstance(image_path, str):
                # Si es una URL externa, mantenerla
                if image_path.startswith(('http://', 'https://')):
                    new_images.append(image_path)
                else:
                    # Reemplazar con ruta local
                    new_images.append(local_path)
        
        if new_images != original_images:
            hotel['images'] = new_images
            updated_count += 1
    
    # Guardar cambios
    try:
        with open('src/data/hotels.json', 'w', encoding='utf-8') as f:
            json.dump(hotels, f, indent=2, ensure_ascii=False)
        print(f"  JSON actualizado: {updated_count} hoteles modificados")
        return True
    except Exception as e:
        print(f"  Error al guardar JSON: {e}")
        return False

def organize_images():
    """Función principal para organizar imágenes."""
    print("Iniciando organización de imágenes...\n")
    
    hotels = load_hotel_data()
    if not hotels:
        print("No se pudieron cargar los datos de hoteles.")
        return
    
    print(f"Procesando {len(hotels)} hoteles...")
    
    # Organizar imágenes existentes
    organized = organize_images_by_hotel(hotels)
    
    # Crear placeholders si es necesario
    placeholders = create_missing_image_placeholders(hotels)
    
    # Actualizar JSON
    json_updated = update_json_with_local_paths(hotels)
    
    # Resumen
    print(f"\n=== RESUMEN DE ORGANIZACIÓN ===")
    print(f"Imágenes organizadas: {organized}")
    print(f"Placeholders creados: {placeholders}")
    print(f"JSON actualizado: {'Sí' if json_updated else 'No'}")
    
    if organized > 0 or placeholders > 0:
        print("✓ Organización de imágenes completada.")
    else:
        print("ℹ No se realizaron cambios (las imágenes ya estaban organizadas).")

if __name__ == "__main__":
    organize_images()
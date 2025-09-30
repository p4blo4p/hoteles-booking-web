#!/usr/bin/env python3
"""
Script para verificar la estructura del proyecto y asegurarse de que todos los archivos necesarios existan.
"""

import os
from pathlib import Path

def check_file_exists(filepath, description):
    """Verifica si un archivo existe y reporta el resultado."""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} - NO ENCONTRADO")
        return False

def check_directory_exists(dirpath, description):
    """Verifica si un directorio existe y reporta el resultado."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ {description}: {dirpath} - NO ENCONTRADO")
        return False

def check_project_structure():
    """Verifica la estructura completa del proyecto."""
    print("Verificando estructura del proyecto...\n")
    
    # Estructura esperada
    structure = {
        "directorios": [
            ("docs/", "Documentación"),
            ("scripts/", "Scripts de utilidad"),
            ("src/", "Código fuente"),
            ("src/templates/", "Plantillas Jinja2"),
            ("src/static/", "Recursos estáticos"),
            ("src/static/css/", "Archivos CSS"),
            ("src/static/js/", "Archivos JavaScript"),
            ("src/static/images/", "Imágenes"),
            ("src/static/images/hotels/", "Imágenes de hoteles"),
            ("src/data/", "Datos"),
            (".github/", "Configuración de GitHub"),
            (".github/workflows/", "Workflows de GitHub Actions"),
        ],
        "archivos": [
            ("docs/README.md", "Documentación principal"),
            ("scripts/generate.py", "Script de generación"),
            ("scripts/download_hotel_images.py", "Script de descarga de imágenes"),
            ("scripts/check_structure.py", "Script de verificación de estructura"),
            ("scripts/fix_json_paths.py", "Script para corregir rutas JSON"),
            ("scripts/check_images_exist.py", "Script para verificar imágenes"),
            ("scripts/organize_images.py", "Script para organizar imágenes"),
            ("src/templates/base.html", "Plantilla base"),
            ("src/templates/index.html", "Plantilla de índice"),
            ("src/templates/hotel.html", "Plantilla de hotel"),
            ("src/static/css/styles.css", "Estilos CSS"),
            ("src/static/js/scripts.js", "Script JavaScript"),
            ("src/data/hotels.json", "Datos de hoteles"),
            (".github/workflows/deploy.yml", "Workflow de despliegue"),
            (".github/workflows/download-images.yml", "Workflow de descarga de imágenes"),
            (".gitignore", "Archivo gitignore"),
            ("requirements.txt", "Dependencias de Python"),
            ("LICENSE", "Licencia del proyecto"),
        ]
    }
    
    # Verificar directorios
    print("=== VERIFICANDO DIRECTORIOS ===")
    dir_results = []
    for dirpath, description in structure["directorios"]:
        dir_results.append(check_directory_exists(dirpath, description))
    
    print("\n=== VERIFICANDO ARCHIVOS ===")
    file_results = []
    for filepath, description in structure["archivos"]:
        file_results.append(check_file_exists(filepath, description))
    
    # Resumen
    total_dirs = len(structure["directorios"])
    total_files = len(structure["archivos"])
    existing_dirs = sum(dir_results)
    existing_files = sum(file_results)
    
    print(f"\n=== RESUMEN ===")
    print(f"Directorios: {existing_dirs}/{total_dirs} existen")
    print(f"Archivos: {existing_files}/{total_files} existen")
    
    if existing_dirs == total_dirs and existing_files == total_files:
        print("✓ Estructura del proyecto completa y correcta.")
        return True
    else:
        print("✗ Faltan algunos archivos o directorios.")
        return False

def create_missing_directories():
    """Crea los directorios que faltan."""
    print("\nCreando directorios faltantes...")
    
    directories = [
        "docs",
        "scripts",
        "src",
        "src/templates",
        "src/static",
        "src/static/css",
        "src/static/js",
        "src/static/images",
        "src/static/images/hotels",
        "src/data",
        ".github",
        ".github/workflows"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  Creado: {directory}/")
        else:
            print(f"  Ya existe: {directory}/")

if __name__ == "__main__":
    if not check_project_structure():
        response = input("\n¿Desea crear los directorios faltantes? (s/n): ")
        if response.lower() == 's':
            create_missing_directories()
            print("\nVerificando estructura nuevamente...")
            check_project_structure()
#!/usr/bin/env python3
"""
Script para generar el sitio web estático a partir de los datos y plantillas.
"""

import json
import os
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def load_hotel_data():
    """Carga los datos de hoteles desde el archivo JSON."""
    data_path = Path('data/hotels.json')
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"📊 Datos cargados: {len(data)} hoteles")
            
            # Mostrar estructura del primer hotel para depuración
            if data and len(data) > 0:
                print("🔍 Estructura del primer hotel:")
                for key, value in data[0].items():
                    print(f"  {key}: {type(value).__name__}")
            
            return data
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {data_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar el archivo JSON: {e}")
        return []

def generate_site():
    """Genera el sitio web estático."""
    print("🚀 Iniciando generación del sitio...")
    
    # Cargar datos de hoteles
    hotels = load_hotel_data()
    if not hotels:
        print("❌ No se pudieron cargar los datos de hoteles.")
        return False
    
    # Verificar estructura de directorios
    templates_dir = Path('templates')
    if not templates_dir.exists():
        print(f"❌ El directorio {templates_dir} no existe")
        return False
    
    # Configurar Jinja2
    try:
        env = Environment(loader=FileSystemLoader(str(templates_dir)))
        
        # Verificar que las plantillas existan
        try:
            template = env.get_template('index.html')
            hotel_template = env.get_template('hotel.html')
            print("✅ Plantillas cargadas correctamente")
        except Exception as e:
            print(f"❌ Error al cargar plantillas: {e}")
            return False
        
        # Crear directorio de salida si no existe
        dist_dir = Path('dist')
        dist_dir.mkdir(exist_ok=True)
        print(f"📁 Directorio de salida: {dist_dir}")
        
        # Generar página principal
        try:
            print("📝 Generando página principal...")
            
            # Preparar contexto para la plantilla
            context = {
                'hoteles': hotels,
                'base_url': os.environ.get('BASE_URL', '')
            }
            
            print(f"📋 Contexto para plantilla: {list(context.keys())}")
            
            index_content = template.render(**context)
            
            # Guardar página principal
            index_path = dist_dir / 'index.html'
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            print(f"✅ Página principal generada: {index_path}")
            
            # Crear directorio para páginas de hotel si no existe
            hotel_dir = dist_dir / 'hotel'
            hotel_dir.mkdir(exist_ok=True)
            print(f"📁 Directorio de hotel: {hotel_dir}")
            
            # Generar páginas individuales para cada hotel
            for i, hotel in enumerate(hotels):
                try:
                    print(f"🏨 Generando página para hotel {i+1}: {hotel.get('nombre', 'Sin nombre')}")
                    
                    # Preparar contexto para la plantilla de hotel
                    hotel_context = {
                        'hotel': hotel,
                        'base_url': os.environ.get('BASE_URL', '')
                    }
                    
                    hotel_content = hotel_template.render(**hotel_context)
                    
                    # Crear nombre de archivo seguro
                    hotel_name = hotel.get('nombre', f'hotel_{i}')
                    safe_name = "".join(c for c in hotel_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    filename = f"hotel_{safe_name.replace(' ', '_').lower()}.html"
                    hotel_path = hotel_dir / filename
                    
                    with open(hotel_path, 'w', encoding='utf-8') as f:
                        f.write(hotel_content)
                    print(f"✅ Página de hotel generada: {hotel_path}")
                    
                except Exception as e:
                    print(f"❌ Error al generar página para hotel {i+1}: {e}")
                    continue
            
            # Verificar archivos generados
            print("\n📂 Verificando archivos generados:")
            for item in dist_dir.iterdir():
                if item.is_dir():
                    print(f"  📁 {item.name}/")
                    for subitem in item.iterdir():
                        print(f"    📄 {subitem.name}")
                else:
                    print(f"  📄 {item.name}")
            
            print("✅ ¡Sitio web generado exitosamente!")
            return True
            
        except Exception as e:
            print(f"❌ Error al generar el contenido: {e}")
            print(f"   Tipo de error: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ Error al configurar Jinja2: {e}")
        return False
    
    # Después de generar todas las páginas
    verify_generated_structure()
    
    return True


def main():
    """Función principal."""
    # Mostrar información de depuración
    root_dir = Path.cwd()
    print(f"📁 Directorio raíz: {root_dir}")
    
    # Generar el sitio
    success = generate_site()
    
    if success:
        print("\n🎉 Generación completada con éxito!")
        sys.exit(0)
    else:
        print("\n💥 Generación fallida!")
        sys.exit(1)

# Al final del script generate.py, añade esta verificación:

def verify_generated_structure():
    """Verifica la estructura generada y muestra información detallada."""
    dist_dir = Path('dist')
    
    if not dist_dir.exists():
        print("❌ El directorio dist/ no existe")
        return False
    
    print("\n📂 Estructura generada:")
    print(f"📁 {dist_dir}/")
    
    # Listar contenido del directorio dist
    for item in dist_dir.iterdir():
        if item.is_dir():
            print(f"  📁 {item.name}/")
            # Listar contenido de subdirectorios
            for subitem in item.iterdir():
                print(f"    📄 {subitem.name}")
        else:
            print(f"  📄 {item.name} ({item.stat().st_size} bytes)")
    
    return True


if __name__ == "__main__":
    main()
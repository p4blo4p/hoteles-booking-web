import os
import json
import re
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Añadir el directorio src al path de Python
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Configuración
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "src" / "templates"
STATIC_DIR = PROJECT_ROOT / "src" / "static"
DATA_DIR = PROJECT_ROOT / "src" / "data"
OUTPUT_DIR = PROJECT_ROOT
BASE_URL = "https://p4blo4p.github.io/hoteles-booking-web-pages"

# Función para cargar datos de hoteles
def load_hotels_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: JSON inválido en {file_path}: {e}")
        sys.exit(1)

# Función para guardar el JSON actualizado
def save_hotels_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON guardado en {file_path}")
    except Exception as e:
        print(f"❌ Error al guardar JSON: {e}")

# Función para renderizar y guardar el HTML
def render_and_save(template_name, context, output_path):
    try:
        env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
        template = env.get_template(template_name)
        html_content = template.render(**context)
        
        # Reemplazar URLs de Unsplash con rutas locales de imágenes WebP
        if 'hoteles' in context:
            for hotel in context['hoteles']:
                if 'imagenes' in hotel:
                    # Reemplazar la imagen principal del hotel
                    if 'hotel' in hotel['imagenes']:
                        unsplash_patterns = [
                            r'src="https://images\.unsplash\.com/photo-1574680096145-d0b6c799f9b6\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                            r'src="https://images\.unsplash\.com/photo-1574227488958-009048826034\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                            r'src="https://images\.unsplash\.com/photo-1564564267028-f0e28c3b42d5\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                            r'src="https://images\.unsplash\.com/photo-1582562690819-0a5a5c7d98a7\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                            r'src="https://images\.unsplash\.com/photo-1564013799919-ab600027ffc6\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                            r'src="https://images\.unsplash\.com/photo-1551882547-ff40c63fe5fa\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"'
                        ]
                        for pattern in unsplash_patterns:
                            if pattern in html_content:
                                html_content = html_content.replace(
                                    pattern,
                                    f'src="{context["base_url"]}/{hotel["imagenes"]["hotel"]}"'
                                )
                                break
                    
                    # Reemplazar imágenes de película
                    if 'pelicula' in hotel['imagenes']:
                        if isinstance(hotel['imagenes']['pelicula'], list):
                            for i, img_path in enumerate(hotel['imagenes']['pelicula']):
                                unsplash_patterns = [
                                    r'src="https://images\.unsplash\.com/photo-1574227488958-009048826034\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                    r'src="https://images\.unsplash\.com/photo-1564564267028-f0e28c3b42d5\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                    r'src="https://images\.unsplash\.com/photo-1582562690819-0a5a5c7d98a7\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                    r'src="https://images\.unsplash\.com/photo-1564013799919-ab600027ffc6\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                    r'src="https://images\.unsplash\.com/photo-1551882547-ff40c63fe5fa\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"'
                                ]
                                for pattern in unsplash_patterns:
                                    if pattern in html_content:
                                        html_content = html_content.replace(
                                            pattern,
                                            f'src="{context["base_url"]}/{img_path}"'
                                        )
                                        break
                        else:
                            # Para imágenes individuales
                            unsplash_patterns = [
                                r'src="https://images\.unsplash\.com/photo-1574227488958-009048826034\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                r'src="https://images\.unsplash\.com/photo-1564564267028-f0e28c3b42d5\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                r'src="https://images\.unsplash\.com/photo-1582562690819-0a5a5c7d98a7\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                r'src="https://images\.unsplash\.com/photo-1564013799919-ab600027ffc6\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                r'src="https://images\.unsplash\.com/photo-1551882547-ff40c63fe5fa\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"'
                            ]
                            for pattern in unsplash_patterns:
                                if pattern in html_content:
                                    html_content = html_content.replace(
                                        pattern,
                                        f'src="{context["base_url"]}/{hotel["imagenes"]["pelicula"]}"'
                                    )
                                    break
                    
                    # Reemplazar imágenes de galería
                    if 'galeria' in hotel['imagenes']:
                        for i, img_path in enumerate(hotel['imagenes']['galeria']):
                            unsplash_patterns = [
                                r'src="https://images\.unsplash\.com/photo-1574227488958-009048826034\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                r'src="https://images\.unsplash\.com/photo-1564564267028-f0e28c3b42d5\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                r'src="https://images\.unsplash\.com/photo-1582562690819-0a5a5c7d98a7\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                r'src="https://images\.unsplash\.com/photo-1564013799919-ab600027ffc6\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"',
                                r'src="https://images\.unsplash\.com/photo-1551882547-ff40c63fe5fa\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"'
                            ]
                            for pattern in unsplash_patterns:
                                if pattern in html_content:
                                    html_content = html_content.replace(
                                        pattern,
                                        f'src="{context["base_url"]}/{img_path}"'
                                    )
                                    break
        
        # Guardar el archivo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Generado: {output_path}")
        
    except Exception as e:
        print(f"❌ Error al renderizar {template_name}: {e}")

# Función principal
def main():
    print("🚀 Iniciando generación del sitio...")
    print(f"📁 Directorio raíz: {PROJECT_ROOT}")
    
    # Verificar que los directorios existan
    for dir_path in [TEMPLATES_DIR, DATA_DIR, STATIC_DIR]:
        if not dir_path.exists():
            print(f"❌ El directorio {dir_path} no existe")
            sys.exit(1)
    
    # Cargar datos de hoteles
    print("\n📖 Cargando datos de hoteles...")
    hotels_data = load_hotels_json(DATA_DIR / "hotels.json")
    print(f"✅ Cargados {len(hotels_data)} hoteles")
    
    # Renderizar index.html
    print("\n🏠️ Renderizando index.html...")
    index_context = {
        'hoteles': hotels_data,
        'base_url': BASE_URL
    }
    render_and_save("index.html", index_context, OUTPUT_DIR / "index.html")
    
    # Crear directorio para páginas de hotel si no existe
    hotel_dir = OUTPUT_DIR / "hotel"
    hotel_dir.mkdir(exist_ok=True)
    
    # Renderizar cada página de hotel
    print("\n🏨 Renderizando páginas de hotel...")
    for hotel in hotels_data:
        hotel_context = {
            'hotel': hotel,
            'base_url': BASE_URL
        }
        output_path = hotel_dir / f"{hotel['id']}.html"
        render_and_save("hotel.html", hotel_context, output_path)
        print(f"  ✅ {hotel['nombre']}")
    
    print("\n🎉 Sitio generado exitosamente!")
    print(f"📍 URL base: {BASE_URL}")
    print(f"📂 Archivos generados en: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
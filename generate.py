import os
import json
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Configuración
TEMPLATES_DIR = Path("templates")
STATIC_DIR = Path("static")
DATA_DIR = Path("data")
OUTPUT_DIR = Path(".")
BASE_URL = "https://p4blo4p.github.io/hoteles-booking-web-pages"

# Función para cargar datos de hoteles
def load_hotels_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Función para guardar el JSON actualizado
def save_hotels_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Función para renderizar y guardar el HTML
def render_and_save(template_name, context, output_path):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template(template_name)
    html_content = template.render(**context)
    
    # Reemplazar URLs de Unsplash con rutas locales de imágenes WebP
    if 'hoteles' in context:
        for hotel in context['hoteles']:
            if 'imagenes' in hotel:
                # Reemplazar la imagen principal del hotel
                if 'hotel' in hotel['imagenes']:
                    unsplash_pattern = r'src="https://images\.unsplash\.com/photo-1574680096145-d0b6c799f9b6\?ixlib=rb-4\.0\.3&auto=format&fit=crop&w=800&q=80"'
                    if unsplash_pattern in html_content:
                        html_content = html_content.replace(
                            unsplash_pattern,
                            f'src="{BASE_URL}/{hotel["imagenes"]["hotel"]}"'
                        )
                
                # Reemplazar otras URLs de Unsplash para este hotel
                hotel_id = hotel['id']
                for key in ['pelicula', 'galeria']:
                    if key in hotel['imagenes']:
                        if isinstance(hotel['imagenes'][key], list):
                            for i, img_path in enumerate(hotel['imagenes'][key]):
                                # Buscar patrones de Unsplash y reemplazarlos
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
                                            f'src="{BASE_URL}/{img_path}"'
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
                                        f'src="{BASE_URL}/{hotel["imagenes"][key]}"'
                                    )
                                    break
    
    # Guardar el archivo
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

# Función principal
def main():
    print("Iniciando generación del sitio...")
    
    # Verificar que los directorios existan
    for dir_path in [TEMPLATES_DIR, DATA_DIR, STATIC_DIR]:
        if not dir_path.exists():
            print(f"❌ El directorio {dir_path} no existe")
            return
    
    # Cargar datos de hoteles
    print("Cargando datos de hoteles...")
    hotels_data = load_hotels_json(DATA_DIR / "hotels.json")
    print(f"✅ Cargados {len(hotels_data)} hoteles")
    
    # Renderizar index.html
    print("\nRenderizando index.html...")
    index_context = {
        'hoteles': hotels_data,
        'base_url': BASE_URL
    }
    render_and_save("index.html", index_context, OUTPUT_DIR / "index.html")
    print("✅ index.html generado")
    
    # Crear directorio para páginas de hotel si no existe
    hotel_dir = OUTPUT_DIR / "hotel"
    hotel_dir.mkdir(exist_ok=True)
    
    # Renderizar cada página de hotel
    print("\nRenderizando páginas de hotel...")
    for hotel in hotels_data:
        hotel_context = {
            'hotel': hotel,
            'base_url': BASE_URL
        }
        output_path = hotel_dir / f"{hotel['id']}.html"
        render_and_save("hotel.html", hotel_context, output_path)
        print(f"✅ {hotel['nombre']} - {output_path}")
    
    print("\n🎉 Sitio generado exitosamente!")
    print(f"📍 URL base: {BASE_URL}")

if __name__ == "__main__":
    main()

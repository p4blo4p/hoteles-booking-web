import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader

# Obtener el directorio actual del script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuración con rutas absolutas
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, 'templates')
STATIC_DIR = os.path.join(SCRIPT_DIR, 'static')
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
OUTPUT_DIR = SCRIPT_DIR  # Directorio raíz del proyecto

print(f"Directorio del script: {SCRIPT_DIR}")
print(f"Directorio de plantillas: {TEMPLATES_DIR}")
print(f"Directorio de datos: {DATA_DIR}")
print(f"Directorio de salida: {OUTPUT_DIR}")

# Verificar que los directorios existen
for dir_path in [TEMPLATES_DIR, STATIC_DIR, DATA_DIR]:
    if not os.path.exists(dir_path):
        print(f"ERROR: El directorio {dir_path} no existe")
        exit(1)

# Listar archivos en el directorio de plantillas
print("Archivos en el directorio de plantillas:")
for file in os.listdir(TEMPLATES_DIR):
    print(f"  - {file}")

# Cargar el entorno de plantillas
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Cargar datos de hoteles
hoteles_json_path = os.path.join(DATA_DIR, 'hoteles.json')
print(f"Buscando archivo de hoteles en: {hoteles_json_path}")

if not os.path.exists(hoteles_json_path):
    print(f"ERROR: El archivo {hoteles_json_path} no existe")
    exit(1)

with open(hoteles_json_path, 'r', encoding='utf-8') as f:
    hoteles = json.load(f)

print(f"Cargados {len(hoteles)} hoteles")

# Obtener el dominio base desde la variable de entorno
# Por defecto usar el de GitHub Pages
BASE_URL = os.environ.get('BASE_URL', 'https://p4blo4p.github.io/hoteles-booking-web-pages')
print(f"Usando BASE_URL: {BASE_URL}")

# Renderizar index.html
print("Renderizando index.html...")
index_template = env.get_template('index.html')
index_html = index_template.render(hoteles=hoteles, base_url=BASE_URL)
index_output_path = os.path.join(OUTPUT_DIR, 'index.html')
with open(index_output_path, 'w', encoding='utf-8') as f:
    f.write(index_html)
print(f"Generado: {index_output_path}")

# Crear directorio para hoteles si no existe
hotels_dir = os.path.join(OUTPUT_DIR, 'hotel')
if not os.path.exists(hotels_dir):
    os.makedirs(hotels_dir)
    print(f"Creado directorio: {hotels_dir}")

# Renderizar cada hotel
print("Renderizando páginas de hoteles...")
hotel_template = env.get_template('hotel.html')
for hotel in hoteles:
    hotel_html = hotel_template.render(hotel=hotel, base_url=BASE_URL)
    output_path = os.path.join(hotels_dir, f"{hotel['id']}.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(hotel_html)
    print(f"Generado: {output_path}")

print("Sitio generado exitosamente")

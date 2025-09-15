import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader

# Configuración
TEMPLATES_DIR = 'templates'
STATIC_DIR = 'static'
DATA_DIR = 'data'
OUTPUT_DIR = '.'

# Cargar el entorno de plantillas
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Cargar datos de hoteles
with open(os.path.join(DATA_DIR, 'hoteles.json'), 'r', encoding='utf-8') as f:
    hoteles = json.load(f)

# Renderizar index.html
index_template = env.get_template('index.html')
index_html = index_template.render(hoteles=hoteles)
with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)

# Crear directorio para hoteles si no existe
hotels_dir = os.path.join(OUTPUT_DIR, 'hotel')
if not os.path.exists(hotels_dir):
    os.makedirs(hotels_dir)

# Renderizar cada hotel
hotel_template = env.get_template('hotel.html')
for hotel in hoteles:
    hotel_html = hotel_template.render(hotel=hotel)
    output_path = os.path.join(hotels_dir, f"{hotel['id']}.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(hotel_html)

print("Sitio generado exitosamente")

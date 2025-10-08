#!/usr/bin/env python3
"""
Script para generar el sitio web estático a partir de los datos y plantillas.
Mejorado para manejar correctamente base_url, rutas de imágenes y URLs SEO-friendly.
Versión 2.0 - URLs optimizadas para SEO: /hotel/beverly-hills/ en lugar de /hotel/hotel_beverly-hills.html
"""
import json
import os
import sys
import shutil
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def clean_hotel_id(hotel_id):
    """Limpia el ID del hotel removiendo prefijos redundantes y caracteres inválidos para URLs SEO-friendly."""
    if not hotel_id:
        return ""
    
    # Remover prefijos como 'hotel-', 'hotel_', etc.
    cleaned_id = re.sub(r'^hotel[-_]', '', str(hotel_id).lower())
    # Mantener solo caracteres alfanuméricos y guiones
    cleaned_id = re.sub(r'[^a-z0-9-]', '-', cleaned_id)
    # Remover guiones múltiples
    cleaned_id = re.sub(r'-+', '-', cleaned_id)
    # Remover guiones al inicio y final
    cleaned_id = cleaned_id.strip('-')
    return cleaned_id

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
                if key == 'imagenes' and isinstance(value, dict):
                    for img_key, img_value in value.items():
                        print(f"    imagenes.{img_key}: {type(img_value).__name__}")
        return data
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {data_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar el archivo JSON: {e}")
        return []

def copy_static_files():
    """Copia los archivos estáticos al directorio de salida."""
    print("📁 Copiando archivos estáticos...")
    # Directorios origen y destino
    static_src = Path('static')
    static_dest = Path('dist/static')

    if not static_src.exists():
        print(f"⚠️ El directorio origen {static_src} no existe")
        return False

    try:
        # Crear directorio destino si no existe
        static_dest.mkdir(parents=True, exist_ok=True)

        # Copiar todo el contenido recursivamente
        files_copied = 0
        for item in static_src.rglob('*'):
            if item.is_file():
                # Calcular ruta relativa
                relative_path = item.relative_to(static_src)
                dest_path = static_dest / relative_path

                # Crear directorios padre si no existen
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Copiar archivo
                shutil.copy2(item, dest_path)
                files_copied += 1
                print(f"✅ Copiado: {relative_path}")
        print(f"✅ Archivos estáticos copiados a {static_dest} ({files_copied} archivos)")
        return True
    except Exception as e:
        print(f"❌ Error al copiar archivos estáticos: {e}")
        return False

def generate_seo_files(hotels, base_url):
    """Genera sitemap.xml y robots.txt usando templates."""
    print("🗺️ Generando archivos SEO...")
    
    try:
        # Configurar Jinja2 para templates SEO
        templates_dir = Path('src/templates')
        env = Environment(loader=FileSystemLoader(str(templates_dir)))
        
        # Preparar datos para templates
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        site_base_url = base_url or 'https://p4blo4p.github.io/hoteles-booking-web-pages'
        
        # Preparar hoteles con IDs limpios
        hotels_with_clean_ids = []
        for hotel in hotels:
            hotel_copy = hotel.copy()
            hotel_copy['clean_id'] = clean_hotel_id(hotel.get('id', ''))
            hotels_with_clean_ids.append(hotel_copy)
        
        # Generar sitemap.xml
        try:
            sitemap_template = env.get_template('sitemap.xml')
            sitemap_content = sitemap_template.render(
                base_url=site_base_url,
                hotels=hotels_with_clean_ids,
                current_date=current_date
            )
            
            sitemap_path = Path('dist/sitemap.xml')
            with open(sitemap_path, 'w', encoding='utf-8') as f:
                f.write(sitemap_content)
            print(f"✅ Sitemap generado: {sitemap_path}")
        except Exception as e:
            print(f"⚠️ Error generando sitemap (usando fallback): {e}")
            # Fallback simple si no existe template
            generate_simple_sitemap(hotels_with_clean_ids, site_base_url, current_date)
        
        # Generar robots.txt
        try:
            robots_template = env.get_template('robots.txt')
            robots_content = robots_template.render(
                base_url=site_base_url,
                current_date=current_date,
                current_time=current_time,
                site_name='Hoteles de Cine'
            )
            
            robots_path = Path('dist/robots.txt')
            with open(robots_path, 'w', encoding='utf-8') as f:
                f.write(robots_content)
            print(f"✅ Robots.txt generado: {robots_path}")
        except Exception as e:
            print(f"⚠️ Error generando robots.txt (usando fallback): {e}")
            # Fallback simple si no existe template
            generate_simple_robots(site_base_url)
        
        return True
        
    except Exception as e:
        print(f"❌ Error al generar archivos SEO: {e}")
        return False

def generate_simple_sitemap(hotels, base_url, current_date):
    """Genera un sitemap básico si no hay template."""
    sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{base_url}/</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
'''
    
    for hotel in hotels:
        sitemap_content += f'''    <url>
        <loc>{base_url}/hotel/{hotel['clean_id']}/</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
'''
    
    sitemap_content += '</urlset>'
    
    sitemap_path = Path('dist/sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print(f"✅ Sitemap básico generado: {sitemap_path}")

def generate_simple_robots(base_url):
    """Genera un robots.txt básico si no hay template."""
    robots_content = f'''User-agent: *
Allow: /

Sitemap: {base_url}/sitemap.xml

Crawl-delay: 1
'''
    
    robots_path = Path('dist/robots.txt')
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(robots_content)
    print(f"✅ Robots.txt básico generado: {robots_path}")

def generate_site():
    """Genera el sitio web estático con URLs SEO-friendly."""
    print("🚀 Iniciando generación del sitio...")
    print("📝 Mejoras SEO: URLs /hotel/beverly-hills/ en lugar de /hotel/hotel_beverly-hills.html")

    # Cargar datos de hoteles
    hotels = load_hotel_data()
    if not hotels:
        print("❌ No se pudieron cargar los datos de hoteles.")
        return False

    # Verificar estructura de directorios
    templates_dir = Path('src/templates')
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

        # Obtener BASE_URL
        base_url = os.environ.get('BASE_URL', '')
        print(f"🌐 BASE_URL: {base_url}")

        # Generar página principal
        try:
            print("📝 Generando página principal...")
            # Preparar hoteles con IDs limpios para el template principal
            hoteles_con_clean_id = []
            for hotel in hotels:
                hotel_copy = hotel.copy()
                hotel_copy['clean_id'] = clean_hotel_id(hotel.get('id', ''))
                hoteles_con_clean_id.append(hotel_copy)
            
            # Preparar contexto para la plantilla
            context = {
                'hoteles': hoteles_con_clean_id,
                'base_url': base_url
            }
            index_content = template.render(**context)

            # Guardar página principal
            index_path = dist_dir / 'index.html'
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            print(f"✅ Página principal generada: {index_path}")

            # Crear directorio base para páginas de hotel si no existe
            hotel_base_dir = dist_dir / 'hotel'
            hotel_base_dir.mkdir(exist_ok=True)
            print(f"📁 Directorio base de hoteles: {hotel_base_dir}")

            # Generar páginas individuales para cada hotel con estructura SEO-friendly
            print("\n🏨 Generando páginas de hoteles con URLs SEO-friendly...")
            for i, hotel in enumerate(hotels):
                try:
                    hotel_name = hotel.get('nombre', 'Sin nombre')
                    print(f"🏨 Generando página para hotel {i+1}: {hotel_name}")
                    
                    # Limpiar ID del hotel para URL SEO-friendly
                    original_id = hotel.get('id', f'hotel_{i}')
                    clean_id = clean_hotel_id(original_id)
                    
                    print(f"  🔄 ID: '{original_id}' -> '{clean_id}'")
                    
                    # Crear directorio específico para el hotel
                    hotel_dir = hotel_base_dir / clean_id
                    hotel_dir.mkdir(exist_ok=True)
                    
                    # Preparar contexto para la plantilla de hotel
                    hotel_context = {
                        'hotel': hotel,
                        'base_url': base_url,
                        'clean_id': clean_id
                    }
                    hotel_content = hotel_template.render(**hotel_context)

                    # Guardar como index.html en el directorio del hotel
                    hotel_path = hotel_dir / 'index.html'
                    with open(hotel_path, 'w', encoding='utf-8') as f:
                        f.write(hotel_content)
                    print(f"  ✅ Generado: {hotel_path}")
                    print(f"  🌐 URL SEO: /hotel/{clean_id}/")
                    
                except Exception as e:
                    print(f"❌ Error al generar página para hotel {i+1}: {e}")
                    continue

            # Copiar archivos estáticos
            print("\n📁 Copiando archivos estáticos...")
            if not copy_static_files():
                print("⚠️ Advertencia: No se pudieron copiar todos los archivos estáticos")

            # Generar archivos SEO (sitemap.xml y robots.txt)
            print("\n🗺️ Generando archivos SEO...")
            generate_seo_files(hotels, base_url)

            # Verificar estructura final
            verify_generated_structure()

            print("\n✅ ¡Sitio web generado exitosamente con URLs SEO-friendly!")
            print("\n📋 URLs generadas:")
            for hotel in hotels[:5]:  # Mostrar primeras 5
                clean_id = clean_hotel_id(hotel.get('id', ''))
                print(f"  🏨 {hotel.get('nombre', 'Sin nombre')}: /hotel/{clean_id}/")
            if len(hotels) > 5:
                print(f"  ... y {len(hotels) - 5} hoteles más")
            
            return True
        except Exception as e:
            print(f"❌ Error al generar el contenido: {e}")
            import traceback
            traceback.print_exc()
            return False
    except Exception as e:
        print(f"❌ Error al configurar Jinja2: {e}")
        return False

def verify_generated_structure():
    """Verifica la estructura generada y muestra información detallada."""
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ El directorio dist/ no existe")
        return False

    print("\n📂 Estructura generada:")
    print(f"📁 {dist_dir}/")

    # Función recursiva para mostrar estructura (limitada)
    def show_structure(path, indent=0, max_depth=2):
        if indent > max_depth:
            return
        for item in sorted(path.iterdir()):
            if item.is_dir():
                print(f"{' ' * indent}📁 {item.name}/")
                if indent < max_depth:
                    show_structure(item, indent + 1, max_depth)
            else:
                size = item.stat().st_size
                print(f"{' ' * indent}📄 {item.name} ({size} bytes)")

    show_structure(dist_dir)

    # Verificar archivos clave
    key_files = [
        'index.html',
        'sitemap.xml',
        'robots.txt',
        'static/css/styles.css',
        'static/js/scripts.js'
    ]
    print("\n🔍 Verificación de archivos clave:")
    for key_file in key_files:
        file_path = dist_dir / key_file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {key_file} ({size} bytes)")
        else:
            print(f"❌ {key_file} (no encontrado)")

    # Verificar páginas de hotel generadas con nueva estructura
    hotel_dir = dist_dir / 'hotel'
    if hotel_dir.exists():
        hotel_subdirs = [d for d in hotel_dir.iterdir() if d.is_dir()]
        print(f"\n✅ Directorios de hotel generados: {len(hotel_subdirs)}")
        for hotel_subdir in hotel_subdirs[:3]:  # Mostrar primeros 3
            index_file = hotel_subdir / 'index.html'
            if index_file.exists():
                print(f"  📄 {hotel_subdir.name}/index.html")
            else:
                print(f"  ❌ {hotel_subdir.name}/ (sin index.html)")
        if len(hotel_subdirs) > 3:
            print(f"  ... y {len(hotel_subdirs) - 3} más")
    else:
        print("❌ No se generaron páginas de hotel")
    return True

def main():
    """Función principal."""
    # Mostrar información de depuración
    root_dir = Path.cwd()
    print(f"📁 Directorio raíz: {root_dir}")
    print("\n🔧 Versión 2.0 - URLs SEO-friendly implementadas")
    print("   ✅ /hotel/beverly-hills/ en lugar de /hotel/hotel_beverly-hills.html")
    print("   ✅ Sitemap.xml automático")
    print("   ✅ Robots.txt optimizado")

    # Generar el sitio
    success = generate_site()
    if success:
        print("\n🎉 Generación completada con éxito!")
        print("\n📝 Próximos pasos:")
        print("  1. Verificar URLs en dist/hotel/")
        print("  2. Probar localmente: python -m http.server 8000 -d dist/")
        print("  3. Hacer commit y push para deploy")
        print("  4. Verificar que las URLs funcionan en producción")
        sys.exit(0)
    else:
        print("\n💥 Generación fallida!")
        sys.exit(1)

if __name__ == "__main__":
    main()

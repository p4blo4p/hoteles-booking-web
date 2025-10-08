# Hoteles Booking Web

Un sitio web estático para la gestión y visualización de información de hoteles, generado automáticamente a partir de datos JSON y plantillas Jinja2.

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso de los Scripts](#uso-de-los-scripts)
- [Flujo de Trabajo Recomendado](#flujo-de-trabajo-recomendado)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Sección para Asistente IA](#sección-para-asistente-ia)

## 🏨 Descripción del Proyecto

Este proyecto es un generador de sitios web estáticos para hoteles que:

- Carga datos de hoteles desde un archivo JSON
- Utiliza plantillas Jinja2 para generar HTML estático
- Gestiona automáticamente la descarga y organización de imágenes
- Proporciona herramientas para verificar y mantener la integridad del proyecto
- Se puede desplegar fácilmente en GitHub Pages

### Características Principales

- ✅ Generación automática de páginas HTML
- ✅ Gestión de imágenes de hoteles
- ✅ **Sistema de testimonios interactivos**
- ✅ **Layout responsivo y moderno**
- ✅ **Galería de imágenes con modal**
- ✅ Verificación de estructura y archivos
- ✅ Corrección automática de rutas
- ✅ Organización de archivos y directorios
- ✅ Integración con GitHub Actions

## 📁 Estructura del Proyecto

```
hoteles-booking-web/
├── docs/                          # Documentación
│   └── README.md                  # Este archivo
├── scripts/                       # Scripts de utilidad
│   ├── generate.py               # Genera el sitio web estático
│   ├── download_hotel_images.py   # Descarga imágenes de hoteles
│   ├── check_structure.py        # Verifica estructura del proyecto
│   ├── fix_json_paths.py         # Corrige rutas en JSON
│   ├── check_images_exist.py     # Verifica existencia de imágenes
│   └── organize_images.py        # Organiza imágenes en directorios
├── src/                          # Código fuente del sitio
│   ├── templates/                # Plantillas Jinja2
│   │   ├── base.html             # Plantilla base
│   │   ├── index.html            # Página principal
│   │   └── hotel.html            # Página individual de hotel (con testimonios y galería)
│   ├── static/                   # Recursos estáticos
│   │   ├── css/
│   │   │   └── styles.css        # Estilos CSS
│   │   ├── js/
│   │   │   └── scripts.js        # Scripts JavaScript
│   │   └── images/
│   │       └── hotels/           # Imágenes de hoteles
│   └── data/                     # Datos
│       └── hotels.json           # Datos de hoteles en JSON
├── .github/                      # Configuración de GitHub
│   └── workflows/
│       ├── deploy.yml            # Workflow de despliegue
│       └── download-images.yml   # Workflow de descarga de imágenes
├── .gitignore                    # Archivos ignorados por Git
├── requirements.txt              # Dependencias de Python
└── LICENSE                       # Licencia del proyecto
```

## 🔧 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.7+**: [Descargar Python](https://www.python.org/downloads/)
- **Git**: [Descargar Git](https://git-scm.com/downloads)
- **Cuenta de GitHub**: Para clonar y contribuir al proyecto

## 🚀 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/p4blo4p/hoteles-booking-web.git
   cd hoteles-booking-web
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verificar estructura del proyecto**
   ```bash
   python scripts/check_structure.py
   ```

## 🛠️ Uso de los Scripts

### 1. Verificar Estructura del Proyecto

```bash
python scripts/check_structure.py
```
- **Descripción**: Verifica que todos los archivos y directorios necesarios existan
- **Acción**: Crea directorios faltantes si se autoriza

### 2. Descargar Imágenes de Hoteles

```bash
python scripts/download_hotel_images.py
```
- **Descripción**: Descarga imágenes desde URLs especificadas en `hotels.json`
- **Requisito**: Tener URLs válidas en el campo `images` de cada hotel
- **Resultado**: Imágenes guardadas en `src/static/images/hotels/`

### 3. Corregir Rutas en JSON

```bash
python scripts/fix_json_paths.py
```
- **Descripción**: Corrige y normaliza las rutas de imágenes en el archivo JSON
- **Función**: Asegura que todas las rutas sean consistentes
- **Verificación**: Comprueba que las imágenes existan realmente

### 4. Verificar Existencia de Imágenes

```bash
python scripts/check_images_exist.py
```
- **Descripción**: Verifica que todas las imágenes referenciadas en el JSON existan
- **Reporte**: Muestra imágenes faltantes y su ubicación esperada

### 5. Organizar Imágenes

```bash
python scripts/organize_images.py
```
- **Descripción**: Organiza imágenes en la estructura de directorios correcta
- **Acciones**:
  - Renombra archivos según nombres de hoteles
  - Crea placeholders para imágenes faltantes
  - Actualiza rutas en el JSON

### 6. Generar Sitio Web

```bash
python scripts/generate.py
```
- **Descripción**: Genera el sitio web estático completo
- **Entrada**: Datos de `hotels.json` y plantillas Jinja2
- **Salida**: Páginas HTML en el directorio `dist/`

## 🔄 Flujo de Trabajo Recomendado

### Para Iniciar un Nuevo Proyecto

1. **Configurar estructura inicial**
   ```bash
   python scripts/check_structure.py
   ```

2. **Preparar datos de hoteles**
   - Editar `src/data/hotels.json` con la información de los hoteles
   - Incluir URLs de imágenes en el campo `images`

3. **Descargar imágenes**
   ```bash
   python scripts/download_hotel_images.py
   ```

4. **Organizar y verificar imágenes**
   ```bash
   python scripts/organize_images.py
   python scripts/check_images_exist.py
   ```

5. **Generar el sitio**
   ```bash
   python scripts/generate.py
   ```

### Para Actualizar un Proyecto Existente

1. **Actualizar datos en `hotels.json`**
2. **Ejecutar scripts de mantenimiento**:
   ```bash
   python scripts/fix_json_paths.py
   python scripts/download_hotel_images.py
   python scripts/organize_images.py
   ```
3. **Regenerar el sitio**:
   ```bash
   python scripts/generate.py
   ```

## 📝 Formato de Datos (hotels.json)

El archivo `src/data/hotels.json` debe seguir esta estructura:

```json
[
  {
    "id": "hotel-ejemplo",
    "nombre": "Nombre del Hotel",
    "descripcion": "Descripción del hotel",
    "ubicacion": "Ciudad, País",
    "pelicula": "Película Famosa",
    "anio": 2023,
    "precio": 100,
    "rating": 4.5,
    "caracteristicas": ["WiFi", "Piscina", "Gimnasio"],
    "servicios_adicionales": ["Spa", "Room Service", "Concierge"],
    "imagenes": {
      "hotel": "static/images/hotels/hotel-ejemplo/hotel-ejemplo_hotel.webp",
      "pelicula": ["static/images/hotels/hotel-ejemplo/pelicula_1.webp"],
      "galeria": [
        "static/images/hotels/hotel-ejemplo/galeria_1.webp",
        "static/images/hotels/hotel-ejemplo/galeria_2.webp"
      ]
    },
    "testimonios": [
      {
        "nombre": "Juan Pérez",
        "rating": 5,
        "comentario": "Excelente experiencia, muy recomendado.",
        "fecha": "2024-03-15"
      },
      {
        "nombre": "María García",
        "rating": 4,
        "comentario": "Muy buen servicio y instalaciones.",
        "fecha": "2024-02-28"
      }
    ],
    "direccion": "Dirección completa del hotel",
    "telefono": "+1234567890",
    "email": "info@hotel.com",
    "url": "https://www.hotel-ejemplo.com",
    "booking_url": "https://www.booking.com/hotel-ejemplo"
  }
]
```

## 🎨 Funcionalidades de las Páginas de Hotel

### Testimonios Interactivos
- **Estructura completa**: Nombre, fecha, rating con estrellas y comentario
- **Diseño tipo tarjeta**: Con efectos hover y gradientes
- **Layout responsivo**: Se adapta automáticamente a diferentes pantallas
- **Sistema de estrellas**: Visualización dinámica del rating

### Galería de Imágenes
- **Modal interactivo**: Click en cualquier imagen para ampliarla
- **Navegación intuitiva**: Cerrar con X, Escape o click fuera
- **Imágenes organizadas**: Hotel, película y galería general
- **Responsive design**: Optimizado para móviles y tablets

### Layout Moderno
- **Hero section**: Imagen principal con overlay de información
- **Grid layout**: Contenido principal + sidebar
- **Secciones organizadas**: Descripción, características, contacto, etc.
- **Call-to-action**: Botón de reserva destacado

## 🤝 Contribución

### Cómo Contribuir

1. **Hacer un Fork del repositorio**
2. **Crear una rama para tu feature**
   ```bash
   git checkout -b feature/nombre-del-feature
   ```
3. **Realizar tus cambios**
4. **Ejecutar scripts de verificación**
   ```bash
   python scripts/check_structure.py
   python scripts/check_images_exist.py
   ```
5. **Hacer Commit de tus cambios**
   ```bash
   git commit -m "Add some feature"
   ```
6. **Hacer Push a la rama**
   ```bash
   git push origin feature/nombre-del-feature
   ```
7. **Abrir un Pull Request**

### Guía de Estilo

- Usar Python 3.7+ para los scripts
- Seguir PEP 8 para el código Python
- Documentar todas las funciones con docstrings
- Mantener los nombres de archivos descriptivos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🤖 Sección para Asistente IA

### Contexto del Proyecto

Este es un proyecto de generación de sitios web estáticos para hoteles con las siguientes características:

- **Tecnologías**: Python, Jinja2, HTML/CSS/JS, JSON
- **Arquitectura**: Generador estático con separación de datos, lógica y presentación
- **Automatización**: Scripts para mantenimiento y GitHub Actions para CI/CD

### Scripts Disponibles y Sus Propósitos

1. **`generate.py`**: Motor principal de generación del sitio
   - Entrada: `src/data/hotels.json` + plantillas Jinja2
   - Salida: HTML estático en `dist/`
   - Dependencias: `jinja2`

2. **`download_hotel_images.py`**: Gestión de imágenes
   - Descarga desde URLs en JSON
   - Actualiza rutas a locales
   - Dependencias: `requests`

3. **`check_structure.py`**: Verificación de integridad
   - Valida estructura de directorios
   - Crea estructura faltante
   - Sin dependencias externas

4. **`fix_json_paths.py`**: Mantenimiento de datos
   - Normaliza rutas de imágenes
   - Corrige formatos inconsistentes
   - Verifica existencia de archivos

5. **`check_images_exist.py`**: Diagnóstico de imágenes
   - Reporta imágenes faltantes
   - Distingue entre URLs locales y externas
   - Útil para debugging

6. **`organize_images.py`**: Organización de archivos
   - Renombra imágenes según nombres de hoteles
   - Crea placeholders
   - Actualiza JSON con nuevas rutas

### Flujo de Trabajo para el Asistente

Cuando se solicite ayuda con este proyecto:

1. **Identificar el problema**: ¿Es de estructura, datos, imágenes o generación?
2. **Verificar estado actual**: Sugerir ejecutar `check_structure.py` primero
3. **Aplicar solución específica**:
   - Problemas de estructura → `check_structure.py`
   - Problemas de imágenes → `download_hotel_images.py` + `organize_images.py`
   - Problemas de datos → `fix_json_paths.py`
   - Generación → `generate.py`
4. **Verificar resultado**: Sugerir ejecutar `check_images_exist.py` después de cambios
5. **Correcciones completas**: Cuando corrijas algo pasa el archivo completo corregido, no solo las partes a cambiar.
6. **URL temporal para verificacion**: https://p4blo4p.github.io/hoteles-booking-web-pages/
7. **Actualiza README**: Siempre que hagas algun cambio signifcativo haz las modificaciones que debas en el readme para que siga siendo util y si hay algo que no lo sea quitalo o muevelo a otro .md

### Comandos Rápidos de Referencia

```bash
# Verificación completa
python scripts/check_structure.py && python scripts/check_images_exist.py

# Mantenimiento de imágenes
python scripts/download_hotel_images.py && python scripts/organize_images.py

# Generación completa
python scripts/fix_json_paths.py && python scripts/generate.py
```

### Estructura de Datos Esperada

```python
# Estructura completa de un hotel en JSON (actualizada 2024)
hotel = {
    "id": "string",                    # ID único del hotel
    "nombre": "string",                # Nombre del hotel
    "descripcion": "string",           # Descripción larga
    "ubicacion": "string",             # "Ciudad, País"
    "pelicula": "string",              # Película asociada
    "anio": int,                       # Año de la película
    "precio": float,                   # Precio por noche
    "rating": float,                   # Calificación 0-5
    "caracteristicas": list,           # Lista de características
    "servicios_adicionales": list,     # Servicios extra
    "imagenes": {                      # Imágenes organizadas por tipo
        "hotel": "string",             # Imagen principal
        "pelicula": list,              # Imágenes de película
        "galeria": list                # Galería general
    },
    "testimonios": [                   # Lista de testimonios
        {
            "nombre": "string",        # Nombre del huésped
            "rating": int,             # Rating 1-5
            "comentario": "string",    # Comentario
            "fecha": "string"          # Fecha en formato YYYY-MM-DD
        }
    ],
    "direccion": "string",             # Dirección completa
    "telefono": "string",              # Teléfono
    "email": "string",                 # Email
    "url": "string",                   # Sitio web oficial
    "booking_url": "string"            # URL de reserva
}
```

### Problemas Comunes y Soluciones

1. **"No se encuentra el archivo JSON"**
   - Verificar estructura con `check_structure.py`
   - Crear archivo `src/data/hotels.json` si no existe

2. **"Las imágenes no se muestran"**
   - Ejecutar `check_images_exist.py`
   - Corregir rutas con `fix_json_paths.py`
   - Reorganizar con `organize_images.py`

3. **"El sitio no se genera"**
   - Verificar plantillas en `src/templates/`
   - Validar formato JSON
   - Ejecutar `generate.py` con verbosidad

4. **"Error al descargar imágenes"**
   - Verificar URLs en JSON
   - Comprobar conexión a internet
   - Revistar permisos de directorio `src/static/images/hotels/`

5. **"Los testimonios no se muestran"** *(Corregido en 2024)*
   - Verificar estructura de `testimonios` en JSON
   - Asegurar que tiene campos: `nombre`, `rating`, `comentario`, `fecha`
   - Template `hotel.html` actualizado con soporte completo

6. **"Layout se ve mal en móviles"** *(Corregido en 2024)*
   - CSS actualizado con diseño responsive
   - Grid layout adaptativo implementado
   - Estilos específicos para tablets y móviles

### Extensiones Futuras Sugeridas

- Añadir soporte para múltiples idiomas
- Implementar sistema de búsqueda y filtros
- Añadir mapa de ubicación de hoteles
- Integrar sistema de reservas
- Añadir modo oscuro/claro
- Implementar caching para mejor rendimiento

## 📋 Actualizaciones Recientes

### v2.0 - Octubre 2024
- ✅ **Template hotel.html completamente reescrito**
  - Código limpio y bien estructurado
  - Soporte completo para testimonios
  - Layout responsivo con sidebar
  - Modal de galería interactivo

- ✅ **Sistema de testimonios mejorado**
  - Extracción correcta de datos del JSON
  - Diseño tipo tarjeta con efectos hover
  - Rating con estrellas dinámicas
  - Información completa (nombre, fecha, comentario)

- ✅ **CSS modernizado**
  - Grid layout responsivo
  - Estilos para testimonios
  - Modal de galería
  - Mejoras en mobile y tablet

- ✅ **JavaScript interactivo**
  - Funcionalidad de modal
  - Efectos hover en testimonios
  - Manejo de errores en imágenes

---

**Última Actualización**: Este README fue generado para proporcionar una guía completa para el desarrollo y mantenimiento del proyecto Hoteles Booking Web.
```

## Resumen del README

He creado un README completo que incluye:

### Para cualquier persona:
- **Descripción clara** del proyecto y sus características
- **Estructura detallada** del proyecto con árbol de directorios
- **Instrucciones paso a paso** para instalación y uso
- **Documentación de cada script** con ejemplos
- **Flujo de trabajo recomendado** para nuevos y existentes proyectos
- **Guía de contribución** para colaboradores
- **Formato de datos** esperado en el JSON

### Para mí como asistente:
- **Sección específica** con contexto del proyecto
- **Referencia rápida** de todos los scripts y sus propósitos
- **Flujo de trabajo** para diagnosticar y solucionar problemas
- **Comandos rápidos** para tareas comunes
- **Estructura de datos** esperada en formato Python
- **Problemas comunes** y sus soluciones
- **Sugerencias para futuras extensiones**

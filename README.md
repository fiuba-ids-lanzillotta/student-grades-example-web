# Student Grades Example - Web

> **Aviso:** este proyecto es **codigo de ejemplo** con fines didacticos. Puede contener errores, simplificaciones o decisiones de diseno discutibles. Si se usa como base para un trabajo practico u otro entregable, **debe adaptarse a las buenas practicas y consignas especificas de la materia/catedra** (estilo de codigo, manejo de errores, validaciones, tests, estructura, etc.).

## Motivacion

Este proyecto es el **frontend** de un **ejemplo integrador** que muestra como construir una pequena aplicacion full-stack (frontend + backend) usando Flask, donde el frontend consume una API REST en lugar de acceder directamente a la base de datos.

Permite **consultar el detalle academico de un alumno** por su numero de padron, ver las materias que curso con sus notas, agregar nuevas notas y consultar que alumnos cursan una determinada materia.

El objetivo es mostrar como un frontend puede **delegar toda la logica de negocio y acceso a datos a una API**, manteniendo una separacion clara de responsabilidades entre las capas.

## Arquitectura

```
  Browser
     |
     v
  Flask Web (este proyecto, puerto 5001)
     |
     |  requests.get/post (HTTP)
     v
  Flask API (student-grades-example-api, puerto 5000)
     |
     v
  MySQL
```

## Estructura del proyecto

```
student-grades-example-web/
├── app.py                              # Entry point Flask (puerto 5001)
├── requirements.txt                    # Dependencias Python
├── student_grades_example_web/
│   ├── constants.py                    # URL de la API backend y validaciones
│   ├── routes/
│   │   └── alumnos.py                  # Rutas: home, detalle, alumnos por materia
│   └── services/
│       ├── alumnos.py                  # Cliente HTTP para /alumnos
│       └── materias.py                 # Cliente HTTP para /materias
├── templates/
│   ├── base.html                       # Template base (header, footer, flash)
│   ├── index.html                      # Home con buscador por padron
│   ├── detalle.html                    # Detalle del alumno + modales
│   └── 404.html                        # Pagina de error 404 (ruta o alumno inexistente)
└── static/
    ├── css/
    │   └── styles.css                  # Estilos responsive
    └── js/
        └── detalle.js                  # Logica de modales y fetch de alumnos por materia
```

## Requisitos previos

- Python 3.10+
- La API (`student-grades-example-api`) corriendo en el puerto 5000

## Instalacion y ejecucion

El proyecto incluye scripts de setup que crean el entorno virtual, instalan las dependencias y levantan la aplicacion automaticamente.

Asegurate de que la API este corriendo primero, luego:

**Con virtualenv:**

```bash
# Windows
setup_virtualenv.bat

# Linux / macOS
chmod +x setup_virtualenv.sh
./setup_virtualenv.sh
```

**Con pipenv:**

```bash
# Windows
setup_pipenv.bat

# Linux / macOS
chmod +x setup_pipenv.sh
./setup_pipenv.sh
```

Una vez iniciada, la web estara disponible en `http://localhost:5001/`

## Paginas

| Ruta                          | Descripcion                                                  |
|-------------------------------|--------------------------------------------------------------|
| `/`                           | Home con buscador de alumno por padron                       |
| `/detalle/<padron>`           | Detalle del alumno: info + materias cursadas + alta de nota  |
| `/materias/<codigo>/alumnos`  | Endpoint JSON usado por el modal de "alumnos de la materia"  |

## Flujo principal

1. El usuario ingresa un **padron** en el home y submite el formulario.
2. El frontend redirige a `/detalle/<padron>`, que pide a la API los datos del alumno y sus notas.
3. Desde el detalle, el usuario puede:
   - Hacer clic en el **codigo** de una materia para ver los alumnos que la cursan (modal con `fetch` a la propia ruta del frontend, que actua como proxy de la API).
   - Hacer clic en el **nombre** de una materia para ver el detalle de esa nota.
   - Hacer clic en **Agregar nota** para abrir un modal y registrar una nueva (POST al backend).

## Por que se usa `fetch` + JSON en `/materias/<codigo>/alumnos`

Aunque la preferencia general del proyecto es que la comunicacion entre frontend y backend se resuelva con **Flask + Python (SSR)**, hay un caso puntual que se resuelve con una llamada asincronica desde el navegador (`fetch`) a una ruta del propio frontend que devuelve **JSON**: el modal que lista los alumnos que cursan una materia desde `/detalle/<padron>`.

### El problema concreto

El usuario esta parado en `/detalle/<padron>` viendo a **un alumno** y, sin moverse de esa pagina, quiere abrir un modal con la lista de alumnos que cursan **otra materia**. El requerimiento es **mostrar nueva informacion dentro de la pagina actual, sin recargarla ni perder el contexto** (scroll, modales abiertos, estado del formulario).

### Por que Flask "solo" no alcanza

Flask con renderizado del lado del servidor responde a **navegaciones**: cada request devuelve una pagina HTML completa que reemplaza la actual. Con solo Flask + Python las opciones serian:

- **Navegar a `/materias/<codigo>/alumnos` como pagina HTML completa**: el usuario abandona `/detalle/<padron>` y pierde el contexto. Necesita "Volver" para retomar.
- **Pre-renderizar los alumnos de TODAS las materias dentro de `detalle.html`**: hace N llamadas extra a la API en cada carga del detalle aunque el usuario no abra ningun modal, aumenta el tiempo de respuesta y acopla datos que quiza nunca se pidan.

### Que resuelve la version con `fetch`

El `fetch` desde `static/js/detalle.js` permite **actualizacion parcial bajo demanda**:

- Se carga el detalle del alumno una sola vez.
- Cuando el usuario hace clic en un codigo de materia, **recien ahi** se dispara un request asincronico al endpoint del frontend, que internamente llama a la API.
- La respuesta es **JSON** porque solo necesitamos los datos; el "como mostrarlos" (filas `<tr>` del modal) ya esta definido en el DOM/JS de la pagina actual.
- El navegador inyecta esos datos en la tabla del modal sin recargar la pagina.

### Resumen

Lo que `fetch` + JSON resuelve y Flask puro no puede:

- **Cargar datos sin recargar la pagina** (preservar contexto del usuario).
- **Cargar solo lo necesario, cuando se necesita** (evitar trabajo y red innecesarios al renderizar la pagina inicial).

Es el limite natural del SSR: en el momento en que se requieren interacciones dinamicas dentro de una misma vista, hace falta JavaScript en el cliente haciendo HTTP. Flask sigue siendo el servidor, pero el navegador deja de ser un mero "renderer" pasivo.

## Manejo de errores

El frontend define un **error handler 404** centralizado en `app.py` que renderiza `templates/404.html`. Este handler cubre dos casos:

- **Rutas inexistentes**: cualquier URL no mapeada por la app.
- **Alumno inexistente**: cuando la ruta `/detalle/<padron>` no encuentra un alumno, llama a `abort(404, description=...)` con un mensaje especifico que se muestra en la pagina de error.

## Glosario de terminos

- **API REST**: estilo de arquitectura para servicios web que expone recursos via HTTP (GET, POST, PUT, DELETE) usando, en general, JSON como formato de intercambio.
- **Endpoint**: ruta concreta de la API (por ejemplo `GET /alumnos/<padron>`) que responde a un metodo HTTP y realiza una accion sobre un recurso.
- **Body**: contenido (payload) de una request o response. En esta web los formularios llegan al backend como JSON.
- **JSON**: formato de texto para representar datos estructurados (objetos y arrays). Es el formato usado para los bodies de request y response.
- **Flask**: micro framework web de Python. En este ejemplo se usa tanto en el frontend (este proyecto) como en la API backend.
- **Frontend**: aplicacion que renderiza las paginas HTML del lado del servidor y consume la API. En este proyecto corre en el puerto 5001.
- **Backend / API**: servicio HTTP REST (`student-grades-example-api`) que expone los endpoints de alumnos, notas y materias. Corre en el puerto 5000.
- **Blueprint (Flask)**: mecanismo de Flask para agrupar rutas relacionadas en modulos (por ejemplo `routes/alumnos.py`).
- **Service**: capa con la logica de invocacion a la API (cliente HTTP). Vive en `services/` y es invocada desde las routes.
- **SSR (Server-Side Rendering)**: renderizado del HTML en el servidor (con Jinja2) antes de enviarlo al navegador. Es el enfoque usado en este frontend.
- **SPA (Single Page Application)**: alternativa al SSR donde el frontend corre como JavaScript en el navegador y consume la API directamente. **No** es lo que hace este proyecto.
- **Jinja2**: motor de templates que usa Flask para generar HTML dinamico (los archivos `.html` en `templates/`).
- **Template base (`base.html`)**: plantilla con la estructura comun (header, footer, flash) de la que heredan las demas paginas.
- **Flash message**: mensaje temporal de una sola lectura que Flask muestra al usuario tras una accion (exito o error).
- **`requests`**: libreria de Python que el frontend usa para hacer llamadas HTTP a la API.
- **`fetch` (JavaScript)**: API del navegador para hacer requests HTTP de forma asincronica desde el cliente. Se usa puntualmente en `static/js/detalle.js` para actualizar el modal sin recargar la pagina.
- **`abort` (Flask)**: helper de Flask que interrumpe el procesamiento de la request y devuelve un error HTTP (por ejemplo `abort(404)`).
- **Error handler**: funcion registrada con `@app.errorhandler(...)` que centraliza el render de paginas de error (por ejemplo `templates/404.html`).
- **Entorno virtual**: directorio aislado con la version de Python y las dependencias del proyecto, para no mezclarlas con las del sistema.
- **virtualenv / `venv`**: herramienta estandar de Python para crear entornos virtuales. Las dependencias se declaran en `requirements.txt` y se instalan con `pip install -r requirements.txt`. En este proyecto lo levantan los scripts `setup_virtualenv.sh` / `setup_virtualenv.bat`.
- **pipenv**: herramienta alternativa que combina la gestion del entorno virtual con la de dependencias en un solo flujo. Usa `Pipfile` (declaracion) y `Pipfile.lock` (versiones exactas resueltas) en vez de `requirements.txt`. En este proyecto lo levantan los scripts `setup_pipenv.sh` / `setup_pipenv.bat`.
- **`pip`**: gestor de paquetes de Python. Instala librerias desde PyPI dentro del entorno activo.
- **Padron**: identificador unico del alumno (entero positivo).
- **Materia**: asignatura identificada por un `codigo` corto (por ejemplo `TB022`).
- **Nota**: calificacion entera entre 1 y 10 asociada a un alumno y una materia en una fecha determinada. Se considera **aprobada** cuando es `>= 6`.

# Student Grades Example - Web

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
│   └── detalle.html                    # Detalle del alumno + modales
└── static/
    └── css/
        └── styles.css                  # Estilos responsive
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

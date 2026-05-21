import logging
import requests
from ..constants import API_BASE_URL

logger = logging.getLogger(__name__)


def obtener_alumno(padron) -> dict:
    """Consume el endpoint del backend para obtener los datos de un alumno por padron."""
    alumno = {}

    try:
        response = requests.get(f'{API_BASE_URL}/alumnos/{padron}', timeout=10)

        if response.status_code == 200:
            alumno = response.json()

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

    except Exception as e:
        logger.error(f"Error al obtener alumno {padron}: {e}")

    return alumno


def obtener_notas_alumno(padron) -> list[dict]:
    """Consume el endpoint del backend para obtener las notas de un alumno."""
    notas = []

    try:
        response = requests.get(f'{API_BASE_URL}/alumnos/{padron}/notas', timeout=10)

        if response.status_code == 200:
            notas = response.json()

    except Exception as e:
        logger.error(f"Error al obtener notas del alumno {padron}: {e}")

    return notas


def agregar_nota(padron, codigo: str, nota, fecha: str) -> dict:
    """Envia una nueva nota al backend. Retorna {'ok': True} si fue creada, o {'errores': [...]}."""
    try:
        response = requests.post(
            f'{API_BASE_URL}/alumnos/{padron}/notas',
            json={'codigo': codigo, 'nota': nota, 'fecha': fecha},
            timeout=10,
        )

        if response.status_code == 201:
            return {'ok': True}

        try:
            error_data = response.json()
            errores = error_data.get('errors', [])
            mensajes = [e.get('description', e.get('message', 'Error desconocido')) for e in errores]

            if not mensajes:
                mensajes = [f'Error del servidor: HTTP {response.status_code}']

            return {'errores': mensajes}
        except Exception:
            return {'errores': [f'Error del servidor: HTTP {response.status_code}']}

    except requests.exceptions.ConnectionError:
        logger.error(f"No se pudo conectar con la API en {API_BASE_URL}")

        return {'errores': ['No se pudo conectar con el servidor. Verifica que la API este corriendo.']}

    except Exception as e:
        logger.error(f"Error inesperado al agregar nota: {e}")

        return {'errores': [f'Error inesperado: {e}']}

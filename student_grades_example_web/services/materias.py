import logging
import requests
from ..constants import API_BASE_URL

logger = logging.getLogger(__name__)


def obtener_alumnos_materia(codigo: str) -> list[dict]:
    """Consume el endpoint del backend para obtener los alumnos que cursan una materia."""
    try:
        response = requests.get(f'{API_BASE_URL}/materias/{codigo}/alumnos', timeout=10)

        if response.status_code == 200:
            return response.json()

        return []

    except Exception as e:
        logger.error(f"Error al obtener alumnos de la materia {codigo}: {e}")

        return []

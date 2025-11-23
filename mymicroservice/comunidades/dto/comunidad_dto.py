from dataclasses import dataclass
from datetime import datetime
from .artista_dto import ArtistaDTO

@dataclass
class ComunidadDTO:
    idComunidad: int
    artista: ArtistaDTO # se pasa el objeto ARTISTA completo
    nombreComunidad: str
    descComunidad: str | None # puede ser nulo
    rutaImagen: str | None # puede ser nulo
    fechaCreacion: datetime
    numPublicaciones: int | None # puede ser nulo
    numUsuarios: int | None # puede ser nulo
    palabrasVetadas: list[str] | None # puede ser nulo
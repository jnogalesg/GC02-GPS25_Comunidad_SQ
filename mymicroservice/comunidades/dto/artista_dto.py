from dataclasses import dataclass
from .genero_dto import GeneroDTO

@dataclass
class ArtistaDTO:
    idArtista: int
    nombreUsuario: str
    rutaFoto: str | None  # puede ser nulo
    esNovedad: bool
    oyentes: int
    genero: GeneroDTO | None # hace referencia a un objeto Genero

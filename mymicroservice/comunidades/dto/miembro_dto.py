from dataclasses import dataclass

@dataclass
class MiembroDTO:
    idUsuario: int
    nombreUsuario: str
    esArtista: bool
    rutaFoto: str | None # puede ser nulo
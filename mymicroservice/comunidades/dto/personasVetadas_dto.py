from dataclasses import dataclass
from datetime import datetime

@dataclass
class PersonaVetadaDTO:
    idUsuario: int
    idComunidad: int
    fechaVeto: datetime
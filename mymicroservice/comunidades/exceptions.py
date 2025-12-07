# Gestionar excepciones personalizadas para el microservicio de comunidades

class ExternalServiceError(Exception):
    """Se lanza cuando un servicio externo (como el de artistas) devuelve un error."""
    pass

class BusinessRuleError(Exception):
    """Clase base para errores de lógica de negocio (parámetros, no encontrado, etc.)."""
    pass

class MissingParameterError(BusinessRuleError):
    """Se lanza cuando falta un parámetro obligatorio (ej: idComunidad)."""
    pass

class NotFoundError(BusinessRuleError):
    """Se lanza cuando no se encuentra un recurso (ej: Usuario no encontrado)."""
    pass

class AlreadyExistsError(BusinessRuleError):
    """Se lanza cuando algo ya existe (ej: Usuario ya es miembro, Ya ha dado me gusta)."""
    pass
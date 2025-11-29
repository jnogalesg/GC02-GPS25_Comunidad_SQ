from django.conf import settings
from comunidades.models import ComunidadMiembros, PersonasVetadas, Comunidad
from comunidades.dto.miembro_dto import MiembroDTO
from typing import List
from pyexpat import model
import requests

USER_SERVICE_URL = settings.USER_MICROSERVICE_URL

class MiembroDAO:
    @staticmethod
    def get_miembros(usuario: int) -> MiembroDTO:
        """
        # Llamada a la API de usuarios.
        Si falla o no encuentra al usuario, LANZA UNA EXCEPCIÓN.
        """
        if not usuario:
            # Si el ID viene vacío, salta una excepción y no hace la llamada
            raise Exception("Error: falta ID de usuario.")

        # URL de destino en el microservicio de usuarios
        # Permite obtener la información de un usuario específico por su ID
        url_destino = f"{settings.USER_MICROSERVICE_URL}{usuario}"
        
        try:
            # Hacemos la petición con timeout
            response = requests.get(url_destino, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Mapeamos el JSON recibido al MiembroDTO
                return MiembroDTO(
                    idUsuario=data.get('id'),
                    nombreUsuario=data.get('nombreusuario'),
                    esArtista=data.get('esartista'),
                    rutaFoto=data.get('rutafoto', None)
                )
            else:
                # Si devuelve 404 o 500, lanzamos excepción.
                raise Exception(f"Error al obtener usuario {usuario}: El servicio respondió {response.status_code}")
                
        except requests.RequestException as e:
            # Si el servidor está caído o hay error de red
            raise Exception(f"Error de conexión con el microservicio de usuarios: {str(e)}")
        
            
    @staticmethod
    def _to_dto(modelo: ComunidadMiembros) -> MiembroDTO:
        """
        Convierte un modelo ComunidadMiembros a MiembroDTO.
        - Extrae el id de usuario desde el modelo.
        - Llama al servicio de usuarios para obtener el DTO del usuario.
        """
        # Obtener el id del usuario desde las posibles propiedades del modelo
        idUsuario = getattr(modelo, "idUsuario", None)
        
        # Busca al usuario en el servicio de usuarios
        return MiembroDAO.get_miembros(idUsuario)

    @staticmethod
    def get_miembros_comunidad(comunidad: int) -> List[MiembroDTO]:
        """
        Devuelve la lista de miembros (DTOs) de una comunidad.
        """
        # 1. Busca en nuestra BD local los IDs de los miembros
        miembros_models = ComunidadMiembros.objects.filter(idComunidad_id=comunidad)
        
        # 2. Prepara cada DTO (esto hará múltiples llamadas al servicio de usuarios para recuperarlos a todos)
        return [MiembroDAO._to_dto(m) for m in miembros_models] 
            
    @staticmethod
    def get_miembro_especifico(comunidad: int, usuario: int) -> MiembroDTO:
        """
        Busca un miembro específico dentro de una comunidad.
        """
        try:
            # Usamos idComunidad_id para evitar el error de "must be instance"
            miembro = ComunidadMiembros.objects.get(idComunidad_id=comunidad, idUsuario=usuario)
            
            # Convertimos el modelo encontrado a DTO
            return MiembroDAO._to_dto(miembro)
        except ComunidadMiembros.DoesNotExist:
            raise Exception(f"El usuario {usuario} no existe o no pertenece a la comunidad {comunidad}.")
        
    @staticmethod
    def add_miembro(comunidad: int, usuario: int):
        """
        Añade un usuario a una comunidad.
        """
        
        # si ya existe el miembro en la comunidad, lanza una excepción
        if ComunidadMiembros.objects.filter(idComunidad=comunidad, idUsuario=usuario).exists():
            raise Exception("El usuario ya es miembro de la comunidad.")
        
        # si el usuario es el creador de la comunidad, lanza una excepción
        if Comunidad.objects.filter(idComunidad=comunidad, idArtista=usuario).exists():
            raise Exception("El usuario es el creador de la comunidad.")
        
        # si el miembro está vetado de la comunidad, lanza una excepción
        if PersonasVetadas.objects.filter(idComunidad=comunidad, idUsuario=usuario).exists():
            raise Exception("El usuario está vetado en la comunidad.")
        
        nuevo_miembro = ComunidadMiembros.objects.create(
            idComunidad_id=comunidad,  # se añade _id para asignar directamente el id de la comunidad
            idUsuario=usuario
        )
        return MiembroDAO._to_dto(nuevo_miembro) # devolver el DTO del nuevo miembro añadido

        
    @staticmethod
    def eliminar_miembro(comunidad: int, usuario: int):
        """
        Elimina a un miembro de una comunidad.
        """
        try:
            # se busca el miembro de la comunidad que se quiere eliminar
            miembro = ComunidadMiembros.objects.get(idComunidad_id=comunidad, idUsuario=usuario) # idComunidad_id para buscar por id directamente
            # si se encuentra, se elimina el miembro de la comunidad
            miembro.delete()
            # No se devuelve nada, el Controller dará un 204
        except ComunidadMiembros.DoesNotExist:  # si no se encuentra el miembro en la comunidad, salta una excepción
            raise Exception(f"El usuario {usuario} no es miembro de la comunidad {comunidad}.")
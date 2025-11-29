from django.conf import settings
import requests
from comunidades.models import Comunidad
from comunidades.dto.comunidad_dto import ComunidadDTO
from typing import List
from comunidades.dto.artista_dto import ArtistaDTO

USER_SERVICE_URL = settings.USER_MICROSERVICE_URL

class ComunidadDAO:
       
    @staticmethod 
    def get_artista(artista: int) -> ArtistaDTO:
        """
        # Esta función realiza la llamada al microservicio de usuarios para obtener al artista con el id especificado.
        Si falla o no encuentra al artista, LANZA UNA EXCEPCIÓN.
        """        
        # Llamamos al microservicio de usuarios para obtener el artista real
        url_destino = f"{settings.USER_MICROSERVICE_URL}artistas/{artista}"      
        
        try:
            # 2. Hacemos la petición GET
            response = requests.get(url_destino, timeout=5) # timeout es buena práctica
            
            # 3. Si la respuesta es OK (200)
            if response.status_code == 200:
                data = response.json()
                
                # Mapeamos el JSON recibido al ArtistaDTO
                return ArtistaDTO(
                    idArtista=data.get('id'),
                    nombreUsuario=data.get('nombreusuario'),
                    rutaFoto=data.get('rutafoto'),
                    esNovedad=data.get('esnovedad'),
                    oyentes=data.get('oyentes' ),
                    genero=data.get('genero', None) # Puede ser nulo
                )
            else:
                # Si el artista no existe o hay error 404/500
                raise Exception(f"Error al obtener artista {artista}: El servicio respondió {response.status_code}")
                
        except requests.RequestException as e:
            # Si el servidor está caído o no hay conexión
            raise Exception(f"Error de conexión con el microservicio de usuarios: {str(e)}")
        
    @staticmethod
    def _to_dto(modelo: Comunidad) -> ComunidadDTO:
        """
        Traductor que convierte el Modelo -> DTO
        """
        # 1. SIMULAMOS la llamada al servicio de usuarios
        artista_dto = ComunidadDAO.get_artista(modelo.idArtista) # Llamada al servicio de Usuarios para obtener el artista
        
        # 2. Calcular los contadores 
        num_publi = modelo.publicacion_set.count() # Contar publicaciones
        num_miem = modelo.comunidadmiembros_set.count() # Contar miembros

        # 3. Convertimos palabras vetadas de string -> lista
        palabras = modelo.palabrasVetadas.split(',') if modelo.palabrasVetadas else []
        
        # 4. Construimos el DTO final
        return ComunidadDTO(
            idComunidad=modelo.idComunidad,
            artista=artista_dto,
            nombreComunidad=modelo.nombreComunidad,
            descComunidad=modelo.descComunidad,
            rutaImagen=modelo.rutaImagen,
            fechaCreacion=modelo.fechaCreacion,
            numPublicaciones=num_publi,
            numUsuarios=num_miem,   
            palabrasVetadas=palabras 
        )
        
    @staticmethod
    def get_comunidades_usuario(usuario: int) -> List[ComunidadDTO]:
        """
        Obtiene la lista de comunidades a las que pertenece un usuario específico.
        """
        # Filtramos las comunidades que tengan miembros con ese id de usuario. 
        # (__ para relacionar la tabla comunidad con comunidadmiembros, utiliza la relación inversa de Django, al ser Comunidad una ForeignKey en ComunidadMiembros)
        comunidades = Comunidad.objects.filter(comunidadmiembros__idUsuario=usuario)
        
        # Convertimos cada modelo encontrado a DTO y lo devolvemos
        return [ComunidadDAO._to_dto(c) for c in comunidades]
    
    @staticmethod
    def get_all_comunidades() -> List[ComunidadDTO]:
        # Pide los modelos a la BD
        comunidades_models = Comunidad.objects.all()
        
        # Convierte los modelos en DTOs
        return [ComunidadDAO._to_dto(c) for c in comunidades_models]

    @staticmethod
    def crear_comunidad(datos: dict) -> ComunidadDTO:
        datosModelo = {
        'idArtista': datos.get('idArtista'),
        'nombreComunidad': datos.get('nombreComunidad'),
        'descComunidad': datos.get('descComunidad'),
        'rutaImagen': datos.get('rutaImagen'),
        'palabrasVetadas': ','.join(datos.get('palabrasVetadas', [])) 
        }
        
        if Comunidad.objects.filter(idArtista=datos.get('idArtista')).exists():
            raise Exception("Este artista ya tiene una comunidad creada.")
        
        # Crea el modelo en la BD
        # **datos es un truco para "desempaquetar" un diccionario
        nueva_comunidad = Comunidad.objects.create(**datosModelo)
        
        # Convierte el nuevo modelo en un DTO para devolverlo
        return ComunidadDAO._to_dto(nueva_comunidad)

    @staticmethod
    def get_comunidad_especifica(comunidad: int) -> ComunidadDTO:
        """
        Busca UNA comunidad específica por su ID.
        """
        try:
            # 1. Busca en la BD
            modelo = Comunidad.objects.get(idComunidad=comunidad)
            
            # 2. Traduce y devuelve el DTO
            return ComunidadDAO._to_dto(modelo)
        except Comunidad.DoesNotExist:
            raise Exception(f"Comunidad con id {comunidad} no encontrada.")

    @staticmethod
    def actualizar_comunidad(comunidad: int, datos: dict) -> ComunidadDTO:
        """
        Actualiza una comunidad específica.
        """
        try:
            # 1. Busca el objeto a actualizar
            comunidad = Comunidad.objects.get(idComunidad=comunidad)

            # 2. Actualiza los campos (solo los que vengan en 'datos')
            # Usamos .get(key, default) para no borrar campos si no vienen
            comunidad.nombreComunidad = datos.get('nombreComunidad', comunidad.nombreComunidad)
            comunidad.descComunidad = datos.get('descComunidad', comunidad.descComunidad)
            comunidad.rutaImagen = datos.get('rutaImagen', comunidad.rutaImagen)
            
            if 'palabrasVetadas' in datos:
                comunidad.palabrasVetadas = ','.join(datos.get('palabrasVetadas', []))

            # 3. Guarda en la BD
            comunidad.save()
            
            # 4. Devuelve el DTO actualizado
            return ComunidadDAO._to_dto(comunidad)
        except Comunidad.DoesNotExist:
            raise Exception(f"Comunidad con id {comunidad} no encontrada.")

    @staticmethod
    def eliminar_comunidad(comunidad: int):
        """
        Borra una comunidad por su ID.
        """
        try:
            # Se obteniene el modelo de la comunidad especificada y se elimina de la base de datos
            comunidad = Comunidad.objects.get(idComunidad=comunidad)
            comunidad.delete()
            # No se devuelve nada, el Controller dará un 204
        except Comunidad.DoesNotExist: # Si no existe la comunidad, habrá una excepción
            raise Exception(f"Comunidad con id {comunidad} no encontrada.")
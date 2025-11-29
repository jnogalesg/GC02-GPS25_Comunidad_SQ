from typing import List
from comunidades.models import PublicacionMeGusta, Publicacion, ComunidadMiembros
from comunidades.dto.publicacionMeGusta_dto import PublicacionMeGustaDTO

class PublicacionMeGustaDAO:

    @staticmethod
    def _to_dto(modelo: PublicacionMeGusta) -> PublicacionMeGustaDTO:
        return PublicacionMeGustaDTO(
            idPublicacion=modelo.idPublicacion_id, # Accedemos al ID de la publicacion
            idUsuario=modelo.idUsuario,
            fechaMeGusta=modelo.fechaMeGusta
        )

    @staticmethod
    def dar_megusta(id_publicacion: int, id_usuario: int) -> PublicacionMeGustaDTO:
        """
        Crea un registro de 'Me Gusta', verificando antes si es miembro.
        """
        
        # 1. Primero buscamos la publicación para saber a qué comunidad pertenece
        try:
            publicacion = Publicacion.objects.get(idPublicacion=id_publicacion)
        except Publicacion.DoesNotExist:
            raise Exception(f"La publicación {id_publicacion} no existe.")

        # 2. VERIFICACIÓN: ¿Es este usuario miembro de esa comunidad?
        es_miembro = ComunidadMiembros.objects.filter(
            idComunidad_id=publicacion.idComunidad_id, # Usamos _id para comparar rápido
            idUsuario=id_usuario
        ).exists()

        # 3. Si no es miembro, lanzamos un error y bloqueamos el like
        if not es_miembro:
             raise Exception(f"ACCESO DENEGADO: El usuario {id_usuario} no es miembro de esta comunidad.")

        # 4. Si pasa el control, creamos el like
        nuevo_like = PublicacionMeGusta.objects.create(
            idPublicacion_id=id_publicacion, 
            idUsuario=id_usuario
        )
        return PublicacionMeGustaDAO._to_dto(nuevo_like)

    @staticmethod
    def quitar_megusta(id_publicacion: int, id_usuario: int):
        """
        Borra el registro de 'Me Gusta'.
        """
        try:
            like = PublicacionMeGusta.objects.get(
                idPublicacion_id=id_publicacion, 
                idUsuario=id_usuario
            )
            like.delete()
        except PublicacionMeGusta.DoesNotExist:
            raise Exception(f"El usuario {id_usuario} no le ha dado 'Me Gusta' a la publicación {id_publicacion}.")
            
    @staticmethod
    def contar_likes(id_publicacion: int) -> int:
        """
        Devuelve el número total de likes de una publicación.
        (Útil para devolver el contador actualizado)
        """
        return PublicacionMeGusta.objects.filter(idPublicacion_id=id_publicacion).count()
    
    @staticmethod
    def get_likes_de_publicacion(id_publicacion: int) -> List[PublicacionMeGustaDTO]:
        """
        Devuelve la lista de todos los usuarios que dieron like a una publicación.
        """
        # Busamos por el ID de la publicación (usando _id para el string)
        likes = PublicacionMeGusta.objects.filter(idPublicacion_id=id_publicacion)
        
        # Convertimos cada modelo a su DTO
        return [PublicacionMeGustaDAO._to_dto(l) for l in likes]
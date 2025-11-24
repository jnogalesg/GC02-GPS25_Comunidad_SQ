from comunidades.models import Publicacion
from comunidades.dto.publicacion_dto import PublicacionDTO
from typing import List
from django.db.models import Count

class PublicacionDAO:

    @staticmethod
    def _to_dto(modelo: Publicacion) -> PublicacionDTO:
        """
        Convierte un modelo Publicacion a PublicacionDTO.
        """
        # Contamos el número de me gustas
        likes = getattr(modelo, 'meGusta', modelo.publicacionmegusta_set.count())

        return PublicacionDTO(
            idPublicacion=modelo.idPublicacion,
            idComunidad=modelo.idComunidad.idComunidad, # Accedemos al ID del objeto comunidad
            titulo=modelo.titulo,
            contenido=modelo.contenido,
            rutaFichero=modelo.rutaFichero,
            fecha=modelo.fechaPublicacion,
            meGusta=likes
        )

    @staticmethod
    def get_publicaciones_comunidad(idComunidad: str) -> List[PublicacionDTO]:
        '''
        Devuelve una lista de las publicaciones de una comunidad específica.
        '''
        
        # se cuentan los me gusta únicamente en las publicaciones de esta comunidad
        publicaciones = Publicacion.objects.filter(idComunidad=idComunidad).annotate(
            num_megusta=Count('publicacionmegusta')
        )
        return [PublicacionDAO._to_dto(p) for p in publicaciones]

    @staticmethod
    def get_publicacion_especifica(publicacion: str) -> PublicacionDTO:
        """
        Devuelve una publicación específica por su ID.
        """
        try:
            p = Publicacion.objects.annotate(
                num_megusta=Count('publicacionmegusta')
            ).get(idPublicacion=publicacion)
            return PublicacionDAO._to_dto(p)
        except Publicacion.DoesNotExist:
            raise Exception(f"Publicación {publicacion} no encontrada")

    @staticmethod
    def crear_publicacion(datos: dict, idComunidad: str) -> PublicacionDTO:
        """
        Crea una nueva publicación en una comunidad específica.
        """
        
        # Traducimos nombres del DTO -> Modelo
        datos_modelo = {
            'idComunidad_id': idComunidad, # _id para pasar el id directamente y no el objeto comunidad
            'titulo': datos.get('titulo'),
            'contenido': datos.get('contenido'),
            'rutaFichero': datos.get('rutaFichero')
        }
        
        nuevaPublicacion = Publicacion.objects.create(**datos_modelo)
        return PublicacionDAO._to_dto(nuevaPublicacion)
    
    @staticmethod
    def actualizar_publicacion(id_publicacion: str, datos: dict) -> PublicacionDTO:
        """
        Actualiza parcialmente una publicación.
        """
        try:
            # 1. Buscamos la publicación
            publicacion = Publicacion.objects.get(idPublicacion=id_publicacion)
            
            # 2. Actualizamos SOLO los campos que vengan en el diccionario 'datos'
            # Usamos .get('campo', valor_actual) para no borrar lo que ya había si no envían ese campo.
            publicacion.titulo = datos.get('titulo', publicacion.titulo)
            publicacion.contenido = datos.get('contenido', publicacion.contenido)
            publicacion.rutaFichero = datos.get('rutaFichero', publicacion.rutaFichero)
            
            # 3. Guardamos cambios en BD
            publicacion.save()
            
            # 4. Devolvemos el DTO actualizado
            return PublicacionDAO._to_dto(publicacion)
            
        except Publicacion.DoesNotExist:
            raise Exception(f"Publicación {id_publicacion} no encontrada")
    
    @staticmethod
    def eliminar_publicacion(publicacion: str):
        """
        Elimina una publicación específica por su ID.
        """
        try:
            p = Publicacion.objects.get(idPublicacion=publicacion)
            p.delete()
        except Publicacion.DoesNotExist:
             raise Exception(f"Publicación {publicacion} no encontrada")

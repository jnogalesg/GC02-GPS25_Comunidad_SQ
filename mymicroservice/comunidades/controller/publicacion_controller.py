from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comunidades.dao.publicacion_dao import PublicacionDAO
import dataclasses
import traceback

class PublicacionController(APIView):

    def get(self, request, idComunidad=None, idPublicacion=None):
        """
        GET /comunidad/publicaciones/{idComunidad}/ (Lista)
        GET /comunidad/publicaciones/{idComunidad}/{idPublicacion}/ (Detalle)
        """
        try:
            if idPublicacion:
                # Detalle de una publicación
                dto = PublicacionDAO.get_publicacion_especifica(idPublicacion)
                return Response(dataclasses.asdict(dto), status=status.HTTP_200_OK)
            elif idComunidad:
                # Lista de publicaciones de la comunidad
                dtos = PublicacionDAO.get_publicaciones_comunidad(idComunidad)
                data = [dataclasses.asdict(d) for d in dtos]
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Falta idComunidad"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, idComunidad=None):
        """
        POST /comunidad/publicaciones/{idComunidad}/
        """
        if not idComunidad:
             return Response({"error": "Falta idComunidad en la URL"}, status=status.HTTP_400_BAD_REQUEST)
        
        datos = request.data
        # Validación básica (puedes ampliarla)
        if not datos.get('titulo'):
             return Response({"error": "Faltan datos obligatorios (titulo)"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nuevo_dto = PublicacionDAO.crear_publicacion(datos, idComunidad)
            return Response(dataclasses.asdict(nuevo_dto), status=status.HTTP_201_CREATED)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, idComunidad=None, idPublicacion=None):
        """
        PATCH /comunidad/publicaciones/{idComunidad}/{idPublicacion}/
        (Editar publicación)
        """
        if not idPublicacion:
             return Response({"error": "Falta idPublicacion en la URL"}, status=status.HTTP_400_BAD_REQUEST)

        datos_entrada = request.data
        
        try:
            # Llamamos al DAO para actualizar
            publicacion_actualizada_dto = PublicacionDAO.actualizar_publicacion(idPublicacion, datos_entrada)
            
            return Response(dataclasses.asdict(publicacion_actualizada_dto), status=status.HTTP_200_OK)
            
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, idComunidad=None, idPublicacion=None):
        """
        DELETE /comunidad/publicaciones/{idComunidad}/{idPublicacion}/
        """
        if not idPublicacion:
            return Response({"error": "Falta idPublicacion"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            PublicacionDAO.eliminar_publicacion(idPublicacion)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
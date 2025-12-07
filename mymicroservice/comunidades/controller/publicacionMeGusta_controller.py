from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comunidades.dao.publicacionMeGusta_dao import PublicacionMeGustaDAO
import traceback
import dataclasses

class PublicacionMeGustaController(APIView):

    errIdPubli = "Falta idPublicacion en la URL"
    errIdUs = "Falta idUsuario en el body"

    def post(self, request, idPublicacion=None):
        """
        POST /comunidad/publicaciones/megusta/{idPublicacion}/
        """
        if not idPublicacion:
            return Response({"error": self.errIdPubli}, status=status.HTTP_400_BAD_REQUEST)

        # SIMULACIÓN DE AUTH: Leemos el usuario del body
        idUsuario = request.data.get('idUsuario')
        if not idUsuario:
            return Response({"error": self.errIdUs}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Dar Like
            PublicacionMeGustaDAO.dar_megusta(idPublicacion, idUsuario)
            
            # 2. Obtener nuevo contador para devolverlo
            nuevo_total = PublicacionMeGustaDAO.contar_likes(idPublicacion)
            
            # Devuelve { "meGusta": <numero> }
            return Response({"meGusta": nuevo_total}, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Si ya existe (error de integridad), devolvemos conflicto
            return Response({"error": f"No se pudo dar like: {str(e)}"}, status=status.HTTP_409_CONFLICT)
        
    def get(self, request, idPublicacion=None):
        """
        Maneja GET /comunidad/publicaciones/megusta/{idPublicacion}/
        (Ver quién le dio like)
        """
        if not idPublicacion:
            return Response({"error": self.errIdPubli}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Pide la lista al DAO
            lista_likes_dtos = PublicacionMeGustaDAO.get_likes_de_publicacion(idPublicacion)
            
            # 2. Convierte a JSON
            data = [dataclasses.asdict(dto) for dto in lista_likes_dtos]
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, idPublicacion=None):
        """
        DELETE /comunidad/publicaciones/megusta/{idPublicacion}/
        (Quitar like - requiere idUsuario en el body también para saber quién lo quita)
        """
        if not idPublicacion:
            return Response({"error": self.errIdPubli}, status=status.HTTP_400_BAD_REQUEST)

        idUsuario = request.data.get('idUsuario')
        if not idUsuario:
            return Response({"error": self.errIdUs}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Quitar Like
            PublicacionMeGustaDAO.quitar_megusta(idPublicacion, idUsuario)
            
            # 2. Obtener nuevo contador
            nuevo_total = PublicacionMeGustaDAO.contar_likes(idPublicacion)
            
            return Response({"meGusta": nuevo_total}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
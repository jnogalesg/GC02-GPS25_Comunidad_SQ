from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comunidades.dao.personasVetadas_dao import PersonasVetadasDAO
import dataclasses
import traceback

class PersonasVetadasController(APIView):

    def get(self, request, idComunidad=None):
        """ 
        GET /comunidad/vetados/{idComunidad} 
        Obtiene una lista con todos los miembros vetados en una comunidad específica.
        """
        # Si no se proporciona idComunidad en la URL, devolvemos error 400
        if not idComunidad:
             return Response({"error": "Falta idComunidad"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Obtener la lista de vetados desde el DAO
            dtos = PersonasVetadasDAO.get_vetados(idComunidad)
            data = [dataclasses.asdict(d) for d in dtos]
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, idComunidad=None):
        """ 
        POST /comunidad/vetados/{idComunidad} 
        Veta a un miembro en la comunidad especificada en la URL.
        """
        # Si no se proporciona idComunidad en la URL, devolvemos error 400
        if not idComunidad:
             return Response({"error": "Falta idComunidad"}, status=status.HTTP_400_BAD_REQUEST)
         
        idUsuario = request.data.get('idUsuario')
        
        # Si no se proporciona idUsuario en el body, devolvemos error 400
        if not idUsuario:
             return Response({"error": "Falta 'idUsuario' en el body"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nuevo_dto = PersonasVetadasDAO.vetar_miembro(idComunidad, idUsuario)
            return Response(dataclasses.asdict(nuevo_dto), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

    def delete(self, request, idComunidad=None, idUsuario=None):
        """ 
        DELETE /comunidad/vetados/{idComunidad}/{idUsuario} 
        Quita el veto a un miembro en la comunidad especificada en la URL.
        """
        if not idComunidad or not idUsuario:
             return Response({"error": "Faltan IDs en la URL"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            PersonasVetadasDAO.quitar_veto(idComunidad, idUsuario)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comunidades.dao.miembro_dao import MiembroDAO
import dataclasses 
import traceback

class MiembroController(APIView):

    def get(self, request, idComunidad=None, idMiembro=None):
        """
        GET /comunidad/miembros/<idComunidad>/ (Todos los miembros de la comunidad)
        GET /comunidad/miembros/<idComunidad>/<idMiembro>/ (Miembro específico)
        """
        try:
            if idMiembro:
                # --- CASO 1: Miembro específico ---
                miembro_dto = MiembroDAO.get_miembro_especifico(idComunidad, idMiembro)
                return Response(dataclasses.asdict(miembro_dto), status=status.HTTP_200_OK)
            
            else:
                # --- CASO 2: Todos los miembros de la comunidad ---
                miembros_dtos = MiembroDAO.get_miembros_comunidad(idComunidad)
                data = [dataclasses.asdict(dto) for dto in miembros_dtos]
                return Response(data, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, idComunidad=None):
        """
        POST /comunidad/miembros/<idComunidad>/
        (Añade un usuario a esa comunidad)
        """
        # (Idealmente, el id_usuario vendría del TOKEN de autenticación, pero por ahora, lo leemos del body para probar)
        idUsuario = request.data.get('idUsuario')
        if not idUsuario:
            return Response({"error": "Falta 'idUsuario' en el body"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Llama al DAO 
            nuevo_miembro_dto = MiembroDAO.add_miembro(idComunidad, idUsuario)
            # Devuelve el DTO del miembro añadido 
            return Response(dataclasses.asdict(nuevo_miembro_dto), status=status.HTTP_201_CREATED)
        except Exception as e:
            # Captura error si ya existe (restricción unique_together, id único para cada miembro en la comunidad)
            return Response({"error": f"Error: {e}"}, status=status.HTTP_409_CONFLICT)

    def delete(self, request, idComunidad=None, idMiembro=None):
        """
        DELETE /comunidad/miembros/<idComunidad>/<idMiembro>/
        (Elimina a un miembro específico de una comunidad)
        """
        if not idMiembro:
             return Response({"error": "Falta 'idMiembro' en la URL"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # Llama al DAO 
            MiembroDAO.eliminar_miembro(idComunidad, idMiembro)
            return Response(status=status.HTTP_204_NO_CONTENT) # Éxito, sin respuesta
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
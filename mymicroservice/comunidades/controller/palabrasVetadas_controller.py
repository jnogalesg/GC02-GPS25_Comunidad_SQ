from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comunidades.dao.palabrasVetadas_dao import PalabrasVetadasDAO
from comunidades.models import Comunidad
import dataclasses

class PalabrasVetadasController(APIView):

    def get(self, request, idComunidad):
        """
        GET /comunidad/<idComunidad>/palabras-vetadas/
        Obtiene la lista de palabras vetadas para una comunidad específica.
        """
        if not idComunidad: # Comprobamos que se ha pasado idComunidad en la URL
             return Response({"error": "Falta idComunidad en la URL"}, status=status.HTTP_400_BAD_REQUEST)
         
        try:    # Verificamos que la comunidad existe, si no, salta una excepción
            Comunidad.objects.get(idComunidad=idComunidad)
        except Comunidad.DoesNotExist:
            return Response({"error": f"Comunidad con id {idComunidad} no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        try:
            dto = PalabrasVetadasDAO.get_palabras_vetadas(idComunidad)
            return Response(dataclasses.asdict(dto), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, idComunidad):
        """ 
        POST /comunidad/<idComunidad>/palabras-vetadas/
        Añade nuevas palabras vetadas a la comunidad.
        """
        if not idComunidad: # Comprobamos que se ha pasado idComunidad en la URL
             return Response({"error": "Falta idComunidad en la URL"}, status=status.HTTP_400_BAD_REQUEST)
         
        try:    # Verificamos que la comunidad existe, si no, salta una excepción
            Comunidad.objects.get(idComunidad=idComunidad)
        except Comunidad.DoesNotExist:
            return Response({"error": f"Comunidad con id {idComunidad} no encontrada."}, status=status.HTTP_404_NOT_FOUND)
                 
        try:
            nuevas_palabras = request.data.get('palabras', [])
            if not isinstance(nuevas_palabras, list):
                 return Response({"error": "Se espera una lista en el campo 'palabras'"}, status=status.HTTP_400_BAD_REQUEST)
                 
            dto = PalabrasVetadasDAO.add_palabras_vetadas(idComunidad, nuevas_palabras)
            return Response(dataclasses.asdict(dto), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, idComunidad):
        """
        PUT /comunidad/<idComunidad>/palabras-vetadas/
        Reemplaza toda la lista de palabras vetadas de la comunidad.
        """
        if not idComunidad: # Comprobamos que se ha pasado idComunidad en la URL
             return Response({"error": "Falta idComunidad en la URL"}, status=status.HTTP_400_BAD_REQUEST)
         
        try:    # Verificamos que la comunidad existe, si no, salta una excepción
            Comunidad.objects.get(idComunidad=idComunidad)
        except Comunidad.DoesNotExist:
            return Response({"error": f"Comunidad con id {idComunidad} no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        try:
            nueva_lista = request.data.get('palabras', [])
            if not isinstance(nueva_lista, list):
                 return Response({"error": "Se espera una lista en el campo 'palabras'"}, status=status.HTTP_400_BAD_REQUEST)

            dto = PalabrasVetadasDAO.modificar_palabras_vetadas(idComunidad, nueva_lista)
            return Response(dataclasses.asdict(dto), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, idComunidad):
        """
        DELETE /comunidad/<idComunidad>/palabras-vetadas/
        Elimina palabras específicas de la lista de palabras vetadas de la comunidad.
        """
        if not idComunidad: # Comprobamos que se ha pasado idComunidad en la URL
             return Response({"error": "Falta idComunidad en la URL"}, status=status.HTTP_400_BAD_REQUEST)
         
        try:    # Verificamos que la comunidad existe, si no, salta una excepción
            Comunidad.objects.get(idComunidad=idComunidad)
        except Comunidad.DoesNotExist:
            return Response({"error": f"Comunidad con id {idComunidad} no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        try:
            a_borrar = request.data.get('palabras', [])
            if not isinstance(a_borrar, list):
                 return Response({"error": "Se espera una lista en el campo 'palabras'"}, status=status.HTTP_400_BAD_REQUEST)

            dto = PalabrasVetadasDAO.eliminar_palabras_vetadas(idComunidad, a_borrar)
            return Response(dataclasses.asdict(dto), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comunidades.dao.palabrasVetadas_dao import PalabrasVetadasDAO
from comunidades.models import Comunidad
import dataclasses

class PalabrasVetadasController(APIView):

    errIdCom = "Falta errIdComunidad en la URL" # Constante para mensajes de error
    errPalabras = "Se espera una lista en el campo 'palabras'" # Constante para mensajes de error
    
    def get(self, request, errIdComunidad):
        """
        GET /comunidad/<errIdComunidad>/palabras-vetadas/
        Obtiene la lista de palabras vetadas para una comunidad específica.
        """
        if not errIdComunidad: # Comprobamos que se ha pasado errIdComunidad en la URL
             return Response({"error": self.errIdCom}, status=status.HTTP_400_BAD_REQUEST)
         
        try:    # Verificamos que la comunidad existe, si no, salta una excepción
            Comunidad.objects.get(errIdComunidad=errIdComunidad)
        except Comunidad.DoesNotExist:
            return Response({"error": f"Comunidad con id {errIdComunidad} no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        try:
            dto = PalabrasVetadasDAO.get_palabras_vetadas(errIdComunidad)
            return Response(dataclasses.asdict(dto), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, errIdComunidad):
        """ 
        POST /comunidad/<errIdComunidad>/palabras-vetadas/
        Añade nuevas palabras vetadas a la comunidad.
        """
        if not errIdComunidad: # Comprobamos que se ha pasado errIdComunidad en la URL
             return Response({"error": self.errIdCom}, status=status.HTTP_400_BAD_REQUEST)
         
        try:    # Verificamos que la comunidad existe, si no, salta una excepción
            Comunidad.objects.get(errIdComunidad=errIdComunidad)
        except Comunidad.DoesNotExist:
            return Response({"error": f"Comunidad con id {errIdComunidad} no encontrada."}, status=status.HTTP_404_NOT_FOUND)
                 
        try:
            nuevas_palabras = request.data.get('palabras', [])
            if not isinstance(nuevas_palabras, list):
                 return Response({"error": self.errPalabras}, status=status.HTTP_400_BAD_REQUEST)
                 
            dto = PalabrasVetadasDAO.add_palabras_vetadas(errIdComunidad, nuevas_palabras)
            return Response(dataclasses.asdict(dto), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, errIdComunidad):
        """
        PUT /comunidad/<errIdComunidad>/palabras-vetadas/
        Reemplaza toda la lista de palabras vetadas de la comunidad.
        """
        if not errIdComunidad: # Comprobamos que se ha pasado errIdComunidad en la URL
             return Response({"error": self.errIdCom}, status=status.HTTP_400_BAD_REQUEST)
         
        try:    # Verificamos que la comunidad existe, si no, salta una excepción
            Comunidad.objects.get(errIdComunidad=errIdComunidad)
        except Comunidad.DoesNotExist:
            return Response({"error": f"Comunidad con id {errIdComunidad} no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        try:
            nueva_lista = request.data.get('palabras', [])
            if not isinstance(nueva_lista, list):
                 return Response({"error": self.errPalabras}, status=status.HTTP_400_BAD_REQUEST)

            dto = PalabrasVetadasDAO.modificar_palabras_vetadas(errIdComunidad, nueva_lista)
            return Response(dataclasses.asdict(dto), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, errIdComunidad):
        """
        DELETE /comunidad/<errIdComunidad>/palabras-vetadas/
        Elimina palabras específicas de la lista de palabras vetadas de la comunidad.
        """
        if not errIdComunidad: # Comprobamos que se ha pasado errIdComunidad en la URL
             return Response({"error": self.errIdCom}, status=status.HTTP_400_BAD_REQUEST)
         
        try:    # Verificamos que la comunidad existe, si no, salta una excepción
            Comunidad.objects.get(errIdComunidad=errIdComunidad)
        except Comunidad.DoesNotExist:
            return Response({"error": f"Comunidad con id {errIdComunidad} no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        try:
            a_borrar = request.data.get('palabras', [])
            if not isinstance(a_borrar, list):
                 return Response({"error": self.errPalabras}, status=status.HTTP_400_BAD_REQUEST)

            dto = PalabrasVetadasDAO.eliminar_palabras_vetadas(errIdComunidad, a_borrar)
            return Response(dataclasses.asdict(dto), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
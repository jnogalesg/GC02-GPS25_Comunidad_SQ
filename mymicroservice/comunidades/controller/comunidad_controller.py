from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comunidades.dao.comunidad_dao import ComunidadDAO
import dataclasses 
import traceback # Para ver errores completos
from rest_framework.permissions import IsAuthenticated # para proteger rutas con autenticación por token

class ComunidadController(APIView):
    
    def get(self, request, idComunidad=None):
        """
        GET comunidad/ (lista de todas las comunidades) 
        GET comunidad/{idComunidad} (comunidad especifica)
        """
        if idComunidad:
            try:
                # 1. Pide al DAO UN objeto
                comunidad_dto = ComunidadDAO.get_comunidad_especifica(idComunidad)
                return Response(dataclasses.asdict(comunidad_dto), status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Comunidad no encontrada: {e}"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # 1. Pide al DAO
            comunidades_dtos = ComunidadDAO.get_all_comunidades()
            # 2. Convierte DTOs a diccionarios para el JSON
            data = [dataclasses.asdict(dto) for dto in comunidades_dtos]
            # 3. Responde
            return Response(data, status=status.HTTP_200_OK)

    def post(self, request, idComunidad=None):
        """
        POST en comunidad/ (crear una nueva comunidad)
        """
        datos_entrada = request.data
        
        # 1. Valida los datos que nos envía el frontend
        if not datos_entrada.get('idArtista') or \
           not datos_entrada.get('nombreComunidad'):
            return Response({"error": "Datos incompletos (idArtista, nombreComunidad)"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 2. Pasa los datos al DAO para que los cree
            # El DAO se encargará de traducirlos al modelo
            nuevo_dto = ComunidadDAO.crear_comunidad(datos_entrada)
            
            # 3. Responde con el DTO completo
            return Response(dataclasses.asdict(nuevo_dto), status=status.HTTP_201_CREATED)
        
        except Exception as e:
            traceback.print_exc() # Muestra el error real en tu consola
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, idComunidad=None):
        """
        PUT comunidad/ (Actualizar una comunidad existent)
        """

        # comprueba que la url tenga un idComunidad válido
        if not idComunidad:
            return Response({"error": "Falta idComunidad en la URL para actualizar"}, status=status.HTTP_400_BAD_REQUEST)
        
        # se cogen los datos del body para hacer la actualización
        datos_entrada = request.data

        try:
            # llama al método del DAO para actualizar la comunidad
            comunidad_actualizada = ComunidadDAO.actualizar_comunidad(idComunidad, datos_entrada)
            return Response(dataclasses.asdict(comunidad_actualizada), status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request,idComunidad=None):
        """
        DELETE comunidad/{idComunidad} (Borrar una comunidad existente)
        """
        if not idComunidad:
            return Response({"error": "Falta idComunidad en la URL"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            ComunidadDAO.eliminar_comunidad(idComunidad)
            return Response(status=status.HTTP_204_NO_CONTENT) # 204 = Éxito, sin respuesta
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
# --- Nuevo controlador para devolver todas las comunidades a las que pertenece un usuario---
class ComunidadesUsuarioController(APIView):

    def get(self, request, idUsuario=None):
        """
        GET comunidad/mis-comunidades/{idUsuario} 
        Obtener todas las comunidades a las que pertenece un usuario específico.
        """
        if idUsuario is None:
             return Response({"error": "Se requiere el ID del usuario"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Llamamos al DAO con el ID que viene en la URL
            comunidades_dto = ComunidadDAO.get_comunidades_usuario(idUsuario)
            
            data = [dataclasses.asdict(c) for c in comunidades_dto]
            # Devolvemos la lista (vacía o con datos) y status 200 OK
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
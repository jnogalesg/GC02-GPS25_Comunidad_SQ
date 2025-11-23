from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from comunidades.dao.comunidad_dao import ComunidadDAO
import dataclasses 
import traceback # Para ver errores completos

class ComunidadController(APIView):
    
    def get(self, request, idComunidad=None):
        """
        Realiza GET comunidad/ (lista de todas las comunidades) 
        GET comunidad/{idComunidad} (comunidad especifica)
        """
        if idComunidad: # Si se especifica un id, buscamos una comunidad concreta
            try:
                # 1. Pide al DAO la comunidad especificada
                comunidad_dto = ComunidadDAO.get_comunidad_especifica(idComunidad)
                return Response(dataclasses.asdict(comunidad_dto), status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Comunidad no encontrada: {e}"}, status=status.HTTP_404_NOT_FOUND)
        else: # Si no se especifica id, devolvemos todas las comunidades
            # 1. Pide al DAO todas las comunidades
            comunidades_dtos = ComunidadDAO.get_all_comunidades()
            # 2. Convierte DTOs a diccionarios para el JSON
            data = [dataclasses.asdict(dto) for dto in comunidades_dtos]
            # 3. Responde
            return Response(data, status=status.HTTP_200_OK)

    def post(self, request, idComunidad=None):
        """
        Realiza POST en comunidad/ (crear una nueva comunidad)
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
        Realiza PUT comunidad/ (Actualizar una comunidad existent)
        """

        # Comprueba que la url tenga un idComunidad válido
        if not idComunidad:
            return Response({"error": "Falta idComunidad en la URL para actualizar"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Se cogen los datos del body para hacer la actualización
        datos_entrada = request.data

        try:
            # Llama al método del DAO para actualizar la comunidad
            comunidad_actualizada = ComunidadDAO.actualizar_comunidad(idComunidad, datos_entrada)
            return Response(dataclasses.asdict(comunidad_actualizada), status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


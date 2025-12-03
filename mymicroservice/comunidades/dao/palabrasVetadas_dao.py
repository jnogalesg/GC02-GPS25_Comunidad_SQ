from typing import List
from comunidades.models import Comunidad
from comunidades.dto.palabrasVetadas_dto import PalabrasVetadasDTO

class PalabrasVetadasDAO:

    @staticmethod
    def _string_to_list(cadena: str) -> List[str]:
        """"
            Convierte una cadena separada por comas en una lista de palabras.
        """
        if not cadena or cadena.strip() == "":
            return []
        # Separa por comas y quita espacios en blanco alrededor
        return [p.strip() for p in cadena.split(',')]

    @staticmethod
    def _list_to_string(lista: List[str]) -> str:
        """
            Convierte una lista de palabras en una cadena separada por comas.
        """
        if not lista:
            return ""
        # Une la lista con comas
        return ",".join(lista)

    @staticmethod
    def get_palabras_vetadas(idComunidad: int) -> PalabrasVetadasDTO:
        """
            Obtiene la lista de palabras vetadas de una comunidad específica.
        """
        
        # Si la url no tiene idComunidad, lanza excepción
        if not idComunidad:
            raise Exception("Falta id de la Comunidad")
        
        # Obtiene la comunidad con el id especificado
        comunidad = Comunidad.objects.get(pk=idComunidad)
        
        # Usa la función auxiliar para convertir el string a lista
        lista_palabras = PalabrasVetadasDAO._string_to_list(comunidad.palabrasVetadas)
        
        # Devuelve el DTO con la lista de palabras
        return PalabrasVetadasDTO(palabras=lista_palabras)

    @staticmethod
    def add_palabras_vetadas(idComunidad: int, nuevas_palabras: List[str]) -> PalabrasVetadasDTO:
        """
        Añade nuevas palabras vetadas a una comunidad específica.
        """
        
        comunidad = Comunidad.objects.get(pk=idComunidad)
        # Obtenemos las palabras vetadas actuales
        actuales = PalabrasVetadasDAO._string_to_list(comunidad.palabrasVetadas)
        
        # Usamos un set para evitar duplicados y añadimos las nuevas
        conjunto_actualizado = set(actuales)
        # Se eliminan los espacios para evitar problemas
        nuevas_limpias = [p.strip() for p in nuevas_palabras if p.strip()]
        # Actualizamos el conjunto con las nuevas palabras limpias
        conjunto_actualizado.update(nuevas_limpias)
        
        lista_final = list(conjunto_actualizado)
        
        # Guardamos en BD como string
        comunidad.palabrasVetadas = PalabrasVetadasDAO._list_to_string(lista_final)
        comunidad.save()
        
        return PalabrasVetadasDTO(palabras=lista_final)

    @staticmethod
    def eliminar_palabras_vetadas(idComunidad: int, palabras_borrar: List[str]) -> PalabrasVetadasDTO:
        """
        Elimina palabras vetadas específicas de una comunidad.
        """
        comunidad = Comunidad.objects.get(pk=idComunidad)
        actuales = PalabrasVetadasDAO._string_to_list(comunidad.palabrasVetadas)
        
        # Filtramos: nos quedamos con las que NO estén en la lista de borrar
        borrar = set(p.strip() for p in palabras_borrar)
        lista_final = [p for p in actuales if p.strip() not in borrar]
        
        comunidad.palabrasVetadas = PalabrasVetadasDAO._list_to_string(lista_final)
        comunidad.save()
        
        return PalabrasVetadasDTO(palabras=lista_final)

    @staticmethod
    def modificar_palabras_vetadas(idComunidad: int, nueva_lista_completa: List[str]) -> PalabrasVetadasDTO:
        """
        Modifica la lista completa de palabras vetadas de una comunidad.
        """
        comunidad = Comunidad.objects.get(pk=idComunidad)
        
        # Preparamos la nueva lista para sustituir la anterior
        lista_limpia = [p.strip() for p in nueva_lista_completa if p.strip()]
        
        comunidad.palabrasVetadas = PalabrasVetadasDAO._list_to_string(lista_limpia)
        comunidad.save()
        
        return PalabrasVetadasDTO(palabras=lista_limpia)
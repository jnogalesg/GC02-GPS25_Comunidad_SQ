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

from typing import List
from comunidades.models import PersonasVetadas
from comunidades.dto.personasVetadas_dto import PersonaVetadaDTO
from comunidades.dao.miembro_dao import MiembroDAO

class PersonasVetadasDAO:

    @staticmethod
    def _to_dto(modelo: PersonasVetadas) -> PersonaVetadaDTO:
        '''
        Convierte un modelo de PersonasVetadas a un DTO.
        '''
        return PersonaVetadaDTO(
            idUsuario=modelo.idUsuario,
            idComunidad=modelo.idComunidad_id, # Usamos _id para coger el ID directamente
            fechaVeto=modelo.fechaVeto
        )

    @staticmethod
    def get_vetados(comunidad: int) -> List[PersonaVetadaDTO]:
        ''' 
        Devuelve la lista de personas vetadas en una comunidad específica.
        '''
        
        # filtramos para obtener sólamente los vetados de la comunidad especificada (idComunidad en la URL)
        vetados = PersonasVetadas.objects.filter(idComunidad_id=comunidad)
        
        # devolvemos la lista de usuarios vetados
        return [PersonasVetadasDAO._to_dto(v) for v in vetados]

    @staticmethod
    def vetar_miembro(comunidad: int, usuario: int) -> PersonaVetadaDTO:
        '''
        Crea un nuevo veto para un miembro en una comunidad.
        '''
        # Verificamos si ya está vetado para evitar error 500 por duplicado
        if PersonasVetadas.objects.filter(idComunidad_id=comunidad, idUsuario=usuario).exists():
             raise Exception(f"El usuario {usuario} ya está vetado en esta comunidad.")
             
        # Si no existe, creamos el veto
        nuevo_veto = PersonasVetadas.objects.create(
            idComunidad_id=comunidad,
            idUsuario=usuario
        )
        
        # 3. Echar al miembro (Kick)
        try:
            # Eliminamos al miembro de la comunidad (si está en ella)
            MiembroDAO.eliminar_miembro(comunidad, usuario)
            print(f"INFO: Usuario {usuario} expulsado de la comunidad al ser vetado.")
        except Exception:
            # Si el usuario no era miembro, no pasa nada
            pass
        
        # Se devuelve el DTO del nuevo veto
        return PersonasVetadasDAO._to_dto(nuevo_veto)

    @staticmethod
    def quitar_veto(comunidad: int, usuario: int):
        try:
            # Intentamos obtener el veto especificado para eliminarlo
            veto = PersonasVetadas.objects.get(idComunidad_id=comunidad, idUsuario=usuario)
            veto.delete()
            
            # Si no se encuetra el veto, se lanza una excepción
        except PersonasVetadas.DoesNotExist:
            raise Exception(f"El usuario {usuario} no está vetado en la comunidad {comunidad}.")
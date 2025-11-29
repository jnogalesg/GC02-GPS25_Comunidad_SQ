from django.urls import path
from comunidades.controller.comunidad_controller import ComunidadController, ComunidadesUsuarioController 
from comunidades.controller.miembro_controller import MiembroController
from comunidades.controller.publicacion_controller import PublicacionController
from comunidades.controller.publicacionMeGusta_controller import PublicacionMeGustaController
from comunidades.controller.personasVetadas_controller import PersonasVetadasController
from comunidades.controller.palabrasVetadas_controller import PalabrasVetadasController

urlpatterns = [

    # --- Comunidades ---
    # GET (listar), POST (crear)
    path('', ComunidadController.as_view()), 
    # GET (específica), DELETE (borrar), PUT (actualizar)
    path('<int:idComunidad>/', ComunidadController.as_view()),
    
    # --- Palabras Vetadas ---
    # GET (todas), POST (añadir), PUT (reemplazar lista), DELETE (eliminar específica)
    path('<int:idComunidad>/palabras-vetadas/', PalabrasVetadasController.as_view()),

    # --- Mis Comunidades (del usuario logueado) ---
    # GET (todas las comunidades de un usuario)
    path('mis-comunidades/<int:idUsuario>/', ComunidadesUsuarioController.as_view()),
        
    # --- Miembros --- 
    # GET (listar), POST (añadir)
    path('miembros/<int:idComunidad>/', MiembroController.as_view()),
    # GET (específico), DELETE (borrar)
    path('miembros/<int:idComunidad>/<int:idMiembro>/', MiembroController.as_view()),
    
    # --- Me Gusta en Publicaciones ---
    # POST, GET y DELETE (específicos) 
    path('publicaciones/megusta/<int:idPublicacion>/', PublicacionMeGustaController.as_view()),
    
    # --- Publicaciones ---
    # GET (listar), POST (crear)
    path('publicaciones/<int:idComunidad>/', PublicacionController.as_view()),
    # GET (específica), DELETE (borrar)
    path('publicaciones/<int:idComunidad>/<int:idPublicacion>/', PublicacionController.as_view()),
    
    # --- Personas Vetadas ---
    # GET (listar), POST (vetar)
    path('vetados/<int:idComunidad>/', PersonasVetadasController.as_view()),
    # DELETE (quitar veto)
    path('vetados/<int:idComunidad>/<int:idUsuario>/', PersonasVetadasController.as_view()),
]
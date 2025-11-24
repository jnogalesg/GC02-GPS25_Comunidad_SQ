from django.urls import path
from comunidades.controller.comunidad_controller import ComunidadController
from comunidades.controller.miembro_controller import MiembroController
from comunidades.controller.personasVetadas_controller import PersonasVetadasController 
from comunidades.controller.publicacion_controller import PublicacionController

urlpatterns = [

    # --- Comunidades ---
    # GET (listar), POST (crear)
    path('', ComunidadController.as_view()), 
    # GET (específica), DELETE(borrar), PUT (actualizar)
    path('<int:idComunidad>/', ComunidadController.as_view()),
    
    # --- Miembros --- 
    # GET (listar), POST (añadir)
    path('miembros/<int:idComunidad>/', MiembroController.as_view()),
    # GET (específico), DELETE (eliminar)
    path('miembros/<int:idComunidad>/<int:idMiembro>/', MiembroController.as_view()),
    
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
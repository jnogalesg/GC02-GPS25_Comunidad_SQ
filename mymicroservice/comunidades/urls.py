from django.urls import path
from comunidades.controller.comunidad_controller import ComunidadController
from comunidades.controller.miembro_controller import MiembroController 

urlpatterns = [

    # --- Comunidades ---
    # GET (listar), POST (crear)
    path('', ComunidadController.as_view()), 
    # GET (específica), DELETE(borrar), PUT (actualizar)
    path('<int:idComunidad>/', ComunidadController.as_view()),
    
    # --- Miembros --- 
    # GET (listar), POST (añadir)
    path('miembros/<int:idComunidad>/', MiembroController.as_view()),
]
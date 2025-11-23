from django.urls import path
from comunidades.controller.comunidad_controller import ComunidadController 

urlpatterns = [

    # --- Comunidades ---
    # GET (listar), POST (crear)
    path('', ComunidadController.as_view()), 
    # GET (específica), DELETE(borrar), PUT (actualizar)
    path('<int:idComunidad>/', ComunidadController.as_view())
    
]
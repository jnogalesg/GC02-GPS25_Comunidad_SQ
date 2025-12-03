#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import socket
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mymicroservice.settings')
    
    # --- CÓDIGO PERSONALIZADO PARA MOSTRAR DIRECCIÓN LOCAL Y EN RED DE LA API---
    # Si el comando es 'runserver', imprimimos el cuadro bonito antes de nada
    if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "127.0.0.1"
            
        # Buscamos el puerto (indicado a continuación del comando runserver) 
        port = '8000' # Por defecto
        for arg in sys.argv:
            if arg.startswith('0.0.0.0:'):
                port = arg.split(':')[1]
            elif arg.isdigit() and len(arg) >= 4:
                port = arg

        print("\n" + "="*60)
        print(f"🚀  API Comunidades - UnderSounds (Puerto {port})")
        print("="*60)
        print(f"💻  Local:            http://127.0.0.1:{port}/")
        print(f"🌐  En tu red (WiFi): http://{local_ip}:{port}/")
        print("="*60 + "\n")
    # -------------------------------
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

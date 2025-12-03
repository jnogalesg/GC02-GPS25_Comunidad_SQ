# GC02-GPS25_Comunidad
Creación de la base de datos para la API de Comunidad de la aplicación UnderSounds. - GPS 25/26, Ing. Software

**Microservicio de Comunidades (UnderSounds)**

Este proyecto contiene la API REST para la gestión de comunidades de la plataforma UnderSounds, construido con Django y Django REST Framework, conectado con una base de datos SQLite.

## Características Principales
* ⚡️ API REST construida con Django y Django REST Framework
* 🗃️ Base de datos ligera con SQLite 3 (configuración por defecto de Django)
* 🧩 Arquitectura limpia desacoplada con patrón DAO, DTO y Controller (APIView)
* 📑 Documentación y contrato de API definidos con OpenAPI (YAML)
* 🤝 Patrón de Composición de Microservicios (consulta datos de servicios externos como Usuarios)
* 🔒 Preparado para autenticación (el YAML define endpoints con Bearer Auth)

## 🚀 Puesta en marcha (Desarrollo Local)

Sigue estos pasos para clonar, instalar y ejecutar el servidor en tu máquina local.

### 🔙 1. Prerrequisitos

* [Python](https://www.python.org/downloads/) 3.10+
* [Git](https://git-scm.com/install/)

### 🛠️ 2. Instalación

1.  Clona el repositorio (si no lo has hecho):
    ```bash
    git clone https://github.com/jnogalesg/GC02-GPS25_Comunidad
    cd GC02-GPS25_ComunidadBETA
    ```

2.  Crea un entorno virtual. Esto aísla las dependencias del proyecto.
    ```bash
    python -m venv venv
    ```

3.  Activa el entorno virtual:
    ```bash
    # En Windows (CMD o PowerShell)
    .\venv\Scripts\activate
    
    # En macOS/Linux
    source venv/bin/activate
    ```
    Verás un `(venv)` al inicio de tu línea de comandos si se activó correctamente.

4.  Instala todas las dependencias del proyecto:
    ```bash
    pip install -r requirements.txt
    ```
    *`requirements.txt` incluye la instalación de Django, Django REST Framework, request y otras dependecias necesarias*

## ⚙️ 3. Configuración del Entorno

Para garantizar el correcto funcionamiento del microservicio y su integración con el resto del ecosistema UnderSounds, es **obligatorio** revisar la configuración de las siguientes variables de entorno.

Estas variables permiten adaptar la conexión con otros servicios (como la API de Usuarios) sin necesidad de modificar el código fuente, facilitando el despliegue en diferentes entornos (local, producción, docker).

| Variable | Descripción | Valor por Defecto (Desarrollo) |
| :--- | :--- | :--- |
| `USER_MICROSERVICE_URL` | **Crítica.** URL base de la API de Usuarios. Este servicio la utiliza para validar y obtener datos de Artistas y Miembros. Si este servicio cambia de dirección, **debes** actualizar esta variable. | `http://127.0.0.1:3000/api/usuarios/` |
| `DEBUG` | Define si Django se ejecuta en modo depuración (muestra errores detallados). **Debe establecerse a `False` en entornos de producción.** | `True` |

> **Importante:** El sistema intentará conectarse a `http://127.0.0.1:3000/api/usuarios/` por defecto. Si el servicio de usuarios está en otro puerto o dominio, el sistema **fallará** al intentar crear comunidades o añadir miembros si no se configura `USER_MICROSERVICE_URL` correctamente.

### 🧑🏻‍💻 4. Configuración de la Base de Datos

Este proyecto utiliza **SQLite** por defecto, por lo que no requiere un servidor de base de datos externo.

1.  Aplica las migraciones para crear las tablas en el archivo `db.sqlite3`:
```bash
python mymicroservice/manage.py makemigrations
python mymicroservice/manage.py migrate
```
2.  **Crea un superusuario** para acceder al panel de administración:
```bash
python mymicroservice/manage.py createsuperuser
```
*Sigue las instrucciones en pantalla. Puedes usar `admin` como nombre y contraseña para desarrollo local.*

### 🚀 5. Ejecutar el Servidor

Una vez instalado y con la base de datos migrada, puedes iniciar el servidor de desarrollo:

```bash
python mymicroservice/manage.py runserver 0.0.0.0:8084
```

El servidor estará corriendo y escuchando en http://127.0.0.1:8084/

##### 🔍 Inspección y modificación directa de la base de datos:

Puede realizarse desde el panel de superusuario de Django, a través de la dirección: http://127.0.0.1:8084/admin
*(Usa el usuario y contraseña que creaste en el paso 3)*

## 📁 Arquitectura del microservicio
```
mymicroservice/
├── mymicroservice/       # ⚙️ Configuración global del proyecto Django
│   ├── settings.py       # Variables de entorno, apps instaladas, BD
│   ├── urls.py           # Enrutador principal
│   └── wsgi.py           # Punto de entrada para servidores web
│
├── comunidades/          # 📦 App principal (Lógica del dominio Comunidad)
│   ├── controller/       # 🤵 Controladores (APIViews - Gestionan peticiones HTTP)
│   │   ├── comunidad_controller.py
│   │   ├── miembro_controller.py
│   │   └── ...
│   ├── dao/              # 👨‍🍳 Data Access Objects (Acceso a BD y APIs externas)
│   │   ├── comunidad_dao.py
│   │   ├── miembro_dao.py
│   │   └── ...
│   ├── dto/              # 🍛 Data Transfer Objects (Estructuras de datos puras)
│   │   ├── comunidad_dto.py
│   │   ├── artista_dto.py
│   │   └── ...
│   ├── migrations/       # 🗃️ Historial de cambios en la base de datos
│   ├── models.py         # 🧱 Definición de tablas 
│   ├── urls.py           # 🔗 Rutas específicas de la API de comunidades
│   └── admin.py          # 🛠️ Panel de administración
│
├── manage.py             # 🚀 Script de ejecución y gestión del servidor
└── requirements.txt      # 📦 Dependencias del proyecto
```
from django.db import models

# Creación de las tablas para la base de datos del endpoint

class Comunidad(models.Model):
    # Id de la comunidad - lo genera automaticamente django para cada comunidad que se vaya creando
    idComunidad = models.AutoField(primary_key=True) 
    # Id del artista que crea la comunidad
    idArtista = models.IntegerField(unique=True) 
    # Nombre de la comunidad
    nombreComunidad = models.CharField(max_length=100, unique=True)
    # Descripción de la comunidad
    descComunidad = models.TextField(blank=True, null=True)
    # Ruta de la imagen de la comunidad
    rutaImagen = models.CharField(max_length=255, blank=True, null=True)
    # Fecha de creación de la comunidad
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    # Lista de palabras vetadas en la comunidad (lista separada por comas)
    palabrasVetadas = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombreComunidad


class ComunidadMiembros(models.Model):
    # Id de la comunidad
    idComunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    # Id del usuario miembro de la comunidad
    idUsuario = models.IntegerField()
    # Fecha de unión del usuario a la comunidad
    fechaUnion = models.DateTimeField(auto_now_add=True)

    # Creación de restricción
    class Meta:
        # Un usuario no puede estar más de una vez en la misma comunidad
        # CADA ID_USUARIO SOLO PUEDE APARECER UNA VEZ POR CADA ID_COMUNIDAD
        unique_together = ('idComunidad', 'idUsuario')

    def __str__(self):
        return f"Usuario {self.idUsuario} en {self.idComunidad.nombreComunidad}"


class Publicacion(models.Model):
    # Id de la publicación - lo genera automaticamente django para cada publicación que se vaya creando
    idPublicacion = models.AutoField(primary_key=True)
    # Id de la comunidad a la que pertenece la publicación
    idComunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    # Título de la publicación
    titulo = models.CharField(max_length=255)
    # Contenido de la publicación (texto)
    contenido = models.TextField(blank=True, null=True)
    # Fichero adjunto a la publicación (imagen, audio, video, etc.)
    rutaFichero = models.CharField(max_length=255, blank=True, null=True)
    # Fecha de creación de la publicación
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    
    # Creación de restricción
    class Meta:
        # Una publicación debe ser única dentro de una comunidad
        # CADA IDPUBLICACION SOLO PUEDE APARECER UNA VEZ POR CADA IDCOMUNIDAD
        unique_together = ('idPublicacion', 'idComunidad')    

    def __str__(self):
        return self.titulo


class PublicacionMeGusta(models.Model):
    # Id de la publicación
    idPublicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    # Id del usuario que dio me gusta
    idUsuario = models.IntegerField()
    # Fecha en la que se dio el me gusta
    fechaMeGusta = models.DateTimeField(auto_now_add=True)

    # Creación de restricción
    class Meta:
        # Un usuario no puede dar más de un me gusta a la misma publicación
        # CADA IDUSUARIO SOLO PUEDE APARECER UNA VEZ POR CADA IDPUBLICACION
        unique_together = ('idPublicacion', 'idUsuario')

    def __str__(self):
        return f"Me gusta ❤️: Usuario {self.idUsuario} → {self.idPublicacion.titulo}"


class PersonasVetadas(models.Model):
    # Id de la comunidad en la que se realiza el veto
    idComunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    # Id del miembro vetado
    idUsuario = models.IntegerField()
    # Fecha del veto
    fechaVeto = models.DateTimeField(auto_now_add=True)

    # Creación de restricción
    class Meta:
        # Un miembro no puede ser vetado más de una vez en la misma comunidad
        # CADA IDUSUARIO SOLO PUEDE APARECER UNA VEZ POR CADA IDCOMUNIDAD
        unique_together = ('idComunidad', 'idUsuario')

    def __str__(self):
        return f"Usuario {self.idUsuario} vetado en {self.idComunidad.nombreComunidad}"
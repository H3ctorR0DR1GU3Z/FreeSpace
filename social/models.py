from django.db import models
from django.contrib.auth.models import User

class Publicacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publicaciones")
    contenido = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="publicaciones/", blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha}"

class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name="likes")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'publicacion')

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name="comentarios")
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

class Amistad(models.Model):
    de_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="solicitudes_enviadas")
    para_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="solicitudes_recibidas")
    aceptada = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('de_usuario', 'para_usuario')

class Compartido(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    de_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compartidos_enviados")
    para_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compartidos_recibidos")
    fecha = models.DateTimeField(auto_now_add=True)

class MensajePrivado(models.Model):
    de_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enviados")
    para_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recibidos")
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['fecha']
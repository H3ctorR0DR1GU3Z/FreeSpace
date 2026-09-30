from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    nickname = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True, max_length=200)
    foto = models.ImageField(upload_to="perfiles/", blank=True, null=True)
    privado = models.BooleanField(default=False) # True = solo amigos ven
    def __str__(self): return self.usuario.username

class Publicacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publicaciones")
    contenido = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="publicaciones/", blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    def total_likes(self): return self.likes.count()

class HistoriaDestacada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="historias")
    titulo = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to="historias/")
    fecha = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name="likes")
    class Meta: unique_together = ('usuario', 'publicacion')

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name="comentarios")
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

class Amistad(models.Model):
    de_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enviadas")
    para_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recibidas")
    aceptada = models.BooleanField(default=False)
    class Meta: unique_together = ('de_usuario', 'para_usuario')

class MensajePrivado(models.Model):
    de_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_enviados")
    para_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_recibidos")
    contenido = models.TextField(blank=True)
    audio = models.FileField(upload_to="audios/", blank=True, null=True)
    imagen = models.ImageField(upload_to="mensajes/", blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    editado = models.BooleanField(default=False)
    class Meta: ordering = ['fecha']

class Guardado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guardados")
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    class Meta: unique_together = ('usuario', 'publicacion')

@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created: Perfil.objects.get_or_create(usuario=instance)
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("registro/", views.registro, name="registro"),
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("like/<int:publicacion_id>/", views.dar_like, name="dar_like"),
    path("comentar/<int:publicacion_id>/", views.comentar, name="comentar"),
    path("comentario/borrar/<int:id>/", views.borrar_comentario, name="borrar_comentario"),
    path("amistad/enviar/<int:user_id>/", views.enviar_solicitud, name="enviar_solicitud"),
    path("amistad/aceptar/<int:amistad_id>/", views.aceptar_solicitud, name="aceptar_solicitud"),
    path("compartir/<int:pub_id>/a/<int:user_id>/", views.compartir_a_amigo, name="compartir_a_amigo"),
]
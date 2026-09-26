from django.urls import path
from. import views

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("like/<int:publicacion_id>/", views.dar_like, name="dar_like"),
    path("comentar/<int:publicacion_id>/", views.comentar, name="comentar"),
    path("borrar_comentario/<int:id>/", views.borrar_comentario, name="borrar_comentario"),
    path("solicitud/<int:user_id>/", views.enviar_solicitud, name="enviar_solicitud"),
    path("aceptar/<int:amistad_id>/", views.aceptar_solicitud, name="aceptar_solicitud"),
    path("compartir/<int:pub_id>/<int:user_id>/", views.compartir_a_amigo, name="compartir_a_amigo"),
    path("mensajes/", views.bandeja_mensajes, name="mensajes"),
    path("mensajes/<int:user_id>/", views.chat_privado, name="chat_privado"),
    path("registro/", views.registro, name="registro"),
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
]
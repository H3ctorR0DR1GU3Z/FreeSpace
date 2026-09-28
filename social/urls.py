from django.urls import path
from . import views
urlpatterns=[
 path("", views.home, name="home"),
 path("feed/", views.feed, name="feed"),
 path("like/<int:id>/", views.dar_like, name="dar_like"),
 path("comentar/<int:id>/", views.comentar, name="comentar"),
 path("borrar_comentario/<int:id>/", views.borrar_comentario, name="borrar_comentario"),
 path("guardar/<int:id>/", views.guardar_post, name="guardar_post"),
 path("solicitud/<int:uid>/", views.enviar_solicitud, name="enviar_solicitud"),
 path("aceptar/<int:aid>/", views.aceptar_solicitud, name="aceptar_solicitud"),
 path("rechazar/<int:aid>/", views.rechazar_solicitud, name="rechazar_solicitud"),
 path("eliminar_amigo/<int:uid>/", views.eliminar_amigo, name="eliminar_amigo"),
 path("mensajes/", views.bandeja, name="mensajes"),
 path("mensajes/<int:uid>/", views.chat, name="chat"),
 path("editar_mensaje/<int:mid>/", views.editar_mensaje, name="editar_mensaje"),
 path("borrar_mensaje/<int:mid>/", views.borrar_mensaje, name="borrar_mensaje"),
 path("perfil/<int:uid>/", views.ver_perfil, name="ver_perfil"),
 path("configuracion/", views.configuracion, name="configuracion"),
 path("registro/", views.registro, name="registro"),
 path("login/", views.login_view, name="login"),
 path("logout/", views.logout_view, name="logout"),
]
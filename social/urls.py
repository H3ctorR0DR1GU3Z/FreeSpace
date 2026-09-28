from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('feed/', views.feed, name='feed'),
    
    path('like/<int:pid>/', views.dar_like, name='like'),
    path('comentar/<int:pid>/', views.comentar, name='comentar'),
    path('guardar/<int:pid>/', views.guardar_pub, name='guardar'),

    # PERFIL - acepta las dos rutas para no pelear
    path('profile/<int:uid>/', views.ver_perfil, name='profile'),
    path('perfil/<int:uid>/', views.ver_perfil, name='perfil'),

    path('configuracion/', views.configuracion, name='configuracion'),
    
    # MENSAJES - tu archivo se llama messenges.html pero la URL sigue siendo /mensajes/
    path('mensajes/', views.bandeja_mensajes, name='mensajes'),
    path('mensajes/<int:uid>/', views.chat, name='chat'),
    path('borrar_mensaje/<int:mid>/', views.borrar_mensaje, name='borrar_mensaje'),
    path('editar_mensaje/<int:mid>/', views.editar_mensaje, name='editar_mensaje'),

    path('eliminar_amigo/<int:uid>/', views.eliminar_amigo, name='eliminar_amigo'),
    path('aceptar/<int:sid>/', views.aceptar_solicitud, name='aceptar'),
    path('rechazar/<int:sid>/', views.rechazar_solicitud, name='rechazar'),
]
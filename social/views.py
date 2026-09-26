from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Publicacion, Like, Comentario, Amistad, Compartido

def get_amigos(user):
    amistades = Amistad.objects.filter(Q(de_usuario=user) | Q(para_usuario=user), aceptada=True)
    amigos = []
    for a in amistades:
        amigos.append(a.para_usuario if a.de_usuario == user else a.de_usuario)
    return amigos

def home(request):
    if request.user.is_authenticated:
        return redirect("feed")
    return render(request, "home.html")

@login_required
def feed(request):
    if request.method == "POST":
        contenido = request.POST.get("contenido")
        imagen = request.FILES.get("imagen")
        if contenido or imagen:
            Publicacion.objects.create(usuario=request.user, contenido=contenido, imagen=imagen)
            return redirect("feed")

    publicaciones = Publicacion.objects.all().order_by("-fecha")
    perfiles = User.objects.exclude(id=request.user.id)[:10]
    amigos = get_amigos(request.user)
    solicitudes = Amistad.objects.filter(para_usuario=request.user, aceptada=False)
    compartidos = Compartido.objects.filter(para_usuario=request.user).order_by("-fecha")[:10]

    return render(request, "feed.html", {
        "publicaciones": publicaciones,
        "perfiles": perfiles,
        "amigos": amigos,
        "solicitudes": solicitudes,
        "compartidos": compartidos
    })

@login_required
def dar_like(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    like, creado = Like.objects.get_or_create(usuario=request.user, publicacion=publicacion)
    if not creado:
        like.delete()
        liked = False
    else:
        liked = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'likes': publicacion.total_likes(), 'liked': liked})
    return redirect("feed")

@login_required
def comentar(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    if request.method == "POST":
        contenido = request.POST.get("contenido_comentario")
        if contenido:
            Comentario.objects.create(usuario=request.user, publicacion=publicacion, contenido=contenido)
    return redirect("feed")

@login_required
def borrar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    if comentario.usuario == request.user:
        comentario.delete()
    return redirect("feed")

@login_required
def enviar_solicitud(request, user_id):
    para = get_object_or_404(User, id=user_id)
    if para != request.user:
        Amistad.objects.get_or_create(de_usuario=request.user, para_usuario=para)
    return redirect("feed")

@login_required
def aceptar_solicitud(request, amistad_id):
    amistad = get_object_or_404(Amistad, id=amistad_id, para_usuario=request.user)
    amistad.aceptada = True
    amistad.save()
    return redirect("feed")

@login_required
def compartir_a_amigo(request, pub_id, user_id):
    pub = get_object_or_404(Publicacion, id=pub_id)
    para = get_object_or_404(User, id=user_id)
    Compartido.objects.create(publicacion=pub, de_usuario=request.user, para_usuario=para)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'msg': f'Enviado a {para.username}'})
    return redirect("feed")

def registro(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        if not username or not password:
            messages.error(request, "Debes llenar todos los campos.")
            return render(request, "registro.html")

        if password != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "registro.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese usuario ya existe.")
            return render(request, "registro.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("feed")

    return render(request, "registro.html")

def iniciar_sesion(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("feed")
        messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "login.html")

def cerrar_sesion(request):
    logout(request)
    return redirect("home")
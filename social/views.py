from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Perfil, Publicacion, Comentario, Like, Mensaje, Guardado, SolicitudAmistad, Amistad, HistoriaDestacada

def home(request):
    return render(request, 'home.html')

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            Perfil.objects.create(usuario=user)
            auth_login(request, user)
            return redirect('/feed/')
    return render(request, 'registro.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            auth_login(request, user)
            return redirect('/feed/')
    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('/')

@login_required
def feed(request):
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        imagen = request.FILES.get('imagen')
        if contenido or imagen:
            Publicacion.objects.create(usuario=request.user, contenido=contenido, imagen=imagen)
        return redirect('/feed/')
    
    publicaciones = Publicacion.objects.all().order_by('-id')
    perfil = request.user.perfil
    amigos = [a.amigo for a in Amistad.objects.filter(usuario=request.user)]
    solicitudes = SolicitudAmistad.objects.filter(para_usuario=request.user)
    return render(request, 'feed.html', {'publicaciones': publicaciones, 'amigos': amigos, 'solicitudes': solicitudes, 'perfil': perfil})

@login_required
def dar_like(request, pid):
    pub = get_object_or_404(Publicacion, id=pid)
    like, creado = Like.objects.get_or_create(usuario=request.user, publicacion=pub)
    if not creado:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'likes': pub.likes.count(), 'liked': liked})

@login_required
def comentar(request, pid):
    pub = get_object_or_404(Publicacion, id=pid)
    if request.method == 'POST':
        cont = request.POST.get('contenido_comentario') or request.POST.get('contenido')
        if cont:
            c = Comentario.objects.create(usuario=request.user, publicacion=pub, contenido=cont)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'contenido': c.contenido, 'usuario': c.usuario.username})
    return redirect('/feed/')

@login_required
def guardar_pub(request, pid):
    pub = get_object_or_404(Publicacion, id=pid)
    g, creado = Guardado.objects.get_or_create(usuario=request.user, publicacion=pub)
    if not creado:
        g.delete()
        guardado = False
    else:
        guardado = True
    return JsonResponse({'guardado': guardado})

@login_required
def ver_perfil(request, uid):
    perfil_user = get_object_or_404(User, id=uid)
    es_amigo = Amistad.objects.filter(usuario=request.user, amigo=perfil_user).exists() or request.user.id == uid
    if perfil_user.perfil.privado and not es_amigo:
        pubs = []
    else:
        pubs = Publicacion.objects.filter(usuario=perfil_user).order_by('-id')
    return render(request, 'profile.html', {'perfil_user': perfil_user, 'publicaciones': pubs, 'historias': perfil_user.perfil.historias.all()})

@login_required
def configuracion(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        perfil.nickname = request.POST.get('nickname', '')
        perfil.bio = request.POST.get('bio', '')
        perfil.privado = bool(request.POST.get('privado'))
        if request.FILES.get('foto'):
            perfil.foto = request.FILES.get('foto')
        perfil.save()
        if request.POST.get('historia_titulo') and request.FILES.get('historia_img'):
            HistoriaDestacada.objects.create(perfil=perfil, titulo=request.POST.get('historia_titulo'), imagen=request.FILES.get('historia_img'))
        return redirect('/configuracion/')
    guardados = Guardado.objects.filter(usuario=request.user)
    return render(request, 'configuracion.html', {'perfil': perfil, 'guardados': guardados})

@login_required
def bandeja_mensajes(request):
    amigos = Amistad.objects.filter(usuario=request.user)
    conversaciones = []
    for a in amigos:
        ultimo = Mensaje.objects.filter(de_usuario__in=[request.user, a.amigo], para_usuario__in=[request.user, a.amigo]).order_by('-id').first()
        noread = Mensaje.objects.filter(de_usuario=a.amigo, para_usuario=request.user, leido=False).count()
        conversaciones.append({'amigo': a.amigo, 'ultimo': ultimo, 'noread': noread})
    return render(request, 'messenges.html', {'conversaciones': conversaciones})

@login_required
def chat(request, uid):
    otro = get_object_or_404(User, id=uid)
    if request.method == 'POST':
        cont = request.POST.get('contenido', '')
        img = request.FILES.get('imagen')
        audio = request.FILES.get('audio')
        if cont or img or audio:
            Mensaje.objects.create(de_usuario=request.user, para_usuario=otro, contenido=cont, imagen=img, audio=audio)
        return redirect(f'/mensajes/{uid}/')
    mensajes = Mensaje.objects.filter(de_usuario__in=[request.user, otro], para_usuario__in=[request.user, otro]).order_by('id')
    mensajes.filter(para_usuario=request.user).update(leido=True)
    return render(request, 'chat.html', {'otro': otro, 'mensajes': mensajes})

@login_required
def borrar_mensaje(request, mid):
    m = get_object_or_404(Mensaje, id=mid, de_usuario=request.user)
    uid = m.para_usuario.id
    m.delete()
    return redirect(f'/mensajes/{uid}/')

@login_required
def editar_mensaje(request, mid):
    m = get_object_or_404(Mensaje, id=mid, de_usuario=request.user)
    if request.method == 'POST':
        m.contenido = request.POST.get('contenido', m.contenido)
        m.editado = True
        m.save()
    return redirect(f'/mensajes/{m.para_usuario.id}/')

@login_required
def eliminar_amigo(request, uid):
    Amistad.objects.filter(usuario=request.user, amigo_id=uid).delete()
    Amistad.objects.filter(usuario_id=uid, amigo=request.user).delete()
    return redirect('/feed/')

@login_required
def aceptar_solicitud(request, sid):
    s = get_object_or_404(SolicitudAmistad, id=sid, para_usuario=request.user)
    Amistad.objects.get_or_create(usuario=s.de_usuario, amigo=s.para_usuario)
    Amistad.objects.get_or_create(usuario=s.para_usuario, amigo=s.de_usuario)
    s.delete()
    return redirect('/feed/')

@login_required
def rechazar_solicitud(request, sid):
    s = get_object_or_404(SolicitudAmistad, id=sid, para_usuario=request.user)
    s.delete()
    return redirect('/feed/')
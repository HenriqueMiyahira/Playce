from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import CadastroUsuarioForm, PerfilUsuarioForm
from .services import nome_usuario, reservas_do_usuario


def usuarios(request):
    if request.user.is_authenticated:
        return redirect('perfil')

    return redirect('login')


def _preparar_campos(form):
    for field in form.fields.values():
        field.widget.attrs.setdefault('class', 'form-control')

    return form


def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('perfil')

    form = _preparar_campos(AuthenticationForm(request, data=request.POST or None))

    if request.method == 'POST' and form.is_valid():
        auth_login(request, form.get_user())
        messages.success(request, 'Login realizado com sucesso.')
        return redirect(request.GET.get('next') or 'perfil')

    return render(request, 'usuarios/login.html', {'form': form})


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('perfil')

    form = _preparar_campos(CadastroUsuarioForm(request.POST or None))

    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        auth_login(request, usuario)
        messages.success(request, 'Conta criada com sucesso. Seja bem-vindo ao Playce!')
        return redirect('perfil')

    return render(request, 'usuarios/cadastro.html', {'form': form})


@login_required
@require_POST
def logout_usuario(request):
    auth_logout(request)
    messages.info(request, 'Voce saiu da sua conta.')
    return redirect('home_index')


@login_required
def perfil(request):
    reservas = reservas_do_usuario(request.user)[:5]
    contexto = {
        'nome_usuario': nome_usuario(request.user),
        'reservas': reservas,
    }
    return render(request, 'usuarios/perfil.html', contexto)


@login_required
def editar_perfil(request):
    form = _preparar_campos(PerfilUsuarioForm(request.POST or None, user=request.user))

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Perfil atualizado com sucesso.')
        return redirect('perfil')

    return render(request, 'usuarios/perfil_form.html', {'form': form})

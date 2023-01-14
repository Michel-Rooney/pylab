from django.shortcuts import render, redirect, get_object_or_404
from .models import Empresa, Tecnologias, Vagas
from .utils import nova_empresa_is_valid
from django.contrib import messages
import os

def nova_empresa(request):
    if request.method == 'GET':
        techs = Tecnologias.objects.all()
        return render(request, 'nova_empresa.html', {'techs':techs})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cidade = request.POST.get('cidade')
        endereco = request.POST.get('endereco')
        nicho = request.POST.get('nicho')
        tecnologias = request.POST.getlist('tecnologias')
        caracteristicas = request.POST.get('caracteristicas')
        logo = request.FILES.get('logo')

        if not nova_empresa_is_valid(request, nome, email, cidade, endereco, nicho, tecnologias, caracteristicas, logo):
            return redirect('/home/nova_empresa/')
        
        try:
            empresa = Empresa(
                logo=logo, nome=nome, email=email, cidade=cidade, endereco=endereco, nicho_mercado=nicho, caracteristica_empresa=caracteristicas
            )
            empresa.save()
            empresa.tecnologias.add(*tecnologias)
            empresa.save()
            messages.success(request, 'Empresa cadastrada com sucesso')
            return redirect('/home/nova_empresa/')
        except:
            messages.error(request, 'Erro interno do sistema')
            return redirect('/home/nova_empresa')

def empresas(request):
    empresas = Empresa.objects.all()
    tecnologias = Tecnologias.objects.all()
    return render(request, 'empresas.html', {'empresas':empresas, 'teclogias':tecnologias})

def excluir_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    os.remove(empresa.logo.path)
    empresa.delete()
    messages.success(request, 'Empresa excluida com sucesso')
    return redirect('/home/empresas')

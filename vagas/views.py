from django.shortcuts import redirect
from django.contrib import messages
from .utils import vaga_is_valid
from empresa.models import Vagas
from django.http import Http404

def nova_vaga(request):
    if request.method == 'POST':
        empresa = request.POST.get('empresa')
        titulo = request.POST.get('titulo')
        experiencia = request.POST.get('experiencia')
        data_final = request.POST.get('data_final')
        status = request.POST.get('status')
        tecnologias_domina = request.POST.getlist('tecnologias_domina')
        tecnologias_nao_domina = request.POST.getlist('tecnologias_nao_domina')
        email = request.POST.get('email')

        if not vaga_is_valid(request, empresa, titulo, experiencia, data_final, status, tecnologias_domina, tecnologias_domina, email):
            return redirect(f'/home/empresa/{empresa}')

        vaga = Vagas(
            empresa_id=empresa, titulo=titulo, nivel_experiencia=experiencia, data_final=data_final, status=status, email=email
        )
        vaga.save()
        vaga.tecnologias_estudar.add(*tecnologias_nao_domina)
        vaga.tecnologias_dominadas.add(*tecnologias_domina)
        vaga.save()
        messages.success(request, 'Vaga criada com sucesso')
        return redirect(f'/home/empresa/{empresa}')
    elif request.method == 'GET':
        raise Http404

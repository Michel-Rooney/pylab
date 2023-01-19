from .utils import vaga_is_valid, nova_tarefa_is_valid, atualizar_status_is_valid
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from apps.empresa.models import Vagas, Tecnologias
from django.utils.html import strip_tags
from django.contrib import messages
from .models import Tarefa, Emails
from django.conf import settings
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

def vaga(request, id):
    vaga = get_object_or_404(Vagas, id=id)
    tarefas = Tarefa.objects.filter(vaga=vaga).filter(realizada=False)
    emails = Emails.objects.filter(vaga=vaga)
    return render(request, 'vaga.html', {'vaga':vaga, 'tarefas':tarefas, 'emails':emails})

def nova_tarefa(request, id_vaga):
    titulo = request.POST.get('titulo')
    prioridade = request.POST.get('prioridade')
    data = request.POST.get('data')

    if not nova_tarefa_is_valid(request, titulo, prioridade, data):
        return redirect(f'/vagas/vaga/{id_vaga}')

    try:
        tarefa = Tarefa(vaga_id=id_vaga, titulo=titulo, prioridade=prioridade, data=data)
        tarefa.save()
        messages.success(request, 'Tarefa criada com sucesso')
        return redirect(f'/vagas/vaga/{id_vaga}')
    except:
        messages.error(request, 'Erro interno do sistema')
        return redirect(f'/vagas/vaga/{id_vaga}')

def realizar_tarefa(request, id):
    tarefa_list = Tarefa.objects.filter(id=id).filter(realizada=False)

    if not tarefa_list.exists():
        messages.error(request, 'Erro interno do sistema')
        return redirect(f'/home/empresas/')
    
    try:
        tarefa = tarefa_list.first()
        tarefa.realizada = True
        tarefa.save()
        messages.success(request, 'Tarefa realizada com sucesso')
        return redirect(f'/vagas/vaga/{tarefa.vaga.id}')
    except:
        messages.error(request, 'Erro interno do sistema')
        return redirect(f'/vagas/vaga/{tarefa.vaga.id}')
        
def envia_email(request, id_vaga):
    vaga = Vagas.objects.get(id=id_vaga)
    assunto = request.POST.get('assunto')
    corpo = request.POST.get('corpo')

    html_content = render_to_string('emails/template_email.html', {'corpo': corpo})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, [vaga.email, settings.EMAIL_HOST_USER])
    email.attach_alternative(html_content, "text/html")
    if email.send():
        mail = Emails(vaga=vaga, assunto=assunto, corpo=corpo, enviado=True)
        mail.save()
        messages.success(request, 'Email enviado com sucesso.')
        return redirect(f'/vagas/vaga/{id_vaga}')
    else:
        mail = Emails(vaga=vaga, assunto=assunto, corpo=corpo, enviado=False)
        mail.save()
        messages.error(request, 'Erro interno do sistema!')
        return redirect(f'/vagas/vaga/{id_vaga}')
    
def adicionar_tecnologia_estudar(request, id_tech, id_vaga):
    try:
        tecnologia = get_object_or_404(Tecnologias, id=id_tech)
        vaga = get_object_or_404(Vagas, id=id_vaga)
        vaga.tecnologias_estudar.add(tecnologia)
        vaga.tecnologias_dominadas.remove(tecnologia)
        vaga.save()
        messages.success(request, f'{tecnologia} está na sua lista de estudo')
    except:
        messages.error(request, 'Erro interno do sistema')
    return redirect(f'/vagas/vaga/{id_vaga}')

def adicionar_tecnologia_domina(request, id_tech, id_vaga):
    try:
        tecnologia = get_object_or_404(Tecnologias, id=id_tech)
        vaga = get_object_or_404(Vagas, id=id_vaga)
        vaga.tecnologias_dominadas.add(tecnologia)
        vaga.tecnologias_estudar.remove(tecnologia)
        vaga.save()
        messages.success(request, f'{tecnologia} está na sua lista de domino')
    except:
        messages.error(request, 'Erro interno do sistema')
    return redirect(f'/vagas/vaga/{id_vaga}')

def atualizar_status(request, id_vaga):
    try:
        vaga = get_object_or_404(Vagas, id=id_vaga)
        status = request.POST.get('status')
        if not atualizar_status_is_valid(request, status):
            return redirect(f'/vagas/vaga/{id_vaga}')
        vaga.status = status
        vaga.save()
        messages.success(request, 'Status atulizado com sucesso')
    except:
        messages.error(request, 'Não foi possível atulizar os status')
    return redirect(f'/vagas/vaga/{id_vaga}')
from empresa.models import Tecnologias, Vagas, Empresa
from django.contrib import messages
from datetime import datetime, date
import re

def vaga_is_valid(request, empresa: str, titulo: str, experiencia: str, data_final: str, statu: str, tecnologias_domina: list, tecnologias_nao_domina: list, email: str) -> bool:
    tecnologias = [str(tech.id) for tech in Tecnologias.objects.all()]
    experiencias = [exp[0] for exp in Vagas.choices_experiencia]
    empresas = [str(emp.id) for emp in Empresa.objects.all()]
    status = [st[0] for st in Vagas.choices_status]
    padrao_email = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$') # example@domain.com
    data_atual = datetime.strftime(date.today(), "%Y-%m-%d")

    if (len(titulo.strip()) == 0) or (not data_final) or (len(status.strip()) == 0) or (len(email.strip()) == 0):
        messages.error(request, 'Preencha todos os campos')
        return False
    if not tecnologias_domina > tecnologias:
        messages.error(request, 'Tecnologia que domina inválida')
        return False
    if not tecnologias_nao_domina > tecnologias:
        messages.error(request, 'Tecnologia que não domina inválida')
        return False
    if not experiencia in experiencias:
        messages.error(request, 'A experiência escolhida é inválida')
        return False
    if not empresa in empresas:
        messages.error(request, 'A empresa escolhida é inválida')
        return False
    if not statu in status:
        messages.error(request, 'O Status escolhido é inválido')
        return False
    if not padrao_email.match(email):
        messages.error(request, 'Digite um email válido')
        return False
    if not data_final >= data_atual:
        messages.error(request, 'A data escolhida já passou')
        return False
    return True

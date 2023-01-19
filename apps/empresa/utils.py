from django.contrib import messages
from .models import Empresa


def nova_empresa_is_valid(request, nome, email, cidade, endereco, nicho, tecnologias, caracteristicas, logo):
    if (len(nome.strip()) == 0) or (len(email.strip()) == 0) or (len(cidade.strip()) == 0) or (len(endereco.strip()) == 0) or (len(nicho.strip()) == 0) or (len(caracteristicas.strip()) == 0) or (not logo):
        messages.error(request, 'Preencha todos os campos')
        return False
    if logo.size > 100_000_000:
        messages.error(request, 'A logo deve ser menor que 10mb')
        return False

    if nicho not in [i[0] for i in Empresa.choices_nicho_mercado]:
        messages.error(request, 'Nicho de mercado inválido')
        return False

    return True
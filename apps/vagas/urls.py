from django.urls import path
from . import views

urlpatterns = [
    path('nova_vaga/', views.nova_vaga, name='nova_vaga'),
    path('vaga/<int:id>/', views.vaga, name='vaga'),
    path('nova_tarefa/<int:id_vaga>/', views.nova_tarefa, name='nova_tarefa'),
    path('realizar_tarefa/<int:id>/', views.realizar_tarefa, name='realizar_tarefa'),
    path('envia_email/<int:id_vaga>/', views.envia_email, name='envia_email'),
    path('adicionar_tecnologia_estudar/<int:id_tech>/<int:id_vaga>/', views.adicionar_tecnologia_estudar, name='adicionar_tecnologia_estudar'),
    path('adicionar_tecnologia_domina/<int:id_tech>/<int:id_vaga>', views.adicionar_tecnologia_domina, name='adicionar_tecnologia_domina'),
    path('atualizar_status/<int:id_vaga>/', views.atualizar_status, name='atualizar_status'),
]
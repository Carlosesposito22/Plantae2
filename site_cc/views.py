from site_cc.models import Event, EventMember
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from site_cc.utils import Calendar
from site_cc.forms import EventForm, AddMemberForm
import calendar
import requests
import google.generativeai as genai
from .forms import EventForm
from .models import Event, EventMember
from .forms import EventForm  

API_KEY = 'AIzaSyDF834PQjSJFlpv0KjtJXgmefEVmIWlNTY'
genai.configure(api_key=API_KEY)

pragas_doencas = {
    'Tomate': {
        'pragas': [
            {
                'nome': 'Traça-do-tomateiro',
                'caracteristicas': 'Larvas que perfuram os frutos e folhas, causando grandes prejuízos.',
                'descricao': 'As larvas se alimentam das folhas e frutos, criando buracos e deformidades.',
                'tratamento': (
                    '1. Aplicar inseticidas biológicos, como Bacillus thuringiensis, que são seguros para polinizadores. '
                    '2. Usar armadilhas de feromônio para capturar machos, reduzindo a população. '
                    '3. Incentivar a presença de predadores naturais, como pássaros e insetos benéficos.'
                ),
                'aplicavel_para': ['Tomate']
            },
            {
                'nome': 'Pulgão',
                'caracteristicas': 'Inseto que suga a seiva da planta, causando folhas enroladas.',
                'descricao': 'Insetos que se alimentam de seiva, causando danos que enfraquecem a planta.',
                'tratamento': (
                    '1. Introduzir controle biológico com joaninhas ou crisopídeos, que se alimentam de pulgões. '
                    '2. Aplicar sabão inseticida ou óleo de neem, que desidrata os insetos. '
                    '3. Aumentar a diversidade de plantas ao redor para atrair predadores naturais.'
                ),
                'aplicavel_para': ['Tomate', 'Alface']
            },
            {
                'nome': 'Broca-do-fruto',
                'caracteristicas': 'Larvas que perfuram os frutos e causam apodrecimento.',
                'descricao': 'Inseto cujas larvas penetram nos frutos, levando à deterioração.',
                'tratamento': (
                    '1. Monitorar a plantação frequentemente para detectar infestações precoces. '
                    '2. Remover e destruir frutos infetados para interromper o ciclo de vida do inseto. '
                    '3. Considerar o uso de inseticidas biológicos apenas se as infestações forem severas.'
                ),
                'aplicavel_para': ['Tomate']
            }
        ],
        'doencas': [
            {
                'nome': 'Requeima',
                'caracteristicas': 'Manchas escuras nas folhas e frutos.',
                'descricao': 'Doença fúngica que causa necrose e pode destruir plantações inteiras.',
                'tratamento': (
                    '1. Aplicação de fungicidas preventivos à base de cobre ou bicarbonato de sódio. '
                    '2. Práticas de rotação de culturas e remoção de restos de cultura para reduzir a incidência. '
                    '3. Melhorar a ventilação e a drenagem para diminuir a umidade, um fator-chave para a doença.'
                ),
                'aplicavel_para': ['Tomate']
            },
            {
                'nome': 'Murcha-bacteriana',
                'caracteristicas': 'Murcha súbita e amarelecimento das folhas.',
                'descricao': 'Infecção que bloqueia os vasos da planta, causando murcha irreversível.',
                'tratamento': (
                    '1. Escolha variedades resistentes à murcha-bacteriana. '
                    '2. Praticar um manejo adequado da irrigação, evitando encharcamento. '
                    '3. Incorporar compostos orgânicos ao solo para melhorar a saúde do solo e a resistência da planta.'
                ),
                'aplicavel_para': ['Tomate', 'Batata']
            },
            {
                'nome': 'Mancha-bacteriana',
                'caracteristicas': 'Manchas pequenas que se tornam marrons.',
                'descricao': 'Infecção bacteriana que afeta a qualidade das folhas e frutos.',
                'tratamento': (
                    '1. Remover e destruir as plantas infectadas imediatamente. '
                    '2. Aplicar bactericidas à base de extratos naturais, como o de alho. '
                    '3. Aumentar a rotação de culturas para evitar a persistência da bactéria no solo.'
                ),
                'aplicavel_para': ['Tomate']
            }
        ]
    },
    'Cenoura': {
        'pragas': [
            {
                'nome': 'Mosca-da-cenoura',
                'caracteristicas': 'Larvas que se alimentam das raízes, causando deformações.',
                'descricao': 'As larvas formam galerias nas raízes, levando à perda de qualidade.',
                'tratamento': (
                    '1. Cobrir o solo com redes finas para impedir que as moscas ponham ovos. '
                    '2. Praticar a rotação de culturas para quebrar o ciclo de vida da praga. '
                    '3. Introduzir plantas repelentes, como cebolinha ou alho, nas proximidades.'
                ),
                'aplicavel_para': ['Cenoura']
            },
            {
                'nome': 'Nematóides',
                'caracteristicas': 'Vermes que atacam as raízes, causando galhas.',
                'descricao': 'Microscópicos parasitas que comprometem o crescimento das raízes.',
                'tratamento': (
                    '1. Utilizar plantas antagonistas, como a mostarda, que ajudam a repelir nematóides. '
                    '2. Aplicar compostos orgânicos como farinha de neem, que têm propriedades nematicidas. '
                    '3. Praticar a rotação de culturas para reduzir a população de nematóides no solo.'
                ),
                'aplicavel_para': ['Cenoura', 'Rúcula']
            },
            {
                'nome': 'Pulgão-verde',
                'caracteristicas': 'Suga a seiva das folhas, causando enrolamento.',
                'descricao': 'Pequenos insetos que causam danos significativos às folhas.',
                'tratamento': (
                    '1. Pulverizar com uma solução de sabão ou detergente natural para desidratar os pulgões. '
                    '2. Utilizar controle biológico com insetos predadores, como joaninhas. '
                    '3. Plantar flores que atraem insetos benéficos, como flores da família Asteraceae.'
                ),
                'aplicavel_para': ['Cenoura']
            }
        ],
        'doencas': [
            {
                'nome': 'Queima-das-folhas',
                'caracteristicas': 'Lesões marrons nas folhas.',
                'descricao': 'Infecção fúngica que reduz a área foliar, afetando a fotossíntese.',
                'tratamento': (
                    '1. Aplicar fungicidas à base de cobre ou soluções caseiras com bicarbonato de sódio. '
                    '2. Remover e descartar folhas afetadas para limitar a propagação do fungo. '
                    '3. Aumentar a circulação de ar entre as plantas para evitar umidade excessiva.'
                ),
                'aplicavel_para': ['Cenoura']
            },
            {
                'nome': 'Podridão-mole',
                'caracteristicas': 'Apodrecimento aquoso e de odor desagradável nas raízes.',
                'descricao': 'Infecção bacteriana que ocorre em condições de alta umidade.',
                'tratamento': (
                    '1. Melhorar a drenagem do solo e evitar irrigação excessiva. '
                    '2. Aplicar compostos que contenham microrganismos benéficos, como biofertilizantes. '
                    '3. Remover qualquer material em decomposição próximo à cultura para reduzir a carga bacteriana.'
                ),
                'aplicavel_para': ['Cenoura']
            }
        ]
    },
    'Alface': {
        'pragas': [
            {
                'nome': 'Lagarta-das-folhas',
                'caracteristicas': 'Insetos que devoram as folhas, deixando buracos.',
                'descricao': 'Insetos que danificam as folhas e afetam a aparência e qualidade.',
                'tratamento': (
                    '1. Uso de inseticidas naturais, como extrato de neem, que são menos prejudiciais. '
                    '2. Remoção manual das lagartas e ovos visíveis nas folhas. '
                    '3. Introduzir predadores naturais, como pássaros e insetos benéficos, para controle.'
                ),
                'aplicavel_para': ['Alface']
            },
            {
                'nome': 'Pulgão',
                'caracteristicas': 'Inseto que suga a seiva da planta, transmitindo viroses.',
                'descricao': 'Causa folhas amareladas e enroladas, favorecendo fungos.',
                'tratamento': (
                    '1. Pulverização com óleo de neem, que também ajuda a controlar fungos. '
                    '2. Uso de controle biológico, como larvas de joaninhas. '
                    '3. Plantar espécies que atraem insetos benéficos nas proximidades.'
                ),
                'aplicavel_para': ['Tomate', 'Alface']
            },
            {
                'nome': 'Tripes',
                'caracteristicas': 'Insetos que causam manchas prateadas nas folhas.',
                'descricao': 'Pequenos insetos que deformam e danificam o tecido das folhas.',
                'tratamento': (
                    '1. Aplicar inseticidas naturais, como extratos de pimenta ou alho, que podem repelir trips. '
                    '2. Usar armadilhas adesivas amarelas para capturar os adultos. '
                    '3. Promover a biodiversidade no jardim, plantando flores que atraem inimigos naturais.'
                ),
                'aplicavel_para': ['Alface']
            }
        ],
        'doencas': [
            {
                'nome': 'Míldio',
                'caracteristicas': 'Manchas amareladas nas folhas com fungo branco na parte inferior.',
                'descricao': 'Doença que afeta a qualidade e produtividade da alface.',
                'tratamento': (
                    '1. Aplicar fungicidas específicos à base de cobre ou bicarbonato de sódio. '
                    '2. Melhorar a ventilação entre as plantas para reduzir a umidade. '
                    '3. Remover folhas infectadas e manter um solo bem drenado para prevenir a umidade excessiva.'
                ),
                'aplicavel_para': ['Alface']
            },
            {
                'nome': 'Podridão de esclerotínia',
                'caracteristicas': 'Podridão branca com micélio de fungo no caule.',
                'descricao': 'Afeta o caule e folhas, levando à morte da planta.',
                'tratamento': (
                    '1. Remover e destruir plantas infectadas imediatamente. '
                    '2. Aplicar fungicidas preventivos que contenham ingredientes naturais, como fungos benéficos. '
                    '3. Evitar irrigação por cima e melhorar a circulação de ar ao redor das plantas.'
                ),
                'aplicavel_para': ['Alface']
            }
        ]
    },
    'Batata': {
        'pragas': [
            {
                'nome': 'Besouro-da-batata',
                'caracteristicas': 'Inseto que se alimenta das folhas.',
                'descricao': 'Causa danos extensos ao se alimentar das folhas da planta.',
                'tratamento': (
                    '1. Uso de controle biológico com insetos predadores, como percevejos e joaninhas. '
                    '2. Aplicar inseticidas naturais, como extrato de neem, que são menos prejudiciais. '
                    '3. Rotação de culturas para interromper o ciclo de vida do besouro.'
                ),
                'aplicavel_para': ['Batata']
            },
            {
                'nome': 'Lagarta-rosada',
                'caracteristicas': 'Ataca os tubérculos, formando galerias.',
                'descricao': 'Diminui a qualidade e a capacidade de armazenamento dos tubérculos.',
                'tratamento': (
                    '1. Aplicação de inseticidas biológicos específicos. '
                    '2. Monitorar frequentemente a presença de lagartas e removê-las manualmente quando possível. '
                    '3. Melhorar a qualidade do solo e a saúde das plantas para aumentar a resistência.'
                ),
                'aplicavel_para': ['Batata']
            }
        ],
        'doencas': [
            {
                'nome': 'Murcha-bacteriana',
                'caracteristicas': 'Murcha súbita e escurecimento dos vasos.',
                'descricao': 'Afeta o sistema vascular da planta, impedindo a passagem de água.',
                'tratamento': (
                    '1. Usar variedades resistentes e adaptar o manejo da irrigação para evitar estresse hídrico. '
                    '2. Praticar a rotação de culturas para minimizar a presença da bactéria no solo. '
                    '3. Incorporar matéria orgânica ao solo para melhorar sua estrutura e saúde.'
                ),
                'aplicavel_para': ['Tomate', 'Batata']
            },
            {
                'nome': 'Requeima',
                'caracteristicas': 'Manchas escuras nas folhas e tubérculos.',
                'descricao': 'Progride rapidamente e causa necrose nas partes afetadas.',
                'tratamento': (
                    '1. Aplicação de fungicidas naturais e prevenção com plantas resistentes. '
                    '2. Remoção imediata de folhas e tubérculos afetados para limitar a propagação. '
                    '3. Melhorar a drenagem do solo e evitar excessos de umidade.'
                ),
                'aplicavel_para': ['Batata']
            },
            {
                'nome': 'Podridão-seca',
                'caracteristicas': 'Áreas murchas e descoloridas nos tubérculos.',
                'descricao': 'Causada por fungos, levando ao apodrecimento lento dos tubérculos.',
                'tratamento': (
                    '1. Manter o solo saudável com práticas de rotação e adubação orgânica. '
                    '2. Evitar o excesso de umidade e garantir a ventilação adequada ao redor dos tubérculos. '
                    '3. Remover tubérculos infectados para impedir a propagação da doença.'
                ),
                'aplicavel_para': ['Batata']
            }
        ]
    },
    'Rucula': {
        'pragas': [
            {
                'nome': 'Nematóides',
                'caracteristicas': 'Atacam as raízes, causando galhas.',
                'descricao': 'Reduzem a absorção de nutrientes, prejudicando o crescimento.',
                'tratamento': (
                    '1. Rotação de culturas para quebrar o ciclo dos nematóides. '
                    '2. Uso de plantas repelentes, como a calêndula, que ajudam a deter nematóides. '
                    '3. Aplicação de compostos orgânicos, como farinha de neem, que têm propriedades nematicidas.'
                ),
                'aplicavel_para': ['Cenoura', 'Rúcula']
            },
            {
                'nome': 'Pulgão',
                'caracteristicas': 'Suga a seiva e causa amarelecimento.',
                'descricao': 'Favorece o crescimento de fungos devido à substância pegajosa.',
                'tratamento': (
                    '1. Controle biológico com inimigos naturais, como joaninhas. '
                    '2. Uso de inseticidas suaves, como sabão inseticida. '
                    '3. Plantar flores que atraem insetos benéficos nas proximidades.'
                ),
                'aplicavel_para': ['Tomate', 'Alface', 'Rúcula']
            },
            {
                'nome': 'Lagarta-da-ruz',
                'caracteristicas': 'Danos às folhas por alimentação.',
                'descricao': 'Pode reduzir a qualidade da colheita.',
                'tratamento': (
                    '1. Uso de armadilhas e controle manual das lagartas. '
                    '2. Aplicação de inseticidas naturais, como extratos de pimenta ou alho. '
                    '3. Incentivar a presença de aves e insetos predadores no cultivo.'
                ),
                'aplicavel_para': ['Rúcula']
            }
        ],
        'doencas': [
            {
                'nome': 'Míldio',
                'caracteristicas': 'Manchas amareladas e pó branco nas folhas.',
                'descricao': 'Afeta a qualidade da planta e pode ser disseminada pelo vento.',
                'tratamento': (
                    '1. Aplicar fungicidas específicos, como bicarbonato de sódio ou cobre. '
                    '2. Melhorar a ventilação nas plantações para reduzir a umidade. '
                    '3. Remover e destruir folhas infectadas para limitar a propagação.'
                ),
                'aplicavel_para': ['Rúcula']
            },
            {
                'nome': 'Podridão-rota',
                'caracteristicas': 'Apodrecimento das folhas em alta umidade.',
                'descricao': 'Causa danos extensos em condições úmidas.',
                'tratamento': (
                    '1. Melhorar a drenagem do solo e evitar encharcamento. '
                    '2. Aplicar fungicidas preventivos à base de extratos naturais. '
                    '3. Remover folhas afetadas e manter o espaço entre as plantas para melhor circulação de ar.'
                ),
                'aplicavel_para': ['Rúcula']
            }
        ]
    }
}



plantas = {
    'Tomate': {
        'se_da_bem': ['Cenoura', 'Alface'],
        'nao_se_da_bem': ['Batata'],
        'indiferente': ['Rúcula'],
    },
    'Cenoura': {
        'se_da_bem': ['Alface', 'Rúcula'],
        'nao_se_da_bem': ['Batata'],
        'indiferente': ['Tomate'],
    },
    'Alface': {
        'se_da_bem': ['Cenoura', 'Rúcula'],
        'nao_se_da_bem': ['Batata'],
        'indiferente': ['Tomate'],
    },
    'Batata': {
        'se_da_bem': ['Rúcula'],
        'nao_se_da_bem': ['Tomate', 'Cenoura'],
        'indiferente': ['Alface'],
    },
    'Rúcula': {
        'se_da_bem': ['Cenoura', 'Alface'],
        'nao_se_da_bem': ['Batata'],
        'indiferente': ['Tomate'],
    },
}
## Dicionário para as culturas e os intervalos de dias para colheita
CULTURA_PRAZOS = {
    'Tomate': (105),
    'Cenoura': (85),
    'Alface': (38),
    'Batata': (105),
    'Rúcula': (35),
}



def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month

from django.http import JsonResponse

@login_required(login_url="signup")
def create_colheita_event(request, plantio_event_id):
    if request.method == "POST":
        plantio_event = get_object_or_404(Event, id=plantio_event_id)

        # Verifica se a cultura tem tempo de colheita definido
        tempo_colheita = CULTURA_PRAZOS.get(plantio_event.cultura, None)
        if tempo_colheita:
            # Calcula as datas de início e fim para o evento de colheita
            colheita_start_time = plantio_event.start_time + timedelta(days=tempo_colheita)
            colheita_end_time = plantio_event.end_time + timedelta(days=tempo_colheita)

            # Cria o evento de colheita
            colheita_event = Event.objects.create(
                user=plantio_event.user,
                title=f"{plantio_event.title} - Colheita",
                description=f"Colheita de {plantio_event.description}",
                start_time=colheita_start_time,
                end_time=colheita_end_time,
                cultura=plantio_event.cultura,
                local=plantio_event.local,
                type="Colheita",
            )

            return JsonResponse({
                "success": True,
                "message": "Evento de colheita criado com sucesso.",
                "colheita_event_id": colheita_event.id
            })

        return JsonResponse({"success": False, "message": "Tempo de colheita não definido para a cultura."}, status=400)

    return JsonResponse({"success": False, "message": "Método inválido"}, status=405)


@login_required(login_url="signup")
def create_or_edit_event(request):
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        if event_id and event_id.strip():  # Verifica se o event_id é válido e não vazio
            # Edita o evento existente
            try:
                event = Event.objects.get(pk=event_id, user=request.user)
                # Exclui o evento anterior
                event.delete()
                success_message = "Evento editado com sucesso."
            except Event.DoesNotExist:
                return JsonResponse({"success": False, "message": "Evento não encontrado para edição."}, status=404)
        else:
            success_message = "Evento criado com sucesso."

        # Cria um novo evento (ou substitui o anterior editado)
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user  # Define o usuário, independentemente de ser criação ou edição
            event.save()
            return JsonResponse({
                "success": True,
                "message": success_message,
                "event_id": event.id,
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat(),
                "type": event.type,
                "cultura": event.cultura,
                "local": event.local,
            })

        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse({"success": False, "message": "Método inválido"}, status=405)


from django.http import JsonResponse
from datetime import timedelta
from django.contrib.auth.decorators import login_required

# Defina CULTURA_PRAZOS na view para corresponder aos valores do JS
CULTURA_PRAZOS = {
    'Tomate': 105,
    'Cenoura': 85,
    'Alface': 38,
    'Batata': 105,
    'Rúcula': 35,
}

@login_required(login_url="signup")
def create_plantio_event(request):
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        if event_id and event_id.strip():  # Verifica se o event_id é válido e não vazio
            try:
                # Busca o evento existente para edição e o exclui
                event = Event.objects.get(pk=event_id, user=request.user)
                event.delete()
                success_message = "Evento de plantio editado com sucesso."
            except Event.DoesNotExist:
                return JsonResponse({"success": False, "message": "Evento de plantio não encontrado para edição."}, status=404)
        else:
            success_message = "Evento de plantio criado com sucesso."

        # Cria um novo evento com os dados do formulário
        form = EventForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]
            cultura = form.cleaned_data["cultura"]
            local = form.cleaned_data["local"]
            event_type = form.cleaned_data["type"]

            # Cria apenas o evento de plantio (ou substitui o anterior editado)
            first_event = Event.objects.create(
                user=request.user,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
                cultura=cultura,
                local=local,
                type=event_type,
            )

            return JsonResponse({
                "success": True,
                "message": success_message,
                "tempo_colheita": CULTURA_PRAZOS.get(cultura, None),
                "cultura": cultura,
                "open_recommendation_modal": True,
                "event_id": first_event.id,
                "title": title,
                "description": description,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "type": event_type,
                "local": local,
            })

        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse({"success": False, "message": "Método inválido"}, status=405)




@login_required(login_url="signup")
def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)

def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = get_object_or_404(Event, id=event_id)
            if member.count() < 10:  # Corrigido para 10 membros
                user = forms.cleaned_data["user"]
                EventMember.objects.create(event=event, user=user)
                return redirect("site_cc:calendar")
            else:
                print("--------------User limit exceeded!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)



def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user  # Se necessário, mantenha a atribuição do usuário
            form.save()
            return redirect("site_cc:calendar")

        context = {"form": forms}
        return render(request, self.template_name, context)


def delete_event(request, event_id):
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return JsonResponse({'success': True, 'message': 'Evento excluído com sucesso!'})
        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Evento não encontrado!'}, status=404)
    return JsonResponse({'success': False, 'message': 'Método não permitido!'}, status=405)

def next_week(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next_event = event
        next_event.id = None
        next_event.start_time += timedelta(days=7)
        next_event.end_time += timedelta(days=7)
        next_event.save()
        return JsonResponse({'message': 'Success!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_day(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next_event = event
        next_event.id = None
        next_event.start_time += timedelta(days=1)
        next_event.end_time += timedelta(days=1)
        next_event.save()
        return JsonResponse({'message': 'Success!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def tempo(request):
    API_KEY = "6d3d2107fd1048258f901644241611"
    cidade = "Carpina"
    
    link_forecast = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade}&days=7&lang=pt"
    
    try:
        requisicao_forecast = requests.get(link_forecast)
        requisicao_forecast.raise_for_status()
        requisicao_forecast_dic = requisicao_forecast.json()

        if "forecast" not in requisicao_forecast_dic or "current" not in requisicao_forecast_dic:
            contexto = {'erro': 'Não foi possível obter a previsão do tempo.'}
        else:
            previsao = []
            cidade_info = {
                'nome': requisicao_forecast_dic['location']['name'],
            }

            today = datetime.now().date().strftime("%Y-%m-%d")

            # Informações atuais do tempo
            temperatura_atual = requisicao_forecast_dic['current']['temp_c']
            descricao_atual = requisicao_forecast_dic['current']['condition']['text']
            umidade_atual = requisicao_forecast_dic['current']['humidity']
            vento_velocidade_atual = requisicao_forecast_dic['current']['wind_kph']
            precipitacao_atual = requisicao_forecast_dic['current']['precip_mm']
            indice_uv_atual = requisicao_forecast_dic['current']['uv']

            # Informações do dia atual
            dia_atual = requisicao_forecast_dic['forecast']['forecastday'][0]
            horas_sol = dia_atual['day'].get('sunshine', 'N/A')
            fases_da_lua = dia_atual['astro'].get('moon_phase', 'N/A')
            por_do_sol = dia_atual['astro'].get('sunset', 'N/A')
            nascer_do_sol = dia_atual['astro'].get('sunrise', 'N/A')
            temperatura_max_atual = dia_atual['day']['maxtemp_c']
            temperatura_min_atual = dia_atual['day']['mintemp_c']

            for item in requisicao_forecast_dic['forecast']['forecastday']:
                is_critical = (
                    item['day']['maxtemp_c'] > 35 or
                    item['day']['mintemp_c'] < 5 or
                    item['day']['maxwind_kph'] > 50 or
                    item['day']['totalprecip_mm'] > 50 
                )
                
                previsao.append({
                    'data': item['date'],
                    'descricao': item['day']['condition']['text'],
                    'temperatura_max': item['day']['maxtemp_c'],
                    'temperatura_min': item['day']['mintemp_c'],
                    'umidade': item['day']['avghumidity'],
                    'precipitacao': item['day']['totalprecip_mm'],
                    'vento_velocidade': item['day']['maxwind_kph'],
                    'is_critical': is_critical
                })

            contexto = {
                'cidade': cidade_info,
                'previsao': previsao,
                'today': today,
                'temperatura_atual': temperatura_atual,
                'descricao_atual': descricao_atual,
                'umidade_atual': umidade_atual,
                'vento_velocidade_atual': vento_velocidade_atual,
                'precipitacao_atual': precipitacao_atual,
                'indice_uv_atual': indice_uv_atual,
                'horas_sol': horas_sol,
                'fases_da_lua': fases_da_lua,
                'por_do_sol': por_do_sol,
                'nascer_do_sol': nascer_do_sol,
                'temperatura_max_atual': temperatura_max_atual,
                'temperatura_min_atual': temperatura_min_atual,
            }

    except requests.exceptions.RequestException as e:
        contexto = {
            'erro': f"Erro ao fazer a requisição: {e}"
        }
    
    return render(request, 'site_cc/tempo.html', contexto)



def praga(request):
    return render(request, 'site_cc/praga.html')

def detalhes_problema(request):
    # Captura o parâmetro 'plantio' da URL
    plantio_selecionado = request.GET.get('plantio', 'Nenhum plantio selecionado')  # Valor padrão caso não seja passado
    return render(request, 'site_cc/detalhes_problema.html', {
        'plantio_selecionado': plantio_selecionado,
    })

from .models import ProblemaReportado
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@login_required
def detectar_pragas_doencas(request):
    if request.method == 'POST':
        try:
            plantio_selecionado = request.POST.get('plantio')
            descricao_problema = request.POST.get('detalhes')

            # Salva o problema no banco de dados
            problema = ProblemaReportado.objects.create(
                plantio=plantio_selecionado,
                descricao=descricao_problema,
                usuario=request.user
            )

            # Simula lógica de detecção (ajuste conforme necessário)
            pragas_encontradas = []
            doencas_encontradas = []
            if plantio_selecionado in pragas_doencas:
                for praga in pragas_doencas[plantio_selecionado]['pragas']:
                    if any(palavra in descricao_problema.lower() for palavra in praga['caracteristicas'].lower().split()):
                        pragas_encontradas.append({
                            'nome': praga.get('nome', 'Nome não disponível'),
                            'descricao': f"{praga.get('descricao', 'Descrição não disponível')} Esta praga é caracterizada por {praga.get('caracteristicas', 'características desconhecidas')}.",
                            'tratamento': "\n".join(praga.get('tratamento', 'Tratamento não disponível').split(' . '))
                        })

                for doenca in pragas_doencas[plantio_selecionado]['doencas']:
                    if any(palavra in descricao_problema.lower() for palavra in doenca['caracteristicas'].lower().split()):
                        doencas_encontradas.append({
                            'nome': doenca.get('nome', 'Nome não disponível'),
                            'descricao': f"{doenca.get('descricao', 'Descrição não disponível')} Esta doença geralmente apresenta {doenca.get('caracteristicas', 'características desconhecidas')}.",
                            'tratamento': "\n".join(doenca.get('tratamento', 'Tratamento não disponível').split(' . '))
                        })

            return JsonResponse({
                'success': True,
                'problema': {
                    'id': problema.id,
                    'plantio': problema.plantio,
                    'descricao': problema.descricao,
                    'data_reporte': problema.data_reporte.strftime('%d/%m/%Y %H:%M'),
                    'resolvido': problema.resolvido
                },
                'pragas': pragas_encontradas,
                'doencas': doencas_encontradas
            })
        except Exception as e:
            print(f"Erro na view detectar_pragas_doencas: {e}")
            return JsonResponse({
                'success': False,
                'message': f'Erro no processamento: {str(e)}'
            }, status=500)

    return JsonResponse({'success': False, 'message': 'Método inválido.'}, status=405)




def recomendacao(request):
    resultado = None
    texto_gerado = None
    planta = request.GET.get('planta')

    print(f"Planta selecionada: {planta}")

    if planta:
        planta = planta.capitalize()
        if planta in plantas:
            resultado = plantas[planta]

            prompt_fixo = """
            Você só pode falar sobre agronomia, sustentabilidade, práticas agrícolas, tipos de solo e plantio. 
            Não quero que fuja para temas paralelos, como sugestões de vídeos ou coisas do tipo. Quero que tudo que for sugerir ou responder envolva apenas texto.
            Se a pergunta não tiver nada sobre agricultura ou algo relacionado, responda com: 
            'Não posso responder sobre esse tema, fui treinado apenas para práticas agrícolas.'
            """

            prompt_geracao = f"Escreva um texto de 8 linhas onde fala sobre {planta}, focando em informações sobre sua compatibilidade com estas plantas, explicando o motivo da compatibilidade {resultado['se_da_bem']} ou de não serem compatíveis. Se houver competição por nutrientes, informe quais são e sugira maneiras de melhorar o solo com materiais caseiros."

            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt_geracao)
                texto_gerado = response.text.strip()

                if 'Não posso responder' in texto_gerado:
                    texto_gerado = "Nenhuma informação válida gerada sobre a planta."
            except Exception as e:
                print(f"Erro ao gerar texto: {e}")
                texto_gerado = "Erro ao gerar texto de recomendação."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'planta': planta,
            'resultado': resultado,
            'texto_gerado': texto_gerado if texto_gerado else "Nenhum texto gerado pela IA.",
        })
    # Caso contrário, renderiza a página HTML
    contexto = {
        'plantas': plantas.keys(),
        'planta': planta,
        'resultado': resultado,
        'texto_gerado': texto_gerado if texto_gerado else "Nenhum texto gerado pela IA.",
    }

    return render(request, 'site_cc/recomendacao.html', contexto)

def all_events_list(request):
    events = Event.objects.get_all_events(user=request.user)
    return render(request, "site_cc/events_list.html", {'events': events})

def running_events_list(request):
    events = Event.objects.get_running_events(user=request.user)
    return render(request, "site_cc/events_list.html", {'events': events})

def calendar_view(request):
    login_url = "accounts:signin"
    if not request.user.is_authenticated:
        return redirect(login_url)

    d = get_date(request.GET.get("month", None))
    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(withyear=True)

    context = {
        "calendar": mark_safe(html_cal),
        "prev_month": prev_month(d),
        "next_month": next_month(d),
    }
    return render(request, "calendar.html", context)



def event_member_delete(request, event_member_id):
    event_member = get_object_or_404(EventMember, id=event_member_id)
    event_member.delete()
    return redirect(reverse_lazy("site_cc:calendar"))


@login_required(login_url="accounts:signin")
def calendar_view_new(request, event_id=None):
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        if event_id:
            event = get_object_or_404(Event, pk=event_id, user=request.user)
            form = EventForm(request.POST, instance=event)
        else:
            form = EventForm(request.POST)

        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.user = request.user
            new_event.save()
            return redirect("site_cc:calendar")
    else:
        form = EventForm()
        if event_id:
            event = get_object_or_404(Event, id=event_id, user=request.user)
            form = EventForm(instance=event)

    events = Event.objects.get_all_events(user=request.user)
    events_month = Event.objects.get_running_events(user=request.user)
    event_list = [
        {
            "id": event.id,
            "title": event.title,
            "type": event.type,
            "cultura": event.cultura,  # Certifique-se de que a cultura está incluída aqui
            "local": event.local,
            "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "description": event.description,
            "duration_readable": event.duration_readable,
        }
        for event in events
    ]

    API_KEY = "6d3d2107fd1048258f901644241611"
    cidade = "Carpina"
    link_forecast = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade}&days=30&lang=pt"
    
    previsoes = {}
    fases_lua = {}
    try:
        requisicao_forecast = requests.get(link_forecast)
        requisicao_forecast.raise_for_status()
        dados_previsao = requisicao_forecast.json().get('forecast', {}).get('forecastday', [])

        for dia in dados_previsao:
            data = dia['date']
            icone_url = dia['day']['condition']['icon']
            
            if icone_url.startswith("//"):
                icone_url = "https:" + icone_url
            
            previsoes[data] = {
                'descricao': dia['day']['condition']['text'],
                'icone': icone_url,
                'temperatura_max': dia['day']['maxtemp_c'],
                'temperatura_min': dia['day']['mintemp_c'],
                'umidade': dia['day']['avghumidity'],
                'vento': dia['day']['maxwind_kph'],
                'precipitacao': dia['day']['totalprecip_mm'],
                'indice_uv': dia['day'].get('uv', 'N/A')
            }

            fase_da_lua = dia['astro'].get('moon_phase', 'N/A')
            iluminacao = dia['astro'].get('moon_illumination', 'N/A')

            fluxo_seiva = ''
            if fase_da_lua in ['New Moon', 'Lua Nova', 'Lua nova']:
                fluxo_seiva = 'Seiva em baixo'
            elif fase_da_lua in ['Waxing Crescent', 'Crescente']:
                fluxo_seiva = 'Seiva subindo'
            elif fase_da_lua in ['First Quarter', 'Quarto Crescente']:
                fluxo_seiva = 'Seiva subindo'
            elif fase_da_lua in ['Waxing Gibbous', 'Crescente Gibosa']:
                fluxo_seiva = 'Seiva em cima'
            elif fase_da_lua in ['Full Moon', 'Lua Cheia', 'Lua cheia']:
                fluxo_seiva = 'Seiva em cima'
            elif fase_da_lua in ['Waning Gibbous', 'Minguante Gibosa']:
                fluxo_seiva = 'Seiva descendo'
            elif fase_da_lua in ['Last Quarter', 'Quarto Minguante']:
                fluxo_seiva = 'Seiva descendo'
            elif fase_da_lua in ['Waning Crescent', 'Minguante']:
                fluxo_seiva = 'Seiva em baixo'
            else:
                fluxo_seiva = 'Informação indisponível'

            fases_lua[data] = {
                'fase_da_lua': fase_da_lua,
                'iluminacao': iluminacao,
                'fluxo_seiva': fluxo_seiva
            }
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter previsão do tempo: {e}")

    context = {
        "form": form,
        "events": event_list,
        "events_month": events_month,
        "previsoes": previsoes,
        "fases_lua": fases_lua
    }
    return render(request, "site_cc/calendar.html", context)


from django.http import JsonResponse
import google.generativeai as genai

def alerta_colheita(request):
    texto_gerado = None
    cultura = request.GET.get('cultura')
    
    # Log para confirmar a cultura recebida
    print(f"Cultura recebida para o alerta de colheita: {cultura}")

    if cultura:
        cultura = cultura.capitalize()
        
        # Prompt para geração de texto
        prompt_geracao = (
            f"Escreva um texto de 8 linhas sobre a cultura {cultura}, "
            "focando em dicas de colheita, cuidados finais antes de colher e sinais de maturidade. "
            "Explique se há necessidade de melhorar o solo após a colheita e como fazer isso com compostos caseiros."
        )

        try:
            # Instancia o modelo e tenta gerar o conteúdo
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt_geracao)
            
            # Verifica se a resposta foi gerada
            if response and response.text:
                texto_gerado = response.text.strip()
                print(f"Texto gerado pela IA: {texto_gerado}")
            else:
                texto_gerado = "Nenhuma informação válida gerada pela IA para essa cultura."
                print("A IA não gerou uma resposta válida.")

        except Exception as e:
            print(f"Erro ao gerar texto: {e}")
            texto_gerado = "Erro ao gerar texto de alerta de colheita."

    else:
        texto_gerado = "Cultura não especificada."
        print("Cultura não foi passada no request.")

    # Retorna o JSON com status HTTP 200 explicitamente
    return JsonResponse({
        'cultura': cultura,
        'texto_gerado': texto_gerado,
    }, status=200)
@login_required(login_url="accounts:signin")
def mainpage_view(request):
    return render(request, "site_cc/mainpage.html")  # Renderiza o template mainpage.html

def homepage_view(request):
    return render(request, "site_cc/homepage.html")  # Substitua pelo caminho correto do template

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def listar_problemas(request):
    if request.method == 'GET':
        problemas = ProblemaReportado.objects.filter(usuario=request.user).order_by('-data_reporte')
        problemas_data = [{
            'id': problema.id,
            'plantio': problema.plantio,
            'descricao': problema.descricao,
            'data_reporte': problema.data_reporte.strftime('%d/%m/%Y %H:%M'),
            'resolvido': problema.resolvido
        } for problema in problemas]
        return JsonResponse({'success': True, 'problemas': problemas_data})
    
    if request.method == 'POST':
        problema_id = request.POST.get('id')
        resolvido = request.POST.get('resolvido') == 'true'
        try:
            problema = ProblemaReportado.objects.get(id=problema_id, usuario=request.user)
            problema.resolvido = resolvido
            problema.save()
            return JsonResponse({'success': True})
        except ProblemaReportado.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Problema não encontrado.'}, status=404)
    
    return JsonResponse({'success': False, 'message': 'Método inválido.'}, status=405)





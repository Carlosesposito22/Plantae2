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

API_KEY = 'AIzaSyC4AVfey0X8ONDz9f_vdw6Sq9yDdhHFowk'
genai.configure(api_key=API_KEY)

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

@login_required(login_url="signup")
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        cultura = form.cleaned_data["cultura"]  # Cultura selecionada no formulário
        local = form.cleaned_data["local"]

        # Obtenha o tempo médio de colheita para a cultura selecionada
        tempo_colheita = CULTURA_PRAZOS.get(cultura, None)

        # Cria o evento no banco de dados
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            cultura=cultura,
        )

        # Redireciona para o calendário com o tempo médio e cultura na URL
        if tempo_colheita:
            return HttpResponseRedirect(reverse("site_cc:calendar") + f"?tempo_colheita={tempo_colheita}&cultura={cultura}")
        else:
            return HttpResponseRedirect(reverse("site_cc:calendar"))
    return render(request, "event.html", {"form": form})






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
            return JsonResponse({'message': 'Evento excluído com sucesso!'})
        except Event.DoesNotExist:
            return JsonResponse({'message': 'Evento não encontrado!'}, status=404)
    return JsonResponse({'message': 'Método não permitido!'}, status=405)

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
    API_KEY = "741f449bc3d44b16b85205922242710"
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

            prompt_geracao = f"Escreva um texto de 8 linhas onde fala sobre {planta}, focando em informações sobre sua compatibilidade com estas plantas, explicando o motivo da compatibilidade {plantas} ou de não serem compatíveis, caso as plantas compitam por mesmos nutrientes informe quais são e de dicas de como melhorar o solo caso mesmo assim a pessoa queira plantar, essas dicas precisam ser com materiais fáceis de encontrar, de preferência encontrados em casa."

            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt_geracao)
                texto_gerado = response.text.strip()

                if 'Não posso responder' in texto_gerado:
                    texto_gerado = "Nenhuma informação válida gerada sobre a planta."
            except Exception as e:
                print(f"Erro ao gerar texto: {e}")

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

def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('site_cc:calendar')  
    else:
        form = EventForm(instance=event)
    
    return render(request, "event.html", {'form': form})

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
            "cultura": event.cultura,
            "local": event.local,
            "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "description": event.description,
            "duration_readable": event.duration_readable,
        }
        for event in events
    ]

    API_KEY = "741f449bc3d44b16b85205922242710"
    cidade = "Carpina"
    link_forecast = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade}&days=30&lang=pt"
    
    previsoes = {}
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
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter previsão do tempo: {e}")

    context = {
        "form": form,
        "events": event_list,
        "events_month": events_month,
        "previsoes": previsoes
    }
    return render(request, "site_cc/calendar.html", context)



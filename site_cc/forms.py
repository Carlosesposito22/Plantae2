from django import forms
from django.forms import ModelForm, DateInput, ChoiceField
from site_cc.models import Event, EventMember

class EventForm(ModelForm):
    TYPE_CHOICES = [
        ('Plantio', 'Plantio'),
        ('Colheita', 'Colheita'),
        ('Preparo', 'Preparo'),
        ('Outros', 'Outros'),
    ]
    CULTURA_CHOICES = [
        ('Tomate', 'Tomate'),
        ('Cenoura', 'Cenoura'),
        ('Rúcula', 'Rúcula'),
        ('Alface', 'Alface'),
        ('Batata', 'Batata'),
    ]

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    cultura = forms.ChoiceField(
        choices=CULTURA_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Event
        fields = ["title", "type", "description", "start_time", "end_time", "cultura","duration_readable"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome do evento"}
            ),
            "type": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Selecione o tipo"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descreva a atividade e coloque aqui todo material necessário",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("A data de término deve ser posterior à data de início.")

        return cleaned_data


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["user"]
        widgets = {
            "user": forms.Select(attrs={"class": "form-control"})
        }

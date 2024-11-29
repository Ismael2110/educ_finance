"""from django_filters.filters import *



class ProgrammeFilterSet(DefaultFilterSet):
    date__lte = DateFilter(
        field_name="date",
        lookup_expr="lte",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "placeholder": "Date minimale",
            }
        ),
        label="Date égale ou inferieure",
    )
    
    date__gte = DateFilter(
        field_name="date",
        lookup_expr="gte",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "placeholder": "Date minimale",
            }
        ),
        label="Date supérieure ou égale",
    )
    
    enseignant = ModelChoiceFilter(
        queryset=User.objects.filter(is_teacher=True),
        field_name="enseignant",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Choisissez un enseignant'
        }),
        label="Enseignant"
    )
    
    promotion = ModelChoiceFilter(
        queryset=Promotion.objects.all(),
        field_name="promotion",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Choisissez une promotion'
        }),
        label="Promotion"
    )
    cours = ModelChoiceFilter(
        queryset=Cours.objects.all(),
        field_name="cours",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Choisissez un cours'
        }),
        label="Cours"
    )
    
    class Meta :
        model = Programme
        fields= {'date':['lte','gte'],'cours':['exact'],'promotion':['exact'], 'enseignant':['exact']}"""
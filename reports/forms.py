from django import forms

from reports.models import KaryaKram, Lakxya, Pragati



class KaryakramForm(forms.ModelForm):
    class Meta:
        model = KaryaKram
        exclude = ('office',)


class LakxyaForm(forms.ModelForm):
    class Meta:
        model = Lakxya
        exclude = ('karyakram','fiscal_year', 'awadhi')


class PragatiForm(forms.ModelForm):
    class Meta:
        model = Pragati
        exclude = ('karyakram','fiscal_year', 'awadhi')

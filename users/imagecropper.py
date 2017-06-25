from PIL import Image
from django import forms
from django.core.files import File
from .models import Profile

class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = Profile
        fields = ('name', 'phoneno','photo', 'x', 'y', 'width', 'height',)

    def save(self):
        photo1 = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo1.photo)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400, 400), Image.ANTIALIAS)
        resized_image.save(photo1.photo.path)

        return photo1
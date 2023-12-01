from django import forms
from .models import TextMessage


class TextMessageForm(forms.ModelForm):

    class Meta:
        model = TextMessage
        fields = ["text_content"]




"""class TextMessageForm(forms.ModelForm):

    class Meta:
        model = TextMessage
        fields = '__all__'"""
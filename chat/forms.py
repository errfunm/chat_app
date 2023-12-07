from django import forms
from .models import TextMessage


class TextMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text_content"].widget.attrs.update({'class': 'w-full p-2 text-sm text-gray-700 border rounded-md'
                                                                  ' focus:outline-none focus:ring-1 focus:ring-blue-500'
                                                                  'focus:border-blue-500'
                                                                  ' rows="4"  placeholder="Type your message here..."'})

    class Meta:
        model = TextMessage
        fields = ["text_content"]

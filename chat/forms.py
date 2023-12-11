from django import forms


class MessageForm(forms.Form):
    img_msg = forms.ImageField(label="Image", required=False)
    txt_msg = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full p-2 text-sm text-gray-700 border rounded-md'
                                              ' focus:outline-none focus:ring-1 focus:ring-blue-500'
                                              'focus:border-blue-500',
                                              'rows': '2',  'placeholder': 'Type your message here...'}),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["img_msg"] and cleaned_data["txt_msg"]:
            raise forms.ValidationError("Please provide either a text message or an image message, but not both.")

        if not cleaned_data["img_msg"] and not cleaned_data["txt_msg"]:
            raise forms.ValidationError("Please provide either a text message or an image message, but not both.")

        return cleaned_data

from django.contrib.auth.forms import BaseUserCreationForm
from accounts.models import User


class RegisterUserForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = BaseUserCreationForm.Meta.fields

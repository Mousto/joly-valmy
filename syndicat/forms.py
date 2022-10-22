from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Utilisateur, Elu

class MonPersonnelCreationForm(UserCreationForm):

    class Meta:
        model = Utilisateur
        fields = "__all__"
class MonEluCreationForm(UserCreationForm):

    class Meta:
        model = Elu
        fields = "__all__"

class MonUserChangeForm(UserChangeForm):

    class Meta:
        model = Utilisateur
        fields = UserChangeForm.Meta.fields
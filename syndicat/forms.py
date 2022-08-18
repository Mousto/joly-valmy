from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Personnel, Elu

class MonPersonnelCreationForm(UserCreationForm):

    class Meta:
        model = Personnel
        fields = "__all__"
class MonEluCreationForm(UserCreationForm):

    class Meta:
        model = Elu
        fields = "__all__"

class MonUserChangeForm(UserChangeForm):

    class Meta:
        model = Personnel
        fields = UserChangeForm.Meta.fields
from django import forms
from .models import Device

class DeviceRegistrationForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'ip_address', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def clean(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError({"password":"Password must be at least 8 characters long."})
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError({"password":"Password must contain at least one digit."})

        if not any(char.isupper() for char in password):
            raise forms.ValidationError({"password":"Password must contain at least one uppercase letter."})

        if not any(char.islower() for char in password):
            raise forms.ValidationError({"password":"Password must contain at least one lowercase letter."})
        
        if not any(char in "!@#$%^&*()" for char in password):
            raise forms.ValidationError({"password":"Password must contain at least one special character (e.g., !@#$%^&*())."})
        
        return self.cleaned_data
class DeviceAvailabilityForm(forms.Form):
    device = forms.ModelChoiceField(queryset=Device.objects.all())
    password = forms.CharField(widget=forms.PasswordInput())

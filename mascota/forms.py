from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Mascota, SolicitudAdopcion, Perfil  # Añadido Perfil aquí


# En forms.py
class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'tipo', 'raza', 'edad', 'sexo', 'descripcion', 'ciudad', 'region', 'codigo_postal', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }


class SolicitudAdopcionForm(forms.ModelForm):
    class Meta:
        model = SolicitudAdopcion
        fields = ['motivo', 'direccion', 'telefono']
        widgets = {
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(max_length=15, required=False, 
                              widget=forms.TextInput(attrs={'class': 'form-control', 
                                                         'placeholder': 'Ej: +56912345678'}),
                              help_text="Incluye el código de país")
    whatsapp = forms.BooleanField(required=False, initial=True,
                                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                label="¿Usar este número para WhatsApp?")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name != 'whatsapp':  # No aplicar a checkboxes
                self.fields[field_name].widget.attrs['class'] = 'form-control'
                
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Guardar datos en el perfil
            try:
                user.perfil.telefono = self.cleaned_data.get('telefono', '')
                user.perfil.whatsapp = self.cleaned_data.get('whatsapp', True)
                user.perfil.save()
            except:
                # Si el perfil no existe, crearlo
                Perfil.objects.create(
                    usuario=user,
                    telefono=self.cleaned_data.get('telefono', ''),
                    whatsapp=self.cleaned_data.get('whatsapp', True)
                )
            
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class FormularioContacto(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu correo electrónico'})
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu mensaje aquí', 'rows': 5})
    )


class PerfilForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Perfil
        fields = ['telefono', 'whatsapp']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
            'whatsapp': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.usuario:
            self.fields['email'].initial = self.instance.usuario.email
            
    def save(self, commit=True):
        perfil = super().save(commit=False)
        if commit:
            # Actualizar el email del usuario
            perfil.usuario.email = self.cleaned_data['email']
            perfil.usuario.save()
            perfil.save()
        return perfil
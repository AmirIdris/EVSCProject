from django import forms
from django.contrib.gis import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.forms import fields

class CustomUserCreationForm(UserCreationForm):

    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm, self).__init__(*args,**kwargs)
        self.fields['is_staff']=forms.BooleanField(label=("Traffic Police"),required=False)
    class Meta:
        model=User
        fields=UserCreationForm.Meta.fields+('is_staff',)



class AddTrafficPoliceForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="password",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.EmailField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number=forms.CharField(label="Phone Number",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))

    location = forms.PointField(widget = forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))


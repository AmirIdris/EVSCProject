from django import forms
from django.contrib.gis import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.forms import fields
from EVSCapp.models import TrafficPoliceLocation

class CustomUserCreationForm(UserCreationForm):

    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm, self).__init__(*args,**kwargs)
        self.fields['is_staff']=forms.BooleanField(label=("Traffic Police"),required=False)
    class Meta:
        model=User
        fields=UserCreationForm.Meta.fields+('is_staff',)



class EditTrafficPoliceForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number=forms.CharField(label="Phone Number",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))


    try:
        traffic_police_locations = TrafficPoliceLocation.objects.all()

        traffic_police_location_list = []

        for traffic_police_location in traffic_police_locations:
            single_traffic_police_location = (traffic_police_location.id, traffic_police_location.location_name)
            traffic_police_location_list.append(single_traffic_police_location)

    except:
        traffic_police_location_list = []

    gender_list = (
        ('M','Male'),
        ('F','Female')
    )

    traffic_police_location_id = forms.ChoiceField(label="Assign Location", choices = traffic_police_location_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Assign Location", choices = gender_list, widget=forms.Select(attrs={"class":"form-control"}))

    







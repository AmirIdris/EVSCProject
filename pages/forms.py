from django import forms

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
    gender = forms.ChoiceField(label="Assign Location", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))

class EditVehicleForm(forms.Form):
    plate_number = forms.CharField(label='Plate Number', max_length=10, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Plate Number'}))

    plate_type = forms.CharField(label='Plate type', max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Plate Type'
    }))
    vehicle_owner = forms.CharField(label='Plate Owner', max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Vehicle Owner'
    }))

    def clean(self):
        cleaned_data = super(EditVehicleForm,self).clean()
        plate_number = cleaned_data.get('plate_number')
        plate_type = cleaned_data.get('plate_type')
        plate_owner = cleaned_data.get('plate_owner')

        if not plate_number and not plate_type and not plate_owner:
            raise forms.ValidationError('fill the forms')

        # traffic_police_location_list = []
        # all_traffic_police = TrafficPolice.objects.all()
        


        # # append all traffic police location to the list
        # for traffic_police in all_traffic_police:
        #     traffic_police_location_list.append({"location": traffic_police.location, "obj": traffic_police})

        # # cheack weather the traffic police location exists or not
        # if len(traffic_police_location_list) > 0:
        #     # calculate distance between record and all traffic police
        #     list_of_distance = []
            
        #     record_location = instance.location
        #     for traffic_police_pair in traffic_police_location_list:
        #         traffic_location = traffic_police_pair["location"]
        #         traffic_obj = traffic_police_pair["obj"]
        #         # create list of neare by traffic police

        #         distance = record_location.distance(traffic_location)*100

        #         list_of_distance.append((distance, traffic_obj))            

        #     # minimum distance 
        #     minimum_distance_pair = min(list_of_distance)
        #     nearby_traffic_police = minimum_distance_pair[1]
        #     print(minimum_distance_pair[0], nearby_traffic_police)

        #     # minimum_distance = index(min(list_of_distance))

        #     print(nearby_traffic_police.fcm_token)
            


        # path_to_fcm = "https://fcm.googleapis.com"
        # # server_key = 'AAAAPrW_CP8:APA91bEElY_DX6m7Kuwpo807REpKV67F9VgGCP_YLf2MZiAj4IBWqyowu_krDS42l50uq0b7vRTF-wtXjj7DBVk-orvVD_05szRH-24Uqh8k_eUdRNmu5mpcbBm6QzSgyHbotaGxt-eX'
        # # reg_id = TrafficPolice.objects.values_list('fcm_token',flat=True).get(user= 18)
        # # print(reg_id)
        # # message_title = 'Notification test'
        # # message_body = "Hi Aman, We made it bro!"
        # # result = FCMNotification(api_key=server_key).notify_single_device(registration_id=reg_id, message_title=message_title, message_body=message_body)

        # push_service = FCMNotification(api_key = 'AAAAbG5wAg0:APA91bH60qfGn4rg2B-2bSWicLWShygvmNrlrSX0LM9VzM9Srqcxvo3XIX9ODSrk92Zhuk4kPQ10V5DCRVVzDXN7koQSSP7S8aQhtRZQEULS10nL57k_Ote3AQzcolVRcuCnV8NgcGdw')
        # # registration_id = TrafficPolice.objects.values_list('fcm_token',flat=True).get(user= nearby_traffic_police.id)
        # registration_id = nearby_traffic_police.fcm_token
        # print(registration_id)
        # message_title = 'Notification test'
        # message_body = "Hi Aman, We made it bro!"
        # result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        
        # print(result)


    







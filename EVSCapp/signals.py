from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import TrafficPolice,SystemAdmin,Records
from django.dispatch import receiver



@receiver(post_save,sender=User)
def register_user(sender, instance, created, **kwargs):
    print("created: ",created)
    if created:
        if instance.is_staff !=True:
            TrafficPolice.objects.create(user=instance)

        else:
            SystemAdmin.objects.create(user=instance)


# sending Notification instantaneously as soon as new record is registered

@receiver(post_save,sender = Records)
def send_notification(sender,instance,created,**kwargs):
    print("created :", created)

    if created:

        


        traffic_police_location_list = []
        all_traffic_police = TrafficPolice.objects.all()
        


        # append all traffic police location to the list
        for traffic_police in all_traffic_police:
            traffic_police_location_list.append({"location": traffic_police.location, "obj": traffic_police})

        # cheack weather the traffic police location exists or not
        if len(traffic_police_location_list) > 0:
            # calculate distance between record and all traffic police
            list_of_distance = []
            
            record_location = instance.location
            for traffic_police_pair in traffic_police_location_list:
                traffic_location = traffic_police_pair["location"]
                traffic_obj = traffic_police_pair["obj"]
                # create list of neare by traffic police

                distance = record_location.distance(traffic_location)*100

                list_of_distance.append((distance, traffic_obj))            

            # minimum distance 
            minimum_distance_pair = min(list_of_distance)
            nearby_traffic_police = minimum_distance_pair[1]
            print(minimum_distance_pair[0], nearby_traffic_police)

            # minimum_distance = index(min(list_of_distance))

            print(nearby_traffic_police.fcm_token)
            


        path_to_fcm = "https://fcm.googleapis.com"
        # server_key = 'AAAAPrW_CP8:APA91bEElY_DX6m7Kuwpo807REpKV67F9VgGCP_YLf2MZiAj4IBWqyowu_krDS42l50uq0b7vRTF-wtXjj7DBVk-orvVD_05szRH-24Uqh8k_eUdRNmu5mpcbBm6QzSgyHbotaGxt-eX'
        # reg_id = TrafficPolice.objects.values_list('fcm_token',flat=True).get(user= 18)
        # print(reg_id)
        # message_title = 'Notification test'
        # message_body = "Hi Aman, We made it bro!"
        # result = FCMNotification(api_key=server_key).notify_single_device(registration_id=reg_id, message_title=message_title, message_body=message_body)

        push_service = FCMNotification(api_key = 'AAAAbG5wAg0:APA91bH60qfGn4rg2B-2bSWicLWShygvmNrlrSX0LM9VzM9Srqcxvo3XIX9ODSrk92Zhuk4kPQ10V5DCRVVzDXN7koQSSP7S8aQhtRZQEULS10nL57k_Ote3AQzcolVRcuCnV8NgcGdw')
        # registration_id = TrafficPolice.objects.values_list('fcm_token',flat=True).get(user= nearby_traffic_police.id)
        registration_id = nearby_traffic_police.fcm_token
        print(registration_id)
        message_title = 'Notification test'
        message_body = "Hi Aman, We made it bro!"
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        
        print(result)


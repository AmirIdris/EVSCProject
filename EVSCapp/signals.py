from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import TrafficPolice,SystemAdmin,Records,Notification,Report, TrafficPoliceLocation
from django.dispatch import receiver
from pyfcm import FCMNotification

import math



@receiver(post_save,sender=User)
def register_user(sender, instance, created, **kwargs):
    print("created: ",created)
    if created:
        if instance.is_staff !=True:
            TrafficPolice.objects.get_or_create(user=instance)

        else:
            SystemAdmin.objects.get_or_create(user=instance)


# sending Notification instantaneously as soon as new record is registered

@receiver(post_save,sender = Records)
def send_notification(sender,instance,created,**kwargs):
    print("created :", created)

    if created:

        traffic_police_location_list = []
        all_traffic_police = TrafficPolice.objects.all()
        all_traffic_police_count =TrafficPolice.objects.all().count()
        traffic_police_location_count = TrafficPoliceLocation.objects.all().count()
        


        # append all traffic police location to the list
        for traffic_police in all_traffic_police:
            if traffic_police.location == None:
                continue
            traffic_police_location_list.append({"latitude": traffic_police.location.latitude, "longitude": traffic_police.location.longitude,"obj": traffic_police})



        # cheack weather the traffic police location exists or not
        if len(traffic_police_location_list) > 0:
            # calculate distance between record and all traffic police
            list_of_distance = []
            
            record_latitude = instance.latitude
            record_longitude = instance.longitude
            radius = 6371
            for traffic_police_pair in traffic_police_location_list:
                traffic_latitude = traffic_police_pair["latitude"]
                traffic_longitude = traffic_police_pair["longitude"]
                traffic_obj = traffic_police_pair["obj"]
                # create list of neare by traffic police

                dlat = math.radians(traffic_latitude-record_latitude)
                dlong = math.radians(traffic_longitude-record_longitude)
                a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(record_latitude)) \
                * math.cos(math.radians(traffic_latitude)) * math.sin(dlong/2) * math.sin(dlong/2)
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                d = radius * c

                list_of_distance.append((d, traffic_obj))            

            # minimum distance 
            minimum_distance_pair = min(list_of_distance)    
            nearby_traffic_police = minimum_distance_pair[1]
            print(minimum_distance_pair[0], nearby_traffic_police)
            # minimum_distance = index(min(list_of_distance))

            print(nearby_traffic_police.fcm_token)
            


        notification = Notification.objects.create(recipient = nearby_traffic_police, records = instance, content = "message_body")
        notification.save()

        print(instance.vehicle.vehicle_plate)
        # create instance of FCMNotification Class by providing API Key
        push_service = FCMNotification(api_key = 'AAAAbG5wAg0:APA91bH60qfGn4rg2B-2bSWicLWShygvmNrlrSX0LM9VzM9Srqcxvo3XIX9ODSrk92Zhuk4kPQ10V5DCRVVzDXN7koQSSP7S8aQhtRZQEULS10nL57k_Ote3AQzcolVRcuCnV8NgcGdw')
        #retrieve registration Id of Traffic Police from The database
        registration_id = nearby_traffic_police.fcm_token
        print(registration_id)

        message_body = "Vehicle with Plate Number: {plate_number} is Moving with speed {speed} km/s" .format(plate_number=instance.vehicle,speed=instance.vehicle_speed)
        message_title = "New Notification!"
        # sending Notification to Single Devices
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body) 
        print(result)
        
        

from django.contrib import admin

# Register your models here.
from EVSCapp.models import *

admin.site.register(Vehicle)
admin.site.register(Records)
admin.site.register(Notification)
admin.site.register(TrafficPoliceLocation)
admin.site.register(TrafficPolice)
admin.site.register(Report)
admin.site.register(SystemAdmin)
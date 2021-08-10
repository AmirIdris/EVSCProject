from django.contrib import admin
from EVSCapp.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.gis import admin
# Register your models here.

class UserCreationFormExtended(UserCreationForm):
  def __init__(self,*args,**kwargs):
    super(UserCreationFormExtended, self).__init__(*args,**kwargs)
    self.fields['is_staff']=forms.BooleanField(label=_("System Admin"),required=False)



class UserAdmin(BaseUserAdmin):
    ordering=['username']
    list_display=['username','first_name','email']
    add_form=UserCreationFormExtended

    fieldsets=(
        (None,{'fields':('username','password')}),
        (_('Personal Info'),{'fields':('first_name','email')}),
        (
            _('Permissions'),
            ({'fields':('is_staff','is_active','is_superuser')})
        ),
        (_('Important dates'),{'fields':('last_login',)})
    )
    add_fieldsets=(
        (None, {
            'classes':('wide',),
            'fields':('username','password1','password2','is_staff')
        }),
    )






# Register your models here.

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Vehicle)
admin.site.register(Records)
admin.site.register(Notification)
admin.site.register(TrafficPoliceLocation)
admin.site.register(TrafficPolice)
admin.site.register(Report)
admin.site.register(SystemAdmin)
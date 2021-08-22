from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django import template
# from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template import loader
from .forms import CustomUserCreationForm, EditVehicleForm
from EVSCapp.models import Vehicle,Records,Report,TrafficPolice,SystemAdmin,TrafficPoliceLocation
from django.views.decorators.csrf import csrf_protect,requires_csrf_token

# from pages.forms import AddTrafficPoliceForm
from django.views.generic import ListView

from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.decorators import user_passes_test

import folium
# Create your views here.

# HomePage View 
# class HomePageView(generic.TemplateView):
#     template_name='pages/home.html'
@login_required(login_url="/login/")
def index(request):
    all_vehicle_count=Vehicle.objects.all().count()
    all_record_count=Records.objects.all().count()
    all_report_count=Report.objects.all().count()
    all_traffic_police_count=TrafficPolice.objects.all().count()
    all_system_admin_count=SystemAdmin.objects.all().count()



    context={
        "all_vehicle_count":all_vehicle_count,
        "all_record_count":all_record_count,
        "all_report_count":all_report_count,
        "all_traffic_police":all_traffic_police_count,
        "all_sytem_admin_count":all_system_admin_count
    }
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))



#SignUp Page View 

class SignUpPageView(generic.CreateView):
    form_class=CustomUserCreationForm
    success_url=reverse_lazy('login')
    template_name='accounts/register.html'
class SearchResultsView(ListView):
    model = TrafficPolice
    template_name = 'manage_traffic_template.html'
    

    def get_queryset(self):
        query = self.request.GET.get('search')
        return TrafficPolice.objects.filter(
            Q(user__username__icontains = query) | Q(user__email__icontains = query)
        )


def add_vehicle(request):
    return render(request, "add_vehicle_template.html")

def add_vehicle_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid method")

        return redirect("add_vehicle")

    else:
        vehicle_code = request.POST.get('code')
        vehicle_plate = request.POST.get('plate_number')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_owner = request.POST.get('vehicle_owner')
        

        plate_number = str(vehicle_code) + str(vehicle_plate)
        print(plate_number)

        try:
            vehicle=Vehicle.objects.create(vehicle_plate=plate_number,vehicle_type=vehicle_type, vehicle_owner = vehicle_owner)
            vehicle.save()
            messages.success(request, "Vehicle Added successfully")
            return redirect("add_vehicle")

        except:
            messages.error(request, "Vehicle is not Added")
            return redirect("add_vehicle")



def manage_vehicle(request):
    vehicles=Vehicle.objects.all()
    context={
            "vehicles":vehicles
            }

    return render(request, "manage_vehicle_template.html",context)


def edit_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    form = EditVehicleForm()

    context = {
        "vehicle": vehicle,
        "id": vehicle_id,
        "form": form
    }

    return render(request, "edit_vehicle_template.html",context)

def edit_vehicle_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        vehicle_id=request.POST.get('vehicle_id')
        vehicle_plate = request.POST.get('vehicle_plate')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_owner = request.POST.get('vehicle_owner')

        try:
            "Inserting into Vehicle model"
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle.vehicle_plate=vehicle_plate
            vehicle.vehicle_type=vehicle_type
            vehicle.vehicle_owner=vehicle_owner

            vehicle.save()
            messages.success(request, "Vehicle updated successfully")
            return redirect('/edit_vehicle/'+vehicle_id)

        except:
            messages.error(request, "Failed To update vehicle")
            return redirect("/edit_vehicle/"+vehicle_id)   

def delete_vehicle(request,vehicle_id):
    vehicle=Vehicle.objects.get(id=vehicle_id)

    try:
        vehicle.delete()
        messages.success(request, "Vehicle deleted successfuly")
        return redirect('manage_vehicle')
    except:
        messages.error(request, "unavle to delete vehicle")

        return redirect('manage_vehicle')
@requires_csrf_token
def add_user(request):
    # form = AddUserForm()
    # context = {
    #     "form":form
    # }
    return render(request, "user_registration_template.html")
@requires_csrf_token
@user_passes_test(lambda u: u.is_superuser)
def add_user_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid method")

    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        usernam = request.POST.get('username')
        is_traffic = request.POST.get('membershipRadios')

        
        password = User.objects.make_random_password()
        print(password)
        if is_traffic == "1":               
            user = User.objects.create(first_name = first_name, last_name = last_name, email = email, username =  usernam, is_staff = False)
            
            user.set_password(password)
            user.save()

            traffic = TrafficPolice.objects.get(user = user.id)
            traffic_id = traffic.id
            print(traffic_id)
            return redirect('detail_info', traffic_id = traffic_id)
            
        elif is_traffic == "2":
            user = User.objects.create(first_name = first_name, last_name = last_name, email = email, username = usernam, is_staff = True)
            user.set_password(password)
            user.save()

            return redirect('manage_system_admin')
                         
                    
                

            # if user.is_staff == True:
            #     return redirect('admin')

        # except:
        #     messages.error(request, "Failed to add user")
        return render(request, 'user_registration_template.html')


        # form = AddUserForm(request.POST)
        # if form.is_valid():
        #     email = form.cleaned_data['email']
        #     password = form.cleaned_data['password']
        #     username = form.cleaned_data['username']
        #     password = form.cleaned_data['password']
        #     first_name = form.cleaned_data['first_name']
        #     last_name = form.cleaned_data['last_name']

        #     try:
        #         user = User.objects.create(email=email,password=password,username=username,first_name=first_name,last_name=last_name)
        #         user.save()
        #         messages.success(request, "student added successfully!")
        #         return redirect("to")

        #     except:
        #         messages.error(request, "Failed to add student")
        #         return redirect("to")

        # else:
        #     return redirect("to")


        # return redirect("to")
def detail_info_view(request,traffic_id):
    traffic = TrafficPolice.objects.get(id = traffic_id)
    locations = TrafficPoliceLocation.objects.all()

    location_found = []
    location_not_found = []

    for location in locations:
        if TrafficPolice.objects.filter(location = location.id).exists():
            location_found.append(location)
        else:
            print(location)
            location_not_found.append(location)




 
    context = {
        'traffic' : traffic,
        'id' : traffic_id,
        'traffic_police_locations': location_not_found

    }

    return render(request,"traffic_info_template.html", context)

def detail_info_view_save(request):

    if request.method != 'POST':
        messages.error(request,'Invalide method is used')
        return redirect("detail_info")
        

    else:
        id = request.POST.get('traffic_police_id')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        traffic_police_location = request.POST.get('traffic_police_location')

        try:
            traffic = TrafficPolice.objects.get(pk = id)
            print(traffic)

            traffic.phone_number = phone_number
            print(traffic.phone_number)
            traffic.gender = gender
            print(traffic_police_location)
            traffic_police_sites = TrafficPoliceLocation.objects.get(pk = traffic_police_location)

            print(traffic_police_sites)
            traffic.location = traffic_police_sites
            print(traffic.location)
            traffic.save(update_fields=['phone_number','gender','location'])
            messages.success(request, "Information is sent to the database successfully")
            # return redirect("edit_traffic_police", traffic_police_id = id )
            return redirect("manage_traffic_police")
        except:
            messages.error(request,"Failed to store detail Information")
            return redirect("detail_info", traffic_id = id )

            





def manage_traffic_police(request):
    traffic = TrafficPolice.objects.all()

    page = request.GET.get('page',1)
    paginator = Paginator(traffic, 10)
    try:
        traffic = paginator.page(page)
    except PageNotAnInteger:
        traffic = paginator.page(1)
    except EmptyPage:
        traffic = paginator.page(paginator.num_pages)


    context = {
        "traffic_polices" : traffic
    }

    return render(request, "manage_traffic_template.html",context)

def add_traffic_police(request):
    form = AddTrafficPoliceForm()

    context = {
        'form' : form
    }

    return render(request, "add_traffic_police.html", context)

def add_traffic_police_save(request):
    if request.method !='POST':
        messages.error(request, "Invalid Method")
        return redirect('add_traffic_police')

    else:
        form = AddTrafficPoliceForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']

            location = form.cleaned_data['location']


            try:
                user = User.objects.create(email = email, first_name = first_name, last_name = last_name, username = userrname, password = password)

                user.save()

            except:
                messages.error(request, "Failed to save")

def edit_traffic_police(request,traffic_police_id):
    traffic = TrafficPolice.objects.get(id = traffic_police_id)

    traffic_police_location = TrafficPoliceLocation.objects.all()

    location_found = []
    location_not_found = []

    for traffic in traffic_police_location:

        if TrafficPolice.objects.filter(location = traffic.pk, id = traffic_police_id).exists():
            location_found.append(traffic)
        else:
            location_not_found.append(traffic)
   

    context ={
        'traffic':traffic,
        'id':traffic_police_id,
        'traffic_police_locations': location_found
    }

    return render(request, "edit_traffic_police_template.html", context)




def edit_traffic_police_save(request):
    if request.method != 'POST':
        messages.error(request, "Invalid Method")
        return redirect("manage_traffic_police")
        
    else:
        id = request.POST.get('traffic_police_id')
        
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        status = request.POST.get('membershipRadios')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        traffic_police_location = request.POST.get('traffic_police_location')

        try:
            user = User.objects.get(traffic = id)
            print(user)
            user.username = username
            user.first_name = first_name
            print(user.first_name)
            user.last_name = last_name
            user.email = email
            if status == "1":
                user.is_active = True
            else:
                user.is_active = False


            user.save()
            print(id)
            traffic = TrafficPolice.objects.get(pk = id)
            print(traffic)

            traffic.phone_number = phone_number
            print(traffic.phone_number)
            traffic.gender = gender
            traffic_police_sites = TrafficPoliceLocation.objects.get(id = traffic_police_location)

            print(traffic_police_sites)
            traffic.location = traffic_police_sites
            # print(traffic.location)
            traffic.save(update_fields=['phone_number','gender','location'])
            messages.success(request, "Profile Updated successfully")
            # return redirect("edit_traffic_police", traffic_police_id = id )
            return redirect("manage_traffic_police")

        except:
            messages.error(request, "Failed to update Profile")
            return redirect("edit_traffic_police", traffic_police_id = id )






def delete_traffic_police(request, traffic_police_id):
    traffic = TrafficPolice.objects.get(id = traffic_police_id)

    try:
        traffic.delete()
        messages.success(request, "successfully deleted")
        return redirect('manage_traffic_police')

    except:
        messages.error(request, "unable to delete traffic police")
        return redirect('manage_traffic_police')

    



def manage_system_admin(request):
    admins = SystemAdmin.objects.all()
    context = {
        "admins" : admins
    }

    return render(request, "admin_view_template.html",context)


def admin_profile(request):
    user = User.objects.get(id = request.user.id)
    context = {
        "user" : user
    }

    return render(request,"admin_profile_template.html", context)

def admin_profile_update(request):
    if request.method != 'POST':
        messages.error(request, "Invalid Method")
        return redirect("admin_profile")

    else:
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        password = request.POST.get('password')

        try:
            user = User.objects.get(id = request.user.id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            if password != None and password != '':
                user.set_password(password)
            user.save()

            system_admin = SystemAdmin.objects.get(user = request.user)
            system_admin.phone_number = phone_number
            system_admin.gender = gender
            system_admin.save()

            messages.success(request, "Profile Updated successfully")
            return redirect("admin_profile")

        except:
            messages.error(request, "Failed to update Profile")
            return redirect("admin_profile")




def records_view(request):
    records=Records.objects.all()
    context = {
        'records':records
    }
    return render(request, "view_records_template.html", context)


# search all traffic police
def search_all_traffic_police(request):
    if request.method == 'GET':
        username = request.GET.get('search')
        traffic = TrafficPolice.objects.filter(Q(user__username__iexact = username)|Q(user__email__iexact = username))
        if traffic.exists():
            context = {
                'traffic_polices' : traffic 
            }
            return render(request, "manage_traffic_template.html",context)

        else:
            return render(request, "manage_traffic_template.html",context = {})

        
#search records by vehicle plate 

def search_all_vehicle_records(request):
    if request.method == 'GET':
        plate = request.GET.get('search')
        records = Records.objects.filter(Q(vehicle__vehicle_plate__iexact = plate))
        if records.exists():
            context = {
                'records' : records 
            }
            return render(request, "view_records_template.html",context)

        else:
            return render(request, "view_records_template.html",context = {})


# search all available vehicle in the system
def search_all_vehicle(request):
    if request.method == 'GET':
        plate = request.GET.get('search')
        vehicle = Vehicle.objects.filter(Q(vehicle_plate__iexact = plate))
        if vehicle.exists():
            context = {
                'vehicles' : vehicle 
            }
            return render(request, "manage_vehicle_template.html",context)

        else:
            return render(request, "manage_vehicle_template.html",context = {})


def view_record_location_on_map(request, location_id):

    record = Records.objects.get(id = location_id)
    traffic_police_location = TrafficPoliceLocation.objects.all()
    record_latitude = record.latitude
    record_longitude = record.longitude

    map = folium.Map(location = [float(record_latitude), float(record_longitude)],zoom_start = 9)



    for traffic_police_location in traffic_police_location:
        latitude = traffic_police_location.latitude
        longitude = traffic_police_location.longitude
        # traffic = TrafficPolice.objects.get(location = traffic_police_location.id)
        # print(traffic)
        folium.Marker(location = [float(latitude),float(longitude)],
        tooltip = 'click for more',
        popup='Located in :' + traffic_police_location.location_name,
        icon = folium.Icon(color = 'blue', icon = 'info-sign')
        ).add_to(map)
    if record.status == False:
        record_status = "Not yet Reported"

    else:
        record_status = "Record is reported"
    folium.Marker(location = [float(record_latitude),float(record_longitude)],
    tooltip = 'click for more',
    popup='Vehicle Plate is:'+ str(record.vehicle.vehicle_plate + "\n" + 'Vehicle speed is :' + str(record.vehicle_speed) + "\n" + "Report status: " + record_status),
    icon = folium.Icon(color = 'red', icon = 'info-sign')
    ).add_to(map)

    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(map)


    folium.LayerControl().add_to(map)

    map = map._repr_html_()

    context = {
        'map':map
    }

    return render(request, "view_record_on_map_template.html",context)

#Location related Views
def manage_location(request):
    location = TrafficPoliceLocation.objects.all()
    context = {
        "locations" : location
    }

    return render(request, "location_view_template.html",context)






def add_location_view(request):
    return render(request, "add_location_template.html")

def add_location_save_view(request):
    if request.method != "POST":
        messages.error(request, "Invalid method")

        return redirect("add_vehicle")

    else:
        location_name = request.POST.get('location_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        

        try:
            location=TrafficPoliceLocation.objects.create(location_name=location_name,latitude=latitude, longitude = longitude)
            location.save()
            messages.success(request, "Location Added successfully")
            return redirect("add_location")

        except:
            messages.error(request, "Location is not Added")
            return redirect("add_location")

def view_location_on_map(request, location_id):

    location = TrafficPoliceLocation.objects.get(id = location_id)
    latitude = location.latitude
    longitude = location.longitude

    map = folium.Map(location = [float(latitude), float(longitude)],zoom_start = 13)
    folium.Marker(location = [float(latitude),float(longitude)],
    tooltip = 'click for more',
    popup='Vehicle Plate is:'+ location.location_name,
    icon = folium.Icon(color = 'red', icon = 'info-sign')
    ).add_to(map)

    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
    folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(map)


    folium.LayerControl().add_to(map)

    map = map._repr_html_()

    context = {
        'map':map
    }

    return render(request, "view_location_on_map_template.html",context)


def data_visualizatio(request):
    return render(request,"chartjs.html")


def assign_traffic_location(request):
    traffics = TrafficPolice.objects.all()
    locations = TrafficPoliceLocation.objects.all()

    none_assigned_traffic = []
    assigned_traffic = []
    free_locations = []
    occupied_location = []
    # print(TrafficPolice.objects.filter(location__isnull=True).values())

    for location in locations:
        if TrafficPolice.objects.filter(location = location.id).exists():
            
            occupied_location.append(location)
        else:
            print(location)
            free_locations.append(location)
    for traffic in traffics: 
        if TrafficPolice.objects.filter(location_id__isnull=True,id =traffic.id):
            print(traffic)
            none_assigned_traffic.append(traffic)
        else:
            assigned_traffic.append(traffic)



    # for traffic in traffics:
    #     if TrafficPolice.objects.filter(location = ).exists():
    #         none_assigned_traffic.append(traffic)
    #     else:
    #         assigned_traffic.append(traffic)

    context = {
        "none_assigned_traffics": none_assigned_traffic,
        "free_locations": free_locations
    }

    
    return render(request,"assign_location_to_traffic_template.html",context)


def assign_traffic_location_save(request):
    if request.method != "POST":
        messages.error(request,"Invalid method has been used")
        return redirect('assign_location_to_traffic')

    else:
        traffic = request.POST.get('traffic')
        location = request.POST.get('location')
        print(traffic)
        print(location)
        

        
        traffic = TrafficPolice.objects.get(pk = traffic)
        print(traffic)
        traffic_locations = TrafficPoliceLocation.objects.get(pk = location)


        print(traffic.id)
        print(traffic)

        traffic.location = traffic_locations
        print(traffic.location)
        traffic.save()
        messages.success(request,"profile is updated successfully")
        return redirect('assign_location_to_traffic')


            






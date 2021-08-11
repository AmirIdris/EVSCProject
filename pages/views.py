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
from .forms import CustomUserCreationForm
from EVSCapp.models import Vehicle,Records,Report,TrafficPolice,SystemAdmin,TrafficPoliceLocation
from django.views.decorators.csrf import csrf_protect,requires_csrf_token

# from pages.forms import AddTrafficPoliceForm
from django.views.generic import ListView

from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.decorators import user_passes_test
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
        vehicle_plate = request.POST.get('vehicle_plate')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_owner = request.POST.get('vehicle_owner')
        try:
            vehicle=Vehicle.objects.create(vehicle_plate=vehicle_plate,vehicle_type=vehicle_type, vehicle_owner = vehicle_owner)
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
    vehicle=Vehicle.objects.get(id=vehicle_id)

    context={
        "vehicle":vehicle,
        "id":vehicle_id
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

            return redirect('manage_system_admins')
                         
                    
                

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
    context = {
        'traffic' : traffic
    }

    return render(request,"traffic_info_template.html", context)




def manage_traffic_police(request):
    traffic_police = TrafficPolice.objects.all()

    page = request.GET.get('page',1)
    paginator = Paginator(traffic_police, 10)
    try:
        traffic_police = paginator.page(page)
    except PageNotAnInteger:
        traffic_police = paginator.page(1)
    except EmptyPage:
        traffic_police = paginator.page(paginator.num_pages)


    context = {
        "traffic_polices" : traffic_police
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
    traffic_police = TrafficPolice.objects.get(id = traffic_police_id)

    traffic_police_location = TrafficPoliceLocation.objects.all()

    location_found = []
    location_not_found = []

    for traffic in traffic_police_location:

        if TrafficPolice.objects.filter(location = traffic.pk).exists():
            location_found.append(traffic)
        else:
            location_not_found.append(traffic)
    

    context ={
        'traffic_police':traffic_police,
        'id':traffic_police_id,
        'traffic_police_locations': location_not_found
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
            user = User.objects.get(traffic_police = id)
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
            traffic_police = TrafficPolice.objects.get(pk = id)
            print(traffic_police)

            traffic_police.phone_number = phone_number
            print(traffic_police.phone_number)
            traffic_police.gender = gender
            traffic_police_sites = TrafficPoliceLocation.objects.get(id = traffic_police_location)

            print(traffic_police_sites)
            traffic_police.location = traffic_police_sites
            # print(traffic_police.location)
            traffic_police.save(update_fields=['phone_number','gender','location'])
            messages.success(request, "Profile Updated successfully")
            # return redirect("edit_traffic_police", traffic_police_id = id )
            return redirect("manage_traffic_police")

        except:
            messages.error(request, "Failed to update Profile")
            return redirect("edit_traffic_police", traffic_police_id = id )






def delete_traffic_police(request, traffic_police_id):
    traffic_police = TrafficPolice.objects.get(id = traffic_police_id)

    try:
        traffic_police.delete()
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

    return render(request,"page-user.html", context)

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

        try:
            user = User.objects.get(id = request.user.id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            system_admin = SystemAdmin.objects.get(user = request.user)
            system_admin.phone_number = phone_number
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






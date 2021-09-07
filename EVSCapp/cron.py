from EVSCapp.models import Vehicle
def my_scheduled_job():
  Vehicle.objects.all().update(status=False)
import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


CITY_KEY={
    "delhi":202396,
    "bengaluru":204108,
    "bangalore":204108,
    "mumbai":204842,
    "chennai":206671,
    "kolkata":206690,
    "hyderabad":202190
}

def login(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if username=="admin" and password=="admin":
            return redirect('/index')
        else:
            context={
                "err_msg":"Incorrect Credentials, Please try again!"
            }
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')



def index(request):
    err_msg = ''
    message = ''
    message_class = ''
    api_key = '0MpHch88YVjLezfAhcz5P69AraFfTDDP'
    
    

    if request.method == 'POST':
        form = CityForm(request.POST)
        request.POST._mutable = True
        city_name=request.POST['name']
        

        if city_name in CITY_KEY:
            request.POST['location_key']=CITY_KEY[city_name]
            if form.is_valid():
                
                existing_city_count = City.objects.filter(name=city_name).count()
                location_key=request.POST['location_key']
                if existing_city_count == 0:
                    
                    forcast_data = requests.get(f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}').json()
                    if 'Message' not in forcast_data:
                        if forcast_data[0]['Temperature']:
                            form.save()
                        else:
                            err_msg = 'City does not exist!'
                    else:
                        err_msg=forcast_data['Message']
                else:
                    err_msg = 'City already exists in the database!'
        else:
            err_msg = 'City does not exist!, Check for spelling mistakes if any'

        if err_msg:
            message = err_msg
            message_class= 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()
    cities = City.objects.all()
    cities_data = []

    for city in cities:
        forcast_data = forcast_data = requests.get(f'http://dataservice.accuweather.com/currentconditions/v1/{city.location_key}?apikey={api_key}').json()
        if 'Message' not in forcast_data:

            temperature_in_celsius=forcast_data[0]['Temperature']['Metric']['Value']
            weather_data = {
                'city': city.name,
                'temperature': temperature_in_celsius,
                'description': forcast_data[0]['WeatherText'],
                'icon': forcast_data[0]['WeatherIcon']
            }
            cities_data.append(weather_data)
        else:
            message = forcast_data['Message']
            message_class= 'is-danger'

    context = {
        'cities_data': cities_data, 
        'form': form,
        'message': message,
        'message_class': message_class
        }

    return render(request, 'index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')
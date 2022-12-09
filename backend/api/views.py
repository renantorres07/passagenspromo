from django.http import HttpResponse, JsonResponse
from .models import Airport
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

#Api to get all airports
@csrf_exempt
def get_all_airports(request):
	if (request.method == "GET"):
		all_airports= Airport.objects.all()
		serialized_all_airports = serializers.serialize("json",all_airports)
		return HttpResponse('{"data":'+serialized_all_airports+'}', content_type='application/json')

#Api to toogle the active status of an airport in the database
@csrf_exempt
def toogle_active(request, iata):
	
	if (request.method == "PATCH"):
				
		try:
			airport = Airport.objects.get(iata_code=iata)

			airport.status = 'A'
			airport.reason = ''	
					
			airport.save()
			serialized_airport = serializers.serialize("json",[airport,])
			return JsonResponse(json.loads(serialized_airport), safe=False)
		except Exception as err:
			return HttpResponse(err)

			
#Api to toogle the active status of an airport in the database
@csrf_exempt
def toogle_inactive(request, iata):
	
	if (request.method == "PATCH"):
		reason = request.GET.get('reason')
		if reason == None:	
			return HttpResponse('No reason given')
		try:
			airport = Airport.objects.get(iata_code=iata)			
			
			airport.status = 'I'
			airport.reason = reason			
			
			airport.save()
			serialized_airport = serializers.serialize("json",[airport,])
			return JsonResponse(json.loads(serialized_airport), safe=False)
		except Exception as err:
			return HttpResponse(err)

import requests
from math import radians, cos, sin, asin, sqrt,floor
import datetime

DATE_FORMAT_STR = "%Y-%m-%dT%H:%M:%S"

#Formula to calculate the distance between two latitude,longitude points.
def haversine(lon1, lat1, lon2, lat2):
    # decimal to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # calculations
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in km.
    return floor(c * r)

#Api to consult the MockAirlines api and return the combinations of flights.		
@csrf_exempt
def mock_airlines_api(request,departure_airport,arrival_airport,departure_date,return_date):
	if (request.method == "GET"):
		try:
			token = request.headers['token']
		except:
			token = None


		if (token == None or token != '3y4WXfiBN8pRaXvaVe8jzyNCCXnnSu9gmaUFvJMaJxXvesUtwEuaP98A8PZSzwCW9TiQhFUtByMaXHVt8yYU7inzhTfmfYRTR3umyiBeHu9ktDJGcyhyTJzhsSfgmJSR'):
			return HttpResponse('User not authenticated.')

		if departure_airport == arrival_airport:
			return HttpResponse("Departure airport and arrival airport can't be equal")

		if datetime.datetime.strptime(departure_date,"%Y-%m-%d") < datetime.datetime.now():
			return HttpResponse("Departure can't be before now")

		if return_date < departure_date:
			return HttpResponse('Return date must be after the departure date')

		API_KEY = 'pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc'
		outgoing_flight_request = requests.get(f"http://stub.2xt.com.br/air/search/{API_KEY}/{departure_airport}/{arrival_airport}/{departure_date}",auth=("demo","swnvlD"))
		return_flight_request = requests.get(f"http://stub.2xt.com.br/air/search/{API_KEY}/{arrival_airport}/{departure_airport}/{return_date}",auth=("demo","swnvlD"))
		
		try:
			outbound_flight_summary = outgoing_flight_request.json()['summary']
			outbound_flight_options = outgoing_flight_request.json()['options']
			return_flight_summary = return_flight_request.json()['summary']
			return_flight_options = return_flight_request.json()['options']
		except:
			return HttpResponse("An error occured while fetching data, please check your parameters.")		
		

		if not (Airport.objects.filter(iata_code=outbound_flight_summary['from']['iata']).exists()):
			return HttpResponse("Our company does not work with this departure airport.")

		if not (Airport.objects.filter(iata_code=outbound_flight_summary['to']['iata']).exists()):
			return HttpResponse("Our company does not work with this arrival airport.")

		response = {
			"summary" : {
				"departure_airport" : {
					"iata":outbound_flight_summary['from']['iata'],
					"city":outbound_flight_summary['from']['city'],
					"lat":outbound_flight_summary['from']['lat'],
					"lon":outbound_flight_summary['from']['lon'],
					"state":outbound_flight_summary['from']['state'],
				},
				"arrival_airport" : {
					"iata":outbound_flight_summary['to']['iata'],
					"city":outbound_flight_summary['to']['city'],
					"lat":outbound_flight_summary['to']['lat'],
					"lon":outbound_flight_summary['to']['lon'],
					"state":outbound_flight_summary['to']['state'],
				},
				"departure_date" : outbound_flight_summary['departure_date'],			
				"return_date" : return_flight_summary['departure_date']
			}
		}

		options = []
		for outbound_flight in outbound_flight_options:
			for return_flight in return_flight_options:
				outbound_flight['price']['fees'] = round(max(outbound_flight['price']['fare']*0.1,40),2)
				outbound_flight['price']['total'] = round(outbound_flight['price']['fees'] + outbound_flight['price']['fare'],2)
				outbound_flight['meta']['range'] = haversine(
														outbound_flight_summary['from']['lon'],
														outbound_flight_summary['from']['lat'],
														outbound_flight_summary['to']['lon'],
														outbound_flight_summary['to']['lat'],
													)
				departure_time = datetime.datetime.strptime(outbound_flight['departure_time'],"%Y-%m-%dT%H:%M:%S")
				arrival_time = datetime.datetime.strptime(outbound_flight['arrival_time'],"%Y-%m-%dT%H:%M:%S")
				flight_duration_in_hours = (arrival_time-departure_time).total_seconds() / 3600
				outbound_flight['meta']['cruise_speed_kmh'] = floor(outbound_flight['meta']['range'] / flight_duration_in_hours)
				outbound_flight['meta']['cost_per_km'] = round(outbound_flight['price']['fees'] / outbound_flight['meta']['range'],2)
				
				return_flight['price']['fees'] = round(max(return_flight['price']['fare']*0.1,40),2)
				return_flight['price']['total'] = round(return_flight['price']['fees'] + return_flight['price']['fare'],2)
				return_flight['meta']['range'] = haversine(
														return_flight_summary['from']['lon'],
														return_flight_summary['from']['lat'],
														return_flight_summary['to']['lon'],
														return_flight_summary['to']['lat'],
													)
				departure_time = datetime.datetime.strptime(return_flight['departure_time'],"%Y-%m-%dT%H:%M:%S")
				arrival_time = datetime.datetime.strptime(return_flight['arrival_time'],"%Y-%m-%dT%H:%M:%S")
				flight_duration_in_hours = (arrival_time-departure_time).total_seconds() / 3600
				return_flight['meta']['cruise_speed_kmh'] = floor(return_flight['meta']['range'] / flight_duration_in_hours)
				return_flight['meta']['cost_per_km'] = round(return_flight['price']['fees'] / return_flight['meta']['range'],2)

				round_trip = {
					"outbound_flight" : outbound_flight,
					"return_flight" : return_flight,
					"price" : {
						"fare":round(outbound_flight['price']['fare']+return_flight['price']['fare'],2),
						"fees":round(outbound_flight['price']['fees']+return_flight['price']['fees'],2),
						"total":round(outbound_flight['price']['total']+return_flight['price']['total'],2)
					}
				}

			options.append(round_trip)
			options.sort(key=lambda option: option["price"]["total"])

		response['round_trip_options'] = options


		return JsonResponse(response, safe=False)
from django.core.management.base import BaseCommand
from api.models import Airport
from requests.auth import HTTPBasicAuth
from django.core import serializers
import requests

class Command(BaseCommand):
	help = 'Cache all the airports from the API into the database.'
	
	def handle(self, *args, **options):
		basic = HTTPBasicAuth('demo','swnvlD')
		r = requests.get('http://stub.2xt.com.br/air/airports/pzrvlDwoCwlzrWJmOzviqvOWtm4dkvuc', auth = basic)
		
		try:
			cache = r.json()
		except:
			self.stderr.write(self.style.ERROR("Invalid JSON received from API."))
			return
		
		for airport in cache:
			if Airport.objects.filter(iata_code=cache[airport]['iata']).exists():
				item = Airport.objects.get(iata_code = cache[airport]['iata'])
				
				item.city = cache[airport]['city']
				item.lat = cache[airport]['lat']
				item.lon = cache[airport]['lon']
				item.state = cache[airport]['state']

				
			else:
				item = Airport(	
						iata_code = cache[airport]['iata'],
						city = cache[airport]['city'],
						lat = cache[airport]['lat'],
						lon = cache[airport]['lon'],
						state = cache[airport]['state']
						)
			
			try:
				item.save()
			except Exception as err:
				self.stderr.write(self.style.ERROR(err))

				
		self.stdout.write(self.style.SUCCESS("Done."))
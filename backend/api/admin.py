from django.contrib import admin
from .models import Airport

class AirportAdmin(admin.ModelAdmin):
	list_display = ('iata_code','city','lat','lon','state','status','reason')

# Register your models here.
admin.site.register(Airport, AirportAdmin)
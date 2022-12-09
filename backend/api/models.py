from django.db import models

# Create your models here.
class Airport(models.Model):
	
	STATUS = (('A','Active'),('I','Inactive'))

	iata_code = models.CharField(max_length=3, unique=True)
	city = models.CharField(max_length = 40)
	lat = models.DecimalField(max_digits=9,decimal_places=6)
	lon = models.DecimalField(max_digits=9,decimal_places=6)
	state = models.CharField(max_length = 2)
	status = models.CharField(max_length=1,choices=STATUS,default='A')
	reason = models.TextField(default='')
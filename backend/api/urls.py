from django.urls import path
from . import views

urlpatterns = [	
	path('toogleActive/<slug:iata>',views.toogle_active,name="toogle"),
	path('toogleInactive/<slug:iata>',views.toogle_inactive,name="toogle"),
	path('all',views.get_all_airports,name="get_all"),
	path('search/<slug:departure_airport>/<slug:arrival_airport>/<slug:departure_date>/<slug:return_date>',views.mock_airlines_api,name="mock_airlines")
]
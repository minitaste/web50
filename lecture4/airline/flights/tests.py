from django.db.models import Max
from django.test import Client, TestCase

from .models import Flight, Airport, Passenger

# Create your tests here.
class FlightTestCase(TestCase):

    def setUp(self):
        # Creating airports
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Creating flights
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a2, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    
    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 2)
        
        
    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 0)


    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.create(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())


    def test_invalid_flight(self):
        a = Airport.objects.get(code="AAA")
        f = Flight.objects.create(origin=a, destination=a, duration=100)
        self.assertFalse(f.is_valid_flight())

    
    def test_invalid_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.create(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())


    def test_index_page(self):
        c = Client()
        response = c.get("/flights/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)


    def test_valid_flight_page(self):
        a = Airport.objects.get(code="AAA")
        f = Flight.objects.create(origin=a, destination=a, duration=100)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)


    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]
        
        c = Client()
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)
 
        
    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Mkas", last="Lox")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

        
    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Mkas", last="Lox")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)



        
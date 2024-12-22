from django.test import TestCase

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

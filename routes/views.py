from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from opencage.geocoder import OpenCageGeocode
import openrouteservice
from .models import FuelPrice
from .serializers import FuelPriceSerializer
from django.conf import settings

class RoutePlannerAPIView(APIView):
    def post(self, request):
        # Parse inputs
        start_location = request.data.get("start_location")
        finish_location = request.data.get("finish_location")

        if not start_location or not finish_location:
            raise ValidationError("Start and finish locations are required.")

        # Initialize API clients
        open_cage_key = settings.OPENCAGE_API_KEY
        ors_key = settings.OPENROUTESERVICE_API_KEY

        geocoder = OpenCageGeocode(open_cage_key)
        ors_client = openrouteservice.Client(key=ors_key)

        try:
            # Geocode addresses
            start_coords = geocoder.geocode(start_location)[0]["geometry"]
            finish_coords = geocoder.geocode(finish_location)[0]["geometry"]

            # Generate route
            route = ors_client.directions(
                coordinates=[
                    (start_coords["lng"], start_coords["lat"]),
                    (finish_coords["lng"], finish_coords["lat"]),
                ],
                profile="driving-car",
            )

            # Calculate route details
            total_distance_km = route["routes"][0]["summary"]["distance"] / 1000  # Distance in km
            total_distance_miles = total_distance_km * 0.621371  # Convert to miles
            fuel_required = total_distance_miles / 10  # Assuming 10 miles per gallon
            fuel_stops = max(1, int(fuel_required / 500))  # Max distance 500 miles per refuel

            # Fetch cost-effective fuel stations
            fuel_prices = FuelPrice.objects.all().order_by("retail_price")[:fuel_stops]
            serializer = FuelPriceSerializer(fuel_prices, many=True)

            # Calculate total cost
            total_cost = round(sum([
                float(station["retail_price"]) * fuel_required  # Ensure retail_price is converted to float for calculation
                for station in serializer.data
            ]), 2)

            # Return response
            return Response({
                "route": route["routes"][0],
                "fuel_stops": serializer.data,
                "total_distance_km": round(total_distance_km, 2),
                "total_distance_miles": round(total_distance_miles, 2),
                "fuel_required": round(fuel_required, 2),
                "total_cost": total_cost,
            })

        except Exception as e:
            return Response({"error": f"Routing failed: {str(e)}"}, status=500)

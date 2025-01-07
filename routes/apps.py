import pandas as pd
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os

class RoutesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'routes'

    def ready(self):
        post_migrate.connect(import_fuel_prices, sender=self)

@receiver(post_migrate)
def import_fuel_prices(sender, **kwargs):
    from routes.models import FuelPrice

    file_path = os.path.expanduser('~/Downloads/spotter/fuel-prices-for-be-assessment.csv')

    try:
        if not FuelPrice.objects.exists():
            if os.path.exists(file_path):
                data = pd.read_csv(file_path)

                for _, row in data.iterrows():
                    FuelPrice.objects.create(
                        opis_truckstop_id=row['OPIS Truckstop ID'],
                        truckstop_name=row['Truckstop Name'],
                        address=row['Address'],
                        city=row['City'],
                        state=row['State'],
                        rack_id=row['Rack ID'],
                        retail_price=row['Retail Price'],
                    )
                print("Fuel prices imported successfully.")
            else:
                print(f"Fuel price CSV not found at {file_path}.")
        else:
            print("Fuel prices already initialized.")
    except Exception as e:
        print(f"Error occurred during initialization: {e}")

import json
from django.core.management.base import BaseCommand
from locations.models import State, LocalGovernment, Country

class Command(BaseCommand):
    help = "Populate LGAs for states in Nigeria from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument('locations/nigerian-states.json', type=str, help='Path to the JSON file containing LGAs data')
        parser.add_argument('--state_name', type=str, help='Name of the state to populate LGAs for (optional)')

    def handle(self, *args, **kwargs):
        json_file = kwargs['locations/nigerian-states.json']
        state_name = kwargs.get('state_name')

        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {json_file} not found"))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Error decoding JSON from file {json_file}"))
            return

        try:
            nigeria = Country.objects.get(name="Nigeria")
        except Country.DoesNotExist:
            self.stdout.write(self.style.ERROR("Country Nigeria does not exist in the database."))
            return

        if state_name:
            states_to_populate = {state_name: data.get(state_name)}
        else:
            states_to_populate = data

        for state_name, lgas in states_to_populate.items():
            if not lgas:
                self.stdout.write(self.style.ERROR(f"No LGAs found for state: {state_name} in the JSON file"))
                continue

            try:
                state = State.objects.get(name=state_name)
            except State.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"State {state_name} does not exist in the database."))
                continue

            for lga_name in lgas:
                LocalGovernment.objects.get_or_create(name=lga_name, state=state)
                self.stdout.write(self.style.SUCCESS(f"Added/Updated LGA: {lga_name} in state: {state_name}"))

        self.stdout.write(self.style.SUCCESS("Finished populating LGAs"))

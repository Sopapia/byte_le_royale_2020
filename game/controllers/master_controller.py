from copy import deepcopy

from game.common.enums import *
from game.common.player import Player
from game.common.action import Action
from game.common.disasters import *
from game.common.city import City
import game.config as config

from game.controllers.controller import Controller
from game.controllers.city_generator_controller import CityGeneratorController
from game.controllers.destruction_controller import DestructionController
from game.controllers.disaster_controller import DisasterController
from game.controllers.effort_controller import EffortController


class MasterController(Controller):
    def __init__(self):
        super().__init__()

        self.city_generator_controller = CityGeneratorController()
        self.destruction_controller = DestructionController()
        self.disaster_controller = DisasterController()
        self.effort_controller = EffortController()

        self.game_over = False

    # Receives all clients for the purpose of giving them the objects they will control
    def give_clients_objects(self, client):
        client.city = City()
        client.team_name = client.code.team_name()
        client.city.city_name = client.code.city_name()
        city_type = client.code.city_type()

        self.city_generator_controller.handle_actions(client, city_type)

    # Generator function. Given a key:value pair where the key is the identifier for the current world and the value is
    # the state of the world, returns the key that will give the appropriate world information
    def game_loop_logic(self, start=1):
        turn = start

        # Basic loop from 1 to max turns
        while True:
            # Wait until the next call to give the number
            yield turn
            # Increment the turn counter by 1
            turn += 1
            # If the next turn number is above the max, the iterator ends
            if turn > config.MAX_TURNS:
                break

    # Receives world data from the generated game log and is responsible for interpreting it
    def interpret_current_turn_data(self, client, world, turn):
        # Turn disaster occurrence into a real disaster
        for disaster in world['disasters']:
            dis = None
            if disaster is DisasterType.earthquake:
                dis = Earthquake()
            elif disaster is DisasterType.fire:
                dis = Fire()
            elif disaster is DisasterType.hurricane:
                dis = Hurricane()
            elif disaster is DisasterType.monster:
                dis = Monster()
            elif disaster is DisasterType.tornado:
                dis = Tornado()
            elif disaster is DisasterType.ufo:
                dis = Ufo()

            if dis is None:
                raise TypeError(f'Attempt to create disaster failed because given type: {disaster}, does not exist.')

            client.disasters.append(dis)

        # read the sensor results from the game map, converting strings to ints and/or floats
        world['sensors'] = {int(key): {int(key2): float(val2) for key2, val2 in val.items()} for key, val in world['sensors'].items()}

        # give client their corresponding sensor odds
        sensor_results = dict()
        for sensor in client.city.sensors.values():
            sensor_results[sensor.sensor_type] = world['sensors'][sensor.sensor_type][sensor.sensor_level]
        client.city.sensor_results = sensor_results

    # Receive a specific client and send them what they get per turn. Also obfuscates necessary objects.
    def client_turn_arguments(self, client, world, turn):
        actions = Action()
        client.action = actions

        obfuscated_city = client.city
        obfuscated_disasters = client.disasters

        args = (actions, obfuscated_city, obfuscated_disasters,)
        return args

    # Perform the main logic that happens per turn
    def turn_logic(self, client, world, turn):
        self.effort_controller.handle_actions(client)
        self.disaster_controller.handle_actions(client)
        self.destruction_controller.handle_actions(client)

        if client.city.structure <= 0:
            self.print("Game is ending because city has been destroyed.")
            self.game_over = True

        if client.city.population <= 0:
            self.print("Game is ending because population has died.")
            self.game_over = True

    # Return serialized version of game
    def create_turn_log(self, client, world, turn):
        data = dict()

        data['rates'] = world['rates']

        data['player'] = client.to_json()

        return data

    # Gather necessary data together in results file
    def return_final_results(self, client, world, turn):
        # data is the json information what will be written to the results file
        data = {
            "Team": client.team_name,  # TODO: Replace with an engine-safe ID of each team
            "Score": turn
        }
        return data

    # Return if the game should be over
    def game_over_check(self):
        return self.game_over

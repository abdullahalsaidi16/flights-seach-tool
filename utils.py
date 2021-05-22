"""
this module for providing common ds for flights search functionality
author: abdullah alsaidi
"""
from typing import List
import pprint
from datetime import datetime, timedelta
from copy import deepcopy


class Passenger:
    def __init__(self, num_bags, place, flights=[], timing=None) -> None:
        self.num_bags = num_bags
        self.flights = flights
        self.place = place
        self.timing = timing
        self.visited = set()
        self.cost = 0
        self.is_done = False
        self.rides = []
        self.path = f"{place}"

    def __str__(self) -> str:
        return f"{self.place} | {self.timing} | {self.visited}"

    def travel(self, flight: 'Flight') -> None:
        """
        function to make the passenger travel and change its attributes according to flight passed

        """
        self.place = flight.dest
        self.timing = flight.arrival
        self.visited.add(flight.dest)
        self.visited.add(flight.source)
        self.rides.append(f"{flight.source}->{flight.dest}")
        self.cost += flight.price
        self.cost += flight.bag_price * self.num_bags
        # print(f"{flight.source} -> {flight.dest}")
        self.path += f" -> {flight.dest}"


class Flight:
    def __init__(self, flight_data: dict) -> None:
        self._id = flight_data["flight_number"]
        self.source = flight_data["source"]
        self.dest = flight_data["destination"]
        self.departure = datetime.strptime(
            flight_data["departure"], "%Y-%m-%dT%H:%M:%S"
        )
        self.arrival = datetime.strptime(flight_data["arrival"], "%Y-%m-%dT%H:%M:%S")
        self.price = int(flight_data["price"])
        self.bags_allowed = int(flight_data["bags_allowed"])
        self.bag_price = int(flight_data["bag_price"])

    def __str__(self) -> str:
        return f"{self.source} -> {self.dest} | {self.departure}-> {self.arrival} | {self.bags_allowed}"

    def __repr__(self) -> str:
        return self.__str__()

    def can_ride(self, passenger: Passenger) -> bool:
        """
        this function check if passenger is eligable to ride on this trip
        """
        # Geo check
        # same citites same trip
        if f"{self.source}->{self.dest}" in passenger.rides:
            return False
        # Timing + Bags check
        if not passenger.timing:
            return passenger.num_bags <= self.bags_allowed

        if any(
            [
                passenger.num_bags > self.bags_allowed,
                passenger.timing > self.departure - timedelta(hours=1),
                passenger.timing < self.departure - timedelta(hours=4),
            ]
        ):
            return False
        return True


class Graph:
    """
    Graph representaion for the cities where the edges of the graph are the flights
    """
    def __init__(self, nodes: set) -> None:
        self.adj = dict()
        self.cost = dict()
        # init graph
        for node_1 in nodes:
            for node_2 in nodes:
                if node_1 != node_2:
                    if self.adj.get(node_1):
                        self.adj[node_1].update({node_2: []})
                    else:
                        self.adj[node_1] = {node_2: []}

    def add_flights(self, flights: List[Flight]) -> None:
        """
        this function to add flight object to the graph
        """
        for flight in flights:
            self.adj[flight.source][flight.dest].append(flight)

    def __repr__(self):
        return pprint.pformat(self.adj, indent=4)

    def find_combinations(self, passenger, include_cost=False) -> None:
        """
        this function find all the possible combinations of trips for the argument passenger
        and print results to the stdout
        """
        self.cost = dict()
        self.backtrack(passenger)
        self.pretty_print_results(include_cost)

    def backtrack(self, passenger: Passenger, flight=None) -> None:
        """
        a recursive function to traverse the graph and finding all possible flight
        in addition the function calculates the minimal cost for each possible trip
        """
        if flight and flight.can_ride(passenger):
            passenger.travel(flight)
            self.cost[passenger.path] = min(
                self.cost.get(passenger.path, 1e5), passenger.cost
            )
        elif flight:
            return

        for dest in self.adj[passenger.place]:
            for available_flight in self.adj[passenger.place][dest]:
                self.backtrack(deepcopy(passenger), available_flight)

    def pretty_print_results(self, include_cost: bool) -> None:
        """
        prettify the printing of the calculated trips
        """
        if include_cost:
            [print(f"{key} | with total cost: {val}") for key, val in self.cost.items()]
        else:
            [print(x) for x in self.cost]

    def get_cost(self) -> dict:
        return self.cost

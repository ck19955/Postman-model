import random
from postman.objects import House, Postman, BusPassenger, BusNetwork
import numpy as np


class LinearBusRouteModel(BusNetwork):
    """Linear bus route with stops and buses

    Parameters
    ==========

    start: int, coordinate of start of the route
    end: int, coordinate of end of the route
    stops: list[BusStop], list of bus stops
    buses: list[Bus], list of the buses on the route
    rates: dict[str,float] (optional) rates of passengers arriving

    A LinearBusRoute instances holds a complete model of the state of all
    buses, bus stops and passengers along its route.

    Examples
    ========

    First create passengers, buses and bus stops:

        >>> dave = BusPassenger('Dave', 'West St', 'East St')
        >>> joan = BusPassenger('Joan', 'West St', 'East St')
        >>> bus = Bus('Number 47', (20, 0), 1, [dave])
        >>> busstops = [BusStop('West St', (0, 100), [joan]),
        ...             BusStop('East St', (100, 100), [])]

    Finally we are ready to create a complete linear bus route model with two
    stops and one bus:

        >>> model = LinearBusRouteModel(0, 100, busstops, [bus])

    This model has a route going from coordinate 0 to 100 with a bus stop at
    each end. There are two passengers Dave and Joan both wanting to go from
    East St to West St. Joan is waiting at the West St bus stop. Dave is on
    the bus which is already heading to East St and is currently at
    coordinate 20.
    """

    def init(self):
        """Initialise the model and return initial events.

        Computes and returns the initial events of the simulation e.g.

            >>> sally = BusPassenger('Sally', 'West St', 'East St')
            >>> bus = Bus('56', (0, 0), 1, [sally])
            >>> model = LinearBusRouteModel(0, 100, [], [bus])
            >>> events = model.init()
            >>> events
            [('boards', 'Sally', '56')]

        This shows that at the start of the simulation Sally boards the number
        56 bus.
        """
        self.passenger_num = 0

        events = []
        return events

    def update(self):
        events = []
        WaitingTimes = []
        BusCapacities = []
        for bus in self.buses:
            for passenger in bus.passengers:
                passenger.update_journey_time()
            BusEvents, JourneyTimes, BusWaitingTimes = self.update_bus(bus)
            for item in BusWaitingTimes:
                WaitingTimes.append(item)
            events += BusEvents
            BusCapacities.append(len(bus.passengers))

        for stop in self.stops:
            events += self.update_stop(stop)
            for passenger in stop.passengers:
                passenger.update_waiting_time()



        return events, WaitingTimes, JourneyTimes, BusCapacities

    def update_bus(self, bus):
        """Update simulation state of bus."""

        # Assume all buses have speed 1 (needs to be an int)

        old_x, old_y = bus.position
        new_x = old_x + bus.speed * bus.direction
        new_y = old_y  # Buses move horizontally
        bus.position = (new_x, old_y)

        events = []
        JourneyTimes = []
        WaitingTimes = []


        # Does the bus stop at any stops?
        for stop in self.stops:
            stop_x, stop_y = stop.position
            if old_x < stop_x <= new_x or old_x > stop_x >= new_x:
                StopEvents, StepJourneyTimes, WaitingTimes = self.stop_at(bus, stop)
                for item in StepJourneyTimes:
                    JourneyTimes.append(item)
                events += StopEvents

        # Does the bus turn around?
        if not (self.start <= new_x <= self.end):
            bus.direction = - bus.direction
            events.append(('turns', bus.name))

        return events, JourneyTimes, WaitingTimes

    def stop_at(self, bus, stop):
        """Handle bus stopping at stop."""

        original_speed = bus.speed
        # Passengers get off if this is their stop
        staying_passengers = []
        leaving_passengers = []
        for passenger in bus.passengers:
            if passenger.destination == stop.name:
                leaving_passengers.append(passenger)
                bus.speed = 0
            else:
                staying_passengers.append(passenger)
        bus.speed = original_speed
        # All passengers waiting at the bus stop get on
        waiting_passengers = stop.passengers
        boarding_passengers = []
        bus.passengers = boarding_passengers + staying_passengers
        # Actually update passengers at bus and stop
        for passenger in waiting_passengers:
            if len(bus.passengers) < 40 and passenger.direction == bus.direction:
                boarding_passengers.append(passenger)
                bus.passengers = boarding_passengers + staying_passengers
                bus.speed = 0

        bus.speed = original_speed
        JourneyTimes = []
        WaitingTimes = []
        for passenger in boarding_passengers:
            waiting_passengers.remove(passenger)
        # Record events for everyone getting on and off
        events = []

        return events, JourneyTimes, WaitingTimes

    def update_stop(self, stop):
        """Update bus stop"""

        # New passengers arrive randomly at each bus stop. The probability of
        # a passenger arriving at particular stop is given by
        #     1 - self.rates[self.name].

        return []

if __name__ == "__main__":
    import doctest
    doctest.testmod()
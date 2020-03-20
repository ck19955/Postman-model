import random
from postman.objects import House, Postman, Letters, RoadNetwork
import numpy as np


class LinearPostmanModel(RoadNetwork):

    def init(self):
        self.letter_num = 0

        events = []
        return events

    def update(self):
        events = []
        WaitingTimes = []
        BusCapacities = []
        for bus in self.buses:
            for letter in bus.letters:
                letter.update_journey_time()
            BusEvents, JourneyTimes, BusWaitingTimes = self.update_bus(bus)
            for item in BusWaitingTimes:
                WaitingTimes.append(item)
            events += BusEvents
            BusCapacities.append(len(bus.letters))

        for stop in self.stops:
            events += self.update_stop(stop)
            for letter in stop.letters:
                letter.update_waiting_time()



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
        remaining_letters = []
        leaving_letters = []
        for letter in bus.letters:
            if letter.destination == stop.name:
                leaving_letters.append(letter)
                bus.speed = 0
            else:
                remaining_letters.append(letter)
        bus.speed = original_speed
        # All passengers waiting at the bus stop get on

        bus.letters = remaining_letters

        JourneyTimes = []
        WaitingTimes = []
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
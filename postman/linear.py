import random
from postman.objects import House, Postman, Letters, RoadNetwork, Cart
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
        for postman in self.postmen:
            for letter in postman.letters:
                letter.update_journey_time()
            BusEvents, JourneyTimes, BusWaitingTimes = self.update_postman(postman)
            for item in BusWaitingTimes:
                WaitingTimes.append(item)
            events += BusEvents
            BusCapacities.append(len(postman.letters))

        for house in self.houses:
            events += self.update_house(house)
            for letter in house.letters:
                letter.update_waiting_time()



        return events, WaitingTimes, JourneyTimes, BusCapacities

    def update_postman(self, postman):
        """Update simulation state of bus."""

        # Assume all buses have speed 1 (needs to be an int)

        old_x, old_y = postman.position
        new_x = old_x + postman.speed * postman.direction
        new_y = old_y  # Buses move horizontally
        postman.position = (new_x, old_y)

        events = []
        JourneyTimes = []
        WaitingTimes = []


        # Does the bus stop at any stops?
        for house in self.houses:
            house_x, house_y = house.position
            if old_x < house_x <= new_x or old_x > house_x >= new_x:
                StopEvents, StepJourneyTimes, WaitingTimes = self.stop_at(postman, house)
                for item in StepJourneyTimes:
                    JourneyTimes.append(item)
                events += StopEvents

        # Does the bus turn around?
        if not (self.start <= new_x <= self.end):
            postman.direction = - postman.direction
            events.append(('turns', postman.name))
        
        '''
        Postman changes direction when he has no letters and is walking wrong direction
        '''
        
        return events, JourneyTimes, WaitingTimes

    def stop_at(self, postman, house):
        """Handle bus stopping at stop."""

        original_speed = postman.speed
        # Passengers get off if this is their stop
        remaining_letters = []
        leaving_letters = []
        for letter in postman.letters:
            if letter.destination == house.name:
                leaving_letters.append(letter)
                postman.speed = 0
            else:
                remaining_letters.append(letter)
        postman.speed = original_speed
        # All passengers waiting at the bus stop get on

        postman.letters = remaining_letters

        JourneyTimes = []
        WaitingTimes = []
        # Record events for everyone getting on and off
        events = []

        return events, JourneyTimes, WaitingTimes

    def update_house(self, house):
        """Update bus stop"""

        # New passengers arrive randomly at each bus stop. The probability of
        # a passenger arriving at particular stop is given by
        #     1 - self.rates[self.name].

        return []

if __name__ == "__main__":
    import doctest
    doctest.testmod()
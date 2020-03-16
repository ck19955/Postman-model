#!/usr/bin/env python3


from postman.objects import BusPassenger, Postman, House
from postman.linear import LinearBusRouteModel
from postman.animate import animate_model

houses = [
    House('House 1', (0, 0), []),
    House('House 2', (25, 0), []),
    House('House 3', (50, 0), []),
    House('House 4', (75, 0), []),
    House('House 5', (100, 0), []),
]

postman = [
    Postman('Postman', (20,0), 1, [], 1.0),
]

model = LinearBusRouteModel(0, 100, houses, postman)

animate_model(model)
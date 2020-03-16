#!/usr/bin/env python3
from postman.objects import BusPassenger, Postman, House
from postman.linear import LinearBusRouteModel
from postman.animate import animate_model

House1_mail = [ 
    BusPassenger('', 'Cart', 'House 1'),
    BusPassenger('', 'Cart', 'House 1'),
    BusPassenger('', 'Cart', 'House 1'),
]

House2_mail = [ 
    BusPassenger('', 'Cart', 'House 2'),
    BusPassenger('', 'Cart', 'House 2'),
    BusPassenger('', 'Cart', 'House 2'),
]

House3_mail = [ 
    BusPassenger('', 'Cart', 'House 3'),
    BusPassenger('', 'Cart', 'House 3'),
    BusPassenger('', 'Cart', 'House 3'),
]

House4_mail = [ 
    BusPassenger('', 'Cart', 'House 4'),
    BusPassenger('', 'Cart', 'House 4'),
    BusPassenger('', 'Cart', 'House 4'),
]

Mail = House1_mail + House2_mail + House3_mail + House4_mail

houses = [
    House('Cart', (0, 0), Mail),
    House('House 1', (25, 0), []),
    House('House 2', (50, 0), []),
    House('House 3', (75, 0), []),
    House('House 4', (100, 0), []),
]

postman = [
    Postman('Postman', (0,0), 1, [], 1.0),
]

model = LinearBusRouteModel(0, 100, houses, postman)

animate_model(model)
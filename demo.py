#!/usr/bin/env python3
from postman.objects import BusPassenger, Postman, House
from postman.linear import LinearBusRouteModel
from postman.animate import animate_model

NumHouses = 10
MailPerHouse = 2


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

Houses = []
HouseSpacing = 100/NumHouses
for i in range(1,NumHouses+1):
    Houses.append(House("House " + str(i), (int((i)*HouseSpacing),0), []))


postman = [
    Postman('Postman', (0,0), 1, Mail, 1.0),
]

model = LinearBusRouteModel(0, 100, Houses, postman)

animate_model(model)
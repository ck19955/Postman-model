#!/usr/bin/env python3
from postman.objects import BusPassenger, Postman, House
from postman.linear import LinearBusRouteModel
from postman.animate import animate_model

NumHouses = 10
MailPerHouse = 2
RoadLength = 100

Mail = []

for i in range(1,MailPerHouse+1):
    for i in range(1,NumHouses+1):
        Mail.append(BusPassenger('Cart', 'House ' + str(i)))

Houses = []
HouseSpacing = RoadLength/NumHouses
for i in range(1,NumHouses+1):
    Houses.append(House("House " + str(i), (int((i)*HouseSpacing),0), []))


postman = [
    Postman('Postman', (0,0), 1, Mail, 1.0),
]

model = LinearBusRouteModel(0, RoadLength, Houses, postman)

animate_model(model)
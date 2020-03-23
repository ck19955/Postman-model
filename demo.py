#!/usr/bin/env python3
from postman.objects import Letters, Postman, House, Cart
from postman.linear import LinearPostmanModel
from postman.animate import animate_model

NumHouses = 10
MailPerHouse = 1
RoadLength = 100

Mail = []

for i in range(1,MailPerHouse+1):
    for i in range(1,NumHouses+1):
        Mail.append(Letters('Cart', 'House ' + str(i)))

Houses = []
HouseSpacing = RoadLength/NumHouses
for i in range(1,NumHouses+1):
    Houses.append(House("House " + str(i), (int((i)*HouseSpacing),0), []))


postman = [
    Postman('Postman', (50,0), 1, [], 1.0),
]

cart = [
    Cart((0,0), Mail)
]

model = LinearPostmanModel(0, RoadLength, Houses, postman, cart)

animate_model(model)
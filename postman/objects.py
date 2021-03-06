class Printable:

    def __repr__(self):
        classname = type(self).__name__
        args = [getattr(self, p) for p in self.parameters]
        return '%s(%s)' % (classname, ', '.join(map(repr, args)))


class Letters(Printable):

    parameters = 'source', 'destination'

    def __init__(self, source, destination):

        if not all(isinstance(p, str) for p in (source, destination)):
            raise TypeError('source and destination should be strings')

        self.source = source
        self.destination = destination
        self.waitingtime = 0
        self.journeytime = 0
        if source[0] > destination[0]:
            self.direction = 1
        else:
            self.direction = -1

    def update_waiting_time(self):
        # Measure the waiting time of each person
        self.waitingtime += 1

    def update_journey_time(self):
        # Measure the journey time of each person
        self.journeytime += 1



class House(Printable):

    parameters = 'name', 'position', 'letters'

    def __init__(self, name, position, letters):

        if not isinstance(name, str):
            raise TypeError('name should be a string')
        if not (isinstance(position, tuple) and len(position) == 2 and
                all(isinstance(c, int) for c in position)):
            raise TypeError('position should be a pair of ints')
        if not all(isinstance(p, Letters) for p in letters):
            raise TypeError('letters should be a list of Letters')
        if not all(p.source == name for p in letters):
            raise ValueError('passenger at the wrong stop')

        self.name = name
        self.position = position
        self.letters = list(letters)

    def init_animation(self, ax):
        """Initialise matplotlib animation for axes ax"""
        self.stop_line, = ax.plot([], [], 'ko', markersize=10)
        self.queue_line, = ax.plot([], [], 'go') # colours and shape
        x, y = self.position
        self.text = ax.text(x, y-3, self.name, rotation=90,
                verticalalignment='top', horizontalalignment='center')
        return [self.stop_line, self.queue_line, self.text]

    def update_animation(self):
        """Update matplotlib animation for axes ax"""
        x, y = self.position
        # Redraw the bus stop
        self.stop_line.set_data([x], [y])
        # Redraw the queueing passingers
        qspace = 2
        num_letters = len(self.letters)
        xdata = [x] * num_letters
        ydata = [y + qspace*(n+1) for n in range(num_letters)]
        self.queue_line.set_data(xdata, ydata)
        # Return the patches for matplotlib to update
        return [self.stop_line, self.queue_line, self.text]



class Postman(Printable):

    parameters = 'name', 'position', 'direction', 'letters', 'speed'

    def __init__(self, name, position, direction, letters, speed):

        if not isinstance(name, str):
            raise TypeError('name should be a string')
        if not (isinstance(position, tuple) and len(position) == 2 and
                all(isinstance(c, int) for c in position)):
            raise TypeError('position should be a pair of ints')
        if direction not in {1, -1}:
            raise TypeError('direction should be 1 or -1')
        if not all(isinstance(p, Letters) for p in letters):
            raise TypeError('letters should be a list of Letters')
        if not isinstance(speed, float):
            raise TypeError('speed should be a positive number')
        if isinstance(speed, float):
            if float(speed) < 0:
                raise TypeError('speed should be a positive number')
        self.name = name
        self.position = position
        self.direction = direction
        self.letters = list(letters)
        self.speed = speed

    def init_animation(self, ax):
        """Initialise matplotlib animation for axes ax"""
        self.bus_line, = ax.plot([], [], 'ms', markersize=10)
        self.letters_line, = ax.plot([], [], 'bo')
        x, y = self.position
        self.text = ax.text(x, y+3, self.name,
                verticalalignment='bottom', horizontalalignment='center')
        return [self.bus_line, self.letters_line, self.text]

    def update_animation(self):
        """Update matplotlib animation for axes ax"""
        # Redraw the bus
        x, y = self.position
        self.bus_line.set_data([x], [y])
        # Redraw the passengers
        pspace = 2
        num_letters = len(self.letters)
        xdata = [x] * num_letters
        ydata = [y - pspace*(n+1) for n in range(num_letters)]
        self.letters_line.set_data(xdata, ydata)
        # Update text position
        self.text.set_x(x)
        self.text.set_y(y+3)
        # Return the patches for matplotlib to update
        return [self.bus_line, self.letters_line, self.text]

class Cart(Printable):
    
    parameters = 'position', 'letters'
    
    def __init__(self, position, letters):
        if not (isinstance(position, tuple) and len(position) == 2 and
                all(isinstance(c, int) for c in position)):
            raise TypeError('position should be a pair of ints')
        if not all(isinstance(p, Letters) for p in letters):
            raise TypeError('letters should be a list of Letters')
        self.position = position
        self.letters = list(letters)
        
    def init_animation(self, ax):
        self.cart_line, = ax.plot([], [], 'rs', markersize=10)
        self.letters_line, = ax.plot([], [], 'bo')
        x, y = self.position
        self.text = ax.text(x, y+3, "cart",
                verticalalignment='bottom', horizontalalignment='center')
        return [self.cart_line, self.letters_line, self.text]

    def update_animation(self):
        x, y = self.position
        self.cart_line.set_data([x], [y])
        # Redraw the passengers
        pspace = 2
        num_letters = len(self.letters)
        xdata = [x] * num_letters
        ydata = [y - pspace*(n+1) for n in range(num_letters)]
        self.letters_line.set_data(xdata, ydata)
        # Update text position
        self.text.set_x(x)
        self.text.set_y(y+3)
        # Return the patches for matplotlib to update
        return [self.cart_line, self.letters_line, self.text]


class RoadNetwork(Printable):

    def __init__(self, start, end, houses, postmen, carts):
        self.start = start
        self.end = end
        self.houses = list(houses)
        self.postmen = list(postmen)
        self.carts = list(carts)

    def init(self):
        """Initialise the model after creating nand return events"""
        raise NotImplementedError("Subclasses should override this method")

    def update(self):
        """Updates the model through one timestep"""
        raise NotImplementedError("Subclasses should override this method")

    def init_animation(self, ax):
        """Initialise matplotlib animation for axes ax"""

        # Initialise self before child objects
        patches = self._init_animation(ax)

        # Initialise all buses
        for postman in self.postmen:
            patches += postman.init_animation(ax)

        # Initialise all bus stops
        for house in self.houses:
            patches += house.init_animation(ax)
        
        for cart in self.carts:
            patches += cart.init_animation(ax)
        # List of patches for matplotlib to update
        return patches

    def update_animation(self):
        """Update matplotlib animation for axes ax"""

        # Redraw self before child objects
        patches = self._update_animation()

        # Redraw bus stops
        for house in self.houses:
            patches += house.update_animation()

        # Redraw buses
        for postman in self.postmen:
            patches += postman.update_animation()
            
        for cart in self.carts:
            patches += cart.update_animation()
        # List of patches for matplotlib to update
        return patches

    def _init_animation(self, ax):
        """Initialise self for animation in axes ax"""
        size = self.end - self.start
        delta = size // 10
        ax.set_xlim([self.start-delta, self.end+delta])
        ax.set_ylim([-size//2, size//2])
        self.route_line, = ax.plot([], [], 'k-', linewidth=3)
        return [self.route_line]

    def _update_animation(self):
        """Redraw self for animation in axes ax"""
        xdata = [self.start, self.end]
        ydata = [0, 0]
        self.route_line.set_data(xdata, ydata)
        return [self.route_line]


if __name__ == "__main__":
    import doctest
    doctest.testmod()

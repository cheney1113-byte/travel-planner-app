class Trip:
    def __init__(self, name):
        self.name = name
        self.days = []

    def add_day(self, day):
        self.days.append(day)

    def show(self):
        print(f"Trip: {self.name}")
        for day in self.days:
            print(f"- {day}")


trip = Trip("My Travel Plan")
trip.add_day("Day 1: Arrive and walk around the city")
trip.add_day("Day 2: Visit main attractions")
trip.show()
class Pax:
    traveller_id = 0
    flight_id = 0
    same_tour_count = 0

    def __init__(self, traveller_id, fl, same):
        self.traveller_id = traveller_id
        self.flight_id = fl
        self.same_tour_count = same

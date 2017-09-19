class Aircraft:
    tail_number = -1
    type_number = 9
    earliest_available_time_stamp = -1  # the time stamp in milliseconds from 1970
    earliest_available_time = 'UNKNOWN'  # the ordinary time form
    latest_available_time_stamp = -1  # the time stamp in milliseconds from 1970
    latest_available_time = 'UNKNOWN'  # the ordinary time form
    departure_port = 'UNKNOWN'
    seat_count = -1

    def __init__(self, tail_number, type_number, earliest_available_time_stamp, latest_available_time_stamp,
                 departure_port, seat_count):
        self.tail_number = tail_number
        self.type_number = type_number
        self.earliest_available_time_stamp = earliest_available_time_stamp
        self.latest_available_time_stamp = latest_available_time_stamp
        self.departure_port = departure_port
        self.seat_count = seat_count

    def display(self):
        print("tail number : ", self.tail_number,
              ", plane_type: ", self.type_number,
              " earliest_available_time_stamp:", self.earliest_available_time_stamp,
              " earliest_available_time:", self.earliest_available_time,
              " latest_available_time_stamp:", self.latest_available_time_stamp,
              " latest_available_time:", self.latest_available_time,
              " departure_port:", self.departure_port,
              " seat_count:", self.seat_count, )

class Airline:
    airline_number = 0
    depart_time_stamp = -1
    depart_time = ''
    arrive_time_stamp = -1
    arrive_time = ''
    depart_airport = ''
    arrive_airport = ''
    plane_type = ''
    plane_tail_number = ''
    delay_time = 0

    def __init__(self, airline_number, depart_time_stamp, arrive_time_stamp, depart_airport, arrive_airport, plane_type,
                 plane_tail_number):
        self.airline_number = airline_number
        self.depart_time_stamp = depart_time_stamp
        self.arrive_time_stamp = arrive_time_stamp
        self.depart_airport = depart_airport
        self.arrive_airport = arrive_airport
        self.plane_type = plane_type
        self.plane_tail_number = plane_tail_number

    def display(self):
        print("Airline number : ", self.airline_number,
              ", depart_time_stamp: ", self.depart_time_stamp,
              ", arrive_time_stamp: ", self.arrive_time_stamp,
              ", depart_airport: ", self.depart_airport,
              ", arrive_airport: ", self.arrive_airport,
              ", plane_type: ", self.plane_type,
              ", plane_tail_number: ", self.plane_tail_number,
              ", delay_time", self.delay_time,
              )

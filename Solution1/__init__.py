#!/usr/bin/python
# -*- coding: UTF-8 -*-
import excel_reader as reader
import datetime, time
from datetime import tzinfo, timedelta
import excel_writer

class UTC(tzinfo):
    """UTC"""

    def __init__(self, offset=0):
        self._offset = offset

    def utcoffset(self, dt):
        return timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return timedelta(hours=self._offset)


def is_time_ovs_closed(timestamp):
    return 1461348000 <= timestamp < 1461358800


def solve_current_situation(current_time_stamp, schedules, aircrafts):
    return


def delay_airline(schedule_set, tmp):
    "schedule set is all the airlines, and the second param is the airline that need to be delayed."
    delay_time = 0  # positive value , can only be 0 or positive.
    if tmp.arrive_airport == 'OVS' and is_time_ovs_closed(
            tmp.arrive_time_stamp):
        delay_time = 1461358800 - tmp.arrive_time_stamp
    else:
        delay_time = 1461358800 - tmp.depart_time_stamp

    tmp.delay_time = delay_time

    tmp.display()
    return delay_time


def solve_maintainence_balance(schedule_set):
    "this method solve the maintainence problem for each plane, return value is the delay time needed for maintainence"
    planes = []
    total_delay = 0
    for aircraft in schedule_set:
        if not planes.__contains__(aircraft.plane_tail_number):
            planes.append(aircraft.plane_tail_number)

    for plane in planes:
        prev = 0
        for airline in schedule_set:
            if airline.plane_tail_number == plane:
                "check if the time is 45min + previous arrive time."
                if airline.depart_time_stamp + airline.delay_time - prev >= 45 * 60:
                    prev = airline.arrive_time_stamp + airline.delay_time
                    continue
                else:
                    delay_value = 45 * 60 - (airline.depart_time_stamp + airline.delay_time - prev)
                    airline.delay_time += delay_value
                    total_delay += delay_value
                    prev = airline.arrive_time_stamp + delay_value
            else:
                break

    return total_delay

def solve_max_capacity_problem(schedule_set):
    depart_time_spot = {}
    arrive_time_spot = {}

    for airline in schedule_set:
        depart_key = airline.depart_time_stamp / 600
        arrive_key = airline.arrive_time_stamp / 600
        if depart_time_spot.__contains__(depart_key):
            if depart_time_spot[depart_key]<5:
                depart_time_spot[depart_key] += 1
            else:
                delay_value = delay_airline(schedule_set,airline)

        else:
            depart_time_spot[depart_key] = 1

        if arrive_time_spot.__contains__(arrive_key):
            arrive_time_spot[arrive_key] += 1
        else:
            arrive_time_spot[arrive_key] = 1

    return depart_time_spot,arrive_time_spot


if __name__ == '__main__':
    print('init')
    schedule = reader.read_from_schedule_for_planetype_9()
    air_crafts = reader.read_from_aircraft()
    print(time.asctime(time.gmtime(1461302220)))
    start_time = 1461302220
    end_time = 1461302220 + 48 * 60 * 60
    # for time in range(start_time, end_time, 600):
    # solve_current_situation(time, schedule, air_crafts)
    count = 0
    total_delay = 0
    for tmp in schedule:
        if tmp.arrive_airport == 'OVS' and is_time_ovs_closed(
                tmp.arrive_time_stamp) or tmp.depart_airport == 'OVS' and is_time_ovs_closed(tmp.depart_time_stamp):
            total_delay += delay_airline(schedule, tmp)
            count += 1
            continue
    print(count)
    # print('total delay ', total_delay)


    total_delay += solve_maintainence_balance(schedule)
    # print('total delay ', total_delay)


    depart_set, arrive_set = solve_max_capacity_problem(schedule)
    # print(depart_set)
    # print(arrive_set)
    excel_writer.write_schedule(schedule)

    sum = 0
    for line in schedule:
        sum += line.delay_time

    print(sum)



#!/usr/bin/python
# -*- coding: UTF-8 -*-

# consider plane shift.
# shift between same type planes do not need extra cost.

import excel_reader as reader
import datetime, time
from datetime import tzinfo, timedelta
import excel_writer


def is_time_ovs_closed(timestamp):
    return 1461348000 <= timestamp < 1461358800


def delay_airline(tmp):
    "schedule set is all the airlines, and the second param is the airline that need to be delayed."
    delay_time = 0  # positive value , can only be 0 or positive.
    if tmp.arrive_airport == 'OVS' and is_time_ovs_closed(
            tmp.arrive_time_stamp):
        delay_time = 1461358800 - tmp.arrive_time_stamp
    else:
        delay_time = 1461358800 - tmp.depart_time_stamp

    tmp.delay_time = delay_time
    return delay_time


def need_delay(airline):
    "schedule set is all the airlines, and the second param is the airline that need to be delayed."
    delay_time = 0  # positive value , can only be 0 or positive.
    if airline.arrive_airport == 'OVS' and is_time_ovs_closed(
            airline.arrive_time_stamp):
        # delay_time = 1461358800 - airline.arrive_time_stamp
        return True
    if airline.depart_airport == 'OVS' and is_time_ovs_closed(
            airline.depart_time):
        # delay_time = 1461358800 - airline.depart_time_stamp
        return True
    return False
    # airline.delay_time = delay_time
    #
    # airline.display()
    # return delay_time


def OVS_reopen_time_stamp():
    return 1461358800


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
            # if depart_time_spot[depart_key]<5:
            depart_time_spot[depart_key] += 1
            # else:
            #     delay_value = delay_airline(schedule_set,airline)
        else:
            depart_time_spot[depart_key] = 1

        if arrive_time_spot.__contains__(arrive_key):
            arrive_time_spot[arrive_key] += 1
        else:
            arrive_time_spot[arrive_key] = 1

    return depart_time_spot, arrive_time_spot


def minimum_idle_time():
    return 45 * 60


def calculate_delay_for_route_without_considering_the_later_on_delays(route):
    "计算对于某一个给定route，由第一个延迟导致的后续航班总延迟。"
    import numpy as np
    tmp_delay_array = np.zeros(len(route))

    delay_total = 0
    first_delay_added = False
    tmp_i = 0
    for i in range(0, len(route) - 1):
        airline = route[i]
        if (not first_delay_added) and airline.delay_time > 0:
            tmp_delay_array[i] = airline.delay_time
            tmp_i = i
            break

    route_arr = route
    for j in range(tmp_i + 1, len(route_arr)):
        wait_time = route_arr[j].depart_time_stamp - (
            route_arr[j - 1].arrive_time_stamp + route_arr[j - 1].delay_time)
        if wait_time < minimum_idle_time():
            tmp_delay = minimum_idle_time() - wait_time
            tmp_delay_array[j] += tmp_delay
    for tmp in tmp_delay_array:
        delay_total += tmp
    return delay_total, tmp_delay_array


def try_swap_routes(RouteA, RouteB, A_airline, B_airline):
    "Route A and RouteB try to swap their planes after A_airline and B_airline respectively, and return the delay caused by swap."
    origin_routeA_delay = 0
    origin_routeB_delay = 0
    for route in RouteA:
        origin_routeA_delay += route.delay_time

    for route in RouteB:
        origin_routeB_delay += route.delay_time

    newA = []
    newB = []
    indexA = 0
    indexB = 0
    for i in range(0, len(RouteA)):
        if RouteA[i] == A_airline:
            indexA = i
            break
    for i in range(0, len(RouteB)):
        if RouteB[i] == B_airline:
            indexB = i
            break

    # the next 2 for cycle construct the new Route A.
    for i in range(0, len(RouteA)):
        if i <= indexA:
            newA.append(RouteA[i])
    for i in range(0, len(RouteB)):
        if i > indexB:
            newA.append(RouteB[i])
    # the next 2 for cycle construct the new Route B.
    for i in range(0, len(RouteB)):
        if i <= indexB:
            newB.append(RouteB[i])
    for i in range(0, len(RouteA)):
        if i > indexA:
            newB.append(RouteA[i])
    # now we need to calculate the delays for new route A and route B respectively.
    newA_delay_total, delay_array_A = calculate_delay_for_route_without_considering_the_later_on_delays(newA)
    newB_delay_total, delay_array_B = calculate_delay_for_route_without_considering_the_later_on_delays(newB)
    if newA_delay_total + newB_delay_total < origin_routeA_delay + origin_routeB_delay:
        print('swap happened!')
        newA[0].display()
        newB[0].display()
        for i in range(0, len(newA)):
            airline = newA[i]
            airline.plane_tail_number = newA[0].plane_tail_number
            airline.delay_time = delay_array_A[i]
        for i in range(0, len(newB)):
            airline = newB[i]
            airline.plane_tail_number = newB[0].plane_tail_number
            airline.delay_time = delay_array_B[i]
    return newA, newB


if __name__ == '__main__':
    print('init')
    schedule = reader.read_from_schedule()
    air_crafts = reader.read_from_aircraft()
    print(time.asctime(time.gmtime(1461302220)))
    start_time = 1461302220
    end_time = 1461302220 + 48 * 60 * 60
    print('question 02')
    # Route_Set = []  # set of class Route.
    Map = {}  # key - value pairs of tail_num to its whole route.
    for air_craft in air_crafts:
        tail_num = air_craft.tail_number
        for single_schedule in schedule:
            if single_schedule.plane_tail_number == tail_num:
                if not Map.__contains__(tail_num):
                    Map[tail_num] = []
                Map.get(tail_num).append(single_schedule)

    # step 1 . 找到首延误航班集合。
    first_delay_airline_set = []  # this is the set of airlines that are affected by the closure of OVS
    for route in Map.values():  # here route is array off airlines, that form a series of tour.
        for airline in route:
            if need_delay(airline):
                first_delay_airline_set.append(airline)
                break

    # Step 2. 计算在各自的route中，因首延误航班导致后续延误 所产生的所有后续延误集合。
    # now we have array first_delay_airline_set full of first delayed airlines
    total_delay = 0  # the delays for all the airlines affected by OVS and their later airlines.
    tail_num_2_total_delayed_airlines_count = {}  # all the planes that have more than one .
    for first_delayed_airline in first_delay_airline_set:
        tail_num = first_delayed_airline.plane_tail_number
        route_arr = Map.get(tail_num)
        for i in range(0, len(route_arr)):
            if route_arr[i] == first_delayed_airline:
                break
        total_delay += delay_airline(first_delayed_airline)  # first add the delay of first airline.
        for j in range(i + 1, len(route_arr)):
            wait_time = route_arr[j].depart_time_stamp - (
                route_arr[j - 1].arrive_time_stamp + route_arr[j - 1].delay_time)
            if wait_time < minimum_idle_time():
                tmp_delay = minimum_idle_time() - wait_time
                route_arr[j].delay_time += tmp_delay
                total_delay += tmp_delay
                arr = tail_num_2_total_delayed_airlines_count.get(
                    tail_num, [])
                arr.append(route_arr[j])
                tail_num_2_total_delayed_airlines_count[tail_num] = arr

    # Step 3,现在对于每一个受到连带影响的航班，对于所有其他飞机，寻求替代可能性。
    for arr in tail_num_2_total_delayed_airlines_count.values():
        second_affected_airline = arr[0]
        tail_num = second_affected_airline.plane_tail_number
        for airline in first_delay_airline_set:
            if airline.plane_tail_number == tail_num:
                land_time = airline.arrive_time_stamp + airline.delay_time
                land_port = airline.arrive_airport
                # now we need to find the other aircrafts at land_port at land_time, that is free to fly.
                for key_tail_num in Map.keys():
                    if not tail_num == key_tail_num:
                        route_arr = Map.get(key_tail_num)
                        for route_arr_airline in route_arr:
                            if route_arr_airline.arrive_airport == land_port and route_arr_airline.arrive_time_stamp < land_time:
                                try_swap_routes(arr, route_arr, airline, route_arr_airline)
                                break
                break
    import excel_writer as writer_tool
    writer_tool.write_schedule(schedule, 'solution2.xls')
    print('task success.')

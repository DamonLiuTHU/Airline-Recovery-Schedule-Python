#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
import xlrd
import numpy as np
import Solution1.Airline as airline
import Solution1.Aircraft as aircraft
import os, sys
retval = os.getcwd()
os.chdir( retval )
print('current dir : '+retval)
file_path = 'Schedules.xlsx'


def read_from_schedule(path='Schedules.xlsx'):
    xlrd.Book.encoding = 'utf-8'
    raw_data = xlrd.open_workbook(path)
    table = raw_data.sheets()[0]
    number_of_rows = table.nrows
    data = []
    for line_number in range(1, number_of_rows):
        row_data = table.row_values(line_number)
        i = -1;
        air = airline.Airline(airline_number=row_data[i + 1], depart_time_stamp=row_data[i + 2],
                              arrive_time_stamp=row_data[i + 3], depart_airport=row_data[i + 4],
                              arrive_airport=row_data[i + 5], plane_type=row_data[i + 6],
                              plane_tail_number=row_data[i + 7])
        data.append(air)
        # air.display()
    # print('total row count : ', number_of_rows)
    return data


def read_from_schedule_for_planetype_9(path='Schedules.xlsx'):
    xlrd.Book.encoding = 'utf-8'
    raw_data = xlrd.open_workbook(path)
    table = raw_data.sheets()[0]
    number_of_rows = table.nrows
    data = []
    for line_number in range(1, number_of_rows):
        row_data = table.row_values(line_number)
        i = -1;
        air = airline.Airline(airline_number=row_data[i + 1], depart_time_stamp=row_data[i + 2],
                              arrive_time_stamp=row_data[i + 3], depart_airport=row_data[i + 4],
                              arrive_airport=row_data[i + 5], plane_type=row_data[i + 6],
                              plane_tail_number=row_data[i + 7])
        if air.plane_type == '9':
            data.append(air)
            # air.display()
    # print('total row count : ', number_of_rows)
    return data


def read_from_aircraft(path='Aircrafts.xlsx'):
    xlrd.Book.encoding = 'utf-8'
    raw_data = xlrd.open_workbook(path)
    table = raw_data.sheets()[0]
    number_of_rows = table.nrows
    data = []
    for line_number in range(1, number_of_rows):
        row_data = table.row_values(line_number)
        i = -0;
        air = aircraft.Aircraft(tail_number=row_data[0], type_number=row_data[1],
                                earliest_available_time_stamp=row_data[2], latest_available_time_stamp=row_data[3],
                                departure_port=row_data[4], seat_count=row_data[5])
        air.earliest_available_time = row_data[7]
        air.latest_available_time = row_data[8]
        data.append(air)
        # air.display()
    # print('total row count : ', number_of_rows)
    return data

# tmp = read_from_schedule()
# tmp = read_from_aircraft()

import xlwt


def write_schedule(schedule_set):
    path = './new_schedule.xls'
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1')
    line = 0
    for schedule in schedule_set:
        write_single_schedule(schedule, sheet1, line)
        line += 1
    book.save(path)


def write_schedule(schedule_set, filename='new.xls'):
    path = './' + filename
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1')
    line = 0
    for schedule in schedule_set:
        write_single_schedule(schedule, sheet1, line)
        line += 1
    book.save(path)


def write_single_schedule(schedule, sheet, line):
    sheet.write(line, 0, schedule.airline_number)
    sheet.write(line, 1, schedule.depart_time_stamp + schedule.delay_time)
    sheet.write(line, 2, schedule.arrive_time_stamp + schedule.delay_time)
    sheet.write(line, 3, schedule.depart_airport)
    sheet.write(line, 4, schedule.arrive_airport)
    sheet.write(line, 5, schedule.plane_type)
    sheet.write(line, 6, schedule.plane_tail_number)
    return

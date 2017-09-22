import excel_reader, excel_writer


def check_aircraft_model(filepath,newfilename):
    data = excel_reader.read_from_schedule(filepath)
    aircraft_data = excel_reader.read_from_aircraft('./data/Aircrafts.xlsx')
    for line in data:
        for aircraft in aircraft_data:
            if line.plane_tail_number == aircraft.tail_number and line.plane_type != aircraft.type_number:
                line.plane_type = aircraft.type_number
                print('error detected.')
    excel_writer.write_schedule(data, newfilename)



check_aircraft_model('./Solution1/solution1.xls',newfilename = 'solution1.xls')
check_aircraft_model('./Solution2/solution2.xls',newfilename = 'solution2.xls')
check_aircraft_model('./Solution3/solution3.xls',newfilename = 'solution3.xls')
check_aircraft_model('./Solution4/solution4.xls',newfilename = 'solution4.xls')

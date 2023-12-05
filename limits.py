import pandas as pd




def get_limits(aircraft, airport, temp):
    aircraft_limits = dict()

    file = aircraft + '.xlsx'
    sheet = airport
    data = pd.read_excel(file, sheet)
    limits = data[['TEMP', temp]]
    vals = data[[temp]]

    aircraft_limits['WAT'] = vals[temp][0]
    aircraft_limits['TODA'] = vals[temp][1]
    aircraft_limits['ASDA'] = vals[temp][2]

    sorted_limits = sorted(aircraft_limits.items(), key=lambda item: item[1])
    print('Limits:', '\t',dict(sorted_limits))
    limit = sorted_limits[0]
    print(f"RTOW: \t\t {limit[1]} ({limit[0]})")

    return limit[1]


##limit = get_limits('SLD', 'WIL', 20)
##print(limit)
import pandas as pd
from flask import abort


def get_limits(aircraft, airport, temp):
    """returns the aircraft performance limited weight"""
    aircraft_limits = dict()

    file = aircraft + '.xlsx'
    sheet = airport
    try:
        data = pd.read_excel(file, sheet)
        vals = data[temp]
    except ValueError:
        abort(401, 'Unable to Calculate. Please confirm airfield and temperature inputs')

    aircraft_limits['WAT'] = vals[0]
    aircraft_limits['TODA'] = vals[1]
    aircraft_limits['ASDA'] = vals[2]

    sorted_limits = sorted(aircraft_limits.items(), key=lambda item: item[1])
   
    limit = sorted_limits[0]
    

    return limit


def get_loads(aircraft, empty_wt, fuel, bgg, bgg_wt, children, RTOW, TOW):
    """returns the maximum payload as per the performance limitation and operational conditions"""
    
    adults = 0

    if bgg == 'Fixed':
        while TOW <= RTOW:
            adults += 1
            TOW += 185
        else:
            adults -= 1
            TOW -= 185
    elif bgg == 'Standard':
        while TOW <= RTOW:
            adults += 1
            TOW += 216
            bgg_wt += 31
        else:
            adults -= 1
            TOW -= 216
            bgg_wt -= 31


    TOB = adults + children
    underload = RTOW - TOW


    if aircraft == 'SLK':
        if TOB > 52:
            adults = 52 - children
            TOB = 52
            if bgg == 'Standard':
                bgg_wt = 52 * 31
                TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
                underload = RTOW - TOW
            else:
                TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
                underload = RTOW - TOW

    elif aircraft == "SLC":
        if TOB > 50:
            adults = 50 - children
            TOB = 50
            if bgg == 'Standard':
                bgg_wt = 50 * 31
                TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
                underload = RTOW - TOW
            else:
                TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
                underload = RTOW - TOW

    else:
        if TOB > 37:
            adults = 37 - children
            TOB = 37
            if bgg == 'Standard':
                bgg_wt = 37 * 31
                TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
                underload = RTOW - TOW
            else:
                TOW = empty_wt + fuel + adults*185 + children*75 + bgg_wt - 50
                underload = RTOW - TOW

    return [adults, bgg_wt, TOW, underload]
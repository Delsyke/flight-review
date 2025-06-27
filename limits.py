import pandas as pd
from flask import abort


MALW = {
"SLC":42000,
"SLO":34500,
"SLK":42000,
"SLD":33900
}

def get_limits(aircraft, airport, temp):
    """returns the aircraft performance limited weight"""
    aircraft_limits = dict()

    file = aircraft + '.xlsx'
    sheet = airport
    try:
        data = pd.read_excel(file, sheet)
        vals = data[temp]
    except ValueError:
        msg = """
        Unable to calculate. Please confirm airfield input and temperatures
        """
        abort(404, 'Unable to Calculate. Please confirm airfield and temperature inputs')

    aircraft_limits['WAT'] = vals[0]
    aircraft_limits['TODA'] = vals[1]
    aircraft_limits['ASDA'] = vals[2]
    # aircraft_limits['MLW'] = MALW[aircraft]

    sorted_limits = sorted(aircraft_limits.items(), key=lambda item: item[1])
   
    limit = sorted_limits[0]
    
    return limit


def get_loads(aircraft, empty_wt, fuel, trip, bgg, bgg_wt, children, RTOW, TOW):
    """returns the maximum payload as per the performance limitation and operational conditions"""
    
    adults = 0
    MLW = MALW[aircraft]
    lw_limit = False

    if bgg == 'Fixed':
        while TOW <= RTOW:
            adults += 1
            TOW += 185  
        else:
            adults -= 1
            TOW -= 185

        LW = TOW - trip
        if LW > MLW:
            lw_limit = True
            while LW > MLW:
                adults -= 1
                TOW -= 185
                LW -= 185
    
    elif bgg == 'Standard':
        while TOW <= RTOW:
            adults += 1
            TOW += 216
            bgg_wt += 31
        else:
            adults -= 1
            TOW -= 216
            bgg_wt -= 31

        LW = TOW - trip
        if LW > MLW:
            lw_limit = True
            while LW > MLW:
                adults -= 1
                TOW -= 216
                LW -= 216
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

    return [adults, bgg_wt, TOW, LW, underload, lw_limit, MLW]
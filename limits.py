import pandas as pd
from flask import abort

MALW = {
    "SLC": 42000,
    "SLO": 34500,
    "SLK": 42000,
    "SLD": 33900
}

MZFWs = {
    "SLC": 39500,
    "SLK": 39500,
    "SLD": 32000,
    "SLO": 32000
}

ADULT_WEIGHT = 185
CHILD_WEIGHT = 75
BAGGAGE_UNIT_WEIGHT = 31
TAXI_FUEL = 50


def get_limits(aircraft, airport, temp):
    """Returns the aircraft performance-limited weight."""
    try:
        data = pd.read_excel(f'{aircraft}.xlsx', sheet_name=airport)
        vals = data[temp]
    except ValueError:
        abort(404, 'Unable to Calculate. Please confirm airfield and temperature inputs')
    
    takeoff_limits = {
        'WAT': vals[0],
        'TODA': vals[1],
        'ASDA': vals[2]
    }
    
    # Return the lowest performance limit
    return min(takeoff_limits.items(), key=lambda item: item[1])


def calculate_baggage_and_weights(adults, children, bgg_type, bgg_wt):
    if bgg_type == 'Standard':
        bgg_wt = (adults + children) * BAGGAGE_UNIT_WEIGHT
    return bgg_wt


def limit_passengers(aircraft, adults, children, bgg, empty_wt, fuel, bgg_wt):
    max_seats = {'SLK': 52, 'SLC': 50}.get(aircraft, 37)
    TOB = adults + children
    if TOB > max_seats:
        adults = max_seats - children
        TOB = max_seats

    bgg_wt = calculate_baggage_and_weights(adults, children, bgg, bgg_wt)
    TOW = empty_wt + fuel + adults * ADULT_WEIGHT + children * CHILD_WEIGHT + bgg_wt - TAXI_FUEL
    return adults, bgg_wt, TOW, TOB


def get_loads(aircraft, empty_wt, fuel, trip, bgg, bgg_wt, children, RTOW, TOW):
    """Returns max payload under performance/operational limits."""
    adults = 0
    MLW = MALW[aircraft]
    lw_limit = False
    MZFW = MZFWs[aircraft]
    zfw_limit = False
    incr = ADULT_WEIGHT + (BAGGAGE_UNIT_WEIGHT if bgg == 'Standard' else 0)


    # Increment until hitting RTOW
    while TOW + incr <= RTOW:
        adults += 1
        TOW += incr
        if bgg == 'Standard':
            bgg_wt += BAGGAGE_UNIT_WEIGHT

    LW = TOW - trip
    ZFW = TOW - fuel

    # Adjust if landing weight exceeds MLW or ZFW exceeds MZFW
    while LW > MLW or ZFW > MZFW:
        decr = ADULT_WEIGHT + (BAGGAGE_UNIT_WEIGHT if bgg == 'Standard' else 0)
        adults -= 1
        TOW -= decr
        LW -= decr
        ZFW -= decr
        if bgg == 'Standard':
            bgg_wt -= BAGGAGE_UNIT_WEIGHT


    TOB = adults + children
    underloads = {
        'takeoff': RTOW - TOW,
        'landing': MLW - LW,
        'zfw': MZFW - ZFW
    }

    underload = min(underloads.values())
    lw_limit = underload == underloads['landing']
    zfw_limit = underload == underloads['zfw']

    # Apply seat limits and recalculate
    adults, bgg_wt, TOW, TOB = limit_passengers(aircraft, adults, children, bgg, empty_wt, fuel, bgg_wt)
    underload = RTOW - TOW

    return [adults, bgg_wt, TOW, LW, underload, lw_limit, MLW, zfw_limit, MZFW, ZFW]

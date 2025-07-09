from flask import Flask, render_template, request
from limits import get_limits, get_loads

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Constants
OW = {
    "SLC": 27691,
    "SLO": 24207,
    "SLK": 28110,
    "SLD": 23633
}

CHILD_WEIGHT = 75
BAGGAGE_UNIT_WEIGHT = 31
TAXI_FUEL = 50  # Fuel burned during taxi


@app.get('/')
def home():
    return render_template('index.html')


@app.post('/')
def review():
    # Extract and clean form data
    aircraft = request.form['aircraft'].upper()
    airfield = request.form['airfield'].upper()
    temp = int(request.form['temp'])
    fuel = int(request.form['fuel'])
    trip = int(request.form['trip'])
    children = int(request.form['children'])

    bgg = request.form['bgg']
    which_bgg = request.form['which-bgg']

    # Calculate baggage weight
    if bgg == 'Standard':
        bgg_wt = children * BAGGAGE_UNIT_WEIGHT
    elif bgg == 'Fixed':
        bgg_wt = int(which_bgg)
    else:
        bgg_wt = 0  # fallback just in case

    # Lookup performance limits
    limits = get_limits(aircraft, airfield, temp)
    limited_by = limits[0]
    RTOW = limits[1]

    # Calculate initial weights
    empty_wt = OW[aircraft]
    TOW = empty_wt + fuel + (children * CHILD_WEIGHT) + bgg_wt - TAXI_FUEL

    # Get load plan
    loads = get_loads(aircraft, empty_wt, fuel, trip, bgg, bgg_wt, children, RTOW, TOW)
    adults, bgg_wt, TOW, LW, underload, lw_limit, MLW, zfw_limit, MZFW, ZFW = loads

    # Adjust limitation logic
    if lw_limit:
        limited_by = 'LW'
        RTOW = MLW + trip
        underload = RTOW - TOW
    elif zfw_limit:
        limited_by = 'ZFW'
        RTOW = MZFW + fuel - TAXI_FUEL
        underload = RTOW - TOW

    # Render output
    return render_template('loads.html',
        aircraft=aircraft,
        airfield=airfield,
        temp=temp,
        rtow=RTOW,
        fuel=fuel,
        trip=trip,
        zfw=ZFW,
        limited_by=limited_by,
        children=children,
        adults=adults,
        bgg_wt=bgg_wt,
        tow=TOW,
        lw=LW,
        landing_fuel=fuel - trip - TAXI_FUEL,
        underload=underload
    )


if __name__ == '__main__':
    app.run(debug=True)

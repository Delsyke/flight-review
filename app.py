from flask import Flask, render_template, request
from limits import get_limits, get_loads


OW = {
"SLC":27691,
"SLO":24207,
"SLK":28110,
"SLD":23633
}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'



@app.get('/')
def home():
	return render_template('index.html')


@app.post('/')
def review():

	# for k,v in request.form.items():
	# 	print(k, v)

	aircraft = request.form['aircraft'].upper()
	airfield = request.form['airfield'].upper()
	temp = int(request.form['temp'])
	fuel = int(request.form['fuel'])
	children = int(request.form['children'])

	bgg = request.form['bgg']
	which_bgg = request.form['which-bgg']


	if bgg == 'Standard':
		bgg_wt = children * 31
	if bgg == 'Fixed':
		bgg_wt = int(which_bgg)

	limits = get_limits(aircraft, airfield, temp)
	RTOW = limits[1]
	limited_by = limits[0]
	empty_wt = OW[aircraft]
	TOW = empty_wt + fuel + children*75 + bgg_wt - 50
	loads = get_loads(aircraft, empty_wt, fuel, bgg, bgg_wt, children, RTOW, TOW)

	return render_template('loads.html',
		aircraft = aircraft,
		airfield = airfield,
		temp = temp,
		rtow = RTOW,
		fuel=fuel,
		limited_by = limited_by,
		children = children,
		adults = loads[0],
		bgg_wt = loads[1],
		tow = loads[2],
		underload = loads[3]
	)




















if __name__ == '__main__':
	app.run(debug=True)

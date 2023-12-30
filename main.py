from flask import Flask, render_template, request
from forms import Dataform
from limits import get_limits, get_loads


OW = {
"SLC":27691,
"SLO":24207,
"SLK":28252,
"SLD":23633
}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'



@app.get('/')
def home():
	form = Dataform()
	return render_template('index.html', form=form)


@app.post('/')
def review():

	# for k,v in request.form.items():
	# 	print(k, v)

	bgg = request.form['bgg']
	which_bgg = request.form['which-bgg']

	form = Dataform()

	if form.validate_on_submit():
		aircraft = form.aircraft.data.upper()
		airfield = form.airfield.data.upper()
		temp = form.temp.data
		fuel = form.fuel.data
		children = form.children.data

	if bgg == 'Standard':
		bgg_wt = children * 31
	elif bgg == 'Fixed':
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
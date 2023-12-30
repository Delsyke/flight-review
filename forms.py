from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SelectMultipleField
from wtforms.validators import InputRequired, Length, NumberRange


class Dataform(FlaskForm):
	aircraft = RadioField('Aircraft', choices=['SLD', 'SLO', 'SLC', 'SLK'], validators=[InputRequired()])
	airfield = StringField('Airfield', validators=([InputRequired()]))
	temp = IntegerField('Temperature', validators=([InputRequired(), NumberRange(min=14, max=32)]))
	fuel = IntegerField('Fuel', validators=[InputRequired()])
	children = IntegerField('Children', validators=([InputRequired()]))



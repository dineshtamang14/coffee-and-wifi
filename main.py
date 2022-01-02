from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import pyshorteners

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

coffee = ("✖", "☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕")
wifi = ("✖", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪")
socket_rating = ("✖", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()],)
    location = StringField('Cafe Location on Google Maps(URL)', validators=[DataRequired(), URL(message="put a validate url")])
    opening_time = StringField('Opening Time eg.8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time eg.5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=coffee)
    wifi_rating = SelectField('Wifi Strength Rating', choices=wifi)
    power_socket = SelectField('Power Socket Availability', choices=socket_rating)
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_name = form.cafe.data
        shortener = pyshorteners.Shortener()
        location = shortener.tinyurl.short(form.location.data)
        opening_time = form.opening_time.data
        closing_time = form.closing_time.data
        coffee_rating = form.coffee_rating.data
        wifi_rating = form.wifi_rating.data
        socket_rating = form.power_socket.data
        with open("cafe-data.csv", "a+", encoding="utf8") as csv_file:
            csv_file.write(f"\n{cafe_name}, {location}, {opening_time}, "
                           f"{closing_time}, {coffee_rating}, {wifi_rating}, {socket_rating}")

            return redirect(url_for("add_cafe"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        csv_data = iter(data)
        next(csv_data)
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)

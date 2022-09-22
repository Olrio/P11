import json, datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

for competition in competitions:
    for club in clubs:
        competition[club['name']] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        flash(f"Sorry, email {request.form['email']} "
              f"is not associated with a club. Please enter a valid email")
        return render_template('index.html'), 401


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if datetime.datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S") < datetime.datetime.now():
        flash(f"Sorry, the competition {foundCompetition['name']} is finished. You can't buy places anymore")
        return render_template('welcome.html', club=foundClub, competitions=competitions), 403
    if foundClub and foundCompetition:
        return render_template('booking.html',
                               club=foundClub,
                               competition=foundCompetition,
                               )
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=foundClub, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > (12 - competition[club['name']]):
        flash(f"Sorry, your total number of places can't exceed 12.")
        return render_template('welcome.html', club=club, competitions=competitions), 403
    if placesRequired > int(club['points']):
        flash(f"Sorry, you just have {club['points']} points."
              f"You can't buy {placesRequired} places.")
        return render_template('welcome.html', club=club, competitions=competitions), 403
    club['points'] = int(club['points']) - placesRequired
    competition[club['name']] += placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from flaskFile.models import UserRide
from flaskFile import db
from flaskFile.ride.forms import Ride
from sqlalchemy import func

ride = Blueprint('ride', __name__)

@ride.route("/find-ride", methods=['GET', 'POST'])
@login_required
def findRide():
    form = Ride()
    if form.validate_on_submit():
        try: 
            ride = UserRide(source=form.source.data, destination=form.destination.data, dateOfRide=form.date.data, preference=form.preference.data, userId=current_user.id)
            db.session.add(ride)
            db.session.commit()
            rideId = ride.id
        except:
            return redirect(url_for('general.errorHandler'))
        return redirect(url_for('ride.result', rideId=rideId))
    return render_template('ride/find-ride.html', title='Find-Ride', form=form)

@ride.route("/update-rides/<int:rideId>", methods=['GET', 'POST']) 
def updateRide(rideId):
    ride = UserRide.query.get(rideId)
    form = Ride()
    if form.validate_on_submit() and request.method == 'POST':
        ride.destination = form.destination.data or ride.destination
        ride.source = form.source.data or ride.source
        ride.dateOfRide = form.date.data or ride.dateOfRide
        ride.preference = form.preference.data or ride.preference
        db.session.commit()
        return redirect(url_for('ride.result', rideId=ride.id))
    elif request.method == 'GET':
        form.destination.data = ride.destination
        form.source.data = ride.source
        form.date.data = ride.dateOfRide
        form.preference.data = ride.preference
    return render_template("ride/update-ride.html", title="Update Ride", form=form, rideId=rideId)

@ride.route("/delete-ride/<int:rideId>", methods=['POST', 'GET'])
@login_required
def deleteRide(rideId):
    ride = UserRide.query.get(rideId)
    if request.method == 'POST':
        if current_user == ride.rider:
            db.session.delete(ride)
            db.session.commit()
            flash("Delete successfully", "warning")
            return redirect(url_for("ride.allRides"))
        else:
            flash("Delele fail due to linvalid user")
            return redirect(url_for("ride.allRides"))
    else:
        return "SHIT"

@ride.route("/all-rides")
@login_required
def allRides():
    pageNum = request.args.get('page', 1, type = int)
    rides = UserRide.query.filter(UserRide.rider == current_user)\
    .order_by(UserRide.dateOfRide.desc())\
    .paginate(per_page = 4, page = pageNum)
    return render_template("ride/your-rides.html", title="My Rides", rides=rides, curPage = pageNum)

@ride.route("/result/<int:rideId>")
@login_required
def result(rideId):
    try:
        pageNum = request.args.get('page', 1, type = int)
        myRide = UserRide.query.filter(UserRide.id == rideId).first()
        avalRide = UserRide.query.filter(UserRide.rider != myRide.rider)\
            .filter(func.lower(UserRide.destination) == func.lower(myRide.destination))\
            .filter(func.lower(UserRide.source) == func.lower(myRide.source))\
            .filter(UserRide.dateOfRide == myRide.dateOfRide)
        avalRide = avalRide.paginate(per_page = 4, page = pageNum)
    except:
        return redirect(url_for('general.errorHandler'))
    return render_template('ride/result.html', title="Result", avalRide = avalRide, rideId=myRide.id, curPage = pageNum)


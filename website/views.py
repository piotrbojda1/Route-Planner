from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from website import db
from website.location import get_location_origin, get_location_destination
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        current_location = request.form['current_location']
        destination = request.form['destination']
        departAt = request.form['departure_date']
        departAt = datetime.datetime.utcnow().isoformat() + 'Z'
        
        # Get the avoid parameters
        avoidType = request.form.getlist('avoid[]')

        # Get the origin and destination coordinates
        origin = get_location_origin(current_location)
        dest = get_location_destination(destination)

        # Create a list to store the routes
        routePlanningLocations = f"{origin[0]},{origin[1]}:{dest[0]},{dest[1]}"
        
        # URL parameters

        API_Key = os.getenv('API_KEY')
        traffic = "true"
        routeRepresentation = "polyline"
        language = "en-GB"
        baseURL = "api.tomtom.com"
        versionNumber = 1
        contentType = "/json"
        routeType = "fastest"
        trafficTypes = "all"
        sectionType = "traffic&sectionType=carTrain&sectionType=travelMode&sectionType=country"
        travelMode = "car"
        report_ = "effectiveSettings"

        url = f"https://{baseURL}/routing/{versionNumber}/calculateRoute/{routePlanningLocations}/{contentType}?key={API_Key}&language={language}&routeRepresentation={routeRepresentation}&computeTravelTimeFor={trafficTypes}&sectionType={sectionType}&report={report_}&departAt={departAt}&routeType={routeType}&traffic={traffic}&travelMode={travelMode}"
        
        # Add the avoid parameters
        avoidParams = "&".join([f"avoid={avoid}" for avoid in avoidType])

        # Add the avoid parameters to the URL
        url += "&" + avoidParams

        # Call the TomTom API and get the response
        response = requests.get(url)
        data = response.json()

        # Get the length and travel time of the route
        for route in data['routes']:
            length_route = route['summary']['lengthInMeters']
            if length_route > 0:
                length_route = float(length_route / 1000)
            travel_time = route['summary']['travelTimeInSeconds']
            if travel_time > 0:
                travel_time = float(travel_time / 3600)

        # Create a empty list to store the routes
            routes = []

         # Append the route to the routes list
            routes.append({
                'origin': current_location,
                'destination': destination,
                'length_route': '{:.2f}'.format(length_route),
                'travel_time': '{:.2f}'.format(travel_time),
                'avoid': avoidType,
            })

        # Redirect to the home page
        return redirect(url_for('views.home'))
    else:
        # Render the home page
        return render_template("home.html", user=current_user)
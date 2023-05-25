from flask import Blueprint, render_template, redirect, request, flash, url_for, session
from flask_login import login_required, current_user
from website import db
from .location import get_location_origin, get_location_destination
from .models import Route
import folium
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

POINTS = None

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
        session['data'] = response.json()
        data = session.get('data')

         # Get the avoid from the response
        for avoid_data in data['report']['effectiveSettings']:
            if avoid_data['key'] == 'avoid':
                avoidType = avoid_data['value']
                break

        # Get the length and travel time of the route
        for route in data['routes']:
            length_route_meters = route['summary']['lengthInMeters']
            if length_route_meters > 0:
                length_route_km, length_route_m = divmod(length_route_meters, 1000)
                length_route_km = int(length_route_km)
                length_route_m = int(length_route_m)

            travel_time_seconds = route['summary']['travelTimeInSeconds']
            if travel_time_seconds > 0:
                travel_time_hours, travel_time_minutes = divmod(travel_time_seconds, 3600)
                travel_time_hours = int(travel_time_hours)
                travel_time_minutes = int(travel_time_minutes / 60)

        # Create a empty list to store the routes
            routes = []

         # Append the route to the routes list
            routes.append({
            'origin': current_location,
            'destination': destination,
            'length_route_km': length_route_km,
            'length_route_m': length_route_m,
            'travel_time_hours': travel_time_hours,
            'travel_time_minutes': travel_time_minutes,
            'avoid': avoidType,
        })

        # Create a new route
        for route in routes:
            new_route = Route(
            origin=route['origin'],
            destination=route['destination'],
            length_route=f"{route['length_route_km']} km {route['length_route_m']} m",
            travel_time=f"{route['travel_time_hours']} h {route['travel_time_minutes']} min",
            user_id=current_user.id,
            avoid=route['avoid']
                            )
        
        points = []
        for route in data['routes']:
            for leg in route['legs']:
                for point in leg['points']:
                    points.append(point)

        global POINTS
        POINTS = points

        # Save the route to the database
        db.session.add(new_route)
        db.session.commit()

        session['new_route_created'] = True

        # Flash a message
        flash('Route created!', category='success')

        # Redirect to the home page
        return redirect(url_for('views.details'))
    else:
        # Get all the routes
        routes = Route.query.filter_by(user_id=current_user.id).all()
        # Render the home page
        return render_template("home.html", user=current_user, routes=routes)

@views.route('/result')
@login_required
def details():
    # Get the points data from the session
    global POINTS
    points = POINTS
    print(points)
    # Create a map
    map = folium.Map(location=[points[0]["latitude"], points[0]["longitude"]], zoom_start=12)

    # Start point marker
    folium.Marker([points[0]["latitude"], points[0]["longitude"]], popup='<i>Start</i>', color='green', fill_color='green').add_to(map)
    # End point marker
    folium.Marker([points[-1]["latitude"], points[-1]["longitude"]], popup='<i>End</i>', color='red', fill_color='red').add_to(map)
    # Draw the route
    folium.PolyLine(locations=[[p["latitude"], p["longitude"]] for p in points], color="blue", weight=2.5, opacity=1).add_to(map)

    # Save the map to a file
    map.save('website/static/maps/map.html')

    # Get the latest route from the database
    routes = Route.query.order_by(Route.id.desc()).first()

    return render_template("result.html", user=current_user, routes=[routes], map_path='maps/map.html')

@views.route('/history')    
@login_required
def routes_history():
    # Get all the routes
    routes = Route.query.filter_by(user_id=current_user.id).all()
    return render_template("history.html", user=current_user, routes=routes)
#!/usr/bin/python3
# -∗- coding: utf-8 -∗-

from flask import Flask, render_template, url_for,request
import folium
import random
app = Flask(__name__)   # Initialise l'application Flask

start_coords = (48.9419981883, 2.61700200964)
folium_map = folium.Map(location=start_coords, zoom_start=1)


@app.route('/',methods=['GET','POST']) 
def accueil():
    try: 
        year = request.form['annee']
    except Exception as e:
        print(e)
        year=' '
    coords = [random.randint(-180,180),random.randint(-84,84)]
    folium.Marker(coords, popup = str(coords)).add_to(folium_map)
    return render_template("accueil.html",map=folium_map._repr_html_(),texte=str(year),annees = list(range(2010,2020,1)), commune = ['Grenoble','Paris'])


if __name__ == '__main__' :
    app.run(debug=True)
    

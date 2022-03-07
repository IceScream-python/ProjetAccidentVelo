#!/usr/bin/python3
# -∗- coding: utf-8 -∗-

from flask import Flask, render_template, url_for
import folium
app = Flask(__name__)   # Initialise l'application Flask

@app.route('/') 
def accueil():
    return render_template("accueil.html")

@app.route('/map')
def map():
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    return folium_map._repr_html_()
 
if __name__ == '__main__' :
    app.run(debug=True)

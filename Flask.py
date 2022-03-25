#!/usr/bin/python3
# -∗- coding: utf-8 -∗-

from flask import Flask, render_template, url_for,request
import folium
#import random
import sqlite3
from requetes import Requetes

app = Flask(__name__)   # Initialise l'application Flask

liste_requete=dict()
start_coords = (48.9419981883, 2.61700200964)
folium_map = folium.Map(location=start_coords, zoom_start=6)

@app.route('/',methods=['GET','POST']) 
def accueil():
    for i in ['annee','departement','gravite']:
        try:
            liste_requete[i] = request.form[str(i)]
        except Exception as e:
            liste_requete[i]=' '
    #coords = [random.randint(-180,180),random.randint(-84,84)]
    #folium.Marker(coords, popup = str(coords)).add_to(folium_map)
    print(liste_requete)

    departements = Requetes.renvoyer_liste('Nom_dep','DEPARTEMENT')
    gravites = Requetes.renvoyer_liste('graviteaccident','ACCIDENTS_VELOS')
    annees = list(range(2008,2020,1))
    #return render_template("accueil.html",map=folium_map._repr_html_(),texte=str(year),annees =  Requetes.renvoyer_liste('annee','ACCIDENTS_VELOS'), communes = Requetes.renvoyer_liste('Nom_dep','DEPARTEMENT') )
    return render_template("accueil.html",map=folium_map._repr_html_(),annees =  annees,departements = departements, gravites = gravites )


@app.route('/stats',methods=['GET','POST'])
def stats():
    return render_template('stats.html')
if __name__ == '__main__' :
    app.run(debug=True)


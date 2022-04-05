# -∗- coding: utf-8 -∗-

from tkinter import Variable
from turtle import width
from flask import Flask, render_template, url_for,request
import folium
import folium.plugins
import sqlite3
from requetes import Requetes

app = Flask(__name__)   # Initialise l'application Flask

liste_requete=dict()
start_coords = (48.9419981883, 2.61700200964) #coordonées de Paris
#folium_map = folium.Map(width=1680, height=750, location=start_coords, zoom_start=6) #Initialise une map folium
markercluster = folium.plugins.FastMarkerCluster

@app.route('/',methods=['GET','POST']) 
def accueil():
    folium_map = folium.Map(width=1680, height=750, location=start_coords, zoom_start=6) #Initialise une map folium
    for i in ['annee','departement','gravite']:
        try:            
            liste_requete[i] =  request.form[str(i)]
        except Exception as e:
            liste_requete[i]= None
    try:
        coordonees = Requetes.liste_affichage(liste_requete)
        print(coordonees)
        folium.plugins.MarkerCluster(coordonees).add_to(folium_map)

    except Exception as e:
       print(e)

    
    print(liste_requete)

    departements =  ['Tout']+ Requetes.renvoyer_liste('nom_dep')
    gravites = ['Tout', 'Indemne','Blessé Léger', 'Blessé Hospitalisé','Tué']
    annees =  ['Tout']+ Requetes.renvoyer_liste('annee')

    #annees = list(range(2010,2020)) test avant d'avoir le sql
    return render_template("accueil.html",map=folium_map._repr_html_(),annees =  annees,departements = departements, gravites = gravites )


@app.route('/stats',methods=['GET','POST'])
def stats():
    liste = {'annee': Requetes.renvoyer_liste('annee'),'météo':Requetes.renvoyer_liste('conditionsatmosperiques'),'departement':Requetes.renvoyer_liste('nom_dep'),'saison':['Ete','Automne','Hiver','Printemps']}
    try:            
        Variable =  request.form['option']
        print(Variable)    
    except:
        Variable ='annee'
    values = Requetes.liste_stat(Variable)
    print(values)
    return render_template('stats.html',Liste = liste[Variable],Variable=Variable, options = liste.keys(),values = values )

if __name__ == '__main__' :
    app.run(debug=True)


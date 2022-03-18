import sqlite3

conn = sqlite3.connect('Accident_France.db')
cur = conn.cursor()

#cur.execute("SELECT Nom_commune FROM COMMUNE WHERE Code_postal == 38420")
#cur.execute("SELECT accidents_velos.date, accidents_velos.typecollision, accidents_velos.graviteaccident, Commune.Nom_commune, Commune.coordonnees_gps FROM accidents_velos JOIN Commune ON accidents_velos.commune_insee=Commune.Code_commune_insee WHERE Code_postal=38420")
cur.execute("SELECT DISTINCT date FROM accidents_velos ORDER BY date ASC")

conn.commit()

liste = cur.fetchall()

cur.close()
conn.close()

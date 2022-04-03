import sqlite3
class Requetes():
    @classmethod
    def renvoyer_liste(self,colonne,Table):
        conn = sqlite3.connect('Accident_France_2.db')
        cur = conn.cursor()
        cur.execute(f"SELECT DISTINCT {colonne} FROM {Table}")
        conn.commit()
        villes = cur.fetchall()
        cur.close()
        conn.close()
        return list(map(lambda x: x[0],villes))

    @classmethod
    def liste_affichage(self,colonne,Table,parametre):
        conn = sqlite3.connect('Accident_France_2.db')
        cur = conn.cursor()
        cur.execute(f"SELECT DISTINCT {colonne} FROM {Table} {parametre}")
        conn.commit()
        resultat = cur.fetchall()
        cur.close()
        conn.close()
        return resultat
   
    @classmethod
    def liste_stat(self,var):
        conn = sqlite3.connect('Accident_France_2.db')
        cur = conn.cursor()
        table = {
            'annee': Requetes.renvoyer_liste('annee'),
            'conditionsatmosperiques':Requetes.renvoyer_liste('conditionsatmosperiques'),
            'nom_dep':Requetes.renvoyer_liste('nom_dep'),
            'saison': ('printemps','ete','automne','hiver')}
        mois = {'hiver' : ('décembre', 'janvier', 'février'), 'printemps' : ('mars', 'avril', 'mai'), 'ete' : ('juin', 'juillet', 'aout'), 'automne' : ('septembre', 'octobre', 'novembre')}
        liste = []
        indice = {'annee':'annee','météo':'conditionsatmosperiques','departement':'nom_dep','saison':'saison'}
        var = indice[var]
        #print(table[var])  
        for v in table[var]:
            liste.append([v])
            for indice in range(4):
                try:
                    if var == 'saison':
                        cur.execute(f"SELECT COUNT(*) FROM ACCIDENTS_VELOS WHERE graviteaccident = {indice} AND ( mois = '{mois[v][0]}' OR mois = '{mois[v][1]}' OR mois = '{mois[v][2]}' )")
                    elif var == 'nom_dep':
                        cur.execute(f"SELECT COUNT(*) FROM DEPARTEMENT JOIN ACCIDENTS_VELOS ON DEPARTEMENT.code = ACCIDENTS_VELOS.departement WHERE ACCIDENTS_VELOS.graviteaccident = {indice} and DEPARTEMENT.nom_dep = '{v}'")
                    else:
                       cur.execute(f"SELECT COUNT(*) FROM ACCIDENTS_VELOS WHERE graviteaccident = {indice} and {var} = '{v}'")
                    liste[-1].append(cur.fetchall()[0][0])
                except Exception as e:
                    print(e)
        cur.close()
        conn.close()
        return liste

        
if __name__=='__main__':
    liste_requete = {"annee":2010,"departement":"AUDE","gravite":"2"}
    print(Requetes.liste_affichage('ACCIDENTS_VELOS.lat, ACCIDENTS_VELOS.lon','ACCIDENTS_VELOS',f"JOIN DEPARTEMENT ON ACCIDENTS_VELOS.num_dep=DEPARTEMENT.code WHERE annee={liste_requete['annee']} AND graviteaccident='{liste_requete['gravite']}' AND DEPARTEMENT.nom_maj='{liste_requete['departement']}'"))

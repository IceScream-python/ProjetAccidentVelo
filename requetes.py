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
        table = {'annee': Requetes.renvoyer_liste('annee'),'conditionsatmosperiques':Requetes.renvoyer_liste('conditionsatmosperiques'),'departement':Requetes.renvoyer_liste('nom_dep'),'saison':[]}
        dic = dict()
        #print(table[var])  
        for v in table[var]:
            dic[v] = {0:0,1:0,2:0,3:0}
            for indice in range(4):
                try:
                    cur.execute(f"SELECT COUNT(*) FROM ACCIDENTS_VELOS WHERE graviteaccident = {indice} and {var} = '{v}'")
                    dic[v][indice] = cur.fetchall()[0][0]
                except:
                    print(v)
                
        cur.close()
        conn.close()
        return dic
        
if __name__=='__main__':
    liste_requete = {"annee":2010,"departement":"AUDE","gravite":"2"}
    print(Requetes.liste_affichage('ACCIDENTS_VELOS.lat, ACCIDENTS_VELOS.lon','ACCIDENTS_VELOS',f"JOIN DEPARTEMENT ON ACCIDENTS_VELOS.num_dep=DEPARTEMENT.code WHERE annee={liste_requete['annee']} AND graviteaccident='{liste_requete['gravite']}' AND DEPARTEMENT.nom_maj='{liste_requete['departement']}'"))

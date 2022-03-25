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
    def liste_affichage(self,departement,annee,mois,jour,gravite):
        pass
    

if __name__=='__main__':
    print(Requetes.renvoyer_liste('Nom_dep','DEPARTEMENT'))

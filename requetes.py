import sqlite3
class Requetes():
    @classmethod
    def renvoyer_liste(self,colonne):
        Table = {'annee':'ACCIDENTS_VELOS','nom_dep':'DEPARTEMENT','conditionsatmosperiques':'ACCIDENTS_VELOS','mois':'ACCIDENTS_VELOS'}
        conn = sqlite3.connect('Accident_France_2.db')
        cur = conn.cursor()
        cur.execute(f"SELECT DISTINCT {colonne} FROM {Table[colonne]}")
        conn.commit()
        villes = cur.fetchall()
        cur.close()
        conn.close()
        return list(map(lambda x: x[0],villes))

    @classmethod
    def liste_affichage(self,dico):
        if None in dico.keys():
            return []
        conn = sqlite3.connect('Accident_France_2.db')
        cur = conn.cursor()
        gravite = {'Indemne':0,'Blessé Léger':1, 'Blessé Hospitalisé':2,'Tué':3}
        condition = ''
        if dico['gravite'] != 'Tout':
            condition += f" ACCIDENTS_VELOS.graviteaccident='{gravite[dico['gravite']]}'" 
        if dico['departement'] != 'Tout':
            if dico['gravite'] != 'Tout':
                condition += ' AND'
            condition += f" DEPARTEMENT.nom_dep='{dico['departement']}'"
        if dico['annee'] != 'Tout':
            if dico['gravite'] != 'Tout' or dico['departement'] != 'Tout':
                condition += ' AND'
            condition += f" ACCIDENTS_VELOS.annee={dico['annee']}"
        if None in dico.keys():
            return []
        print(condition)
        cur.execute(f"SELECT ACCIDENTS_VELOS.lat,ACCIDENTS_VELOS.lon, FROM ACCIDENTS_VELOS JOIN DEPARTEMENT ON ACCIDENTS_VELOS.departement = DEPARTEMENT.code  WHERE {condition} AND (ACCIDENTS_VELOS.lat<>0.0 AND ACCIDENTS_VELOS.lon<>0.0)")
        conn.commit()
        resultat = cur.fetchall()
        cur.close()
        conn.close()
        return resultat
    
    @classmethod
    def num_dep(self,nom_dep):
        conn = sqlite3.connect('Accident_France_2.db')
        cur = conn.cursor()
        cur.execute(f"SELECT DISTINCT code FROM DEPARTEMENT WHERE nom_dep='{nom_dep}'")
        conn.commit()
        num = cur.fetchall()
        cur.close()
        conn.close()
        return num[0][0]

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
    print(Requetes.liste_affichage({'annee':'*','gravite':'Indemne','departement':'Ain'}))
    #print(Requetes.renvoyer_liste('mois'))
    #print(Requetes.num_dep('Ain'))

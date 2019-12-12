"""Modul ai je odgovoran za vestacku inteligenciju igre Santorini, sadrzi klase koje implementiraju minimax i minimax + alfa-beta,
funkcije za staticku procenu stanja itd. Sve sto ima veze za AI ove igre nalazi se ovde.
"""

from tabla import Tabla, IGRAC_CRVENI, IGRAC_PLAVI, protivnik, Potez
import math
import random
import copy
import time
from abc import ABC, abstractmethod


def staticka_funkcija_procene(tabla: Tabla, potez: Potez, na_potezu):
    """Ovo je jednostavna staticka funkcija procene f,koja se računa kao 𝑓 = 𝑛 + 𝑚, gde je 𝑛 broj pločica odredišnog
    polja, a 𝑚 broj nivoa na koje se dodaje plocica poomnozen razlikom rastojanja sopstvenih i protivnickih igraca od tog polja.
    Da bi se ova funkcija izracunala pored stanja/table potreban mi je i potez koji dovodi to tog novog stanja kao i igrac koji 
    je trenutno na potezu.  
    
    :param tabla: Tabla/stanje za koju treba izracunati staticku funkciju procene
    :type tabla: Tabla
    :param potez: Potez koji je doveo to tog stanja
    :type potez: Potez
    :param na_potezu: Igrac za kojeg se racuna staticka funkcija procene
    :type na_potezu: int
    :return: Vrednost staticke funkcije procene
    :rtype: int
    """    
    if tabla.pobeda(na_potezu):
        #print("Pobeda")
        return 100
    if tabla.poraz(na_potezu):
        #print("Poraz")
        return -100

    m = tabla.matrica[potez.x2][potez.y2].broj_spratova
    rastojanja = 0
    for i in range(5):
        for j in range(5):
            if tabla.matrica[i][j].igrac == na_potezu:
                rastojanja += tabla.rastojanje(i, j, potez.xg, potez.yg)
            elif tabla.matrica[i][j].igrac != na_potezu and tabla.matrica[i][j].igrac != None:  # ako je protivnik
                rastojanja -= tabla.rastojanje(i, j, potez.xg, potez.yg)
    l = tabla.matrica[potez.xg][potez.yg].broj_spratova * rastojanja
    return m + l



#TODO ako je odredisno polje vece od trenutnog onda + nesto, + sprat odredisnog polja * 2, idk tako nesto
def unapredjena_staticka_funkcija_procene(tabla: Tabla, potez: Potez, na_potezu):
    """Ovo je jednostavna staticka funkcija procene f,koja se računa kao 𝑓 = 𝑛 + 𝑚, gde je 𝑛 broj pločica odredišnog
    polja, a 𝑚 broj nivoa na koje se dodaje plocica poomnozen razlikom rastojanja sopstvenih i protivnickih igraca od tog polja.
    Da bi se ova funkcija izracunala pored stanja/table potreban mi je i potez koji dovodi to tog novog stanja kao i igrac koji 
    je trenutno na potezu.  
    
    :param tabla: Tabla/stanje za koju treba izracunati staticku funkciju procene
    :type tabla: Tabla
    :param potez: Potez koji je doveo to tog stanja
    :type potez: Potez
    :param na_potezu: Igrac za kojeg se racuna staticka funkcija procene
    :type na_potezu: int
    :return: Vrednost staticke funkcije procene
    :rtype: int
    """    
    if tabla.pobeda(na_potezu):
        #print("Pobeda")
        return 100
    if tabla.poraz(na_potezu):
        #print("Poraz")
        return -100

    m = tabla.matrica[potez.x2][potez.y2].broj_spratova
    rastojanja = 0
    for i in range(5):
        for j in range(5):
            if tabla.matrica[i][j].igrac == na_potezu:
                rastojanja += tabla.rastojanje(i, j, potez.xg, potez.yg)
            elif tabla.matrica[i][j].igrac != na_potezu and tabla.matrica[i][j].igrac != None:  # ako je protivnik
                rastojanja -= tabla.rastojanje(i, j, potez.xg, potez.yg)
    l = tabla.matrica[potez.xg][potez.yg].broj_spratova * rastojanja
    return 3 * m + l # za sad je samo ovo unapredjeno


def svi_moguci_potezi(tabla, na_potezu):
    """Funkcija koja za datu tablu/stanje i igraca vraca sve moguce poteze koje on iz tog stanja moze da izvrsi.
    Prvo obilazi celu tablu i nalazi figure koje pripadaju igracu, onda obilazi sva susedna polja tih figura 
    i nalazi ona na koja igrac moze da se krece, onda iz tih polja obilazi ponovo sva susedna i nalazi polja na 
    kojima moze da gradi. Svaki validni potez se dodaje u listu poteza moguci_potezi i tu listu ova funkcija vraca.  
    
    :param tabla: Stanje igre, stanje table ili vrednost polja u matrici, svejedno  
    :type tabla: Tabla
    :param na_potezu: Igrac za kojeg nalazimo dozvoljene poteze
    :type na_potezu: int
    :return: Lista dozvoljenih poteza
    :rtype: list
    """    
    # lista mogucih stanja
    moguci_potezi = []

    # ako je igra vec zavrsena u datom stanju onda nista, nema vise poteza, i vracam prazan niz
    # igra je zavrsena ako jedan od igraca dostigne 3 nivo
    if tabla.zauzeo_treci_sprat(na_potezu) or tabla.zauzeo_treci_sprat(protivnik(na_potezu)):
        return moguci_potezi

    # pronadji dve figure koje pripadaju trenutnom igracu
    broj_pronadjenih_figura = 0
    for i in range(5):
        if broj_pronadjenih_figura == 2:
            break
        for j in range(5):
            if tabla.matrica[i][j].igrac == na_potezu:
                broj_pronadjenih_figura += 1
                # prodji kroz sva njegova susedna polja
                for k in range(i - 1, i + 2):
                    for l in range(j - 1, j + 2):
                        # proveri da li je novo polje unutar matrice, da li je slobodno i da nije "previsoko"
                        unutar_matrice = k >= 0 and k <= 4 and l >= 0 and l <= 4
                        if not unutar_matrice:
                            continue
                        novo_polje = k != i or l != j  # da li se polje razlikuje od onog u kome se sad nalazi
                        slobodno_polje = tabla.matrica[k][l].igrac == None
                        odgovara_broj_spratova = tabla.matrica[i][j].broj_spratova + 1 >= tabla.matrica[k][l].broj_spratova
                        if unutar_matrice and novo_polje and slobodno_polje and odgovara_broj_spratova:
                            # kad imamo sva polja u koja mozemo da idemo sad treba iz njih da nadjemo sva polja u koja mozemo da gradimo
                            for m in range(k - 1, k + 2):
                                for n in range(l - 1, l + 2):
                                    # isto proveravamo da li je ovo polje unutar matrice, da li je slobodno i da li je broj spratova < 4
                                    unutar_matrice = m >= 0 and m <= 4 and n >= 0 and n <= 4
                                    if not unutar_matrice:
                                        continue
                                    novo_polje = m != k or n != l
                                    slobodno_polje = tabla.matrica[m][n].igrac == None
                                    moze_da_se_gradi = tabla.matrica[m][n].broj_spratova < 4
                                    if unutar_matrice and novo_polje and slobodno_polje and moze_da_se_gradi:
                                        moguci_potezi.append(Potez(i, j, k, l, m, n))
    return moguci_potezi


class Node:
    """Klasa Node prestavlja jedan cvor u stablu, kao atribute ima vrednost i children(listu potomaka)."""
    def __init__(self, vrednost = 0, children = None):
        """Konstruktor koji postavlja vrednosti atributa klase.
        
        :param vrednost: Vrednost ovog cvora, defaults to 0
        :type vrednost: int, optional
        :param children: Lista potomaka cvora, defaults to None
        :type children: lista, optional
        """        
        self.vrednost = vrednost
        self.children = children or []
    
    def max_child_vrednost(self):
        """Medju children(potomcima) ovog cvora nalazi onaj cvor koji ima najvecu vrednost i vraca njegovu vrednost.
        
        :return: Najveca vrednost medju potomcima ovog cvora
        :rtype: int
        """        
        value = -math.inf
        for node in self.children:
            if (node.vrednost > value):
                value = node.vrednost
        return value

    def min_child_vrednost(self):
        """Medju children(potomcima) ovog cvora nalazi onaj cvor koji ima najmanju vrednost i vraca njegovu vrednost.
        
        :return: Najmanja vrednost medju potomcima ovog cvora
        :rtype: int
        """        
        value = math.inf
        for node in self.children:
            if (node.vrednost < value):
                value = node.vrednost
        return value


#Abstraktna klasa za AI
class AI(ABC):
    """Abstraktna klasa koju nasledjuju sve klase koje implementiraju neku vrstu vestacke inteligencije.
    Od atributa ima dubinu, funkciju koja racuna staticku vrednost i bool da li treba stampati vrednosti svih mogucih poteza AI algoritma .
    """    

    def __init__(self, stampaj_vrednosti_svih_poteza,dubina = 2, funkcija_procene = staticka_funkcija_procene):
        """Konsturtor sa parametrima koji postavlja vredsnoti atributa klase
        
        :param stampaj_vrednosti_svih_poteza: Da li treba stampati vrednost svakom moguceg poteza AI
        :type stampaj_vrednosti_svih_poteza: bool
        :param dubina: Dubina do koje treba pretrazivati stablo igre, defaults to 2
        :type dubina: int, optional
        :param funkcija_procene: Funkcija sa kojom se racuna staticka vrednost, defaults to staticka_funkcija_procene
        :type funkcija_procene: function, optional
        """        
        self.stampaj_vrednosti_svih_poteza = stampaj_vrednosti_svih_poteza
        self.dubina = dubina
        self.funkcija_procene = funkcija_procene


    @abstractmethod
    def sledeci_potez(self, tabla, na_potezu):
        """Glavna funkcija ovog modula, igra poziva ovu funkcija, prosledjuje joj stanje i igraca a ova funkija vraca sledeci potez.
        Ovo je abstraktna funkcija tako da je moraju implementirati sve klase koje nasledjuju AI.
        
        :param tabla: Tabla za koju treba naci sledeci potez
        :type tabla: Tabla
        :param na_potezu: Igrac koji je na potezu i za kojeg treba naci sledeci potez
        :type na_potezu: int
        """        
        pass


class MiniMax(AI):
    """Klasa koja nasledjuje AI i implementira obicni MiniMax algoritam"""    

    def __init__(self, stampaj_vrednosti_svih_poteza,dubina = 2, funkcija_procene = staticka_funkcija_procene):
        """Konsturtor sa parametrima koji postavlja vredsnoti atributa klase
        
        :param stampaj_vrednosti_svih_poteza: Da li treba stampati vrednost svakom moguceg poteza AI
        :type stampaj_vrednosti_svih_poteza: bool
        :param dubina: Dubina do koje treba pretrazivati stablo igre, defaults to 2
        :type dubina: int, optional
        :param funkcija_procene: Funkcija sa kojom se racuna staticka vrednost, defaults to staticka_funkcija_procene
        :type funkcija_procene: function, optional
        """          
        super().__init__(stampaj_vrednosti_svih_poteza, dubina, funkcija_procene)

    def sledeci_potez(self, tabla, na_potezu):
        """Igra poziva ovu funkcija, prosledjuje joj stanje i igraca a ova funkija vraca sledeci potez.
        Ovo je abstraktna funkcija tako da je moraju implementirati sve klase koje nasledjuju AI.
        
        :param tabla: Tabla za koju treba naci sledeci potez
        :type tabla: Tabla
        :param na_potezu: Igrac koji je na potezu i za kojeg treba naci sledeci potez
        :type na_potezu: int
        """     

        # moglo bi ovo i prostije da se odradi ali se u zadatku trazi da se stampaju vrednosti svih mogucih poteza pa moram da ga iskomplikujem malo   
        stablo = self.kreiraj_stablo_i_izvrsi_minimax(tabla, self.dubina, na_potezu, True, None)
        svi_potezi = svi_moguci_potezi(tabla, na_potezu)

        # stampaj vrednosti svih poteza
        if self.stampaj_vrednosti_svih_poteza:
            print(f"\n\n\nNa potezu je {na_potezu}, koristi se algoritam MiniMax i vrednsti svih mogucih poteza su:")
            for i in range(len(svi_potezi)):
                print(svi_potezi[i], stablo.children[i].vrednost)
        
        # nadji najbolji potez i vrati ga
        for i in range(len(svi_potezi)):
            if stablo.children[i].vrednost == stablo.vrednost:
                return svi_potezi[i]


    def kreiraj_stablo_i_izvrsi_minimax(self, tabla, dubina, na_potezu, maximizing_player, potez):
        """Rekurzivna funkcija koja kreira stablo dubine n, stablo se sastoji od Node objekata, tj. za svaki cvor se pamti samo vrednost tog
        cvora i njegovi potomci, nad tim stablom se izvrsava minimax i popuni se vrednost svih cvorova u stablu. Ovaj algoritam je uradjen po 
        ugledu na psudo kod minimax algoritma sa moodle-a
        
        :param tabla: Tabla nad kojom treba izvrsavati poteze ili za koju treba racunati staticku funkciju procene
        :type tabla: Tabla
        :param dubina: Dubina razvijanja stabla
        :type dubina: int
        :param na_potezu: Igrac za kojeg se racuna staticka funkcija procene
        :type na_potezu: int
        :param maximizing_player: Da li treba uzimati max ili min vrednost od potomaka
        :type maximizing_player: bool
        :param potez: Potez koji je doveo do ovog stanja
        :type potez: Potez
        :return: Stablo dubine n koje se sastoji od Node objekata, nad kojim je izvrsen minimax i pronadjena vrednost svakog cvora
        :rtype: Node
        """
        # ako ne treba dalje razvijati stablo vracamo staticku funkciju procene        
        if dubina == 0:
            vrednost = self.funkcija_procene(tabla, potez, na_potezu)
            return Node(vrednost)
        
        # pronalazimo sve moguce poteze iz ovog stabla u zavisnosti od toga koji igrac povlaci sad potez
        if maximizing_player:
            svi_potezi = svi_moguci_potezi(tabla, na_potezu)
        else:
            svi_potezi = svi_moguci_potezi(tabla, protivnik(na_potezu))

        # ako nema mogucih poteza vrati vrednost tog cvora vracamo staticku funkciju procene
        if len(svi_potezi) == 0:
            vrednost = self.funkcija_procene(tabla, potez, na_potezu)
            return Node(vrednost)
        else: # inace kreiraj novi node i dodaj mu vrednosti svih mogucih sledecih poteza kao children
            novi_node = Node()
            for p in svi_potezi:
                #nova_tabla = copy.deepcopy(tabla) deepcopy je ZLO
                nova_tabla = Tabla(tabla)
                nova_tabla.izvrsi_potez(p)
                novi_node.children.append(self.kreiraj_stablo_i_izvrsi_minimax(nova_tabla, dubina - 1, na_potezu, not maximizing_player, p))

        # nalazimo minimalnu ili maksimalu vrednost medju potomcima cvora i postavljamo je za vrednost tog cvora
        if maximizing_player:
            novi_node.vrednost = novi_node.max_child_vrednost()
        else:
            novi_node.vrednost = novi_node.min_child_vrednost()
        
        return novi_node

    

class MiniMaxAlfaBeta(AI): 
    """Klasa koja nasledjuje AI i implementira MiniMax algoritam sa alfa-beta odsecanjem""" 
    lista_poteza = []

    def __init__(self, stampaj_vrednosti_svih_poteza,dubina = 3, funkcija_procene = staticka_funkcija_procene):    
        """Konsturtor sa parametrima koji postavlja vredsnoti atributa klase
        
        :param stampaj_vrednosti_svih_poteza: Da li treba stampati vrednost svakom moguceg poteza AI
        :type stampaj_vrednosti_svih_poteza: bool
        :param dubina: Dubina do koje treba pretrazivati stablo igre, defaults to 3
        :type dubina: int, optional
        :param funkcija_procene: Funkcija sa kojom se racuna staticka vrednost, defaults to staticka_funkcija_procene
        :type funkcija_procene: function, optional
        """  
        super().__init__(stampaj_vrednosti_svih_poteza, dubina, funkcija_procene)


    def sledeci_potez(self, tabla, na_potezu):
        """Igra poziva ovu funkcija, prosledjuje joj stanje i igraca a ova funkija vraca sledeci potez.
        Ovo je abstraktna funkcija tako da je moraju implementirati sve klase koje nasledjuju AI.
        
        :param tabla: Tabla za koju treba naci sledeci potez
        :type tabla: Tabla
        :param na_potezu: Igrac koji je na potezu i za kojeg treba naci sledeci potez
        :type na_potezu: int
        """     
        self.na_potezu = na_potezu
        return self.alfa_beta_pretraga(tabla, self.dubina, None)
   

    #TODO da napisem komentare za ovo cudo i za ove funkcije ispod
    def alfa_beta_pretraga(self, tabla, dubina, potez):
        """Ovaj algoritam je uradjen po ugledu na psudo kod za alfa-beta pretragu iz knjige. Figure 5.7.
        
        :param tabla: Tabla nad kojom treba izvrsavati poteze ili za koju treba racunati staticku funkciju procene
        :type tabla: Tabla
        :param dubina: Dubina razvijanja stabla
        :type dubina: int
        :param potez: Potez koji je doveo do ovog stanja
        :type potez: Potez
        :return: Potez koji treba da se izvrsi
        :rtype: Potezs
        """        
        self.lista_poteza.clear()
        v = self.max_value(tabla, dubina, potez, -1000, 1000)

        # stampaj vrednosti svih poteza
        if self.stampaj_vrednosti_svih_poteza:
            print(f"\n\n\nNa potezu je {self.na_potezu}, koristi se algoritam MiniMax sa Alfa Beta odsecanjem i vrednsti svih mogucih poteza su:")
            for p in self.lista_poteza:
                print(p[1], p[0])
        
        for p in self.lista_poteza:
            if p[0] == v:
                return p[1]

    def max_value(self, tabla, dubina, potez, alfa, beta):
        if dubina == 0:
            vrednost = self.funkcija_procene(tabla, potez, self.na_potezu)
            return vrednost

        v = -1000

        svi_potezi = svi_moguci_potezi(tabla, self.na_potezu)
        # ako nema mogucih poteza vrati vrednost tog cvora
        if len(svi_potezi) == 0:
            vrednost = self.funkcija_procene(tabla, potez, self.na_potezu)
            return vrednost
        else:
            for p in svi_potezi:
                nova_tabla = Tabla(tabla)
                nova_tabla.izvrsi_potez(p)
                nova_vrednost = self.min_value(nova_tabla, dubina - 1, p, alfa, beta)

                # sad upisujem sve poteze u self.lista_poteza da bih na kraju znao koji da uzmem
                if dubina == self.dubina:
                    self.lista_poteza.append((nova_vrednost, p))

                v = max(v, nova_vrednost)
                if v >= beta:
                    return v
                alfa = max(alfa, v)
        return v


    def min_value(self, tabla, dubina, potez, alfa, beta):
        if dubina == 0:
            vrednost = self.funkcija_procene(tabla, potez, self.na_potezu)
            return vrednost

        v = 1000

        svi_potezi = svi_moguci_potezi(tabla, protivnik(self.na_potezu))
        # ako nema mogucih poteza vrati vrednost tog cvora
        if len(svi_potezi) == 0:
            vrednost = self.funkcija_procene(tabla, potez, self.na_potezu)
            return vrednost
        else:
            for p in svi_potezi:
                nova_tabla = Tabla(tabla)
                nova_tabla.izvrsi_potez(p)
                nova_vrednost = self.max_value(nova_tabla, dubina - 1, p, alfa, beta)

                v = min(v, nova_vrednost)
                if v <= alfa:
                    return v
                beta = min(beta, v)
        return v


#test
if __name__ == "__main__":
    tabla = Tabla()

    tabla.matrica[2][2].igrac = IGRAC_PLAVI
    tabla.matrica[2][3].igrac = IGRAC_PLAVI
    tabla.matrica[0][0].igrac = IGRAC_CRVENI
    tabla.matrica[0][1].igrac = IGRAC_CRVENI

    ukupno = 0
    for i in range(10):
        start = time.time()
        potez = MiniMax(False).sledeci_potez(tabla, IGRAC_PLAVI)
        print(potez)
        print("Vreme potrebno za izracunavanje: ", time.time() - start)
        ukupno += time.time() - start

    print("Prosek:", ukupno / 10.)

    ukupno = 0
    for i in range(10):
        start = time.time()
        potez = MiniMaxAlfaBeta(False).sledeci_potez(tabla, IGRAC_PLAVI)
        print(potez)
        print("Vreme potrebno za izracunavanje: ", time.time() - start)
        ukupno += time.time() - start

    print("Prosek:", ukupno / 10.)

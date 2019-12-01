from tabla import Tabla, IGRAC_CRVENI, IGRAC_PLAVI, protivnik, Potez
import math
import random
import copy
import time
from abc import ABC, abstractmethod


# staticka funkcija procene neke tabele, za nju mi je potreban i potez kojim se doslo do te tabele
def staticka_funkcija_procene(tabla: Tabla, potez: Potez, na_potezu):
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


class Node:
    def __init__(self, vrednost = 0, children = None):
        self.vrednost = vrednost
        self.children = children or []
    
    def max_child_vrednost(self):
        value = -math.inf
        for node in self.children:
            if (node.vrednost > value):
                value = node.vrednost
        return value

    def min_child_vrednost(self):
        value = math.inf
        for node in self.children:
            if (node.vrednost < value):
                value = node.vrednost
        return value


#todo nasledjivanje nema svrhe u pythonu, mozda i ima ako hocu u novom prozoru da pokazujem vrednosti svih poteza

#Abstraktna klasa za AI, koju ce da naslede svi razliciti algoritmi za easy, medium i hard
class AI(ABC):

    #todo u konstruktoru treba da otvori window gde ce da se prikazuju vrednosti mogucih poteza

    # glavna funkcija ovog modula, igra poziva ovu funkciju, prosledjuje jos stanje i algoritam koji treba da se koristi
    # a ona vraca sledeci potez
    @abstractmethod
    def sledeci_potez(self, tabla, na_potezu):
        pass


class MiniMax(AI):
    def sledeci_potez(self, tabla, na_potezu):
        stablo = self.kreiraj_stablo(tabla, 3, na_potezu, True, None)
        svi_potezi = svi_moguci_potezi(tabla, na_potezu)
        #for i in range(len(svi_potezi)):
        #    print(svi_potezi[i], stablo.children[i].vrednost)
        
        for i in range(len(svi_potezi)):
            if stablo.children[i].vrednost == stablo.vrednost:
                return svi_potezi[i]

    # todo bolje ime da stavim
    # rekurzivna funkcija koja kreira stablo dubine n, stablo se sastoji od Node2 objekata, i izvrsava minimax i izracuna vrednost svakog cvora u stablu
    def kreiraj_stablo(self, tabla, dubina, na_potezu, maximizing_player, potez):
        if dubina == 0:
            vrednost = staticka_funkcija_procene(tabla, potez, na_potezu)
            return Node(vrednost)
        
        if maximizing_player:
            svi_potezi = svi_moguci_potezi(tabla, na_potezu)
        else:
            svi_potezi = svi_moguci_potezi(tabla, protivnik(na_potezu))

        # ako nema mogucih poteza vrati vrednost tog cvora
        if len(svi_potezi) == 0:
            vrednost = staticka_funkcija_procene(tabla, potez, na_potezu)
            return Node(vrednost)
        else:
            novi_node = Node()
            for p in svi_potezi:
                #nova_tabla = copy.deepcopy(tabla) deepcopy je ZLO
                nova_tabla = Tabla(tabla)
                nova_tabla.izvrsi_potez(p)
                novi_node.children.append(self.kreiraj_stablo(nova_tabla, dubina - 1, na_potezu, not maximizing_player, p))

        if maximizing_player:
            novi_node.vrednost = novi_node.max_child_vrednost()
        else:
            novi_node.vrednost = novi_node.min_child_vrednost()
        
        return novi_node

    

class MiniMaxAlfaBeta(AI): 
    lista_poteza = []
    dubina = 4 # konstanta, koliku dubinu treba da pretrazuje...idk, bolje mozda da ovo ide u konsturktor?
    na_potezu = IGRAC_CRVENI # ovo treba da pokazuje za koga se racuna staticka funkcija procene, i ne treba da bude const, vec da se zadaje u ctoru
    
    def sledeci_potez(self, tabla, na_potezu):
        self.na_potezu = na_potezu
        return self.alfa_beta_pretraga(tabla, self.dubina, None)


    def alfa_beta_pretraga(self, tabla, dubina, potez):
        self.lista_poteza.clear()
        v = self.max_value(tabla, dubina, potez, -1000, 1000)
        
        for p in self.lista_poteza:
            if p[0] == v:
                return p[1]

    def max_value(self, tabla, dubina, potez, alfa, beta):
        if dubina == 0:
            vrednost = staticka_funkcija_procene(tabla, potez, self.na_potezu) #ova konstanta je samo privremena todo
            return vrednost

        v = -1000

        svi_potezi = svi_moguci_potezi(tabla, self.na_potezu)
        # ako nema mogucih poteza vrati vrednost tog cvora
        if len(svi_potezi) == 0:
            vrednost = staticka_funkcija_procene(tabla, potez, self.na_potezu)
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
            vrednost = staticka_funkcija_procene(tabla, potez, self.na_potezu) #ova konstanta je samo privremena todo
            return vrednost

        v = 1000

        svi_potezi = svi_moguci_potezi(tabla, protivnik(self.na_potezu))
        # ako nema mogucih poteza vrati vrednost tog cvora
        if len(svi_potezi) == 0:
            vrednost = staticka_funkcija_procene(tabla, potez, self.na_potezu)
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


# vraca listu svih mogucih validnih poteza iz prosledjene table
def svi_moguci_potezi(tabla, na_potezu):
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
        potez = MiniMax().sledeci_potez(tabla, IGRAC_PLAVI)
        print(potez)
        print("Vreme potrebno za izracunavanje: ", time.time() - start)
        ukupno += time.time() - start

    print("Prosek:", ukupno / 10.)

    ukupno = 0
    for i in range(10):
        start = time.time()
        potez = MiniMaxAlfaBeta().sledeci_potez(tabla, IGRAC_PLAVI)
        print(potez)
        print("Vreme potrebno za izracunavanje: ", time.time() - start)
        ukupno += time.time() - start

    print("Prosek:", ukupno / 10.)

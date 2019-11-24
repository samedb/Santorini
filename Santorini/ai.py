from tabla import Tabla, Igrac, Potez
import math
import random
import copy
import time
from abc import ABC, abstractmethod


# staticka funkcija procene neke tabele, za nju mi je potreban i potez kojim se doslo do te tabele
def staticka_funkcija_procene(tabla: Tabla, potez: Potez, na_potezu: Igrac):
    if tabla.pobeda(na_potezu):
        print("Pobeda")
        return 100
    if tabla.poraz(na_potezu):
        print("Poraz")
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

    def __init__(self, tabla: Tabla, potez: Potez, vrednost=0):
        self.tabla = tabla # trenutno stanje igre
        self.potez = potez # potez koji je doveo do trenutnog stanja
        self.children = []  # lista cvorova potomaka
        #self.vrednost = vrednost

class Node2:
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


#Abstraktna klasa za AI, koju ce da naslede svi razliciti algoritmi za easy, medium i hard
class AI(ABC):

    #todo u konstruktoru treba da otvori window gde ce da se prikazuju vrednosti mogucih poteza

    # glavna funkcija ovog modula, igra poziva ovu funkciju, prosledjuje jos stanje i algoritam koji treba da se koristi
    # a ona vraca sledeci potez
    @abstractmethod
    def sledeci_potez(self, tabla, na_potezu):
        pass



class MiniMaxStari(AI):

    def sledeci_potez(self, tabla, na_potezu):
        node = kreiraj_stablo(Node(tabla, None), 3, na_potezu)
        vrednost, potez = self.minimax(node, 3, True, na_potezu)
        print("Stari minimax Vrednost odabranog poteza: ", vrednost, potez)
        return potez

    # prima pocetni cvor stabla, i vraca najbolje sledece stanje/potez uz pomoc minimax algoritma
    def minimax(self, node: Node, dubina: int, maximizing_player, na_potezu):
        # print("Dubina", dubina)
        if dubina == 0 or len(node.children) == 0:
            # ovo moze da se spoji kao jedan parametar, da ne bude posebno potez i tabla
            return staticka_funkcija_procene(node.tabla, node.potez, na_potezu), node.potez
            # ovo plus dubina je ovde sa razlogom, na ovaj nacin vise vrednuje poteze koji se nalaze pri vrhu stabla

        if maximizing_player:
            value = -math.inf
            potez = None
            for child in node.children:
                v, t = self.minimax(child, dubina - 1, False, na_potezu)
                if dubina == 3:
                    print("stari minimax:", child.potez, v)
                if v > value:
                    value = v
                    potez = child.potez
            return value, potez
        else:
            value = math.inf
            potez = None
            for child in node.children:
                v, t = self.minimax(child, dubina - 1, True, na_potezu)
                if v < value:
                    value = v
                    potez = child.potez
            return value, potez


class MiniMaxNovi(AI):
    def sledeci_potez(self, tabla, na_potezu):
        stablo = self.kreiraj_stablo(tabla, 3, na_potezu, True, None)
        svi_potezi = svi_moguci_potezi(tabla, na_potezu)
        #for i in range(len(svi_potezi)):
        #    print(svi_potezi[i], stablo.children[i].vrednost)
        
        for i in range(len(svi_potezi)):
            if stablo.children[i].vrednost == stablo.vrednost:
                return svi_potezi[i]

    # rekurzivna funkcija koja kreira stablo dubine n, stablo se sastoji od Node2 objekata, i izvrsava minimax i izracuna vrednost svakog cvora u stablu
    def kreiraj_stablo(self, tabla, dubina, na_potezu, maximizing_player, potez):
        if dubina == 0:
            vrednost = staticka_funkcija_procene(tabla, potez, na_potezu)
            return Node2(vrednost)
        
        if maximizing_player:
            svi_potezi = svi_moguci_potezi(tabla, na_potezu)
        else:
            svi_potezi = svi_moguci_potezi(tabla, na_potezu.protivnik())

        # ako nema mogucih poteza vrati vrednost tog cvora
        if len(svi_potezi) == 0:
            vrednost = staticka_funkcija_procene(tabla, potez, na_potezu)
            return Node2(vrednost)
        else:
            novi_node = Node2()
            for p in svi_potezi:
                #nova_tabla = copy.deepcopy(tabla)
                nova_tabla = Tabla(tabla)
                nova_tabla.izvrsi_potez(p)
                novi_node.children.append(self.kreiraj_stablo(nova_tabla, dubina - 1, na_potezu, not maximizing_player, p))

        if maximizing_player:
            novi_node.vrednost = novi_node.max_child_vrednost()
        else:
            novi_node.vrednost = novi_node.min_child_vrednost()
        
        return novi_node

    

        


# vraca listu svih mogucih validnih poteza iz prosledjene table
def svi_moguci_potezi(tabla, na_potezu: Igrac):
    # lista mogucih stanja
    moguci_potezi = []

    # ako je igra vec zavrsena u datom stanju onda nista, nema vise poteza, i vracam prazan niz
    # igra je zavrsena ako jedan od igraca dostigne 3 nivo
    if tabla.zauzeo_treci_sprat(na_potezu) or tabla.zauzeo_treci_sprat(na_potezu.protivnik()):
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


# prima pocetni cvor stabla, razvija stablo trazene dubine i vraca ga
def kreiraj_stablo(node: Node, dubina: int, na_potezu: Igrac):
    if dubina == 0:
        return

    svi_potezi = svi_moguci_potezi(node.tabla, na_potezu)
    if dubina == 3:
        print("Broj svih mogucih poteza iz ovog stanja: ", len(svi_potezi))

    for potez in svi_potezi:
        nova_tabla = copy.deepcopy(node.tabla)
        nova_tabla.izvrsi_potez(potez)
        #vrednost = staticka_funkcija_procene(nova_tabla, potez, na_potezu)
        novi_node = Node(nova_tabla, potez)
        kreiraj_stablo(novi_node, dubina - 1, na_potezu.protivnik())
        node.children.append(novi_node)

    return node





# isto kao i ovo iznad samo koristi drugi algoritam
#def minimax_alfa_beta(node: Node):
#    return node.children[0]


# posto se u zadatku trazi jos jedan treci optimizovani algoritam on ide ovde
#def super_zeznuti_algoritam(node):
#    pass


# ovo ce vrv da se izbaci a mozda i nece, prima dva stanja kao parametre i vraca potez kojim se prelazi iz stanja1 u
# stanje 2 u formatu kao sto se trazi u zadatku
#def prebaci_u_potez(stanje1, stanje2):
#    pass



#test
if __name__ == "__main__":
    tabla = Tabla()

    tabla.matrica[2][2].igrac = Igrac.PLAVI
    tabla.matrica[2][3].igrac = Igrac.PLAVI
    tabla.matrica[0][0].igrac = Igrac.CRVENI
    tabla.matrica[0][1].igrac = Igrac.CRVENI

    ukupno = 0
    for i in range(5):
        start = time.time()
        potez = MiniMaxNovi().sledeci_potez(tabla, Igrac.PLAVI)
        print("Vreme potrebno za izracunavanje: ", time.time() - start)
        ukupno += time.time() - start

    print("Prosek:", ukupno / 5.)

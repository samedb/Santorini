from igra import *
import math


class Potez():
    # x1,y1 su pocetna pozicija, x2, y2 su nova pozicija, a xg, yg su pozicija gradnje
    def __init__(self, x1, y1, x2, y2, xg, yg):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.xg = xg
        self.yg = yg

    def __str__(self):
        return f"\t({self.x1}, {self.y1}), ({self.x2}, {self.y2}), ({self.xg}, {self.yg})"

    def __repr__(self):
        return self.__str__()


class Node():

    def __init__(self, stanje: Stanje, igrac: Igrac, potez: Potez):
        self.stanje = stanje
        self.children = [] # lista cvorova potomaka
        self.igrac = igrac # za kojeg igraca (crvenog ili plavog) treba da se racuna vrednost
        self.potez = potez # potez sa kojim se doslo do ovog stanja
        self.vrednost = self.izracunaj_vrednost_stanja() # vrednsot ovog stanja

    def rastojanje(self, x1, y1, x2, y2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return abs(dx - dy)

    def izracunaj_vrednost_stanja(self):
        if self.potez == None:
            return 0
        #staticka funkcija procene nekog stanja
        m = self.stanje.matrica[self.potez.x2][self.potez.y2].broj_spratova
        rastojanja = 0
        for i in range(5):
            for j in range(5):
                if self.stanje.matrica[i][j].igrac == Igrac.PLAVI:
                    rastojanja += self.rastojanje(i, j, self.potez.xg, self.potez.yg)
                elif self.stanje.matrica[i][j].igrac == Igrac.CRVENI:
                    rastojanja -= self.rastojanje(i, j, self.potez.xg, self.potez.yg)
        l = self.stanje.matrica[self.potez.xg][self.potez.yg].broj_spratova * rastojanja
        return m + l

    def kraj_igre(self):
        # proveri da li ima mogucih poteza i da li je nego postavio figuru na polje sa nivoom 3
        return False


#vraca listu svih mogucih validnih stanja do kojih moze da se dodje iz prosledjenog stanja
def svi_moguci_potezi(node):
    #lista mogucih stanja
    moguci_potezi = []

    # pronadji dve figure koje pripadaju trenutnom igracu
    for i in range(5):
        for j in range(5):
            if node.stanje.matrica[i][j].igrac == node.igrac:
                # prodji kroz sva njegova susedna polja
                for k in range(i - 1, i + 2):
                    for l in range(j - 1, j + 2):
                        # proveri da li je novo polje unutar matrice, da li je slobodno i da nije "previsoko"
                        unutar_matrice = k >= 0 and k <= 4 and l >= 0 and l <= 4
                        if not unutar_matrice:
                            continue
                        slobodno_polje = node.stanje.matrica[k][l].igrac == None
                        odgovara_broj_spratova = node.stanje.matrica[i][j].broj_spratova <= node.stanje.matrica[k][l].broj_spratova + 1
                        if unutar_matrice and slobodno_polje and odgovara_broj_spratova:
                            # kad imamo sva polja u koja mozemo da idemo sad treba iz njih da nadjemo sva polja u koja mozemo da gradimo
                            for m in range(k - 1, k + 2):
                                for n in range(l - 1, l + 2):
                                    # isto proveravamo da li je ovo polje unutar matrice, da li je slobodno i da li je broj spratova < 4
                                    unutar_matrice = m >= 0 and m <= 4 and n >= 0 and n <= 4
                                    if not unutar_matrice:
                                        continue
                                    slobodno_polje = node.stanje.matrica[m][n].igrac == None
                                    moze_da_se_gradi = node.stanje.matrica[m][n].broj_spratova < 4
                                    if unutar_matrice and slobodno_polje and moze_da_se_gradi:
                                        moguci_potezi.append(Potez(i, j, k, l, m, n))
    return moguci_potezi


# Ima dva parametra, stanje i potez, nad datim stanjem izvrsava zadati potez i novo stanje vraca
def izvrsi_potez(stanje: Stanje, potez: Potez):
    igrac = stanje.matrica[potez.x1][potez.y1].igrac
    stanje.matrica[potez.x1][potez.y1].igrac = None
    stanje.matrica[potez.x2][potez.y2].igrac = igrac
    stanje.matrica[potez.xg][potez.yg].broj_spratova += 1
    return stanje

# prima pocetni cvor stabla, razvija stablo trazene dubine i vraca ga
def kreiraj_stablo(node, dubina):
    if dubina == 0 or node.vrednost == 1 or node.vrednost == -1: # ako je pobedjena ili izgubljena onda nema sta dalje da trazi tu
        return
    
    svi_potezi = svi_moguci_potezi(node)
    for potez in svi_potezi:
        novo_stanje = izvrsi_potez(node.stanje, potez)
        novi_node = Node(novo_stanje, node.igrac, potez)
        node.children.append(novi_node)
        kreiraj_stablo(novi_node, dubina - 1)
    
    return node

# prima pocetni cvor stabla, i vraca najbolje sledece stanje/potez uz pomoc minimax algoritma
def minimax(node):

    pass

# isto kao i ovo iznad samo koristi drugi algoritam
def minimax_alfa_beta(node: Node):
    return node.children[0]

# posto se u zadatku trazi jos jedan treci optimizovani algoritam on ide ovde
def super_zeznuti_algoritam(node):
    pass

#ovo ce vrv da se izbaci
# prima dva stanja kao parametre i vraca potez kojim se prelazi iz stanja1 u stanje 2 u formatu kao sto se trazi u zadatku
def prebaci_u_potez(stanje1, stanje2):
    pass

#glavna funkcija ovog modula, igra poziva ovu funkciju, prosledjuje jos stanje i algoritam koji treba da se koristi a ona vraca sledeci potez
def sledeci_potez(node, algoritam):
    return svi_moguci_potezi(node)[0]


def stampaj_stablo(node):
    print(node.stanje.matrica)
    for n in node.children:
        stampaj_stablo(n)


# testiram neke stvari

stanje = Stanje()
stanje.matrica[2][2].igrac = Igrac.PLAVI
stanje.matrica[4][4].igrac = Igrac.PLAVI
stanje.matrica[1][1].igrac = Igrac.CRVENI
stanje.matrica[3][3].igrac = Igrac.CRVENI

node = Node(stanje, Igrac.PLAVI, Potez(0,0,0,0,0,0))

kreiraj_stablo(node, 3)


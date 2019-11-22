from tabla import Tabla, Igrac, Potez
import math
import random
import copy

#staticka funkcija procene neke tabele, za nju mi je potreban i potez kojim se doslo do te tabele
def staticka_funkcija_procene(tabla: Tabla, potez: Potez, na_potezu: Igrac):
    if tabla.pobeda(na_potezu):
        return 1000000
    if tabla.poraz(na_potezu):
        return -1000000

    m = tabla.matrica[potez.x2][potez.y2].broj_spratova
    rastojanja = 0
    for i in range(5):
        for j in range(5):
            if tabla.matrica[i][j].igrac == na_potezu:
                rastojanja += tabla.rastojanje(i, j, potez.xg, potez.yg)
            elif tabla.matrica[i][j].igrac != na_potezu and tabla.matrica[i][j].igrac != None: # ako je protivnik
                rastojanja -= tabla.rastojanje(i, j, potez.xg, potez.yg)
    l = tabla.matrica[potez.xg][potez.yg].broj_spratova * rastojanja
    return m + l

class Node():

    def __init__(self, tabla: Tabla, vrednost = 0):
        self.tabla = tabla
        self.children = [] # lista cvorova potomaka
        self.vrednost = vrednost


    def kraj_igre(self):
        # proveri da li ima mogucih poteza i da li je nego postavio figuru na polje sa nivoom 3
        return False


#vraca listu svih mogucih validnih poteza iz prosledjene table
def svi_moguci_potezi(node, na_potezu: Igrac):
    #lista mogucih stanja
    moguci_potezi = []

    #ako je igra vec zavrsena u datom stanju onda nista, nema vise poteza, i vracam prazan niz
    #igra je zavrsena ako jedan od igraca dostigne 3 nivo 
    if node.tabla.da_li_je_zauzeo_treci_sprat(na_potezu) or node.tabla.da_li_je_zauzeo_treci_sprat(na_potezu.protivnik()):
        return moguci_potezi

    # pronadji dve figure koje pripadaju trenutnom igracu
    for i in range(5):
        for j in range(5):
            if node.tabla.matrica[i][j].igrac == na_potezu:
                # prodji kroz sva njegova susedna polja
                for k in range(i - 1, i + 2):
                    for l in range(j - 1, j + 2):
                        # proveri da li je novo polje unutar matrice, da li je slobodno i da nije "previsoko"
                        unutar_matrice = k >= 0 and k <= 4 and l >= 0 and l <= 4
                        if not unutar_matrice:
                            continue
                        novo_polje = k != i or l != j # da li se polje razlikuje od onog u kome se sad nalazi
                        slobodno_polje = node.tabla.matrica[k][l].igrac == None
                        odgovara_broj_spratova = node.tabla.matrica[i][j].broj_spratova + 1 >= node.tabla.matrica[k][l].broj_spratova
                        if unutar_matrice and novo_polje and slobodno_polje and odgovara_broj_spratova:
                            # kad imamo sva polja u koja mozemo da idemo sad treba iz njih da nadjemo sva polja u koja mozemo da gradimo
                            for m in range(k - 1, k + 2):
                                for n in range(l - 1, l + 2):
                                    # isto proveravamo da li je ovo polje unutar matrice, da li je slobodno i da li je broj spratova < 4
                                    unutar_matrice = m >= 0 and m <= 4 and n >= 0 and n <= 4
                                    if not unutar_matrice:
                                        continue
                                    novo_polje = m != k or n != l
                                    slobodno_polje = node.tabla.matrica[m][n].igrac == None
                                    moze_da_se_gradi = node.tabla.matrica[m][n].broj_spratova < 4
                                    if unutar_matrice and novo_polje and slobodno_polje and moze_da_se_gradi:
                                        moguci_potezi.append(Potez(i, j, k, l, m, n))
    return moguci_potezi

# prima pocetni cvor stabla, razvija stablo trazene dubine i vraca ga
def kreiraj_stablo(node: Node, dubina: int, na_potezu: Igrac):
    if dubina == 0:
        return

    svi_potezi = svi_moguci_potezi(node, na_potezu)

    for potez in svi_potezi:
        nova_tabla = copy.deepcopy(node.tabla)
        nova_tabla.izvrsi_potez(potez)
        vrednost = staticka_funkcija_procene(nova_tabla, potez, na_potezu)
        novi_node = Node(nova_tabla, vrednost)
        node.children.append(novi_node)
        kreiraj_stablo(novi_node, dubina - 1, na_potezu)
    
    return node

# prima pocetni cvor stabla, i vraca najbolje sledece stanje/potez uz pomoc minimax algoritma
def minimax(node: Node, dubina: int, maximizingPlayer):
    #print("Dubina", dubina)
    if dubina == 0 or len(node.children) == 0:
        return node.vrednost, node.tabla
    if maximizingPlayer:
        value = -math.inf
        tabla = None
        for child in node.children:
            v, t = minimax(child, dubina - 1, False)
            if v > value:
                value = v
                tabla = child.tabla
        return value, tabla
    else:
        value = math.inf
        tabla = None
        for child in node.children:
            v, t = minimax(child, dubina - 1, True)
            if v < value:
                value = v
                tabla = child.tabla
        return value, tabla

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
def sledeci_potez(tabla: Tabla, na_potezu: Igrac, algoritam):
    node = kreiraj_stablo(Node(tabla), 2, na_potezu)
    vrednost, tabla = minimax(node, 2, True)
    print("Vrednost odabranog poteza: ", vrednost)
    return tabla


def stampaj_stablo(node):
    print(node.stanje.matrica)
    for n in node.children:
        stampaj_stablo(n)


# testiram neke stvari

stanje = Tabla()
stanje.matrica[2][2].igrac = Igrac.PLAVI
stanje.matrica[4][4].igrac = Igrac.PLAVI
stanje.matrica[1][1].igrac = Igrac.CRVENI
stanje.matrica[3][3].igrac = Igrac.CRVENI



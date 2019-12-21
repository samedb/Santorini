"""Modul ai je odgovoran za vestacku inteligenciju igre Santorini, sadrzi klase koje implementiraju minimax i minimax + alfa-beta,
funkcije za staticku procenu stanja itd. Sve sto ima veze za AI ove igre nalazi se ovde."""
from tabla import Tabla, IGRAC_CRVENI, IGRAC_PLAVI, protivnik, Potez
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
        return 100
    if tabla.poraz(na_potezu):
        return -100
    # da sprecim postavljanje kupole kada to nije potrebno, privremeno resenje TODO bolje da resim
    # kupolu postavlja samo kada bas mora
    if tabla.matrica[potez.xg][potez.yg].broj_spratova == 4:
        return -50

    n = tabla.matrica[potez.x2][potez.y2].broj_spratova
    rastojanja = 0
    for i in range(5):
        for j in range(5):
            if tabla.matrica[i][j].igrac == na_potezu:
                rastojanja += tabla.rastojanje(i, j, potez.xg, potez.yg)
            elif tabla.matrica[i][j].igrac != na_potezu and tabla.matrica[i][j].igrac != None:  # ako je protivnik
                rastojanja -= tabla.rastojanje(i, j, potez.xg, potez.yg)
    m = tabla.matrica[potez.xg][potez.yg].broj_spratova * rastojanja
    return n + m

def nova_neka_staticka_funkcija_procene(tabla: Tabla, potez: Potez, na_potezu):
    if tabla.pobeda(na_potezu):
        return 100
    if tabla.poraz(na_potezu):
        return -100
    # da sprecim postavljanje kupole kada to nije potrebno, privremeno resenje TODO bolje da resim
    # kupolu postavlja samo kada bas mora,    mozda je ovo i suvisno idk
    #if tabla.matrica[potez.xg][potez.yg].broj_spratova == 4:
    #    return -50
    suma_visina = 0
    for i in range(5):
        for j in range(5):
            if tabla.matrica[i][j].igrac == na_potezu:
                suma_visina += tabla.matrica[i][j].broj_spratova**2
            elif tabla.matrica[i][j].igrac != na_potezu and tabla.matrica[i][j].igrac != None:  # ako je protivnik
                suma_visina -= tabla.matrica[i][j].broj_spratova**2
    return suma_visina

def optimizovana_neka_nova_staticka_funkcija_procene(tabla: Tabla, potez: Potez, na_potezu):
    """Radi isto sto i funkcija iznad samo je malo optimizovana, brza je 40%
    
    :param tabla: Tabla/stanje za koju treba izracunati staticku funkciju procene
    :type tabla: Tabla
    :param potez: Potez koji je doveo to tog stanja
    :type potez: Potez
    :param na_potezu: Igrac za kojeg se racuna staticka funkcija procene
    :type na_potezu: int
    :return: Vrednost staticke funkcije procene
    :rtype: int
    """    
    if not tabla.ima_mogucih_poteza(na_potezu):
        return -100
    elif not tabla.ima_mogucih_poteza(protivnik(na_potezu)):
        return 100
    else:
        suma_visina = 0
        brojac_figura = 0  # zbog ovoga imam 20% ubrzanje, jer prekidam petlje kad nadjem 4 figure
        for i in range(5):
            for j in range(5):
                if brojac_figura == 4:
                    return suma_visina
                if tabla.matrica[i][j].igrac != None:
                    brojac_figura += 1
                    if tabla.matrica[i][j].igrac == na_potezu:
                        if tabla.matrica[i][j].broj_spratova == 3:
                            return 100
                        suma_visina += tabla.matrica[i][j].broj_spratova**2
                    elif tabla.matrica[i][j].igrac != na_potezu:  # protivnik
                        if tabla.matrica[i][j].broj_spratova == 3:
                            return -100
                        suma_visina -= tabla.matrica[i][j].broj_spratova**2
        return suma_visina


def unapredjena_staticka_funkcija_procene(tabla: Tabla, potez: Potez, na_potezu):
    """Ovo je unapredjena staticka funkcija procene f,koja se računa kao 𝑓 = 3 * 𝑛 + 𝑚 + suma_visina + 5 * razlika_u_visini,
    gde je 𝑛 broj pločica odredišnog polja, a 𝑚 broj nivoa na koje se dodaje plocica poomnozen razlikom rastojanja
    sopstvenih i protivnickih igraca od tog polja, suma_visina je zbir visina spostvenih figura umanjen za zbir visina
    protivnickih figura,razlika_u_visini je razlika u visini izmedju prethodne i sadasnje pozicije figure koja se krece.
    Da bi se ova funkcija izracunala pored stanja/table potreban mi je i potez koji dovodi to tog novog stanja kao i
    igrac koji je trenutno na potezu.
    
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
        return 100
    if tabla.poraz(na_potezu):
        return -100
    # da sprecim postavljanje kupole kada to nije potrebno, privremeno resenje TODO bolje da resim
    # kupolu postavlja samo kada bas mora
    if tabla.matrica[potez.xg][potez.yg].broj_spratova == 4:
        return -50

    n = tabla.matrica[potez.x2][potez.y2].broj_spratova
    rastojanja = 0
    suma_visina = 0
    for i in range(5):
        for j in range(5):
            if tabla.matrica[i][j].igrac == na_potezu:
                rastojanja += tabla.rastojanje(i, j, potez.xg, potez.yg)**2
                suma_visina += tabla.matrica[i][j].broj_spratova**2
            elif tabla.matrica[i][j].igrac != na_potezu and tabla.matrica[i][j].igrac != None:  # ako je protivnik
                rastojanja -= tabla.rastojanje(i, j, potez.xg, potez.yg)**2
                suma_visina -= tabla.matrica[i][j].broj_spratova**2
    m = tabla.matrica[potez.xg][potez.yg].broj_spratova * rastojanja
    razlika_u_visini = tabla.matrica[potez.x2][potez.y2].broj_spratova - tabla.matrica[potez.x1][potez.y1].broj_spratova 
    return 3 * n + m + suma_visina + 5 * razlika_u_visini 


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
        for j in range(5):
            if broj_pronadjenih_figura == 2:
                return moguci_potezi
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


class AI(ABC):
    """Abstraktna klasa koju nasledjuju sve klase koje implementiraju neku vrstu vestacke inteligencije.
    Od atributa ima dubinu, funkciju koja racuna staticku vrednost i bool da li treba stampati vrednosti svih mogucih poteza AI algoritma .
    """    

    # TODO dubina ide napolje, zbog iterativnog produbiljivanja
    def __init__(self, stampaj_vrednosti_svih_poteza, dubina = 2, funkcija_procene = staticka_funkcija_procene):
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
    def sledeci_potez(self, tabla, na_potezu, dubina):
        """Glavna funkcija ovog modula, igra poziva ovu funkcija, prosledjuje joj stanje i igraca a ova funkija vraca sledeci potez.
        Ovo je abstraktna funkcija tako da je moraju implementirati sve klase koje nasledjuju AI.
        
        :param tabla: Tabla za koju treba naci sledeci potez
        :type tabla: Tabla
        :param na_potezu: Igrac koji je na potezu i za kojeg treba naci sledeci potez
        :type na_potezu: int
        # TODO dokumentaicja za dubinu
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

    def sledeci_potez(self, tabla, igrac, dubina):
        """Igra poziva ovu funkcija, prosledjuje joj stanje i igraca a ova funkija vraca sledeci potez.
        Ovde se koriti obicni minimax algoritam za nalazenje najboljeg poteza.
        Ovo je abstraktna funkcija tako da je moraju implementirati sve klase koje nasledjuju AI.
        
        :param tabla: Tabla za koju treba naci sledeci potez
        :type tabla: Tabla
        :param igrac: Igrac koji je na potezu, za kojeg treba naci sledeci potez i za koga se kroz algoritam racuna staticka f-ja procene
        :type igrac: int
        """   
        self.dubina = dubina
        svi_potezi = svi_moguci_potezi(tabla, igrac)
        vrednosti = []
        # nadji vrednosti svih mogucih poteza
        for p in svi_potezi:
            nova_tabla = Tabla(tabla)
            nova_tabla.izvrsi_potez(p)
            vrednosti.append(self.minimax(nova_tabla, self.dubina - 1, igrac, False, p))
        
        # stampaj vrednosti svih poteza ako treba
        if self.stampaj_vrednosti_svih_poteza:
            print(f"\n\n\nNa potezu je {igrac}, koristi se algoritam MiniMax NOVI NOVI i vrednsti svih mogucih poteza su:")
            for i in range(len(svi_potezi)):
                print(svi_potezi[i], vrednosti[i])
        
        # nadji najbolji potez i vrati ga
        index_maximuma = vrednosti.index(max(vrednosti))
        return svi_potezi[index_maximuma]

    def minimax(self, tabla, dubina, igrac, maximizing_player, potez):
        """Rekurzivna funkcija koja racuna (samo) vrednost koju ce minimax algoritam vratiti za prosledjenu tabelu/stanje.
        Ovaj algoritam je uradjen po ugledu na psudo kod minimax algoritma sa moodle-a.
        
        :param tabla: Tabla nad kojom treba izvrsavati poteze ili za koju treba racunati staticku funkciju procene
        :type tabla: Tabla
        :param dubina: Dubina razvijanja stabla
        :type dubina: int
        :param igrac: Igrac za kojeg se racuna staticka funkcija procene
        :type igrac: int
        :param maximizing_player: Da li treba uzimati max ili min vrednost od potomaka
        :type maximizing_player: bool
        :param potez: Potez koji je doveo do ovog stanja
        :type potez: Potez
        :return: Vrednost koji ce minimimax algoritam nadji za stablo koje nastaje iz prosledjene table
        :rtype: int
        """
        # ako ne treba dalje razvijati stablo vracamo staticku funkciju procene        
        if dubina == 0:
            return self.funkcija_procene(tabla, potez, igrac)
        
        # pronalazimo sve moguce poteze iz ovog stanja u zavisnosti od toga koji igrac je sada na potezu
        if maximizing_player:
            svi_potezi = svi_moguci_potezi(tabla, igrac)
        else:
            svi_potezi = svi_moguci_potezi(tabla, protivnik(igrac))

        # ako nema mogucih poteza vrati vrednost tog cvora vracamo staticku funkciju procene
        if len(svi_potezi) == 0:
            return self.funkcija_procene(tabla, potez, igrac)
        else: # inace nadji vrednosti svih mogucih poteza iz ovog stanja
            vrednosti = []
            for p in svi_potezi:
                nova_tabla = Tabla(tabla)
                nova_tabla.izvrsi_potez(p)
                vrednosti.append(self.minimax(nova_tabla, dubina - 1, igrac, not maximizing_player, p))

        # nalazimo minimalnu ili maksimalu vrednost medju potomcima cvora i postavljamo je za vrednost tog cvora
        if maximizing_player:
            return max(vrednosti)
        else:
            return min(vrednosti)


class MiniMaxAlfaBeta(AI): 
    """Klasa koja nasledjuje AI i implementira MiniMax algoritam sa alfa-beta odsecanjem""" 
    #TODO da se dubina izbaci iz konstruktora i da se samo nalazi u funkciji sledeci_potez, to da se uradi za sve ove klase i za AI isto
    def __init__(self, stampaj_vrednosti_svih_poteza,dubina = 3, funkcija_procene = staticka_funkcija_procene):    
        """Konsturtor sa parametrima koji postavlja vredsnoti atributa klase.
        
        :param stampaj_vrednosti_svih_poteza: Da li treba stampati vrednost svakom moguceg poteza AI
        :type stampaj_vrednosti_svih_poteza: bool
        :param dubina: Dubina do koje treba pretrazivati stablo igre, defaults to 3
        :type dubina: int, optional
        :param funkcija_procene: Funkcija sa kojom se racuna staticka vrednost, defaults to staticka_funkcija_procene
        :type funkcija_procene: function, optional
        """  
        super().__init__(stampaj_vrednosti_svih_poteza, dubina, funkcija_procene)


    def sledeci_potez(self, tabla, na_potezu, dubina):
        """Igra poziva ovu funkcija, prosledjuje joj stanje i igraca a ova funkija vraca sledeci potez.
        Ovde se koriti minimax sa alfa-beta odsecanjem za nalazenje najboljeg poteza.
        Ovo je abstraktna funkcija tako da je moraju implementirati sve klase koje nasledjuju AI.
        
        :param tabla: Tabla za koju treba naci sledeci potez
        :type tabla: Tabla
        :param na_potezu: Igrac koji je na potezu i za kojeg treba naci sledeci potez
        :type na_potezu: int
        """     
        self.dubina = dubina
        self.na_potezu = na_potezu
        self.lista_poteza_i_njihovih_vrednosti = []
        v = self.max_value(tabla, self.dubina, None, -1000, 1000)

        # stampaj vrednosti svih poteza
        if self.stampaj_vrednosti_svih_poteza:
            print(f"\n\n\nNa potezu je {self.na_potezu}, koristi se algoritam MiniMax sa Alfa Beta odsecanjem i vrednsti svih mogucih poteza su:")
            for p in self.lista_poteza_i_njihovih_vrednosti:
                print(p[1], p[0])
        
        # vrati najbolji potez, tj. potez iz liste poteza koji ima vrednost koju vraca max_value funkcija
        for p in self.lista_poteza_i_njihovih_vrednosti:
            if p[0] == v:
                return p[1]

    def max_value(self, tabla, dubina, potez, alfa, beta):
        """Vraca maksimalnu vrednost podstabla uz upotrebu minimax algoritma sa alfa beta odsecanjem.
        
        :param tabla: Trenutna tabla/stanje igre, raspored figura i spratova
        :type tabla: Tabla
        :param dubina: Dubina do koje treba pretraziti stablo
        :type dubina: int
        :param potez: Potez koji je doveo do ove table/stanja
        :type potez: Potez
        :param alfa: Vrednost najboljeg izbora koji smo pronasli do sada tokom putanje za MAX
        :type alfa: int
        :param beta: Vrednost najboljeg izbofa (ovde je to najmanja vrednost) koju smo pronali do sada tokom putanja za MIN
        :type beta: int
        :return: Vraca maksimalu vrednost podstabla uz uptrebu minimax algoritma sa alfa beta odsecanjem
        :rtype: int
        """        
        if dubina == 0:
            return self.funkcija_procene(tabla, potez, self.na_potezu)

        v = -1000

        svi_potezi = svi_moguci_potezi(tabla, self.na_potezu)
        # ako nema mogucih poteza vrati vrednost tog cvora
        if len(svi_potezi) == 0:
            return self.funkcija_procene(tabla, potez, self.na_potezu)
        else:
            for p in svi_potezi:
                nova_tabla = Tabla(tabla)
                nova_tabla.izvrsi_potez(p)
                nova_vrednost = self.min_value(nova_tabla, dubina - 1, p, alfa, beta)

                # sad upisujem sve poteze u self.lista_poteza da bih na kraju znao koji da uzmem
                if dubina == self.dubina:
                    self.lista_poteza_i_njihovih_vrednosti.append((nova_vrednost, p))

                v = max(v, nova_vrednost)
                if v >= beta:
                    return v
                alfa = max(alfa, v)
        return v

    def min_value(self, tabla, dubina, potez, alfa, beta):
        """Vraca minimalnu vrednost podstabla uz upotrebu minimax algoritma sa alfa beta odsecanjem.
        
        :param tabla: Trenutna tabla/stanje igre, raspored figura i spratova
        :type tabla: Tabla
        :param dubina: Dubina do koje treba pretraziti stablo
        :type dubina: int
        :param potez: Potez koji je doveo do ove table/stanja
        :type potez: Potez
        :param alfa: Vrednost najboljeg izbora koji smo pronasli do sada tokom putanje za MAX
        :type alfa: int
        :param beta: Vrednost najboljeg izbofa (ovde je to najmanja vrednost) koju smo pronali do sada tokom putanja za MIN
        :type beta: int
        :return: Vraca minimalnu vrednost podstabla uz uptrebu minimax algoritma sa alfa beta odsecanjem
        :rtype: int
        """       
        if dubina == 0:
            return self.funkcija_procene(tabla, potez, self.na_potezu)

        v = 1000

        svi_potezi = svi_moguci_potezi(tabla, protivnik(self.na_potezu))
        # ako nema mogucih poteza vrati vrednost tog cvora
        if len(svi_potezi) == 0:
            return self.funkcija_procene(tabla, potez, self.na_potezu)
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



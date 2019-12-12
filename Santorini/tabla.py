from enum import Enum

IGRAC_PLAVI = 0
IGRAC_CRVENI = 1

def protivnik(igrac):
    """Vraca protivnika igraca kojeg prosledimo kao parametar
    
    :param igrac: Trenutni igrac
    :type igrac: int
    :return: Protivnik trenutnog igraca
    :rtype: int
    """ 
    return 1 - igrac

class GameState(Enum):
    """asdf asdf asdf 
    
    :param Enum: [description]
    :type Enum: [type]
    """    
    POSTAVLJANJE_FIGURA = 0
    SELEKTOVANJE_FIGURE = 1
    POMERANJE_FIGURE = 2
    GRADNJA = 3 
    KRAJ_IGRE = 4

class Potez():
    """sadf fdas dsf sad 
    
    :return: [description]
    :rtype: [type]
    """    
    # x1,y1 su pocetna pozicija, x2, y2 su nova pozicija, a xg, yg su pozicija gradnje
    def __init__(self, x1, y1, x2, y2, xg, yg):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.xg = xg
        self.yg = yg

    # staticka metoda koja prima string jednog poteza kako se upisuje u fajl i pretrvara u objekat klase Potez koji vraca
    @staticmethod
    def iz_stringa(text):
        p = Potez(0, 0, 0, 0, 0, 0)
        reci = text.split(" ")
        p.x1, p.y1 = Potez.string_u_koordinate(reci[0])
        p.x2, p.y2 = Potez.string_u_koordinate(reci[1])
        p.xg, p.yg = Potez.string_u_koordinate(reci[2])
        return p

    # staticka metoda koja prima string jednog polja npr. A0 ili D3 i vraca njegove x i y koordinate
    @staticmethod
    def string_u_koordinate(text):
        x = ord(text[0]) - ord("A")
        y = ord(text[1]) - ord("0")
        return x, y

    # staticka metoda koja prima x i y koordinate i vraca string
    @staticmethod
    def koordinate_u_string(x, y):
        return f"{chr(x + 65)}{y}"

    # preklopljenja funkcija str koja ispisuje Potez u formatu koji se trazi u zadatku npr. A0 A1 B2
    def __str__(self):
        return f"{chr(self.x1 + 65)}{self.y1} {chr(self.x2 + 65)}{self.y2} {chr(self.xg + 65)}{self.yg}"

    # isto ovo gore
    def __repr__(self):
        return self.__str__()



class Polje():
    broj_spratova = 0
    igrac = None


class Tabla():

    def __init__(self, tabla = None):
        self.matrica = ((Polje(), Polje(), Polje(), Polje(), Polje()),
                        (Polje(), Polje(), Polje(), Polje(), Polje()),
                        (Polje(), Polje(), Polje(), Polje(), Polje()),
                        (Polje(), Polje(), Polje(), Polje(), Polje()),
                        (Polje(), Polje(), Polje(), Polje(), Polje()))
        
        # kopiranje tabele koja se prosledi u konstruktoru, nesto kao copy konstruktor 
        if tabla != None:
            for i in range(5):
                for j in range(5):
                    self.matrica[i][j].broj_spratova = tabla.matrica[i][j].broj_spratova
                    if tabla.matrica[i][j].igrac != None:
                        self.matrica[i][j].igrac = tabla.matrica[i][j].igrac



    def postavi_figuru(self, x, y, igrac):
        if self.matrica[x][y].igrac == None:
            self.matrica[x][y].igrac = igrac


    def pomeri_figuru(self, x1, y1, x2, y2):
        figura = self.matrica[x1][y1].igrac
        self.matrica[x1][y1].igrac = None
        self.matrica[x2][y2].igrac = figura

    def gradi(self, x, y):
        self.matrica[x][y].broj_spratova += 1

    # ovo leti napolje, a mozda i ostaje
    def izvrsi_potez(self, potez: Potez):
        self.pomeri_figuru(potez.x1, potez.y1, potez.x2, potez.y2)
        self.gradi(potez.xg, potez.yg)

    def zauzeo_treci_sprat(self, igrac):
        for i in range(5):
            for j in range(5):
                if self.matrica[i][j].broj_spratova == 3 and self.matrica[i][j].igrac == igrac:
                    return True
        return False

    def ima_mogucih_poteza(self, igrac):
        for x in range(5):
            for y in range(5):
                if self.matrica[x][y].igrac == igrac:
                    # prodji kroz sva susedna polja i proveri da li moze na njih da predje, ako ne moze onda je izgubio 
                    for i in range(x - 1, x + 2):
                        for j in range(y - 1, y + 2):
                            if i >= 0 and i <= 4 and j >= 0 and j <= 4 and self.matrica[i][j].igrac == None and self.matrica[i][j].broj_spratova <= self.matrica[x][y].broj_spratova + 1:
                                return True
        return False
    
    def pobeda(self, na_potezu):
        return self.zauzeo_treci_sprat(na_potezu) or not self.ima_mogucih_poteza(protivnik(na_potezu))

    def poraz(self, na_potezu):
        return self.zauzeo_treci_sprat(protivnik(na_potezu)) or not self.ima_mogucih_poteza(na_potezu)

    def pronadji_dozvoljena_polja(self, game_state: GameState, x , y, igrac_na_potezu = None):
        dozvoljena_polja = []
        if game_state == GameState.POSTAVLJANJE_FIGURA:
            for i in range(0, 5):
                for j in range(0, 5):
                    if self.matrica[i][j].igrac == None:
                        dozvoljena_polja.append((i, j))
        elif game_state == GameState.SELEKTOVANJE_FIGURE:
            for i in range(0, 5):
                for j in range(0, 5):
                    if self.matrica[i][j].igrac == igrac_na_potezu:
                        dozvoljena_polja.append((i, j))
        elif game_state == GameState.POMERANJE_FIGURE:
            # moze da klikne i na svoju drugu figuru
            for i in range(5):
                for j in range(5):
                    if self.matrica[i][j].igrac == igrac_na_potezu:
                        dozvoljena_polja.append((i, j))
            # prodji kroz sva polja u neposrednoj blizini selektovane figure
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if i >= 0 and i <= 4 and j >= 0 and j <= 4 and self.matrica[i][j].igrac == None and self.matrica[i][j].broj_spratova <= self.matrica[x][y].broj_spratova + 1 and self.matrica[i][j].broj_spratova < 4:
                        dozvoljena_polja.append((i, j))
        elif game_state == GameState.GRADNJA:
            # prodji kroz sva polja u neposrednoj blizini selektovane figure
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if i >= 0 and i <= 4 and j >= 0 and j <= 4 and self.matrica[i][j].igrac == None and self.matrica[i][j].broj_spratova < 4:  
                        dozvoljena_polja.append((i, j))
        return dozvoljena_polja
        
    def rastojanje(self, x1, y1, x2, y2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return max(dx, dy)

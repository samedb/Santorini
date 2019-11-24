from enum import Enum

class Igrac(Enum):
    PLAVI = 0
    CRVENI = 1

    def protivnik(self):
        if self == Igrac.PLAVI:
            return Igrac.CRVENI
        else:
            return Igrac.PLAVI


class GameState(Enum):
    POSTAVLJANJE_FIGURA = 0
    SELEKTOVANJE_FIGURE = 1
    POMERANJE_FIGURE = 2
    GRADNJA = 3 
    KRAJ_IGRE = 4

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



class Polje():
    broj_spratova = 0
    igrac = None


class Tabla():

    def __init__(self):
        self.matrica = []
        for i in range (5):
            red = []
            for j in range(5):
                polje = Polje()
                red.append(polje)
            self.matrica.append(red)


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

    def zauzeo_treci_sprat(self, igrac: Igrac):
        for i in range(5):
            for j in range(5):
                if self.matrica[i][j].broj_spratova == 3 and self.matrica[i][j].igrac == igrac:
                    return True
        return False

    def ima_mogucih_poteza(self, igrac: Igrac):
        for x in range(5):
            for y in range(5):
                if self.matrica[x][y].igrac == igrac:
                    # prodji kroz sva susedna polja i proveri da li moze na njih da predje, ako ne moze onda je izgubio 
                    for i in range(x - 1, x + 2):
                        for j in range(y - 1, y + 2):
                            if i >= 0 and i <= 4 and j >= 0 and j <= 4 and self.matrica[i][j].igrac == None and self.matrica[i][j].broj_spratova <= self.matrica[x][y].broj_spratova + 1:
                                return True
        return False
    
    def pobeda(self, na_potezu: Igrac):
        return self.zauzeo_treci_sprat(na_potezu) or not self.ima_mogucih_poteza(na_potezu.protivnik())

    def poraz(self, na_potezu: Igrac):
        return self.zauzeo_treci_sprat(na_potezu.protivnik()) or not self.ima_mogucih_poteza(na_potezu)

    def pronadji_dozvoljena_polja(self, game_state: GameState, x , y, igrac_na_potezu: Igrac = None):
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
        return abs(dx - dy)
    

"""Modul tabla sadrzi funkcije i pomocne klase koje se koriste u ai.py i igra.py.
To su klase Polje, Tabla, Potez, GameState"""
from enum import Enum


#TODO komentari
class Igrac:
    NIJEDAN = 0
    IGRAC_PLAVI = 1
    IGRAC_CRVENI = 2



def protivnik(igrac):
    """Vraca protivnika igraca kojeg prosledimo kao parametar.
    
    :param igrac: Trenutni igrac
    :type igrac: int
    :return: Protivnik trenutnog igraca
    :rtype: int
    """ 
    return 3 - igrac


class GameState(Enum):
    """Nasledjuje klasu Enum i tako dobijamo enumeraciju u Python-u. Ova klasa sadrzi sva moguca stanja igre.
    """    
    POSTAVLJANJE_FIGURA = 0
    SELEKTOVANJE_FIGURE = 1
    POMERANJE_FIGURE = 2
    GRADNJA = 3 
    KRAJ_IGRE = 4


class Potez:
    """Preko ove klase predstavlja se jedan potez u igri Santorini, potez se sastoji od pomeranja i gradnje.
    Prema tome od atributa treba da sadrzi pocetno polje, odredisno polje i polje na kojem se gradi.
    """    
    # x1,y1 su pocetna pozicija, x2, y2 su nova pozicija, a xg, yg su pozicija gradnje
    def __init__(self, x1, y1, x2, y2, xg, yg):
        """Konstruktor klase koji inicijalizuje pocetno polje, odredisno polje i polje na kojem se gradi.
        
        :param x1: x koordinata pocetnog polja
        :type x1: int
        :param y1: y koordinata pocetnog polja
        :type y1: int
        :param x2: x koordinata odredisnog polja
        :type x2: int
        :param y2: y koordinata odredisnog polja
        :type y2: int
        :param xg: x koordinata polja na kojem se gradi
        :type xg: int
        :param yg: y koordinata polja na kojem se gradi
        :type yg: int
        """        
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.xg = xg
        self.yg = yg

    @staticmethod
    def iz_stringa(text):
        """Staticka funkcija koja prima string jednog poteza kako se on upisuje u fajl i
        pretvara ga u objekat klase Potez koji vraca.
        
        :param text: Potez u tekstualnom obliku, onako kako se pise u fajlu
        :type text: str
        :return: Objekat klase Potez koji odgovara ulaznog tekstu
        :rtype: Potez
        """        
        p = Potez(0, 0, 0, 0, 0, 0)
        reci = text.split(" ")
        p.x1, p.y1 = Potez.string_u_koordinate(reci[0])
        p.x2, p.y2 = Potez.string_u_koordinate(reci[1])
        p.xg, p.yg = Potez.string_u_koordinate(reci[2])
        return p

    @staticmethod
    def string_u_koordinate(text):
        """Staticka funkcija koja prima string jednog polja npr. A0 ili D3 i vraca njegove x i y koordinate.
        
        :param text: Polje u tekstualnog obliku, koje treba prebaciti u x i y koordinate    
        :type text: str
        :return: x i y koordinate prosledjenog polja
        :rtype: int
        """               
        x = ord(text[0]) - ord("A")
        y = ord(text[1]) - ord("0")
        return x, y

    @staticmethod
    def koordinate_u_string(x, y):
        """Staticka funkija koja prima x i y kooridnate i vraca string koji dogovara tim koordinatama npr. B2, C0.
        
        :param x: x koordinata polja
        :type x: int
        :param y: y koordinata polja
        :type y: int
        :return: Polje u tekstualnom obliku
        :rtype: str
        """        
        return f"{chr(x + 65)}{y}"

    def __str__(self):
        """Preklopljenja funkcija str koja ispisuje Potez u formatu koji se trazi u zadatku npr. A0 A1 B2.
        
        :return: Potez u tekstualnom obliku kako se trazi u zadatku 
        :rtype: str
        """        
        return f"{Potez.koordinate_u_string(self.x1, self.y1)} {Potez.koordinate_u_string(self.x2, self.y2)} {Potez.koordinate_u_string(self.xg, self.yg)}"

    def __repr__(self):
        # isto kao i __str__
        return self.__str__()
        

class Polje:
    """Klasa koja predstavlja jedno polje u tabli, polje je opisano brojem spratova
    i igracem koji se trenutno nalazi u tom polju."""
    broj_spratova = 0
    igrac = Igrac.NIJEDAN


class Tabla:
    """Tabla je matrica objekata klase Polje i predstavlja glavnu klasu za igru Santorini."""

    def __init__(self, tabla = None):
        """Konstruktor klase Tabla, kreira matricu Polja koja je u pocetku prazna.
        On je istovremeno i copy construktor (posto u pythonu mora da ima samo jedan ctor), ukoliko se kao drugi
        parametar prosledi tabla on kopira njen sadrzaj u trenutnu tablu. Ovo je uradjeno zbog performansi, funkcija
        koji ima python copy.deepcopy(object) je bila previse spora pa sam napravio svoj copy ctor.
        
        :param tabla: tabla ciji sadrzaj treba prekopriati u ovom objektu, defaults to None
        :type tabla: Tabla, optional
        """        
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
                    self.matrica[i][j].igrac = tabla.matrica[i][j].igrac

    def postavi_figuru(self, x, y, igrac):
        """Postavlja figuru igraca na koordinate x, y u tabli ako je to polje slobodno.
        
        :param x: x koordinata polja gde treba postaviti figuru
        :type x: int
        :param y: y koordinata polja gde treba postaviti figuru
        :type y: int
        :param igrac: igrac (plavi ili crveni) koji treba postaviti u datom polju
        :type igrac: int
        """        
        if self.matrica[x][y].igrac == Igrac.NIJEDAN:
            self.matrica[x][y].igrac = igrac

    def pomeri_figuru(self, x1, y1, x2, y2):
        """Pomera figuru sa pocetnog na odredisno polje.
        
        :param x1: x koordinata pocetnog polja
        :type x1: int
        :param y1: y koordinata pocetnog polja
        :type y1: int
        :param x2: x koordinata odredisnog polja
        :type x2: int
        :param y2: y koordinata odredisnog polja
        :type y2: int
        """ 
        figura = self.matrica[x1][y1].igrac
        self.matrica[x1][y1].igrac = Igrac.NIJEDAN
        self.matrica[x2][y2].igrac = figura

    def gradi(self, x, y):
        """Gradi jedan sprat na polju x, y.
        
        :param x: x koordinata polja gde treba graditi sprat
        :type x: int
        :param y: y koordinata polja gde treba graditi sprat
        :type y: int
        """        
        self.matrica[x][y].broj_spratova += 1

    def izvrsi_potez(self, potez: Potez):
        """Izvrsava dati potez nam tablom, tako sto poziva funkije pomeri_figuru i gradi sa atributima prosledjenog poteza.
        
        :param potez: Potez koji treba izvrsiti
        :type potez: Potez
        """        
        self.pomeri_figuru(potez.x1, potez.y1, potez.x2, potez.y2)
        self.gradi(potez.xg, potez.yg)

    def zauzeo_treci_sprat(self, igrac):
        """Prolazi kroz celu matricu/tablu i proverava da li je igrac zauzeo treci sprat.
        
        :param igrac: Igrac za kojeg proveravamo da li zauzeo treci sprat
        :type igrac: int
        :return: True ako je zauzeo treci sprat inace False
        :rtype: bool
        """        
        for i in range(5):
            for j in range(5):
                if self.matrica[i][j].broj_spratova == 3 and self.matrica[i][j].igrac == igrac:
                    return True
        return False

    def ima_mogucih_poteza(self, igrac):
        """Proverava za datog igraca da li mu je preostalo ispravnih poteza.
        
        :param igrac: Igrac za kojeg se proverava da li ima mogucih poteza
        :type igrac: int
        :return: True ako ima mogucih poteza, inace False
        :rtype: bool
        """
        for x in range(5):
            for y in range(5):
                if self.matrica[x][y].igrac == igrac:
                    # prodji kroz sva susedna polja i proveri da li moze na njih da predje, ako ne moze onda je izgubio 
                    for i in range(x - 1, x + 2):
                        for j in range(y - 1, y + 2):
                            if i >= 0 and i <= 4 and j >= 0 and j <= 4 and self.matrica[i][j].igrac == Igrac.NIJEDAN and self.matrica[i][j].broj_spratova <= self.matrica[x][y].broj_spratova + 1:
                                return True
        return False
    
    def pobeda(self, na_potezu):
        """Proverava da li je dati igrac pobedio.
        
        :param na_potezu: Igrac za kojeg se proverava da li je pobedio
        :type na_potezu: int
        :return: True ako je pobedio, inace False
        :rtype: bool
        """        
        return self.zauzeo_treci_sprat(na_potezu) or not self.ima_mogucih_poteza(protivnik(na_potezu))

    def poraz(self, na_potezu):
        """Proverava da li je dati igrac izgubio.
        
        :param na_potezu: Igarc za kojeg se proverava da li je izgubio
        :type na_potezu: int
        :return: True ako je izgubio, inace False
        :rtype: bool
        """        
        return self.zauzeo_treci_sprat(protivnik(na_potezu)) or not self.ima_mogucih_poteza(na_potezu)

    def pronadji_dozvoljena_polja(self, game_state: GameState, x , y, igrac_na_potezu = Igrac.NIJEDAN):
        """Funkcija koja nalazi listu svih dozvoljenih polja koje igrac moze da selektuje, to zavisi od mnogih faktora
        od trenutnog gameState-a, od pozicije selektovanog igraca (x, y) itd.
        
        :param game_state: Trenutni GameState 
        :type game_state: GameState
        :param x: x koordinata igraca ili selektovanog polja
        :type x: int
        :param y: y koordinata igraca ili selektovanog polja
        :type y: int
        :param igrac_na_potezu: Igrac koji je trenutno na potezu i za kojeg se nalaze dozvoljena polja, defaults to None
        :type igrac_na_potezu: int, optional
        :return: Listu dozvoljenih polja
        :rtype: list
        """        
        dozvoljena_polja = []
        if game_state == GameState.POSTAVLJANJE_FIGURA:
            for i in range(0, 5):
                for j in range(0, 5):
                    if self.matrica[i][j].igrac == Igrac.NIJEDAN:
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
                    if i >= 0 and i <= 4 and j >= 0 and j <= 4 and self.matrica[i][j].igrac == Igrac.NIJEDAN and self.matrica[i][j].broj_spratova <= self.matrica[x][y].broj_spratova + 1 and self.matrica[i][j].broj_spratova < 4:
                        dozvoljena_polja.append((i, j))
        elif game_state == GameState.GRADNJA:
            # prodji kroz sva polja u neposrednoj blizini selektovane figure
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if i >= 0 and i <= 4 and j >= 0 and j <= 4 and self.matrica[i][j].igrac == Igrac.NIJEDAN and self.matrica[i][j].broj_spratova < 4:  
                        dozvoljena_polja.append((i, j))
        return dozvoljena_polja
        
    def rastojanje(self, x1, y1, x2, y2):
        """Funkcija koja racuna rastojanje izmedju dva polja u tabli, ne uzima u obzir da li ima prepreka vec samo racuna rastojanje "vazdusnom linijom".
        
        :param x1: x koordinata prvog polja
        :type x1: int
        :param y1: y koordinata prvog polja
        :type y1: int
        :param x2: x koordinata drugog polja
        :type x2: int
        :param y2: y koordinata drugog polja
        :type y2: int
        :return: Rastojanje izmedju ova dva polja
        :rtype: int
        """        
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return max(dx, dy)

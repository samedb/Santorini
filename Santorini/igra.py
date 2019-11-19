from tkinter import *
from enum import Enum
from tkinter import messagebox


class Igrac(Enum):
    PLAVI = 0
    CRVENI = 1


class GameState(Enum):
    POSTAVLJANJE_FIGURA = 0
    SELEKTOVANJE_FIGURE = 1
    POMERANJE_FIGURE = 2
    GRADNJA = 3 
    KRAJ_IGRE = 4

class Polje():
    broj_spratova = 0
    igrac = None

    def uradiNesto(self, event):
        print("Radim nesto")


class Stanje():

    def __init__(self):
        self.matrica = []
        for i in range (0, 5):
            red = []
            for j in range(0, 5):
                polje = Polje()
                #polje.broj_spratova = i
                #polje.igrac = j
                red.append(polje)
            self.matrica.append(red)

    def izvrsi_potez(self, potez):
        # todo 
        print("Izvrsava se potez")


class Tabla(Canvas):

    def __init__(self, parent):
        Canvas.__init__(self, parent)
        self.config(width = 500, height = 550) 
        self.bind("<Button-1>", self.mouse_click)
        #inicijalizacije matrice
        self.stanje = Stanje()
        self.na_potezu = Igrac.PLAVI # plavi igrac je prvi na potezu
        self.game_state = GameState.POSTAVLJANJE_FIGURA # u pocetku svi igraci postavljaju svoje figure na tablu
        self.broj_figura = 0 # treba mi za prvu fazu gde se postavljaju figure
        self.sastavi_poruku()
        self.dozvoljena_polja = []
        self.selektovana_figura = None
        self.crtaj(self.stanje)
    
    def crtaj(self, stanje):
        self.delete("all")
        for i in range (0, 5):
            for j in range(0, 5):
                #izracunaj koordinate tog polja
                x1 = i * 100
                y1 = j * 100 + 50
                #nacrtaj pozadinu
                if self.selektovana_figura == (i, j): # ako je to polje na kojem se nalazi selektovana figura onda oboji zutom bojom
                    boja = "yellow"
                elif (i, j) in self.dozvoljena_polja: #ako je to polje dozvoljeno u sledecem potezu onda zelenom bojom
                    boja = "green"
                else:
                    boja = "grey" # ako nije nista od toga onda siva boja
                self.create_rectangle(x1 + 2, y1 + 2, x1 + 98, y1 + 98, fill = boja)
                #nacrtaj spratove
                stepen = stanje.matrica[i][j].broj_spratova
                if stepen >= 1:
                    self.create_rectangle(x1 + 8, y1 + 8, x1 + 92, y1 + 92, width = 3)
                if stepen >= 2:
                    self.create_rectangle(x1 + 15, y1 + 15, x1 + 85, y1 + 85, width = 3)
                if stepen >= 3:
                    self.create_rectangle(x1 + 25, y1 + 25, x1 + 75, y1 + 75, width = 3)
                if stepen >= 4:
                    self.create_oval(x1 + 30, y1 + 30, x1 + 70, y1 + 70, fill = "black")
                #nacrtaj igraca
                if stanje.matrica[i][j].igrac == Igrac.PLAVI: # 0 znaci plavi igrac
                    self.create_oval(x1 + 30, y1 + 30, x1 + 70, y1 + 70, fill = "blue")
                elif stanje.matrica[i][j].igrac == Igrac.CRVENI: # 1 znaci crveni igrac
                    self.create_oval(x1 + 30, y1 + 30, x1 + 70, y1 + 70, fill = "red")

        self.create_text(250, 25, text = self.poruka, font = "Airal 12")

    def mouse_click(self, e):
        print(e.x, e.y) # koordinate piksela na koji je klikuo mis u ovom canvasu
        #ako je kliknuo vam table ili je kraj meca
        if e.y < 50 or self.game_state == GameState.KRAJ_IGRE:
            return
        # preracunavanje tih kooridnata u indekse polja tabele
        x = int(e.x / 100)
        y = int((e.y - 50) / 100)
        print(f"Polje koje je pritisnuto je: {x}, {y}")
        #self.stanje.matrica[x][y].broj_spratova += 1

        try:
            if self.game_state == GameState.POSTAVLJANJE_FIGURA:
                self.postavi_figuru(x, y) 
                self.broj_figura += 1
                if self.broj_figura == 2:
                    self.zameni_igraca()
                elif self.broj_figura == 4:
                    self.game_state = GameState.SELEKTOVANJE_FIGURE
                    self.zameni_igraca()
                    print("Sad pocinje prava igra")

            elif self.game_state == GameState.SELEKTOVANJE_FIGURE:
                self.selektuj_figuru(x, y)
                self.game_state = GameState.POMERANJE_FIGURE
                self.sastavi_poruku()
                self.pronadji_dozvoljena_polja()

            elif self.game_state == GameState.POMERANJE_FIGURE:
                #ako klikne na istu figuru ili na svoju drugu figuru
                if self.stanje.matrica[x][y].igrac == self.na_potezu:
                    self.selektuj_figuru(x, y)
                else:
                    x1, y1 = self.selektovana_figura
                    self.pomeri_figuru(x1, y1, x, y)
                    self.game_state = GameState.GRADNJA
                
                self.pronadji_dozvoljena_polja()
                self.sastavi_poruku()
            elif self.game_state == GameState.GRADNJA:
                self.gradi(x, y)
                self.game_state = GameState.SELEKTOVANJE_FIGURE
                self.sastavi_poruku()
                self.zameni_igraca()
                self.pronadji_dozvoljena_polja()

                #proveri da li je kraj meca, tj da li ima mogucih poteza za igraca na potezu
                if not self.ima_mogucih_poteza():
                    if self.na_potezu == Igrac.CRVENI:
                        pobednik = Igrac.PLAVI
                    else:
                        pobednik = Igrac.CRVENI
                    self.pobeda(f"Pobedio je {pobednik} jer {self.na_potezu} nema mogucih poteza!")

                
        except Exception as error:
            print(error)


        #crtaj ide na kraj ove funkcije
        self.crtaj(self.stanje)

    def selektuj_figuru(self, x, y):
        if self.stanje.matrica[x][y].igrac == self.na_potezu:
            self.selektovana_figura = (x, y)
        else:
            raise Exception("Morate da selektujete neku vasu figuru")



    def postavi_figuru(self, x, y):
        if self.stanje.matrica[x][y].igrac == None:
            self.stanje.matrica[x][y].igrac = self.na_potezu
        else:
            raise Exception("Polje je vec zauzeto")

    def pomeri_figuru(self, x1, y1, x2, y2):
        if (x2, y2) in self.dozvoljena_polja:
            figura = self.stanje.matrica[x1][y1].igrac
            self.stanje.matrica[x1][y1].igrac = None
            self.stanje.matrica[x2][y2].igrac = figura
            self.selektovana_figura = (x2, y2) # slektovana figura/polje je polje gde se sada nalazi figura, jer gradimo u susednim poljima

            #proveri da li je figura postavljena na polje sa brojem spratova 3, ako jeste onda je pobeda
            if self.stanje.matrica[x2][y2].broj_spratova == 3:
                self.crtaj(self.stanje)
                self.pobeda(f"Pobedio je {self.na_potezu} jer je zauzeo polje sa nivoom 3!")
        else:
            raise Exception("Nedozvoljen potez")

    def gradi(self, x, y):
        if (x, y) in self.dozvoljena_polja:
            self.stanje.matrica[x][y].broj_spratova += 1
        else:
            raise Exception("Ne mozete da gradite na ovom polju")

    def zameni_igraca(self):
        if self.na_potezu == Igrac.PLAVI:
            self.na_potezu = Igrac.CRVENI
        else:
            self.na_potezu = Igrac.PLAVI

        self.sastavi_poruku()
        self.pronadji_dozvoljena_polja()
        self.selektovana_figura = None


        '''
            if trenutni igrac == AI
                sledeci_potez = AI.potez(trenutno_stanje)
                izvrsi_potez(sledeci_potez) # ova funkcija crta redom sve korake, vise puta poziva funkciju crtaj da bi pokazala kako se sleketuje figura
                pomera figura i gradi, sa nekim delay-om izmedju koraka
                zameni_igraca()
        '''

    def pobeda(self, poruka):
        self.game_state = GameState.KRAJ_IGRE
        messagebox.showinfo("Pobeda", poruka)
        self.crtaj(self.stanje)

    def ima_mogucih_poteza(self):
        for x in range(0, 5):
            for y in range(0, 5):
                if self.stanje.matrica[x][y].igrac == self.na_potezu:
                    # prodji kroz sva susedna polja i proveri da li moze na njih da predje, ako ne moze onda je izgubio 
                    for i in range(x - 1, x + 2):
                        for j in range(y - 1, y + 2):
                            if i >= 0 and i <= 4 and j >= 0 and j <= 4 and self.stanje.matrica[i][j].igrac == None and self.stanje.matrica[i][j].broj_spratova <= self.stanje.matrica[x][y].broj_spratova + 1:
                                print("Prvo moguce polje je ", i , j, " za " , x, y)
                                return True
        return False

    def sastavi_poruku(self):
        #if self.game_state != GameState.KRAJ_IGRE:
        self.poruka = f"Na potezu je {self.na_potezu} \na gamestate je {self.game_state}"

    def pronadji_dozvoljena_polja(self):
        self.dozvoljena_polja.clear()

        if self.game_state == GameState.SELEKTOVANJE_FIGURE:
            for i in range(0, 5):
                for j in range(0, 5):
                    if self.stanje.matrica[i][j].igrac == self.na_potezu:
                        self.dozvoljena_polja.append((i, j))
        elif self.game_state == GameState.POMERANJE_FIGURE:
            x, y = self.selektovana_figura
            # prodji kroz sva polja u neposrednoj blizini selektovane figure
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if i >= 0 and i <= 4 and j >= 0 and j <= 4 and self.stanje.matrica[i][j].igrac == None and self.stanje.matrica[i][j].broj_spratova <= self.stanje.matrica[x][y].broj_spratova + 1 and self.stanje.matrica[i][j].broj_spratova < 4:   #ovde nisam siguran da li moze figura da se spusit sa 2. na 0. sprat
                        self.dozvoljena_polja.append((i, j))
        elif self.game_state == GameState.GRADNJA:
            x, y = self.selektovana_figura
            # prodji kroz sva polja u neposrednoj blizini selektovane figure
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if i >= 0 and i <= 4 and j >= 0 and j <= 4 and self.stanje.matrica[i][j].igrac == None and self.stanje.matrica[i][j].broj_spratova < 4:   #ovde nisam siguran da li moze figura da se spusit sa 2. na 0. sprat
                        self.dozvoljena_polja.append((i, j))
        
        
        
        #todo da sredim ova govna, funkcije da prepravim, i da izbacim suvisne i redudnantne delove

        # da pogedam kako je uradio onaj lik sa githuba i da mu ukradem po koju foru
    

    
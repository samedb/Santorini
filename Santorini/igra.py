from tkinter import Canvas
from enum import Enum
from tkinter import messagebox
import time
import random
from ai import MiniMaxStari, MiniMaxNovi, MiniMaxAlfaBeta
from tabla import Tabla, GameState, IGRAC_CRVENI, IGRAC_PLAVI, protivnik


TIPOVI_IGRACA = ("Osoba", "AI easy", "AI medium", "AI hard")

# zadatak ove klase je da crta Tablu i da prima inpute od korisnika, kao i da upravlja potezima AI-a

class IgraCanvas(Canvas):

    def __init__(self, parent, igrac1, igrac2):
        Canvas.__init__(self, parent)
        self.config(width = 500, height = 550) 
        self.bind("<Button-1>", self.mouse_click)

        #postavljanje tip igraca koji su prosledjeni kao parametri
        self.plavi_AI = self.odaberi_AI(igrac1)
        self.crveni_AI = self.odaberi_AI(igrac2)

        #inicijalizacije matrice
        self.tabla = Tabla()
        self.na_potezu = None # da napisem dobar komentar za ovo
        self.game_state = GameState.POSTAVLJANJE_FIGURA # u pocetku svi igraci postavljaju svoje figure na tablu
        self.broj_figura = 0 # treba mi za prvu fazu gde se postavljaju figure
        self.sastavi_poruku()
        self.selektovana_figura = (-2, -2)
        self.crtaj(self.tabla)
        self.zameni_igraca()

    def odaberi_AI(self, tip_igraca):
        if tip_igraca == TIPOVI_IGRACA[0]: #Osoba
            return None
        elif tip_igraca == TIPOVI_IGRACA[1]: #AI easy
            return MiniMaxNovi()
        elif tip_igraca == TIPOVI_IGRACA[2]: #AI medium
            return MiniMaxAlfaBeta()
        elif tip_igraca == TIPOVI_IGRACA[3]: #AI hard
            return MiniMaxAlfaBeta() #todo da se uradi jos jedan klasa
    
    def crtaj(self, tabla):
        self.delete("all")
        for i in range (0, 5):
            for j in range(0, 5):
                #izracunaj koordinate tog polja
                x1 = i * 100
                y1 = j * 100 + 50
                #nacrtaj pozadinu
                if self.selektovana_figura == (i, j): # ako je to polje na kojem se nalazi selektovana figura onda oboji zutom bojom
                    boja = "yellow"
                #ako je to polje dozvoljeno u sledecem potezu onda zelenom bojom
                elif (i, j) in tabla.pronadji_dozvoljena_polja(self.game_state, self.selektovana_figura[0], self.selektovana_figura[1], self.na_potezu):
                    boja = "green"
                else:
                    boja = "grey" # ako nije nista od toga onda siva boja
                self.create_rectangle(x1 + 2, y1 + 2, x1 + 98, y1 + 98, fill = boja)
                #nacrtaj spratove
                stepen = tabla.matrica[i][j].broj_spratova
                if stepen >= 1:
                    self.create_rectangle(x1 + 8, y1 + 8, x1 + 92, y1 + 92, width = 3)
                if stepen >= 2:
                    self.create_rectangle(x1 + 15, y1 + 15, x1 + 85, y1 + 85, width = 3)
                if stepen >= 3:
                    self.create_rectangle(x1 + 25, y1 + 25, x1 + 75, y1 + 75, width = 3)
                if stepen >= 4:
                    self.create_oval(x1 + 30, y1 + 30, x1 + 70, y1 + 70, fill = "black")
                #nacrtaj igraca
                if tabla.matrica[i][j].igrac == IGRAC_PLAVI: # 0 znaci plavi igrac
                    self.create_oval(x1 + 30, y1 + 30, x1 + 70, y1 + 70, fill = "blue")
                elif tabla.matrica[i][j].igrac == IGRAC_CRVENI: # 1 znaci crveni igrac
                    self.create_oval(x1 + 30, y1 + 30, x1 + 70, y1 + 70, fill = "red")

        self.create_text(250, 25, text = self.poruka, font = "Airal 12")
        self.update_idletasks()

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

        dozvoljena_polja = self.tabla.pronadji_dozvoljena_polja(self.game_state, self.selektovana_figura[0], self.selektovana_figura[1], self.na_potezu)
        print("Dozvoljena polja: ", dozvoljena_polja)
        if (x, y) not in dozvoljena_polja:
            print("Neispravan potez!")
            return

        if self.game_state == GameState.POSTAVLJANJE_FIGURA:
            self.tabla.postavi_figuru(x, y, self.na_potezu) 
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

        elif self.game_state == GameState.POMERANJE_FIGURE:
            #ako klikne na istu figuru ili na svoju drugu figuru
            if self.tabla.matrica[x][y].igrac == self.na_potezu:
                self.selektuj_figuru(x, y)
            else:
                x1, y1 = self.selektovana_figura
                self.tabla.pomeri_figuru(x1, y1, x, y)
                self.selektovana_figura = (x, y)
                self.game_state = GameState.GRADNJA
            
        elif self.game_state == GameState.GRADNJA:
            self.tabla.gradi(x, y)
            self.game_state = GameState.SELEKTOVANJE_FIGURE
            self.zameni_igraca()

        self.sastavi_poruku()
        self.crtaj(self.tabla)
        self.da_li_je_kraj()

    def selektuj_figuru(self, x, y):
        self.selektovana_figura = (x, y)


    def zameni_igraca(self):
        if self.na_potezu == None:
            self.na_potezu = IGRAC_PLAVI
        else:
            self.na_potezu = protivnik(self.na_potezu)

        self.selektovana_figura = (-2, -2)
        self.crtaj(self.tabla)


        if (self.na_potezu == IGRAC_PLAVI and self.plavi_AI != None) or (self.na_potezu == IGRAC_CRVENI and self.crveni_AI != None):



        # ovde treba da proverava da li igra AI sad
        #privremeno je crveni igrac uvek AI
        #if self.na_potezu == IGRAC_CRVENI:

            if self.game_state == GameState.SELEKTOVANJE_FIGURE:
                #AI odredi sledeci potez
                PAUZA_IZMEDJU_POTEZA = 1 #sekunda
                pocetak = time.time()
                if self.na_potezu == IGRAC_PLAVI:
                    potez = self.plavi_AI.sledeci_potez(self.tabla, self.na_potezu)
                if self.na_potezu == IGRAC_CRVENI:
                    potez = self.crveni_AI.sledeci_potez(self.tabla, self.na_potezu)
                vreme_potrebno_za_nalazenje_poteza = time.time() - pocetak
                if vreme_potrebno_za_nalazenje_poteza < PAUZA_IZMEDJU_POTEZA:
                    time.sleep(PAUZA_IZMEDJU_POTEZA - vreme_potrebno_za_nalazenje_poteza)



                print("Na potezu je " + str(self.na_potezu) + " i on je odgirao sledeci potez: " + str(potez))

                self.tabla.izvrsi_potez(potez)
                self.game_state = GameState.SELEKTOVANJE_FIGURE
                self.da_li_je_kraj()
                self.after(200, self.zameni_igraca)

            if self.game_state == GameState.POSTAVLJANJE_FIGURA:
                dozvoljena_polja = self.tabla.pronadji_dozvoljena_polja(self.game_state, -2, -2, self.na_potezu)
                #ovo da se uradi malo bolje i da se izmesti u ai.py
                random_polja = random.sample(range(len(dozvoljena_polja)), 2)
                x1, y1 = dozvoljena_polja[random_polja[0]][0], dozvoljena_polja[random_polja[0]][1]
                x2, y2 = dozvoljena_polja[random_polja[1]][0], dozvoljena_polja[random_polja[1]][1]
                self.tabla.postavi_figuru(x1, y1, self.na_potezu) 
                self.tabla.postavi_figuru(x2, y2, self.na_potezu) 
                self.broj_figura += 2

                if self.broj_figura == 4:
                    self.game_state = GameState.SELEKTOVANJE_FIGURE

                self.after(200, self.zameni_igraca)
        
        

        '''
            if trenutni igrac == AI
                sledeci_potez = AI.potez(trenutno_stanje)
                izvrsi_potez(sledeci_potez) # ova funkcija crta redom sve korake, vise puta poziva funkciju crtaj da bi pokazala kako se sleketuje figura
                pomera figura i gradi, sa nekim delay-om izmedju koraka
                zameni_igraca()
        '''

  
    def sastavi_poruku(self):
        self.poruka = f"Na potezu je {self.na_potezu} \na gamestate je {self.game_state}"

    def da_li_je_kraj(self):
        if self.game_state == GameState.POSTAVLJANJE_FIGURA:
            return
        #proveri da li je kraj meca, tj da li ima mogucih poteza za igraca na potezu
        if not self.tabla.ima_mogucih_poteza(self.na_potezu):
            messagebox.showinfo("Pobeda", f"Pobedio je {self.na_potezu.protivnik()} jer {self.na_potezu} nema mogucih poteza!")
            self.game_state = GameState.KRAJ_IGRE
        
        if self.tabla.zauzeo_treci_sprat(self.na_potezu):
            messagebox.showinfo("Pobeda", f"Pobedio je {self.na_potezu} jer je zauzeo polje sa nivoom 3!")
            self.game_state = GameState.KRAJ_IGRE
    
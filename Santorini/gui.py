"""Modul gui je prvi modul ove aplikacije, on zadrzi sve Frame-ove i odgovoran je za otvaranje prozora i navigaciju izmedju Frame-ova.
Za graficki korisnicki interfejs (gui) ove aplikacije upotrebljena je tkinter biblioteka.
"""
from tkinter import Tk, Frame, Label, Button, sys, LEFT, BOTTOM, ttk, messagebox, filedialog, IntVar, Checkbutton
from igra import IgraCanvas, TIPOVI_IGRACA
from datetime import datetime

# konstanta, koristi se na vise mesta u ovom modulu
LARGE_FONT= ("Verdana bold", 24)


class Application(Tk):
    """Glavni prozor aplikacije, fiksne velicine 800x600, sadrzi container u kome se kasnije smenjuju razni Frame-ovi"""    

    def __init__(self, *args, **kwargs):
        """Konstruktor klase Application, postavlja naslov, velicinu i default font prozora. Kreira container i postavlja ga u prozoru. 
        Preko tog containera ce se kasnije smenjivati razni Frame-ovi. Na kraju poziva funkciju show_frame i postavlja PocetniFrame u containeru
        """        
        Tk.__init__(self, *args, **kwargs)

        Tk.title(self, "Santorini")
        Tk.geometry(self, "800x600")
        Tk.resizable(self, 0, 0)
        Tk.option_add(self, "*Font", "Arial 16 bold")

        self.container = Frame(self)
        self.container.pack(side="top", fill='both' , expand = 1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_frame(PocetniFrame)


    def show_frame(self, cont, *args, **kwarg):
        """Instancira frame koji dobije kao parametar i postavlja ga u container.
        
        :param cont: Frame koji treba prikazati u containeru
        :type cont: Frame
        """        
        frame = None
        frame = cont(self.container, self, *args, **kwarg)
        frame.grid(row=0, column=0, sticky="nsew") 
        frame.tkraise()


class PocetniFrame(Frame):
    """Frame koji se prikazuje pri pokretanju aplikacije, sadrzi meni za dalju navigaciju"""    

    def __init__(self, parent, controller):
        """Konstruktor klase PocetniFrame koji inicijalizuje atribute klase i formira Navigacioni meni, sadrzi naslov i tri buttona: Igra, Pravila i Izlaz
        
        :param parent: Roditeljski Frame u kome ce se nalaziti PocetniFrame
        :type parent: Frame
        :param controller: Referenca na root, na Application koji upravlja time koji ce se frame prikazivati u njegovom containeru
        :type controller: Tk
        """        
        Frame.__init__(self,parent)
        label = Label(self, text="Santorini\n\n", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        Button(self, text="Igra",    command=lambda: controller.show_frame(OdabirTipaIgreFrame), width = 25).pack(pady = 10)
        Button(self, text="Pravila", command=lambda: controller.show_frame(PravilaFrame),        width = 25).pack(pady = 10)
        Button(self, text="Izlaz",   command=sys.exit,                                           width = 25).pack(pady = 10) # ugasi aplikaciju


class OdabirTipaIgreFrame(Frame):
    """Kada u glavnom meniju odaberemo Igra to nas vodi do ovog Frame-a, ovde se biraju tipovi korisnika (Osoba ili AI) i tezina AI (easy, medium, hard).
    Osim toga nudi opcije za ispisivanje vrednosti AI algoritma kod svakog poteza, kao i mogucnost izvrsavanja implementirane strategije do kraja
    Sadrzi i kraci opis razlicitih nivoa tezine vestacke inteligencije
    """   

    def __init__(self, parent, controller):
        """Konstruktor klase OdabirTipaIgreFrame koji inicijalizuje atribute klase i formira Frame, sadrzi naslov , combobox-ove za odabir tipa igraca i tezine,
        Checkbuttone za ispisivanje vrednosti AI algoritma kod svakog poteza i izvrsavanja implementirane strategije do kraja.
        Ispod toga ide opis razlicitih nivoa tezine i buttoni za povratak na pocetnu stranu i pokretanje igre.
        
        :param parent: Roditeljski Frame u kome ce se nalaziti OdabirTipaIgreFrame
        :type parent: Frame
        :param controller: Referenca na root, na Application koji upravlja time koji ce se frame prikazivati u njegovom containeru
        :type controller: Tk
        """  
        Frame.__init__(self, parent)
        Label(self, text="Odabir tipa i težine igre", font=LARGE_FONT).grid(row = 0, columnspan = 2, sticky = "n", pady = 30)

        Label(self, text = "Plavi igrač").grid(row = 1, column = 0)
        cb1 = ttk.Combobox(self, state="readonly", values = TIPOVI_IGRACA, width = 25)
        cb1.grid(row = 2, column = 0, padx = 40, pady = 20)
        cb1.current(0)

        Label(self, text = "Crveni igrač").grid(row = 1, column = 1)
        cb2 = ttk.Combobox(self, state="readonly", values = TIPOVI_IGRACA, width = 25)
        cb2.grid(row = 2, column = 1, padx = 40, pady = 20)
        cb2.current(0)

        #vs ili protiv izmedju
        Label(self, text = "vs").grid(row = 2, columnspan = 2)

        Button(self, text="Učitaj iz fajla", command=self.ucitaj_fajl, width = 20).grid(row = 3, columnspan = 2)

        self.naziv_fajla_labela = Label(self, text = "")
        self.naziv_fajla_labela.grid(row = 4, columnspan = 2)

        stampaj_vrednosti_algoritma = IntVar()
        Checkbutton(self, text="Štampaj vrednosti svih mogućih poteza AI", variable=stampaj_vrednosti_algoritma).grid(row = 5, columnspan = 2)

        preskoci_crtanje_poteza = IntVar()
        Checkbutton(self, text="Izvršavanje implementirane strategije do kraja", variable=preskoci_crtanje_poteza).grid(row = 6, columnspan = 2)

        objasnjenje_tezina = "Opis raznih nivoa veštačke inteligencije \n• AI easy - minimax algoritam sa dubinom 2 \n• AI medium - minimax algoritam sa dubinom 3 uz alfa-beta odsecanje \n• AI hard - minimax algoritam sa dubinom 4 uz alfa-beta odsecanje"
        Label(self, text=objasnjenje_tezina, justify = LEFT, font = "Arial 16").grid(row = 7, columnspan = 2, pady = 40)

        Button(self, text="Nazad na početnu stranu", command=lambda: controller.show_frame(PocetniFrame), width = 20).grid(row = 8, column = 0)
        
        # informacije o tipovima igraca, nazivu fajla u kome se pise ili cita stanje igre itd. prosledjujem IgraFrame-u preko kwargs, koje on onda u konstruktoru procita
        Button(self, text="Pokreni igru", command=lambda: controller.show_frame(IgraFrame, igrac1 = cb1.get(), igrac2 = cb2.get(), naziv_fajla = self.naziv_fajla_labela["text"], stampaj_vrednosti_svih_poteza = stampaj_vrednosti_algoritma.get(), preskoci_crtanje_poteza = preskoci_crtanje_poteza.get()), width = 20).grid(row = 8, column = 1)

    #Otvara openFileDialog, selektuje fajl i putanju pamti u naziv_fajla_labela
    def ucitaj_fajl(self):
        """Funkcija koja otvara openFileDialog, preko koga se bira neki fajl sa potezima za igru santorini da bi smo mogli da nastavimo.
        Putanju do tog fajla se postavlja kao tekst labele naziv_fajla_labela i tako je cuva za kasnije jer mi je potrebna u IgraFrame-u.
        """        
        self.naziv_fajla_labela["text"] = filedialog.askopenfilename(initialdir = "Igre/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))


class IgraFrame(Frame):
    """Frame u kome se nalazi IgraCanvas tj. u kome se igra Santorini, osim igre sadrzi i button za povratak na pocetnu stranu."""   

    def __init__(self, parent, controller, *args, **kwarg):
        """Konstruktor klase Igra koji inicijalizuje atribute klase i formira IgraFrame, sadrzi IgraCanvas i button za povratak na pocetnu stranicu.
        Prima kwargs od OdabirTipaIgreFrame da bi znao koji igraci igraju, koji je fajl za poteze i ostala podesavanja, koja dalje prosledjuje IgraCanvas-u
        
        :param parent: Roditeljski Frame u kome ce se nalaziti IgraFrame
        :type parent: Frame
        :param controller: Referenca na root, na Application koji upravlja time koji ce se frame prikazivati u njegovom containeru
        :type controller: Tk
        """  
        Frame.__init__(self, parent)
        self.controller = controller

        igrac1 = kwarg.get("igrac1", TIPOVI_IGRACA[0])
        igrac2 = kwarg.get("igrac2", TIPOVI_IGRACA[0])
        naziv_fajla = kwarg.get("naziv_fajla", "")
        stampanje_poteza = kwarg.get("stampaj_vrednosti_svih_poteza", "0")
        preskoci_crtanje_poteza = kwarg.get("preskoci_crtanje_poteza", "0")
        # IgraFrame samo ucita ili kreira fajl, prodledjuje putanju do njega IgraCanvas-u i on onda radi sa njim sta hoce
        if naziv_fajla == "":
            naziv_fajla = self.kreiraj_fajl()

        self.igraCanvas = IgraCanvas(self, igrac1, igrac2, naziv_fajla, stampanje_poteza == 1, preskoci_crtanje_poteza != 1)
        self.igraCanvas.place(x = 150, y = 0)
        Button(self, text="Nazad na početnu stranu", command=self.povratak_na_pocetnu).pack(side = BOTTOM, pady = 3)
        

    def povratak_na_pocetnu(self):
        """Funkcija koja prikazuje dijalog, ako se pritisne yes onda se zatvara fajl i vraca se na PocetniFrame/pocetnu stranicu"""        
        odg = messagebox.askquestion("Nazad na pocetnu stranicu?", "Da li ste sigurni da zelite da prekinete igru i da se vratite na pocetnu stranicu?")
        if odg == "yes":
            self.igraCanvas.zatovori_fajl()
            self.controller.show_frame(PocetniFrame)
    

    def kreiraj_fajl(self):
        """Kreira fajl u folderu igre koji nosi naziv u formatu Santorini <trenutni datum i vreme>.txt i vraca ga
        
        :return: Putanja do novo-otvorenog fajla
        :rtype: str
        """        
        naziv_fajla = f"Igre/Santorini {datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.txt"
        f = open(naziv_fajla, "w+")
        f.close()
        return naziv_fajla


class PravilaFrame(Frame):
    """Frame koji prikazuje pravila igre Santorini"""   

    __pravila_igre__ = """
        •  Igra se igra na tabli 5x5, koja se inicijalno sastoji iz 25 praznih polja. Igru igraju 
        dva igrača, koji povlače poteze naizmenično. Na početku igre, prvi, a zatim i drugi igrač
        postavljaju svoje figure na bilo koje od slobodnih polja. Nakon postavljanja figura, igrači
        naizmenično igraju povlačeći poteze.

        •  Potez igrača se sastoji iz pomeranja figure i gradnje. Najpre se jedna odabrana figura
        pomera na neko od slobodnih susednih polja (uključujući dijagonalne susede, pri čemu
        odredišno polje mora biti najviše jednu pločicu iznad izvorišnog polja. Ukoliko igrač ne
        može da pomeri nijednu od svojih figura prema ovim pravilima, gubi igru.

        •  Drugi deo poteza je gradnja. Ova faza podrazumeva dodavanje pločice na jedno od
        slobodnih polja susednih odredišnom polju pomerene figure (uključujući dijagonalne
        susede). Pločica koja se dodaje na polje nivoa 3 je kružna kupola. Polja nivoa 4 (3 pločice
        i kružna kupola na vrhu) su „blokirana“ u nastavku igra. Nije dozvoljeno postavljanje figura
        na takva polja, niti dalja izgradnja nad tim poljima.

        •  Igra se može završiti na dva načina:
            •   kada igrač koji je na potezu pomeri jednu od figura na polje nivoa 3 (izgrađene tri
                pločice na tom polju) – pobednik je igrač koji je pomerio svoju figuru na polje nivoa 3;
            •   kada igrač koji je na potezu ne može da odigra potez prema pravilima igre –
                pobednik je igrač koji nije na potezu."""

    def __init__(self, parent, controller):
        """Konstruktor klase PravilaFrame koji inicijalizuje atribute klase i formira Frame, sadrzi labelu sa pravilima igre Santorini i button za povratak na pocetnu stranicu
        
        :param parent: Roditeljski Frame u kome ce se nalaziti PravilaFrame
        :type parent: Frame
        :param controller: Referenca na root, na Application koji upravlja time koji ce se frame prikazivuati u njegovom containeru
        :type controller: Tk
        """  
        Frame.__init__(self, parent)
        Label(self, text="Pravila igre Santorini", font=LARGE_FONT).pack(pady = 20)
        Label(self, text = self.__pravila_igre__, font = "Arial 13", justify = LEFT).pack(pady = 10)
        Button(self, text="Nazad na početnu stranu", command=lambda: controller.show_frame(PocetniFrame)).pack(side = BOTTOM, pady = 10)


# pokretanje aplikacije
if __name__ == "__main__":
    app = Application()
    app.mainloop()




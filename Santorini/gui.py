from tkinter import Tk, Frame, Label, Button, sys, LEFT, BOTTOM, ttk, messagebox, filedialog, IntVar, Checkbutton
from igra import IgraCanvas, TIPOVI_IGRACA
from datetime import datetime

LARGE_FONT= ("Verdana bold", 24)

class Application(Tk):

    def __init__(self, *args, **kwargs):

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
        frame = None
        frame = cont(self.container, self, *args, **kwarg)
        frame.grid(row=0, column=0, sticky="nsew") 
        frame.tkraise()


class PocetniFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="Santorini\n\n", font=LARGE_FONT)
        label.pack(pady=20,padx=10)

        Button(self, text="Igra",    command=lambda: controller.show_frame(OdabirTipaIgreFrame), width = 25).pack(pady = 10)
        Button(self, text="Pravila", command=lambda: controller.show_frame(PravilaFrame),        width = 25).pack(pady = 10)
        Button(self, text="Izlaz",   command=sys.exit,                                           width = 25).pack(pady = 10)


class OdabirTipaIgreFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Label(self, text="Odabir tipa i tezine igre", font=LARGE_FONT).grid(row = 0, columnspan = 2, sticky = "n", pady = 30)

        Label(self, text = "Plavi igrac").grid(row = 1, column = 0)
        cb1 = ttk.Combobox(self, values = TIPOVI_IGRACA, width = 25)
        cb1.grid(row = 2, column = 0, padx = 40, pady = 20)
        cb1.current(0)

        Label(self, text = "Crveni igrac").grid(row = 1, column = 1)
        cb2 = ttk.Combobox(self, values = TIPOVI_IGRACA, width = 25)
        cb2.grid(row = 2, column = 1, padx = 40, pady = 20)
        cb2.current(0)

        #vs ili protiv izmedju
        Label(self, text = "vs").grid(row = 2, columnspan = 2)

        Button(self, text="Ucitaj iz fajla", command=self.ucitaj_fajl, width = 20).grid(row = 3, columnspan = 2)

        self.naziv_fajla_labela = Label(self, text = "")
        self.naziv_fajla_labela.grid(row = 4, columnspan = 2)

        check_var = IntVar()
        Checkbutton(self, text="Stampaj vrednosti svih mogucih poteza AI", variable=check_var).grid(row = 5, columnspan = 2)

        objasnjenje_tezina = "Opis raznih nivoa vestacke inteligencije \nLupam \n• AI easy - minimax algoritam sa dubinom 5 \n• AI medium - minimax algoritam sa dubinom 10 uz alfa-beta odsecanje \n• AI hard - minimax algoritam sa dubinom 15 uz alfa-beta odsecanje"
        Label(self, text=objasnjenje_tezina, justify = LEFT, font = "Arial 16").grid(row = 6, columnspan = 2, pady = 50)

        Button(self, text="Nazad na pocetnu stranu", command=lambda: controller.show_frame(PocetniFrame), width = 20).grid(row = 7, column = 0)
        
        Button(self, text="Pokreni igru", command=lambda: controller.show_frame(IgraFrame, igrac1 = cb1.get(), igrac2 = cb2.get(), naziv_fajla = self.naziv_fajla_labela["text"], stampaj_vrednosti_svih_poteza = check_var.get()), width = 20).grid(row = 7, column = 1)

    #Otvara openFileDialog, selektuje fajl i putanju pamti u naziv_fajla_labela
    def ucitaj_fajl(self):
        self.naziv_fajla_labela["text"] = filedialog.askopenfilename(initialdir = "Igre/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))

class IgraFrame(Frame):
    x_offset = 150
    y_offset = 50

    def __init__(self, parent, controller, *args, **kwarg):
        Frame.__init__(self, parent)
        self.controller = controller

        igrac1 = kwarg.get("igrac1", TIPOVI_IGRACA[0])
        igrac2 = kwarg.get("igrac2", TIPOVI_IGRACA[0])
        naziv_fajla = kwarg.get("naziv_fajla", "")
        stampanje_poteza = kwarg.get("stampaj_vrednosti_svih_poteza", "0")
        if naziv_fajla == "":
            naziv_fajla = self.kreiraj_fajl()

        self.igraCanvas = IgraCanvas(self, igrac1, igrac2, naziv_fajla, stampanje_poteza == 1)
        self.igraCanvas.place(x = 150, y = 0)
        Button(self, text="Nazad na pocetnu stranu", command=self.povratak_na_pocetnu).pack(side = BOTTOM, pady = 3)
        

    def povratak_na_pocetnu(self):
        odg = messagebox.askquestion("Nazad na pocetnu stranicu?", "Da li ste sigurni da zelite da prekinete igru i da se vratite na pocetnu stranicu?")
        if odg == "yes":
            self.igraCanvas.zatovori_fajl()
            self.controller.show_frame(PocetniFrame)
    
    def kreiraj_fajl(self):
        #kreiraj fajl koji u imenu nosi trenutno vreme
        naziv_fajla = f"Igre/Santorini {datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.txt"
        f = open(naziv_fajla, "w+")
        f.close()
        return naziv_fajla


class PravilaFrame(Frame):

    pravila = """
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
        Frame.__init__(self, parent)
        Label(self, text="Pravila igre Santorini", font=LARGE_FONT).pack(pady = 20)
        Label(self, text = self.pravila, font = "Arial 13", justify = LEFT).pack(pady = 10)
        Button(self, text="Nazad na pocetnu stranu", command=lambda: controller.show_frame(PocetniFrame)).pack(side = BOTTOM, pady = 10)



if __name__ == "__main__":
    app = Application()
    app.mainloop()

    #todo celava latinica
    # todo combobox da bude readonly\



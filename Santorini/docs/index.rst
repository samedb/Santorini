.. Santorini documentation master file, created by
   sphinx-quickstart on Thu Dec 12 13:07:10 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Dokumentacija za igru Santorini
=====================================

   Ova aplikacija se sastoji od cetiri modula
   
   * **gui.py** - prvi modul ove aplikacije, on zadrzi sve Frame-ove i odgovoran je za otvaranje prozora i navigaciju izmedju Frame-ova. Za graficki korisnicki interfejs (gui) ove aplikacije upotrebljena je tkinter biblioteka. Preko ovog modula se i pokrece aplikacija
   * **tabla.py** - sadrzi funkcije i pomocne klase koje se koriste u ai.py i igra.py. To su klase Polje, Tabla, Potez, GameState
   * **igra.py** - modul cija je glavna klasa IgraCanvas. Onda je odgovorna za crtanje trenutnog stanja igre, prikazivanje poruka, primanja inputa od korisnika i upravljanje AI-om kada je jedan od igraca vestacka inteligencija.
   * **ai.py** - je odgovoran za vestacku inteligenciju igre Santorini, sadrzi klase koje implementiraju minimax i minimax + alfa-beta, funkcije za staticku procenu stanja itd. Sve sto ima veze za AI ove igre nalazi se ovde.

   Dokumentacija je automatski generisana uz pomoc docstring-a i sphinx biblioteke

.. toctree::
   :maxdepth: 2
   :caption: Sadrzaj:
   
   modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

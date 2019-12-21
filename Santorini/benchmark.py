from ai import *

# probna staicka funkcija procene, samo za test sluzi
def test_staticka_funkcija_procene(tabla: Tabla, potez: Potez, na_potezu):
    return potez.x1

# test vremena potregnog za nalazenje poteza
# kad koristim pypy interpreter onda se vreme potrebno za nalazenje poteza za bilo koji algoritam smanji 10 do 15 puta
if __name__ == "__main__":
    tabla = Tabla()

    tabla.matrica[2][2].igrac = Igrac.PLAVI
    tabla.matrica[2][3].igrac = Igrac.PLAVI
    tabla.matrica[0][0].igrac = Igrac.CRVENI
    tabla.matrica[0][1].igrac = Igrac.CRVENI
    tabla.matrica[1][1].broj_spratova = 3

    # ukupno = 0
    # for i in range(10):
    #     start = time.time()
    #     potez = MiniMax(False, 3, test_staticka_funkcija_procene).sledeci_potez(tabla, IGRAC_PLAVI)
    #     print(potez)
    #     print("Vreme potrebno za izracunavanje: ", time.time() - start)
    #     ukupno += time.time() - start

    # print("Prosek:", ukupno / 10.)

    # ukupno = 0
    # for i in range(10):
    #     start = time.time()
    #     potez = MiniMax(False, 3, test_staticka_funkcija_procene).sledeci_potez(tabla, IGRAC_PLAVI)
    #     print(potez)
    #     print("Vreme potrebno za izracunavanje: ", time.time() - start)
    #     ukupno += time.time() - start

    # print("Prosek:", ukupno / 10.)

    ukupno = 0
    for i in range(10):
        start = time.time()
        potez = MiniMaxAlfaBeta(False, 5, optimizovana_nova_staticka_funkcija_procene).sledeci_potez(tabla, Igrac.PLAVI, 4)
        print(potez)
        print("Vreme potrebno za izracunavanje: ", time.time() - start)
        ukupno += time.time() - start

    print("Prosek:", ukupno / 10.)

    ukupno = 0
    for i in range(10):
        start = time.time()
        potez = MiniMaxAlfaBeta(False, 5, optimizovana_neka_nova_staticka_funkcija_procene2).sledeci_potez(tabla, Igrac.PLAVI, 4)
        print(potez)
        print("Vreme potrebno za izracunavanje: ", time.time() - start)
        ukupno += time.time() - start

    print("Prosek:", ukupno / 10.)

    # print("obicna staticka funkcija:")
    # start = time.time()
    # for i in range(100000):
    #     v = staticka_funkcija_procene(tabla, Potez(0, 2, 0, 1, 1, 1), 0)
    # print("Vreme potrebno za obicnu staticku funkciju procene ", time.time() - start)

    # print("optimizovana nova funkcija:")
    # start = time.time()
    # for i in range(100000):
    #     v = optimizovana_neka_nova_staticka_funkcija_procene(tabla, None, 0)
    # print("Vreme potrebno za obicnu staticku funkciju procene ", time.time() - start)


    # print("nova neka funkcija2:")
    # start = time.time()
    # for i in range(100000):
    #     v = nova_neka_staticka_funkcija_procene(tabla, Potez(0, 2, 0, 1, 1, 1), 0)
    # print("Vreme potrebno za naprednu staticku funkciju procene ", time.time() - start)
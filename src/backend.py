from datetime import date
import os
import sys

def get_prazniki_path(filename="Prazniki.txt"):
    # Vrne pravilno pot do Prazniki.txt, tako v .exe kot v Python skripti
    if getattr(sys, 'frozen', False):
        # Če se izvaja kot EXE
        base_path = sys._MEIPASS
    else:
        # Če se izvaja kot Python skripta
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)


class KoledarLogika:

    dnevi_tedna = ("Pon", "Tor", "Sre", "Čet", "Pet", "Sob", "Ned")
    meseci = ("Januar", "Februar", "Marec", "April", "Maj", "Junij", 
              "Julij", "Avgust", "September", "Oktober", "November", "December")
    dnevi_mesecev = (31,28,31,30,31,30,31,31,30,31,30,31)

    @staticmethod
    def izracunaj_dan(dan, mesec, leto):
        from time import localtime
        razlika = date.today() - date(leto, mesec, dan)
        return (localtime().tm_wday - razlika.days % 7) % 7

    @staticmethod
    def prestopno_leto(leto):
        return leto % 400 == 0 or (leto % 100 != 0 and leto % 4 == 0)

    @classmethod
    def dnevi_v_mesecu(cls, mesec, leto):
        dni = cls.dnevi_mesecev[mesec-1]
        if mesec == 2 and cls.prestopno_leto(leto):
            dni = 29
        return dni

    @staticmethod
    def get_prazniki(file_path=None):
        # Vrne seznam praznikov iz datoteke Prazniki.txt
        if file_path is None:
            file_path = get_prazniki_path("Prazniki.txt")

        prazniki = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                vrstice = f.readlines()
                for vrstica in vrstice:
                    print(vrstica)
                    ime_praznika, dan, mesec, leto = vrstica.strip().split("/")
                    ime_praznika = ime_praznika.replace("_", " ")

                    if ime_praznika.endswith("*"):
                        # Znak * na koncu imena praznika pomeni, da je praznik ponovljiv
                        ponovljiv = True
                        ime_praznika = ime_praznika.replace("*", "")
                    else:
                        ponovljiv = False

                    prazniki.append(Praznik(ime_praznika, int(dan), int(mesec), int(leto), ponovljiv))
        except FileNotFoundError:
            print("Prazniki.txt ni bil najden.")

        return prazniki


class Praznik:
    def __init__(self, ime, dan, mesec, leto, ponovljiv=True):
        self.ime = ime
        self.datum = date(leto, mesec, dan)
        self.ponovljiv = ponovljiv
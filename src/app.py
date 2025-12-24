import customtkinter as ctk
from datetime import datetime
from frontend import Header, MrezaDatumov, DatumFrame
from backend import KoledarLogika

class Koledar(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("Koledar")
        self.geometry("1200x800")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=6)

        self.dnevi_tedna = KoledarLogika.dnevi_tedna
        self.meseci = KoledarLogika.meseci

        self.header = Header(self)
        self.header.grid(row=0,column=0, padx=5, pady=5, sticky="nsew")
        self.mreza_datumov = MrezaDatumov(self)
        self.mreza_datumov.grid(row=1,column=0, padx=5, pady=5, sticky="nsew")

        self.generiraj_mesec(datetime.now().month, datetime.now().year)

    def generiraj_mesec(self, mesec, leto):
        prazniki = KoledarLogika.get_prazniki()
        dan = KoledarLogika.izracunaj_dan(1, mesec, leto)
        dni_v_mesecu = KoledarLogika.dnevi_v_mesecu(mesec, leto)

        for okno in self.mreza_datumov.winfo_children():
            if isinstance(okno, DatumFrame):
                okno.destroy()

        for i in range(dan, dan + dni_v_mesecu):
            datum = DatumFrame(self.mreza_datumov, i-dan+1)
            datum.grid(row=i//7 + 1, column=i%7, sticky="nsew")
            if i % 7 == 6:
                datum.nastavi_barvo_dneva("#D60000")
            for praznik in prazniki:
                if ((praznik.datum.year == leto and praznik.datum.month == mesec and praznik.datum.day == i-dan+1)
                    or (praznik.ponovljiv and praznik.datum.month == mesec and praznik.datum.day == i-dan+1)):
                    datum.nastavi_barvo_dneva("#7900D6")
                    
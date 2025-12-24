import customtkinter as ctk
from datetime import datetime

class DatumFrame(ctk.CTkFrame):
    def __init__(self, parent, dan):
        super().__init__(parent, border_width=1, border_color="black")
        self.dan = dan
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=1)
        self.label = ctk.CTkLabel(self, text=str(dan), font=("Arial", 50, "bold"), anchor="center")
        self.label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def nastavi_barvo_dneva(self, barva):
        self.label.configure(text_color=(barva, barva))


class MrezaDatumov(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        for i in range(0,7):
            self.columnconfigure(i, weight=1)
            if i != 0:
                self.rowconfigure(i, weight=1)
        for i in range(0,7):
            dan = ctk.CTkLabel(self, text=parent.dnevi_tedna[i], font=("Arial", 30))
            dan.grid(row=0, column=i, pady=10, padx=5)


class Header(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # Datum input
        self.txt_datum = ctk.CTkLabel(self, text="Vnesi natančen datum DD/MM/LLLL: ", font=("Arial", 15), anchor="center")
        self.txt_datum.grid(row=1, column=0, padx=5, sticky="ew")
        self.vnos_datum = ctk.CTkEntry(self)
        self.vnos_datum.grid(row=1, column=1, padx=5, sticky="ew")
        self.vnos_gumb1 = ctk.CTkButton(self, text="Pojdi na datum", command=self.skok_datum)
        self.vnos_gumb1.grid(row=1, column=2, padx=5, sticky="ew")

        # Combobox meseci
        self.txt_mesec = ctk.CTkLabel(self, text="Mesec: ", font=("Arial", 15), anchor="center")
        self.txt_mesec.grid(row=1, column=4, padx=5, sticky="ew")
        self.kombo_meseci = ctk.CTkComboBox(self, values=parent.meseci, state="readonly")
        self.kombo_meseci.grid(row=1, column=5, padx=5, sticky="ew")
        self.kombo_meseci.set(parent.meseci[datetime.now().month - 1])

        # Leto input
        self.txt_leto = ctk.CTkLabel(self, text="Leto: ", font=("Arial", 15), anchor="center")
        self.txt_leto.grid(row=1, column=6, padx=5, sticky="ew")
        self.vnos_leto = ctk.CTkEntry(self)
        self.vnos_leto.grid(row=1, column=7, padx=5, sticky="ew")
        self.vnos_leto.insert(0,str(datetime.now().year))
        self.vnos_gumb2 = ctk.CTkButton(self, text="Potrdi", command=self.skok_mesec_leto)
        self.vnos_gumb2.grid(row=1, column=8, padx=5, sticky="ew")

        # Error sporočila
        self.err_1 = ctk.CTkLabel(self, text="", font=("Arial", 15), anchor="center")
        self.err_1.grid(row=2, column=1, padx=5, sticky="ew")
        self.err_2 = ctk.CTkLabel(self, text="", font=("Arial", 15), anchor="center")
        self.err_2.grid(row=2, column=7, padx=5, sticky="ew")

    def skok_datum(self):
        vnos = self.vnos_datum.get().strip()
        if not vnos:
            return
        try:
            dan, mesec, leto = map(int, vnos.split("/"))
            from datetime import date
            date(leto, mesec, dan)
        except ValueError:
            self.vnos_datum.delete(0, ctk.END)
            self.err_1.configure(text="Neveljaven vnos!")
            self.err_2.configure(text="")
            return
        
        self.err_1.configure(text="")
        self.err_2.configure(text="")
        self.app.generiraj_mesec(mesec, leto)
        self.vnos_datum.delete(0, ctk.END)
        self.kombo_meseci.set(self.app.meseci[mesec-1])
        self.vnos_leto.delete(0, ctk.END)
        self.vnos_leto.insert(0,str(leto))

    def skok_mesec_leto(self):
        try:
            mesec = self.app.meseci.index(self.kombo_meseci.get()) + 1
            leto = int(self.vnos_leto.get())
            self.app.generiraj_mesec(mesec, leto)
            self.err_1.configure(text="")
            self.err_2.configure(text="")
        except:
            self.err_1.configure(text="")
            self.err_2.configure(text="Neveljaven vnos!")
            self.vnos_leto.delete(0, ctk.END)
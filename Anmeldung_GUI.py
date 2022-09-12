import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import requests, re
import json
import urllib


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.famAnz = 0
        self.einzPersAnz = 0
        self.url = "https://terminvereinbarung.muenchen.de/bba/termin/index.php?loc=BB"
        self.url2 = "https://www22.muenchen.de/kvr/termin/index.php?cts=1064399=1"

        self.dateWindows = None

        # self.geometry("280x100")
        self.title('Login')
        # self.resizable(0, 0)
        # configure the grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # username
        famAnz_label = ttk.Label(self, text="Anzahl Familie:")
        famAnz_label.grid(column=0, row=0, sticky=tk.W)  # , padx=5, pady=5)

        fam_entry = ttk.Entry(self)
        fam_entry.grid(column=1, row=0)  # , sticky=tk.E, padx=5, pady=5)

        # password
        einzelpers_label = ttk.Label(self, text="Anzahl Einzelpersonen:")
        einzelpers_label.grid(column=0, row=1, sticky=tk.W)  # , padx=5, pady=5)

        einzelpers_entry = ttk.Entry(self)
        einzelpers_entry.grid(column=1, row=1)  # , sticky=tk.E, padx=5, pady=5)

        # login button
        submit_button = ttk.Button(self, text="Submit",
                                   command=lambda: self.refresh(int(fam_entry.get()), int(einzelpers_entry.get())))
        submit_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)
        self.treeview = ttk.Treeview(self, columns=("Ergebnisse"))
        self.treeview.heading("#0", text="Ergebnisse")
        self.treeview.column("#0", stretch=True)
        self.treeview.grid(row=4, columnspan=4, sticky='nsew')

    def refresh(self, famAnz, einzPersAnz):

        self.famAnz = famAnz
        self.einzPersAnz = einzPersAnz
        self.treeview.delete(*self.treeview.get_children())
        self.__getDates()

    def selectItem(self, a):
        curItem = self.treeview.focus()
        if 'final' in self.treeview.item(curItem)["tags"]:
            place = self.treeview.item(self.treeview.parent(self.treeview.parent(curItem)))["text"]

            check = tkinter.messagebox.askyesno("Anmeldung", f"Willst du den Termin im {place} am {self.treeview.item(self.treeview.parent(curItem))['text']} um { self.treeview.item(curItem)['text']} Buchen?")
            if check:
                try:
                    with requests.Session() as s:

                        headers = {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }

                        id = self.treeview.parent(curItem) + self.treeview.item(curItem)["text"]
                        print(id)
                        payload = {"step": "WEB_APPOINT_NEW_APPOINT", "APPOINT": id}
                        payload2 = {"step": 'WEB_APPOINT_SAVE_APPOINT', 'CONTACT[salutation]': 'Frau', 'CONTACT[surname]': 'a',
                                    'CONTACT[email]': 'mail@adress.com', 'CONTACT[birthday]': '19.10.1988',
                                    'CONTACT[privacy]': '1'}
                        #payload2 = 'step=WEB_APPOINT_SAVE_APPOINT&CONTACT%5Bsalutation%5D=Frau&CONTACT%5Bsurname%5D=a&CONTACT%5Bemail%5D=hihibep916%40ukgent.com&CONTACT%5Bbirthday%5D=19.10.1988&CONTACT%5Bprivacy%5D=1'
                        payload2 = urllib.parse.urlencode(payload2)
                        payload = urllib.parse.urlencode(payload)

                        # print(str(r.content.decode()))
                        if "rup" in self.treeview.item(curItem)["tags"]:
                            r = s.post(self.url2,
                                       data=payload, headers=headers, cookies=self.cookie2)
                            print(r.request.body)
                            r = s.post(self.url2,
                                       data=payload2, headers=headers, cookies=self.cookie2)
                        else:
                            r = s.post(self.url,
                                       data=payload, headers=headers, cookies=self.cookie)
                            print(r.request.body)
                            r = s.post(self.url,
                                       data=payload2, headers=headers, cookies=self.cookie)
                    tkinter.messagebox.showinfo(title="Success", message="Buchung war erfolgreich!")

                except:
                    tkinter.messagebox.showerror(title="Error", message="Buchung war nicht erfolgreich!")
            else:
                tkinter.messagebox.showinfo(title="Abbort", message="Buchung abgebrochen!")
            self.refresh(self.famAnz,self.einzPersAnz)

    def __getDates(self):
        payload = f'step=WEB_APPOINT_SEARCH_BY_CASETYPES&CASETYPES%5BAn-%20oder%20Ummeldung%20-%20Einzelperson%5D={self.einzPersAnz}&CASETYPES%5BAn-%20oder%20Ummeldung%20-%20Einzelperson%20mit%20eigenen%20Fahrzeugen%5D=0&CASETYPES%5BAn-%20oder%20Ummeldung%20-%20Familie%5D={self.famAnz}&CASETYPES%5BAn-%20oder%20Ummeldung%20-%20Familie%20mit%20eigenen%20Fahrzeugen%5D=0&CASETYPES%5BMeldebescheinigung%5D=0&CASETYPES%5BHaushaltsbescheinigung%5D=0&CASETYPES%5BFamilienstands%C3%A4nderung%2F%20Namens%C3%A4nderung%5D=0&CASETYPES%5BAntrag%20Personalausweis%5D=0&CASETYPES%5BAntrag%20Reisepass%2FExpressreisepass%5D=0&CASETYPES%5BAntrag%20vorl%C3%A4ufiger%20Reisepass%5D=0&CASETYPES%5BAntrag%20oder%20Verl%C3%A4ngerung%2FAktualisierung%20Kinderreisepass%5D=0&CASETYPES%5BAusweisdokumente%20-%20Familie%20(Minderj%C3%A4hrige%20und%20deren%20gesetzliche%20Vertreter)%5D=0&CASETYPES%5BeID-Karte%20beantragen%20(EU%2FEWR)%5D=0&CASETYPES%5BNachtr%C3%A4gliche%20Anschriften%C3%A4nderung%20Personalausweis%2FReisepass%2FeAT%5D=0&CASETYPES%5BNachtr%C3%A4gliches%20Einschalten%20eID%20%2F%20Nachtr%C3%A4gliche%20%C3%84nderung%20PIN%5D=0&CASETYPES%5BWiderruf%20der%20Verlust-%20oder%20Diebstahlanzeige%20von%20Personalausweis%20oder%20Reisepass%5D=0&CASETYPES%5BVerlust-%20oder%20Diebstahlanzeige%20von%20Personalausweis%5D=0&CASETYPES%5BVerlust-%20oder%20Diebstahlanzeige%20von%20Reisepass%5D=0&CASETYPES%5BPersonalausweis%2C%20Reisepass%20oder%20eID-Karte%20abholen%5D=0&CASETYPES%5BF%C3%BChrungszeugnis%20beantragen%5D=0&CASETYPES%5BGewerbezentralregisterauskunft%20beantragen%20%E2%80%93%20nat%C3%BCrliche%20Person%5D=0&CASETYPES%5BGewerbezentralregisterauskunft%20beantragen%20%E2%80%93%20juristische%20Person%5D=0&CASETYPES%5BBis%20zu%205%20Beglaubigungen%20Unterschrift%5D=0&CASETYPES%5BBis%20zu%205%20Beglaubigungen%20Dokument%5D=0&CASETYPES%5BBis%20zu%2020%20Beglaubigungen%5D=0&CASETYPES%5BFahrzeug%20wieder%20anmelden%5D=0&CASETYPES%5BFahrzeug%20au%C3%9Fer%20Betrieb%20setzen%5D=0&CASETYPES%5BAdress%C3%A4nderung%20in%20Fahrzeugpapiere%20eintragen%20lassen%5D=0&CASETYPES%5BNamens%C3%A4nderung%20in%20Fahrzeugpapiere%20eintragen%20lassen%5D=0'
        with requests.Session() as s:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            s.get(self.url)
            self.cookie = s.cookies
            print(self.cookie)
            r = s.post(self.url,
                       data=payload, headers=headers)

            rawHTML = str(r.content.decode())
            finder = re.findall(r'jsonAppoints = .*;', rawHTML)[0][16:-2]
            jDates = (json.loads(finder))
            s.get(self.url2)

            self.cookie2 = s.cookies
            r = s.post(self.url2,
                       data=payload, headers=headers)

            rawHTML2 = str(r.content.decode())
            finder2 = re.findall(r'jsonAppoints = .*;', rawHTML2)[0][16:-2]

            jDates.update(dict(json.loads(finder2)))
            for place in jDates:
                # print(jDates[place]["caption"])
                self.treeview.insert("", "end", text=(jDates[place]["caption"]), iid=place)
                P = jDates[place]
                for row in P["appoints"]:
                    if (len(P["appoints"][row]) > 0):
                        self.treeview.insert(place, "end", text=(row), iid=place + "___" + row + "___")
                        for i in P["appoints"][row]:
                            self.treeview.insert(place + "___" + row + "___", "end", text=(i),
                                                 tags=["final"] if jDates[place][
                                                                       "caption"] != "Bürgerbüro Ruppertstraße" else [
                                                     "final", "rup"])
            self.treeview.bind('<ButtonRelease-1>', self.selectItem)


if __name__ == "__main__":
    app = App()
    app.mainloop()

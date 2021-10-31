import json


class Kalorije:
    def __init__(self):
        self.jedi = []
        self.jedilniki = []
        self._jedi_po_imenih = {}
        self._jedilniki_po_imenih = {}

    def dodaj_jed(self, ime, ogljikovi_hidrati=0, beljakovine=0, mascobe=0):
        if ime in self._jedi_po_imenih:
            return ValueError('To ze imas')
        nova = Jed(ime, ogljikovi_hidrati, beljakovine, mascobe)
        self.jedi.append(nova)
        self._jedi_po_imenih[ime] = nova
        return nova

    def odstrani_jed(self, jed):
        self.jedi.remove(jed)
        del self._jedi_po_imenih[jed.ime]

    def dodaj_v_jedilnik(self, ime, zajtrk, kosilo, vecerja):
        if ime in self._jedilniki_po_imenih:
            raise ValueError('To ze imas')
        nov = Jedilnik(ime, zajtrk, kosilo, vecerja)
        self.jedilniki.append(nov)
        self._jedilniki_po_imenih[ime] = nov
        return nov

    def odstrani_jedilnik(self, jedilnik):
        self.jedilniki.remove(jedilnik)
        del self._jedilniki_po_imenih[jedilnik.ime]

    def poisci_jedilnik(self, ime):
        return self._jedilniki_po_imenih[ime]

    def poisci_jed(self, ime):
        return self._jedi_po_imenih[ime]

    def izracun_kalorij(self, ogljikovi_hidrati, beljakovine, mascobe):
        vrednost = ogljikovi_hidrati * 4 + beljakovine * 4 + mascobe * 9
        return vrednost

    def seznam_jedi(self):
        return {
            'jedi': [{
                'ime': jed.ime,
                'ogljikovi_hidrati': jed.ogljikovi_hidrati,
                'beljakovine': jed.beljakovine,
                'mascobe': jed.mascobe,
            } for jed in self.jedi],
            
            'jedilniki': [{
                'ime': jedilnik.ime,
                'zajtrk': jedilnik.zajtrk,
                'kosilo': jedilnik.kosilo,
                'vecerja': jedilnik.vecerja,
            } for jedilnik in self.jedilniki]
        }

    @classmethod
    def nalozi_iz_seznama(cls, seznam_jedi):
        kalorije = cls()
        for jed in seznam_jedi['jedi']:
            kalorije.dodaj_jed(
                jed['ime'],
                jed['ogljikovi_hidrati'],
                jed['beljakovine'],
                jed['mascobe'],
            )
        for jedilnik in seznam_jedi['jedilniki']:
            kalorije.dodaj_v_jedilnik(
                jedilnik['ime'],
                jedilnik['zajtrk'],
                jedilnik['kosilo'],
                jedilnik['vecerja'],
            )
        return kalorije

    def shrani_seznam(self, ime_datoteke):
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            json.dump(self.seznam_jedi(), datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def nalozi_seznam(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            seznam_jedi = json.load(datoteka)
        return cls.nalozi_iz_seznama(seznam_jedi)

    def napake_v_jedeh(self, ime):
        napake = {}
        if not ime:
            napake["ime"] = "Ime mora biti neprazno."
        for jed in self.jedi:
            if jed.ime == ime:
                napake["ime"] = "Ime je že zasedeno."
        return napake

class Jed:
    def __init__(self, ime, ogljikovi_hidrati, beljakovine, mascobe):
        self.ime = ime
        self.ogljikovi_hidrati = ogljikovi_hidrati
        self.beljakovine = beljakovine
        self.mascobe = mascobe

class Jedilnik:
    def __init__(self, ime, zajtrk, kosilo, vecerja):
        self.ime = ime
        self.zajtrk = zajtrk
        self.kosilo = kosilo
        self.vecerja = vecerja

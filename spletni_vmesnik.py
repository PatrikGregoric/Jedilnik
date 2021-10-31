from os import path
import bottle
from osnova import Kalorije
from datetime import date

def uporabnikov_jedilnik():
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime')
    if uporabnisko_ime:
        try:
            kalorije = Kalorije.nalozi_seznam(uporabnisko_ime)
        except FileNotFoundError:
            kalorije = Kalorije()
        return kalorije
    else:
        bottle.redirect('/prijava/')

def shrani_uporabnikov_jedilnik(kalorije):
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime')
    kalorije.shrani_seznam(uporabnisko_ime)

@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napake = {}, polja = {}, uporabnisko_ime = None)

@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/")
    bottle.redirect('/')

@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie("uporabnisko_ime", path="/")
    bottle.redirect('/')

@bottle.get('/')
def prva_stran():
    kalorije = uporabnikov_jedilnik()
    return bottle.template(
        'osnovna_stran.html',
        kalorije=kalorije,
        uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime')
        )

@bottle.get('/jedi/')
def moje_jedi():
    kalorije = uporabnikov_jedilnik()
    return bottle.template("jedi", kalorije=kalorije, uporabnisko_ime=bottle.request.get_cookie('uporabnisko_ime'))

@bottle.get('/jedilniki/')
def moji_jedilniki():
    kalorije = uporabnikov_jedilnik()
    return bottle.template("jedilniki", kalorije=kalorije, uporabnisko_ime=bottle.request.get_cookie('uporabnisko_ime'))

@bottle.get('/dodaj-v-jedilnik/')
def dodaj_v_jedilnik_get():
    kalorije = uporabnikov_jedilnik()
    return bottle.template("dodaj_jedilnik", kalorije=kalorije, uporabnisko_ime=bottle.request.get_cookie('uporabnisko_ime'))

@bottle.post('/dodaj-v-jedilnik/')
def dodaj_v_jedilnik_post():
    kalorije = uporabnikov_jedilnik()
    ime = bottle.request.forms.getunicode('ime_jedilnika')
    zajtrk = bottle.request.forms.getunicode('zajtrk')
    kosilo = bottle.request.forms.getunicode('kosilo')
    vecerja = bottle.request.forms.getunicode('vecerja')
    kalorije.dodaj_v_jedilnik(ime, zajtrk, kosilo, vecerja)
    shrani_uporabnikov_jedilnik(kalorije)
    bottle.redirect('/')

@bottle.get('/dodaj-jed/')
def dodaj_jed_get():
    kalorije = uporabnikov_jedilnik()
    return bottle.template("dodaj_jed", kalorije=kalorije, napake={}, polja={}, uporabnisko_ime=bottle.request.get_cookie('uporabnisko_ime'))

@bottle.post('/dodaj-jed/')
def dodaj_jed_post():
    kalorije = uporabnikov_jedilnik()
    ime = bottle.request.forms.getunicode('ime_jedi')
    ogljikovi_hidrati = int(bottle.request.forms['ogljikovi_hidrati'])
    beljakovine = int(bottle.request.forms['beljakovine'])
    mascobe = int(bottle.request.forms['mascobe'])
    napake = kalorije.napake_v_jedeh(ime)
    polja = {"ime": ime}
    if napake:
        return bottle.template("dodaj_jed", napake=napake, polja=polja, uporabnisko_ime=bottle.request.get_cookie('uporabnisko_ime'))
    else:
        kalorije.dodaj_jed(ime, ogljikovi_hidrati, beljakovine, mascobe)
        kalorije.izracun_kalorij(ogljikovi_hidrati, beljakovine, mascobe)
        shrani_uporabnikov_jedilnik(kalorije)
        bottle.redirect('/')

@bottle.post('/odstrani-jed/')
def odstrani_jed():
    kalorije = uporabnikov_jedilnik()
    jed = kalorije.poisci_jed(bottle.request.forms['jed'] or None)
    kalorije.odstrani_jed(jed)
    shrani_uporabnikov_jedilnik(kalorije)
    bottle.redirect('/jedi/')

@bottle.post('/odstrani-jedilnik/')
def odstrani_jedilnik():
    kalorije = uporabnikov_jedilnik()
    jedilnik = kalorije.poisci_jedilnik(bottle.request.forms['jedilnik'] or None)
    kalorije.odstrani_jedilnik(jedilnik)
    shrani_uporabnikov_jedilnik(kalorije)
    bottle.redirect('/jedilniki/')

bottle.run(reloader=True, debug=True)

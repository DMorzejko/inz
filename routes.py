# Routes - to tutaj ustawiamy wszystkie linki i podpinamy do nich funkcje

from flask import *
routes = Blueprint('routes', __name__)

from layout import *
from funkcje import *

@routes.route('/logowanie')
def W_logowanie():
    return wyswietl(2, ["Logowanie", logowanie(), ['formularz_nowy_pacjent.css']])

@routes.route('/nowy_pacjent')
def W_nowy_pacjent():
    return wyswietl(2, ["Dodaj krwiodawcę", nowy_pacjent(), ['formularz_nowy_pacjent.css']])

@routes.route('/pobierz_krew', methods = ['GET'])
def W_pobierz_krew():
    krwiodawca = request.args.get('krwiodawca')
    return wyswietl(2, ["Pobierz krew", pobierz_krew(krwiodawca), ['pobierz_krew.css']])

@routes.route('/historia', methods = ['GET'])
def W_historia_pobran():
    data1 = request.args.get('data1')
    data2 = request.args.get('data2')
    return wyswietl(2, ["Historia pobrań", historia(data1, data2), ['historia_pobran.css']])

@routes.route('/badania')
def W_badania():
    return wyswietl(2, ["Wyniki badań", badania(), ['']])

@routes.route('/tabela', methods = ['GET'])
def W_stany():
    oddzial = request.args.get('oddzial_id')
    return wyswietl(2, ["Stany krwi", stany(oddzial), ['stany_krwi.css','tabelka_krwiodawcy.css']])

@routes.route('/o_projekcie')
def W_o_projekcie():
    return wyswietl(2, ["O projekcie", o_projekcie(), ['']])


@routes.route('/nowy_pacjent_odbierz', methods = ['POST'])
def W_nowy_pacjent_odbierz():
    # Pobierz dane z formularza
    imie = request.form['imie']
    nazwisko = request.form['nazwisko']
    plec = request.form['plec']
    data_ur = request.form['data']
    gk_id = request.form['grupakrwi_id']
    adres = request.form['adres']
    opis = request.form['opis']
    pesel = request.form['pesel']

    # Wstaw dane do bazy
    dane = [gk_id, imie, nazwisko, plec, data_ur, pesel, adres, opis]
    dodajKrwiodawce(dane)

    # Wyswietl jakis testowy HTML
    html = "<h1>Dodano " + imie + " " + nazwisko + ".</h1>"
    html += "<a href=\"/krwiodawcy\">Zobacz</a><br><br>"
    html += "<a href=\"/nowy_pacjent\">Dodaj kolejny</a><br>"

    return wyswietl(2, ["Nowy Pacjent", html, ['formularz_nowy_pacjent.css']])

@routes.route('/krwiodawcy')
def W_krwiodawcy():
    return wyswietl(2, ["Krwiodawcy", krwiodawcy(), ['tabelka_krwiodawcy.css']])

@routes.route('/poziomy')
def W_poziomy():
    return wyswietl(2, ["Poziomy", poziomy(), ['formularz_nowy_pacjent.css']])

@routes.route('/kontakt')
def W_funkcja2():
    return wyswietl(2, ["Kontakt", kontakt(), ['']])

@routes.route('/info')
def W_funkcja3():
    return wyswietl(2, ["Info", info(), ['']])

@routes.route('/interfejs')
def W_interfejs():
    return render_template('interfejs-test.html')

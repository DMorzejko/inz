# Routes - to tutaj ustawiamy wszystkie linki i podpinamy do nich funkcje

from flask import *
routes = Blueprint('routes', __name__)

from layout import *
from funkcje import *

@routes.route('/logowanie')
def W_logowanie():
    return wyswietl(2, ["Logowanie", logowanie(), ['']])

@routes.route('/nowy_pacjent')
def W_nowy_pacjent():
    return wyswietl(2, ["Dodaj krwiodawcę", nowy_pacjent(), ['']])

@routes.route('/projekt')
def W_projekt():
        return wyswietl(2, ["Logowanie", info(), ['']])

@routes.route('/mapa', methods = ['GET'])
def W_mapa():
    data1 = request.args.get('data1')
    data2 = request.args.get('data2')
    return wyswietl(2, ["Mapa", historia(data1, data2), ['']])

@routes.route('/badania')
def W_badania():
    return wyswietl(2, ["Wyniki badań", badania(), ['']])

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

    return wyswietl(2, ["Nowy Pacjent", html, ['']])

@routes.route('/tabela')
def W_tabela():
    return wyswietl(2, ["Tabela", tabela(), ['']])

@routes.route('/poziomy')
def W_poziomy():
    return wyswietl(2, ["Poziomy", poziomy(), ['']])

@routes.route('/kontakt')
def W_funkcja2():
    return wyswietl(2, ["Kontakt", kontakt(), ['']])


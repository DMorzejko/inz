# Routes - to tutaj ustawiamy wszystkie linki i podpinamy do nich funkcje

from flask import *
routes = Blueprint('routes', __name__)

from layout import *
from funkcje import *

@routes.route('/logowanie')
def W_logowanie():
    return wyswietl(1, ["Logowanie", logowanie(), ['']])

@routes.route('/projekt')
def W_projekt():
    return wyswietl(1, ["Logowanie", info(), ['']])

@routes.route('/tabela')
def W_tabela():
    return wyswietl(1, ["Tabela obiektów", tabela(), ['']])

@routes.route('/mapa')
def W_mapa():
    mapa = 0
    return wyswietl(1, ["Mapa", mapa, ['']])



@routes.route('/kontakt')
def W_funkcja2():
    return wyswietl(1, ["Kontakt", kontakt(), ['']])

@routes.route('/nowy_obiekt')
def W_nowy_obiekt():
    return wyswietl(1, ["Nowy Obiekt", poziomy(), ['']])


@routes.route('/nowy_obiekt_odbierz', methods = ['POST'])
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
    dodajObiekt(dane)

    # Wyswietl jakis testowy HTML
    html = "<h1>Dodano " + imie + " " + nazwisko + ".</h1>"
    html += "<a href=\"/krwiodawcy\">Zobacz</a><br><br>"
    html += "<a href=\"/nowy_pacjent\">Dodaj kolejny</a><br>"

    return wyswietl(1, ["Nowy Pacjent", html, ['']])












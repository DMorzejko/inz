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

@routes.route('/edit/<int:obiekt_id>', methods=['GET', 'POST'])
def edit_obiekt(obiekt_id):
    obiekt = get_obiekt_by_id(obiekt_id)

    if obiekt is None:
        return "Obiekt o podanym ID nie istnieje.", 404

    if request.method == 'POST':
        updated_data = (
            request.form['nazwa'],
            request.form['klient'],
            request.form['ulica'],
            request.form['numer_budynku'],
            request.form['kod_pocztowy'],
            request.form['miasto'],
            request.form['czynnosc'],
            request.form['ilosc_bram'],
            request.form['uwagi'],
            request.form['zrobione'] == 'on'
        )
        update_obiekt(obiekt_id, updated_data)
        return redirect(url_for('routes.W_tabela'))
    tresc = render_template('edit_obiekt.html', obiekt=obiekt)
    return wyswietl(1, ["Edycja obiektu", tresc, ['style.css']])
@routes.route('/kontakt')
def W_funkcja2():
    return wyswietl(1, ["Kontakt", kontakt(), ['']])

@routes.route('/delete/<int:obiekt_id>')
def delete_obiekt_route(obiekt_id):
    delete_obiekt(obiekt_id)
    return redirect(url_for('routes.W_tabela'))


@routes.route('/nowy_obiekt', methods=['GET', 'POST'])
def nowy_obiekt():
    if request.method == 'POST':
        nazwa = request.form['nazwa']
        klient = request.form['klient']
        ulica = request.form['ulica']
        numer_budynku = request.form['numer_budynku']
        kod_pocztowy = request.form['kod_pocztowy']
        miasto = request.form['miasto']
        osoba_kontaktowa = request.form['osoba_kontaktowa']
        numer_kontaktowy = request.form['numer_kontaktowy']
        czynnosc = request.form['czynnosc']
        ilosc_bram = request.form['ilosc_bram']
        uwagi = request.form['uwagi']
        zrobione = request.form['zrobione']

        dodaj_obiekt_baza(nazwa, klient, ulica, numer_budynku, kod_pocztowy, miasto, osoba_kontaktowa, numer_kontaktowy, czynnosc, ilosc_bram, uwagi, zrobione)
        return redirect(url_for('routes.W_tabela'))

    tresc = render_template('dodaj_obiekt.html')
    return wyswietl(1, ["Dodaj nowy obiekt", tresc, ['style.css']])














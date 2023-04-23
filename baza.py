# Funkcje łączące do bazy danych - wyświetlanie, wstawienie, usuwanie, itp.
from datetime import datetime
from flask import *

baza = Blueprint('baza', __name__)

import mysql.connector
import random
import string
import hashlib
import binascii



# Pobiera "surowe" dane z funkcji tabelaBaza() i wyswietla w tabelce
def tabela():
    wynik = tabelaBaza()
    id = tabelaBazaId()

    i=0
    html = """
    <script>
    function editSelectedObiekt() {
        var checkboxes = document.querySelectorAll('input[type=checkbox]');
        var selectedId = null;
    
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                selectedId = checkboxes[i].id.replace('checkbox_', '');
                break;
            }
        }
    
        if (selectedId !== null) {
            location.href = '/edit/' + selectedId;
        } else {
            alert('Proszę zaznaczyć obiekt do edycji.');
        }
    }
    </script>
    <div class="form-tytul">
    <br>
            <span class="tytul2"><h2>Tabela obiektów</h2></span>
            </div>
            <div class="przyciski"><br>
            <br>
            <a href="/nowy_obiekt" class="btn btn-light btn-lg"><span class="link">Dodaj Obiekt</span></a>
            <button name="edytuj" id="button_edytuj" type="edit" class="btn btn-light btn-lg" onclick="editSelectedObiekt()">Edytuj / Pokaż</button>
            <button name="usun" id="button_usun" type="delete" class="btn btn-light btn-lg">Usuń</button>
            <br><br>""" \
           "<table class=\"Tabela-obiektow table table-success table-striped\">\n"
    html += "<tr><td>Zaznacz</td><td>Nazwa Obiektu</td><td>Klient</td><td>Ulica</td><td>Numer budynku</td><td>Kod Pocztowy</td>" \
            "<td>Miasto</td><td>Czynność</td><td>Ilość Bram</td><td>Uwagi</td><td>Zrobione?</td></tr>\n"
    for obiekt in wynik:
        html += '<tr><td><input type="checkbox" id="checkbox_{}" name="checkbox_{}"><span></span></td>'.format(obiekt[0], obiekt[0])
        for pole in obiekt[1:]:
            html += """<td>""" + str(pole) + "</td>"
        html += "</tr>\n"
    html += "</table>\n"
    return html

# Zwraca liste wszystkich krwiodawców z bazy danych
# ( result[0] to lista danych jednego krwiodawcy, a np. result[0][0] to id pierwszego kriwodawcy )
def tabelaBaza():
    conn = DbConnection()
    sql = "SELECT Id, Nazwa, Klient, Ulica, Numer_Budynku, Kod_pocztowy, " \
          "Miasto, Czynnosc, Ilosc_bram, Uwagi, Zrobione " \
          "from Obiekt order by Nazwa;"
    conn.execute(sql)
    result = conn.getData()
    del conn
    return result

def list_to_dict(obiekt_list):
    keys = ['Id', 'Nazwa', 'Klient', 'Ulica', 'Numer_Budynku', 'Kod_Pocztowy', 'Miasto', 'Osoba_Kontaktowa', 'Numer_Kontaktowy', 'Czynnosc', 'Ilosc_Bram', 'Uwagi', 'Zrobione']
    return {keys[i]: obiekt_list[i] for i in range(len(keys))}
def get_obiekt_by_id(obiekt_id):
    conn = DbConnection()
    sql = "SELECT * FROM Obiekt WHERE Id = %s;"
    o = (obiekt_id,)
    conn.execute(sql, o)
    result = conn.getData()
    del conn

    obiekt = result[0] if result else None

    if obiekt is not None:
        obiekt = list_to_dict(obiekt)

    # Wydrukuj zwracany obiekt
    print("Zwracany obiekt:", obiekt)

    return obiekt
def tabelaBazaId():
    conn = DbConnection()
    sql = "SELECT Id from Obiekt  order by Nazwa;"
    conn.execute(sql)
    result = conn.getData()
    print(result[0])
    del conn
    return result
def update_obiekt(obiekt_id, updated_data):
    conn = DbConnection()
    sql = """UPDATE Obiekt SET Nazwa=%s, Klient=%s, Ulica=%s, Numer_Budynku=%s,
             Kod_pocztowy=%s, Miasto=%s, Czynnosc=%s, Ilosc_bram=%s, Uwagi=%s, Zrobione=%s
             WHERE Id=%s;"""
    conn.execute(sql, (*updated_data, obiekt_id))
    conn.commit()
    del conn


# Zwraca dane krwiodawcy o podanym id w postaci listy
def krwiodawca(id):
    conn = DbConnection()
    conn.execute('SELECT * FROM Krwiodawcy WHERE Id=' + str(id))
    result = conn.getData()[0]
    del conn
    return result


# Zwraca listę stanów krwi, przy podaniu id oddziału zwraca stany w ml dla danego oddziału z podziałem na grupy

# zwraca listę oddziałów wraz z adresem


# Dodaje krwiodawce do bazy danych, należy podać listę danych do funkcji
# Format: # [grupaKrwi_id, 'Stefan', 'Nowak', 'M', '12-10-1945', '12345678901', 'Struga 12, Opole', 'Opis']
def dodajObiekt(data):
    conn = DbConnection()
    sql = 'SELECT MAX(Id) FROM Obiekt'
    conn.execute(sql)
    Id = conn.getData()[0][0] + 1
    sql = "INSERT INTO Obiekt (id, Nazwa, Klient, Ulica, Numer_Budynku, Kod_Pocztowy, Miasto, Osoba_Kontaktowa, "\
        "Numer_Kontaktowy, Czynnosc, Ilosc_bram, Uwagi, Zrobione) VALUES ({}, '{}','{}','{}','{}','{}','{}', '{}', '{}', '{}', '{}', '{}', '{}')"\
        .format(Id, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11])
    conn.execute(sql)
    conn.commit()
    print(sql)
    del conn


# Zmiania dane krwiodawcy o danym id. W argumecie id należy podać id krwiodawcy,
# w data - tablicę danych [grupaKrwi_id, imie, nazwisko, płeć, data_urodzenia, pesel, adres, dodatkowy_opis]
'''def edytujKrwiodawce(id, data):
    conn = DbConnection()
    sql = f'UPDATE Krwiodawcy SET ' \
          f'grupy_krwi_id = {data[0]}, ' \
          f'imie = {data[1]}, ' \
          f'nazwisko = {data[2]}, ' \
          f'plec = {data[3]}, ' \
          f'data_urodzenia = {data[4]}, ' \
          f'pesel = {data[5]}, ' \
          f'adres = {data[6]}, ' \
          f'dodatkowy_opis = {data[7]} ' \
          f'WHERE id = {id}'
    conn.execute(sql)
    conn.commit()
    del conn
'''



# klasa połączenia z bazą - utworzenie instancji klasy tworzy połączenie i ułatwia obsługe bazy
class DbConnection:

    # __init__ tworzy połączenie przy stworzeniu instancji klasy ( np. db = DbConnection() )
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='mysql0.small.pl',
            port='3306',
            user='m2518_jelen',
            password="Silnehaslo123",
            database="m2518_inz",
            charset="utf8")
        self.cursor = self.connection.cursor()

    # __del__ zamyka połączenie przy usunięciu instancji klasy ( np. del db )
    def __del__(self):
        self.cursor.close()
        self.connection.close()

    # execute wykonuje podane polecenie sql ( np. db.execute('SELECT * FROM ...') )
    def execute(self, sql, params=None):
        if params is not None:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)

    # zatwirdza wprowadzone do bazy zmiany ( np. db.commit() )
    def commit(self):
        self.connection.commit()

    # zwraca dane z kursora w postaci listy, której każdy wiersz jest listą/wierszem z wyniku zapytania
    def getData(self):
        rowdata = []
        data = []
        for row in self.cursor.fetchall():
            for item in row:
                rowdata.append(item)
            data.append(rowdata.copy())
            rowdata.clear()
        return data
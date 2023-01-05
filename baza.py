# Funkcje łączące do bazy danych - wyświetlanie, wstawienie, usuwanie, itp.
from datetime import datetime
from flask import *

baza = Blueprint('baza', __name__)

# Zainstalujcie "mysql-connector-python" (bo są 2 do wyboru)
import mysql.connector


# Pobiera "surowe" dane z funkcji krwiodawcyBaza() i wyswietla w tabelce
def tabela():
    wynik = tabelaBaza()
    html = """<div class="form-tytul">
            <span class="tytul2"><h2>Tabela obiektów</h2></span>
            </div>""" \
           "<table class=\"Tabela-obiektow\">\n"
    html += "<tr><td>Nazwa Obiektu</td><td>KLient</td><td>Ulica</td><td>Numer budynku</td><td>Kod Pocztowy</td>" \
            "<td>Miasto</td><td>Czynność</td><td>Ilość Bram</td><td>Uwagi</td><td>Zrobione?</td></tr>\n"
    for krwiodawca in wynik:
        html += "<tr>"
        for pole in krwiodawca:
            html += "<td>" + str(pole) + "</td>"
        html += "</tr>\n"
    html += "</table>\n"
    return html

# Zwraca liste wszystkich krwiodawców z bazy danych
# ( result[0] to lista danych jednego krwiodawcy, a np. result[0][0] to id pierwszego kriwodawcy )
def tabelaBaza():
    conn = DbConnection()
    # conn.execute('SELECT * FROM Krwiodawcy')
    sql = "SELECT Nazwa, Klient, Ulica, Numer_Budynku, Kod_pocztowy, " \
          "Miasto, Czynnosc, Ilosc_bram, Uwagi, Zrobione " \
          "from Obiekt  order by Nazwa;"
    conn.execute(sql)
    result = conn.getData()
    del conn
    return result


# Zwraca dane krwiodawcy o podanym id w postaci listy
def krwiodawca(id):
    conn = DbConnection()
    conn.execute('SELECT * FROM Krwiodawcy WHERE Id=' + str(id))
    result = conn.getData()[0]
    del conn
    return result


# Zwraca listę stanów krwi, przy podaniu id oddziału zwraca stany w ml dla danego oddziału z podziałem na grupy
def stanKrwi(idOddzialu=None):
    conn = DbConnection()
    sql = 'SELECT GrupyKrwi.id, sum(ilosc_ml) FROM Krew ' \
          'JOIN Pobrania ON Krew.pobrania_id = Pobrania.id ' \
          'JOIN Krwiodawcy ON Pobrania.krwiodawcy_id = Krwiodawcy.id ' \
          'JOIN GrupyKrwi ON GrupyKrwi.id = Krwiodawcy.grupy_krwi_id ' \
          'JOIN Pracownicy ON Pracownicy.id = Pobrania.pracownicy_id ' \
          'JOIN Oddzialy ON Oddzialy.id = Pracownicy.oddzial_rckik_id'
    if idOddzialu is not None:
        sql += ' WHERE Oddzialy.id = ' + str(idOddzialu)
    sql += ' GROUP BY 1'
    conn.execute(sql)
    data = conn.getData()[:][:]
    sql = 'SELECT id, CONCAT(GrupyKrwi.Grupa, " RH", GrupyKrwi.RH) FROM GrupyKrwi'
    conn.execute(sql)
    grupy = conn.getData()[:][:]
    del conn
    result = []
    for i in range(len(grupy)):
        grupy[i].append(0)
        for j in data:
            if j[0] == grupy[i][0]:
                grupy[i][2] = int(j[1])
        result.append(grupy[i][1:])
    return result

# zwraca listę grup krwi wraz z id ( [['1', 'A Rh-'], ['2', 'A Rh+'] ... )
def grupyKrwi():
    conn = DbConnection()
    sql = 'SELECT * FROM GrupyKrwi'
    conn.execute(sql)
    data = conn.getData()
    del conn
    result = []
    for i in data:
        result.append([i[0], str(i[1]) + ' Rh' + str(i[2])])
    return result

# zwraca listę oddziałów wraz z adresem
def listaOddzialow():
    conn = DbConnection()
    sql = 'SELECT * FROM Oddzialy'
    conn.execute(sql)
    data = conn.getData()
    del conn
    result = []
    for i in data:
        result.append([i[0], str(i[1])])
    return result

# zwraca listę krwiodawców wraz z id
def listaKrwiodawcow():
    conn = DbConnection()
    sql = 'SELECT id, nazwisko, imie FROM Krwiodawcy order by Nazwisko'
    conn.execute(sql)
    data = conn.getData()
    del conn
    result = []
    for i in data:
        k = str(i[1]) + " " + str(i[2])
        result.append([i[0], k])
    return result


# Dodaje krwiodawce do bazy danych, należy podać listę danych do funkcji
# Format: # [grupaKrwi_id, 'Stefan', 'Nowak', 'M', '12-10-1945', '12345678901', 'Struga 12, Opole', 'Opis']
def dodajKrwiodawce(data):
    conn = DbConnection()
    sql = 'SELECT MAX(Id) FROM Krwiodawcy'
    conn.execute(sql)
    Id = conn.getData()[0][0] + 1
    sql = "INSERT INTO Krwiodawcy (id, grupy_krwi_id, imie, nazwisko, plec, data_urodzenia, pesel, adres," \
          " dodatkowy_opis) VALUES ({}, {}, '{}', '{}', '{}', STR_TO_DATE('{}', '%Y-%m-%d'), '{}', '{}', '{}')"\
        .format(Id, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
    conn.execute(sql)
    conn.commit()
    print(sql)
    del conn


# Zmiania dane krwiodawcy o danym id. W argumecie id należy podać id krwiodawcy,
# w data - tablicę danych [grupaKrwi_id, imie, nazwisko, płeć, data_urodzenia, pesel, adres, dodatkowy_opis]
def edytujKrwiodawce(id, data):
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


# Dodaje pobranie krwi. W argumentach należy podać [id krwiodawcy, id pracownika, ilość pobranej krwi,
# opcjonalnie data pobrania], data w formacie datetime (np. data = datetime(2022, 12, 24) -> 24 grudnia 2022)
def pobranieKrwi(krwiodawca_id, pracownik_id, ml, data=datetime.today()):
    conn = DbConnection()
    # Pobranie ostatnich id
    sql = 'SELECT MAX(Id) FROM Pobrania'
    conn.execute(sql)
    id_pobrania = conn.getData()[0][0] + 1
    sql = 'SELECT MAX(Id) FROM Krew'
    conn.execute(sql)
    id_krew = conn.getData()[0][0] + 1
    # Insert pobrania
    sql = f"INSERT INTO Pobrania (id, krwiodawcy_id, pracownicy_id, data)" \
          f"VALUES ({id_pobrania}, {krwiodawca_id}, {pracownik_id}, " \
          f"STR_TO_DATE('{data.date()}', '%Y-%m-%d'))"
    conn.execute(sql)
    # Insert krew
    sql = f"INSERT INTO Krew (id, ilosc_ml, pobrania_id)" \
          f"VALUES ({id_krew}, {ml}, {id_pobrania})"
    conn.execute(sql)
    conn.commit()
    del conn

# Zwraca historie pobran z zakresu 2 dat
# data_pobrania, ilość, grupa krwi, oddział, krwiodawca
def historia_baza(data_od, data_do):
    conn = DbConnection()
    sql = "select data, ilosc_ml, grupa, rh, Oddzialy.adres, Krwiodawcy.imie, Krwiodawcy.nazwisko from Pobrania left join Krwiodawcy on Pobrania.krwiodawcy_id = Krwiodawcy.id left join Krew on Pobrania.id = Krew.id left join GrupyKrwi on GrupyKrwi.id = Krwiodawcy.grupy_krwi_id left join Pracownicy on Pobrania.pracownicy_id = Pracownicy.id join Oddzialy on Oddzialy.id = Pracownicy.oddzial_rckik_id where data>='" + data_od + "' and data<='" + data_do + "' order by data;"
    conn.execute(sql)
    data = conn.getData()
    del conn
    result = []
    for i in data:
        o = i[4].split() # oddział - samo miasto
        result.append([i[0].strftime("%Y-%m-%d"), str(i[1])+' ml', i[2]+' Rh '+i[3], o[-1], i[5]+' '+i[6]])
    return result


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
    def execute(self, sql):
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
# Funkcje łączące do bazy danych - wyświetlanie, wstawienie, usuwanie, itp.
from flask import *

baza = Blueprint('baza', __name__)

import mysql.connector




# Pobiera "surowe" dane z funkcji tabelaBaza() i wyswietla w tabelce
def tabela():
    wynik = tabelaBaza()
    id = tabelaBazaId()

    i=0
    nowy_obiekt_url = url_for('routes.nowy_obiekt')
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
    function deleteSelectedObiekt() {
    var checkboxes = document.querySelectorAll('input[type=checkbox]');
    var selectedId = null;

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            selectedId = checkboxes[i].id.replace('checkbox_', '');
            break;
        }
    }

    if (selectedId !== null) {
        if (confirm('Czy na pewno chcesz usunąć ten obiekt?')) {
            location.href = '/delete/' + selectedId;
        }
    } else {
        alert('Proszę zaznaczyć obiekt do usunięcia.');
    }
}
    </script>
    <div class="form-tytul">
    
            <span class="tytul2"><h2>Tabela obiektów</h2></span>
            </div>
            <div class="przyciski"><br>
            <br>"""
    html += f"""<br><br><br>
            <a href="{nowy_obiekt_url}" class="btn btn-light btn-lg"><span class="link">Dodaj Obiekt</span></a>            <button name="edytuj" id="button_edytuj" type="edit" class="btn btn-light btn-lg" onclick="editSelectedObiekt()">Edytuj / Pokaż</button>
            """
    html += """
            <button name="usun" id="button_usun" type="button" class="btn btn-light btn-lg" onclick="deleteSelectedObiekt()">Usuń</button>
            <br>
           "<table class=\"Tabela-obiektow table table-success table-striped\">\n"""
    html += "<tr><td>Zaznacz</td><td>Nazwa Obiektu</td><td>Klient</td><td>Ulica</td><td>Numer budynku</td><td>Kod Pocztowy</td>" \
            "<td>Miasto</td><td>Czynność</td><td>Ilość Bram</td><td>Uwagi</td><td>Zrobione?</td></tr>\n"
    for obiekt in wynik:
        html += '<tr><td><input type="checkbox" id="checkbox_{}" name="checkbox_{}" style="transform: scale(1.8);"><span></span></td>'.format(obiekt[0], obiekt[0])
        for pole in obiekt[1:]:
            html += """<td>""" + str(pole) + "</td>"
        html += "</tr>\n"
    html += "</table>\n"
    return html


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
             Kod_Pocztowy=%s, Miasto=%s, Osoba_kontaktowa=%s, Numer_Kontaktowy=%s, Czynnosc=%s, Ilosc_Bram=%s, Uwagi=%s, Zrobione=%s
             WHERE Id=%s;"""
    conn.execute(sql, (*updated_data, obiekt_id))
    conn.commit()
    del conn

def delete_obiekt(obiekt_id):
    conn = DbConnection()
    sql = "DELETE FROM Obiekt WHERE Id = %s;"
    conn.execute(sql, (obiekt_id,))
    conn.commit()
    del conn

def dodaj_obiekt_baza(nazwa, klient, ulica, numer_budynku, kod_pocztowy, miasto, osoba_kontaktowa, numer_kontaktowy, czynnosc, ilosc_bram, uwagi, zrobione):
    conn = DbConnection()
    sql = '''
        INSERT INTO Obiekt (Nazwa, Klient, Ulica, Numer_Budynku, Kod_Pocztowy, Miasto, Osoba_Kontaktowa, Numer_Kontaktowy, Czynnosc, Ilosc_Bram, Uwagi, Zrobione)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    conn.execute(sql, (nazwa, klient, ulica, numer_budynku, kod_pocztowy, miasto, osoba_kontaktowa, numer_kontaktowy, czynnosc, ilosc_bram, uwagi, zrobione))
    conn.commit()
    del conn






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
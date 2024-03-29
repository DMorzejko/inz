# Funkcje łączące do bazy danych - wyświetlanie, wstawienie, usuwanie, itp.
from flask import *


baza = Blueprint('baza', __name__)
import mysql.connector

# Pobiera "surowe" dane z funkcji tabelaBaza() i wyswietla w tabelce
'''def tabela(currentMode):
    wynik = tabelaBaza()
    id = tabelaBazaId()


    table_class = "Tabela-obiektow table table-success table-striped" if currentMode == "light-mode" else "Tabela-obiektow table table-striped table-dark"

    i=0
    nowy_obiekt_url = url_for('nowy_obiekt')
    html = render_template('l2-strona.html', mode=currentMode)
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
    html += f"""
            <button class="btn btn-light btn-lg" onclick="location.href='{url_for('nowy_obiekt')}'">
    <span class="link">Dodaj Obiekt</span>
</button>            <button name="edytuj" id="button_edytuj" type="edit" class="btn btn-light btn-lg" onclick="editSelectedObiekt()">Edytuj / Pokaż</button>
            """
    html += """
            <button name="usun" id="button_usun" type="button" class="btn btn-light btn-lg" onclick="deleteSelectedObiekt()">Usuń</button>
            <br>"""
    # Określanie klasy dla tabeli w zależności od trybu
    html += f"<table class=\"{table_class}\">\n"


    html += "<tr><td>Zaznacz</td><td>Nazwa Obiektu</td><td>Klient</td><td>Ulica</td><td>Numer budynku</td><td>Kod Pocztowy</td>" \
            "<td>Miasto</td><td>Czynność</td><td>Ilość Bram</td><td>Uwagi</td><td>Pilne</td><td>Zrobione?</td></tr>\n"
    for obiekt in wynik:
        html += '<tr><td><input type="checkbox" id="checkbox_{}" name="checkbox_{}" style="transform: scale(1.8);"><span></span></td>'.format(obiekt[0], obiekt[0])
        for pole in obiekt[1:]:
            html += """<td>""" + str(pole) + "</td>"
        html += "</tr>\n"
    html += "</table>\n"
    return html'''






def tabelaBaza():
    conn = DbConnection()
    sql = "SELECT Id, Nazwa, Klient, Ulica, Numer_Budynku, Kod_pocztowy, " \
          "Miasto, Czynnosc, Ilosc_bram, Uwagi, Pilne, Zrobione " \
          "from Obiekt order by Nazwa;"
    conn.execute(sql)
    result = conn.getData()
    del conn
    return result

def tabelaBazaId():
    conn = DbConnection()
    sql = "SELECT Id from Obiekt  order by Nazwa;"
    conn.execute(sql)
    result = conn.getData()
    del conn
    return result

def list_to_dict(obiekt_list):
    keys = ['Id', 'Nazwa', 'Klient', 'Ulica', 'Numer_Budynku', 'Kod_Pocztowy', 'Miasto', 'Osoba_Kontaktowa',\
           'Numer_Kontaktowy', 'Czynnosc', 'Ilosc_Bram', 'Uwagi', 'Pilne', 'Zrobione']
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
    return obiekt

def update_obiekt(obiekt_id, updated_data):
    conn = DbConnection()
    sql = """UPDATE Obiekt SET Nazwa=%s, Klient=%s, Ulica=%s, Numer_Budynku=%s,
             Kod_Pocztowy=%s, Miasto=%s, Osoba_kontaktowa=%s, Numer_Kontaktowy=%s,
             Czynnosc=%s, Ilosc_Bram=%s, Uwagi=%s, Pilne=%s, Zrobione=%s
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


def dodaj_obiekt_baza(nazwa, klient, ulica, numer_budynku, kod_pocztowy, miasto, osoba_kontaktowa, numer_kontaktowy, czynnosc, ilosc_bram, uwagi, pilne, zrobione):
    conn = DbConnection()
    sql = '''
        INSERT INTO Obiekt (Nazwa, Klient, Ulica, Numer_Budynku, Kod_Pocztowy, Miasto, Osoba_Kontaktowa, Numer_Kontaktowy, Czynnosc, Ilosc_Bram, Uwagi, Pilne, Zrobione)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    conn.execute(sql, (nazwa, klient, ulica, numer_budynku, kod_pocztowy, miasto, osoba_kontaktowa, numer_kontaktowy, czynnosc, ilosc_bram, uwagi, pilne, zrobione))
    conn.commit()
    del conn

def get_user_by_username(username):
    from main import User
    conn = DbConnection()
    sql = "SELECT * FROM users WHERE username = %s"
    conn.execute(sql, (username,))
    user_data = conn.getData()
    if user_data:
        user_id = user_data[0][0]
        password = user_data[0][2]
        email = user_data[0][3]
        is_active = user_data[0][4]
        is_admin = user_data[0][5]

        user = User(user_id, username, password, email, is_active, is_admin)
        return user

    return None

def get_user_by_id(user_id):
    conn = DbConnection()
    conn.execute("SELECT id, username, password, email, is_active, is_admin FROM users WHERE id = %s", (user_id,))
    user = conn.getData()
    if user:
        return User(*user[0])
    return None


class User:
    def __init__(self, id, username, password, email, is_active, is_admin):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.is_active = is_active
        self.is_admin = is_admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)






# klasa połączenia z bazą - utworzenie instancji klasy tworzy połączenie i ułatwia obsługe bazy
class DbConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='mysql0.small.pl',
            port='3306',
            user='m2518_jelen',
            password="Silnehaslo123",
            database="m2518_inz",
            charset="utf8")
        self.cursor = self.connection.cursor()
    def __del__(self):
        self.cursor.close()
        self.connection.close()
    def execute(self, sql, params=None):
        if params is not None:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
    def commit(self):
        self.connection.commit()
    def getData(self):
        rowdata = []
        data = []
        for row in self.cursor.fetchall():
            for item in row:
                rowdata.append(item)
            data.append(rowdata.copy())
            rowdata.clear()
        return data
# Funkcje wyświetlające "treść" - wycinek kodu HTML, który zostanie wrzucony w dane miejsce na stronie

from flask import *
funkcje = Blueprint('funkcje', __name__)

from baza import *

def logowanie():
    return render_template('logowanie.html')

'''def pobierz_krew(krwiodawca):
    # Sprawdz wybrany oddzial
    if krwiodawca is None:
        krwiodawca = -1
    if krwiodawca == "":
        krwiodawca = -1

    # Pobierz listę oddzialów z bazy
    kk = listaKrwiodawcow()
    k_lista = ""
    if krwiodawca == -1:
        k_lista += "<option disabled selected value></option>"
    for k in kk:
        if str(krwiodawca) == str(k[0]):
            zaznacz = " selected"
        else:
            zaznacz = ""
        k_lista += "<option value=\"" + str(k[0]) + "\"" + zaznacz + ">" + k[1] + "</option>\n"

    s2 = ""
    # Jeśli jest wybrany oddział
    if krwiodawca != -1:
        # Pobierz stany z bazy
        s2 += "<br><h1>Id krwiodawcy: " + str(krwiodawca) + "</h1></br>\n"
        # Wyswietl kolejne dane i pola formularza
        s2 += "<p>Tu będzie dalsza część fomularza... </p>\n";

    s1 =  render_template('projekt.html',krwiodawcy=k_lista)
    return s1 + s2'''

'''def historia(data1, data2):
    # Sprawdz daty
    if data1 is None:
        data1 = ''
    if data1 == "":
        data1 = ''

    if data2 is None:
        data2 = ''
    if data2 == "":
        data2 = ''

    # Ustaw daty domyślne do wyświetlenia (jeśli nie wybrano)
    d1 = data1
    d2 = data2
    if d1 == '':
        d1 = '2010-01-01'
    if d2 == '':
        d2 = '2022-12-31'

    tabelka = ''
    if (data1 != '' and data2 != ''):
        # Pobierz dane z bazy
        dane = historia_baza(data1, data2)

        # Tabelka
        tabelka ="<!-- Tabelka historia -->\n"
        tabelka += "<table class=\"Tabelka-historia\">\n"
        tabelka += "<tr><th>Lp.</th><th>Data</th><th>Ilość</th><th>Gr. krwi</th><th>Oddział</th><th>Krwiodawca</th></tr>\n"

        i=0
        for d in dane:
            i += 1
            tabelka += "<tr><td>" + str(i) + "</td><td>"+ d[0] + "</td><td>" + d[1] + "</td><td>" + d[2] + "</td><td>" + d[3] + "</td><td>" + d[4] + "</td></tr>\n"

        # Jeśli tabelka pusta - wyświetl info
        if (len(dane) == 0):
            tabelka += "<tr><td colspan=6>Brak pobrań krwi z tego zakresu dat.</td></tr>\n"

        tabelka += "</table>\n"
        tabelka += "<!-- Tabelka historia -->\n"

    s1 =  render_template('mapa.html', d1=d1, d2=d2)
    return s1 + tabelka'''


def badania():
    return "<h1>Wyniki badań</h1>"

'''def stany(oddzial):
    # Liczba ml uznawana jako 100%
    STANY_MAX = 1000

    # Sprawdź parametry czy jest wybrany oddział
    if oddzial is None:
        oddzial = -1
    if oddzial == "":
        oddzial = -1

    # Pobierz listę oddzialów z bazy - pole rozwijane
    odd = listaOddzialow()
    oddzialy_lista = ""
    if oddzial == -1:
        oddzialy_lista += "<option disabled selected value></option>"
    for o in odd:
        if str(oddzial) == str(o[0]):
            zaznacz = " selected"
        else:
            zaznacz = ""
        oddzialy_lista += "<option value=\"" + str(o[0]) + "\"" + zaznacz + ">" + o[1] + "</option>\n"

    html = ""
    # Jeśli jest wybrany oddział
    if oddzial != -1:
        # Pobierz stany z bazy
        stany_baza = stanKrwi(oddzial)

        # Tabelka
        html += "\n\n<!-- Tabelka stanów krwi -->\n<table class=\"Tabelka-krwiodawcy\">\n<tr>\n"
        for s in stany_baza:
            html += "<td>" + s[0] + "</td>\n"
        html += "</tr><tr>\n"

        for s in stany_baza:
            procent = s[1] * 100 / STANY_MAX
            procent_z = int(procent // 10) * 10 # Zaokrąglenie w dół do pełnych 10%
            if procent_z > 100:
                procent_z = 100
            html += "<td><img src=\"../grafiki/stany/" + str(procent_z) + ".png\"></td>\n"
        html += "</tr><tr>\n"

        for s in stany_baza:
            html += "<td>" + str(s[1]) + " ml</td>\n"
        html += "</tr>\n</table>\n"

    szablon =  render_template('edit_obiekt.html',oddzialy=oddzialy_lista)
    return szablon + html'''

def o_projekcie():
    return "<h1>O projekcie</h1>"+info()

def poziomy():
    return ""

def kontakt():
    return """<div class="form-tytul"><h2>Dane kontaktowe:</h2></div>\
            <div class="projekt"> \
            d.morzejko@student.po.opole.pl<br> \
            Kontakt telefoniczny: 666 91 81 81.<br></div>"""

def info():
    return '<div class="form-tytul"><h2>Za projekt odpowiedzialny:</h2></div> \
           <div class="projekt"> \
           <h2>Daniel Morzejko</h2> \
           Informatyka I, niestacjonarne, nr. Indeksu: s64597<br> \
           d.morzejko@student.po.edu.pl<br> \
           Projekt i wykonanie aplikacji webowej wspomagającej pracę działu serwisu.<br> \
           Promotor: Dr Hab. Inż. Marek Rydel</div>'

def glowna():
    return """<div class="projekt"><h3>Witaj na stronie poświęconej pracy inżynierskiej Daniela Morzejko.</h3> \
           Strona ta, jest serwisem webowym wspierającym pracę serwisu bram przeciwpożarowych.<br> \
           Aby zacząć, kliknij w Logowanie</div>"""

def nowy_obiekt():
    #opt += "<option value=\"" + str(i[0]) + "\">" + i[1] +"</option>\n"
    return render_template('nowy-obiekt.html')

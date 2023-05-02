# Funkcje wyświetlające "treść" - wycinek kodu HTML, który zostanie wrzucony w dane miejsce na stronie

from flask import *
funkcje = Blueprint('funkcje', __name__)

from baza import *

def logowanie():
    return render_template('logowanie.html')

def o_projekcie():
    return "<h1>O projekcie</h1>"+info()

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


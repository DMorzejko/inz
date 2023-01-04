# Layout - funkcje wyświetające cały układ strony (nagłówek/menu/stopkę/itp.)

from flask import *
layout = Blueprint('layout', __name__)


# Layout docelowy
def layout2(args):
    tytul = args[0] # tytuł, który widać na karcie przeglądarki
    tresc = args[1] # treść w "głównym obszarze" - generowana w funkcje.py
    style = args[2] # dodatkowe style CSS do podstron
    css_lista = ""
    for i in style:
        if i != '':
            css_lista += "<link rel=\"stylesheet\" href=\"/" + i + "\">\n      "
    n = render_template('l2-naglowek.html')
    s = render_template('l2-stopka.html', wersja="1.0")
    return render_template('l2-strona.html', css=css_lista, naglowek=n, stopka=s, title=tytul, tresc=tresc)
    # return render_template('l2-strona.html', css=css_lista, menu=m, title=tytul, tresc=tresc)

# Wyświetlenie całej strony - wybranie layout'u + treść
def wyswietl(layout, args):
    if layout == 2:
        return layout2(args)
    else:
        return "Błędny layout"

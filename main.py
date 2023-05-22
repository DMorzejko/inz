from flask import Flask, request, redirect, url_for, session, render_template, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from baza import User, get_user_by_id, get_user_by_username
from layout import *
from funkcje import *
import requests

'''from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment


def create_assessment(
    project_id: str, recaptcha_site_key: str, token: str, recaptcha_action: str
) -> Assessment:
    """Create an assessment to analyze the risk of a UI action.
    Args:
        project_id: GCloud Project ID
        recaptcha_site_key: Site key obtained by registering a domain/app to use recaptcha services.
        token: The token obtained from the client on passing the recaptchaSiteKey.
        recaptcha_action: Action name corresponding to the token.
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Set the properties of the event to be tracked.
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_site_key
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    project_name = f"projects/{project_id}"

    # Build the assessment request.
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    response = client.create_assessment(request)

    # Check if the token is valid.
    if not response.token_properties.valid:
        print(
            "The CreateAssessment call failed because the token was "
            + "invalid for for the following reasons: "
            + str(response.token_properties.invalid_reason)
        )
        return

    # Check if the expected action was executed.
    if response.token_properties.action != recaptcha_action:
        print(
            "The action attribute in your reCAPTCHA tag does"
            + "not match the action you are expecting to score"
        )
        return
    else:
        # Get the risk score and the reason(s)
        # For more information on interpreting the assessment,
        # see: https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
        for reason in response.risk_analysis.reasons:
            print(reason)
        print(
            "The reCAPTCHA score for this token is: "
            + str(response.risk_analysis.score)
        )
        # Get the assessment name (id). Use this to annotate the assessment.
        assessment_name = client.parse_assessment_path(response.name).get("assessment")
        print(f"Assessment name: {assessment_name}")
    return response
'''

aplikacja = Flask(__name__)
aplikacja.secret_key = 'tajny_klucz'

login_manager = LoginManager()
login_manager.init_app(aplikacja)
login_manager.login_view = "W_logowanie"

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

def verify_login_credentials(username, password):
    user = get_user_by_username(username)
    if user is not None and user.password == password:
        return True
    return False

@aplikacja.route("/")
def index():
    return wyswietl(1, ["Inz", glowna(), ['']])

@aplikacja.route('/logowanie', methods=['GET', 'POST'])
def W_logowanie():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if verify_login_credentials(username, password):
            user = get_user_by_username(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Błąd logowania', 401

    else:
        return wyswietl(1, ["Logowanie", logowanie(), ['']])

@aplikacja.route('/wyloguj')
@login_required
def wyloguj():
    logout_user()
    return redirect(url_for('W_logowanie'))

@aplikacja.route('/projekt')
def W_projekt():
    return wyswietl(1, ["Logowanie", info(), ['']])

@aplikacja.route('/tabela')
@login_required
def W_tabela():
    return wyswietl(1, ["Tabela obiektów", tabela(), ['']])

@aplikacja.route('/mapa')
@login_required
def W_mapa():
    obiekty = pobierz_obiekty_z_bazy()
    obiekty_json = json.dumps([obiekt.__dict__ for obiekt in obiekty])
    tresc = render_template('mapa.html', obiekty_json=obiekty_json)
    return wyswietl(1, ["Mapa", tresc, ['style.css']])

@aplikacja.route('/edit/<int:obiekt_id>', methods=['GET', 'POST'])
@login_required
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
            request.form['osoba_kontaktowa'],
            request.form['numer_kontaktowy'],
            request.form['czynnosc'],
            request.form['ilosc_bram'],
            request.form['uwagi'],
            'TAK' if request.form['pilne_hidden'] == 'TAK' else 'NIE',
            'TAK' if request.form['zrobione_hidden'] == 'TAK' else 'NIE'
        )
        update_obiekt(obiekt_id, updated_data)
        return redirect(url_for('W_tabela'))

    tresc = render_template('edit_obiekt.html', obiekt=obiekt)
    return wyswietl(1, ["Edycja obiektu", tresc, ['style.css']])

@aplikacja.route('/kontakt')
def W_funkcja2():
    return wyswietl(1, ["Kontakt", kontakt(), ['']])

@aplikacja.route('/delete/<int:obiekt_id>')
@login_required
def delete_obiekt_route(obiekt_id):
    delete_obiekt(obiekt_id)
    return redirect(url_for('W_tabela'))

@aplikacja.route('/nowy_obiekt', methods=['GET', 'POST'])
@login_required
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
        pilne = request.form['pilne']
        zrobione = request.form['zrobione']

        dodaj_obiekt_baza(nazwa, klient, ulica, numer_budynku, kod_pocztowy, miasto, osoba_kontaktowa, numer_kontaktowy, czynnosc, ilosc_bram, uwagi, pilne, zrobione)
        return redirect(url_for('W_tabela'))

    pusty_obiekt = {
        'Nazwa': '',
        'Klient': '',
        'Ulica': '',
        'Numer_Budynku': '',
        'Kod_Pocztowy': '',
        'Miasto': '',
        'Osoba_Kontaktowa': '',
        'Numer_Kontaktowy': '',
        'Czynnosc': '',
        'Ilosc_Bram': '',
        'Uwagi': '',
        'Pilne': '',
        'Zrobione': ''
    }

    tresc = render_template('dodaj_obiekt.html', obiekt=pusty_obiekt)
    return wyswietl(1, ["Dodaj nowy obiekt", tresc, ['style.css']])

def pobierz_obiekty_z_bazy():
    conn = DbConnection()
    sql = ("SELECT * FROM Obiekt")
    conn.execute(sql)
    obiekty_raw = conn.getData()
    del conn

    obiekty = []
    for obiekt_raw in obiekty_raw:
        obiekt = Obiekt(*obiekt_raw)
        obiekty.append(obiekt)
    return obiekty

def adres_na_wspolrzedne(adres, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": adres,
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            wspolrzedne = data['results'][0]['geometry']['location']
            return wspolrzedne['lat'], wspolrzedne['lng']
    return None, None

class Obiekt:
    def __init__(self, id, nazwa,klient, ulica, numer_budynku, kod_pocztowy, miasto, osoba_kontaktowa, numer_kontaktowy, czynnosc, ilosc_bram, uwagi, pilne, zrobione):
        self.Id = id
        self.Nazwa = nazwa
        self.Klient = klient
        self.Ulica = ulica
        self.Numer_Budynku = numer_budynku
        self.Kod_Pocztowy = kod_pocztowy
        self.Miasto = miasto
        self.Osoba_Kontaktowa = osoba_kontaktowa
        self.Numer_Kontaktowy = numer_kontaktowy
        self.Czynnosc = czynnosc
        self.Ilosc_Bram = ilosc_bram
        self.Uwagi = uwagi
        self.Pilne = pilne
        self.Zrobione = zrobione

if __name__ == "__main__":
    aplikacja.run(debug=True)

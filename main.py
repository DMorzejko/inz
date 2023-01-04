# Plik main - łączy całą aplikację razem, uruchamia aplikację

from flask import *
aplikacja = Flask(__name__, )
from routes import *

aplikacja.register_blueprint(funkcje)
aplikacja.register_blueprint(routes)
aplikacja.register_blueprint(layout)
aplikacja.register_blueprint(baza)

@aplikacja.route("/")
def index():
    return wyswietl(2, ["Inz", glowna(), ['']])

# Wejdz na http://localhost:8080
# i zobacz czy dziala
if __name__ == "__main__":

    aplikacja.run(host="127.0.0.1", port=8080, debug=True)
    #aplikacja.run()
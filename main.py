# Plik main - łączy całą aplikację razem, uruchamia aplikację

from flask import *
aplikacja = Flask(__name__, )
from routes import *
import os
import mysql.connector

aplikacja.register_blueprint(funkcje)
aplikacja.register_blueprint(routes)
aplikacja.register_blueprint(layout)
aplikacja.register_blueprint(baza)
class UserPass:
    def __init__(self, user='', password=''):
        self.user = user
        self.password = password

    def hash_password(self):
        #Hashowanie hasła
        #generowanie wartości na podstawie os.urandom(60)
        os_urandom_static = b'\x19Sx\xd6i[\xcc\xf5\xf1\x85mW\xbd.\x93\xb9\xbd\x16\xd4\xaa\xdc\xda\x8d\x0f\xe2\xe6b\x12\xe5\x19\x98&\x01^w;F\x0b\xe8\x14+\xd2uh3\xa7\xa2\xafa\x857\xd6\xad\xd7L\xb4\xa8\xf7\x0fq'
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 10000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(self, stored_password, provided_password):
        #weryfikowanie podanego hasła z hasłem z bd
        salt = stored_password[:64]
        stored_password = stored_password[:64]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt, 10000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def get_random_user_password(self):
        random_user = ''.join(random.choice(string.ascii_lowercase)for i in range(3))
        self.user = random_user

        password_characters =  string.ascii_letters #+ string.digits + string.punctuation
        random_password = ''.join(random.choice(password_characters)for i in range(3))
        self.password = random_password

@aplikacja.route('/init_app')
def init_app():
    conn = DbConnection()
    sql = 'select count(*) as cnt from users where is_active and is_admin;'
    conn.execute(sql)
    result = conn.getData()
    active_admins = result.fetchone()



@aplikacja.route("/")
def index():
    return wyswietl(1, ["Inz", glowna(), ['']])

# Wejdz na http://localhost:8080
# i zobacz czy dziala
if __name__ == "__main__":

    aplikacja.run(host="127.0.0.1", port=8080, debug=True)
    aplikacja.run()
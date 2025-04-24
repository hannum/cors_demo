# Toteuta taustapalvelu, joka palauttaa annettua lentokentän ICAO-koodia vastaavan
# lentokentän nimen ja kaupungin JSON-muodossa. Tiedot haetaan opintojaksolla käytetystä lentokenttätietokannasta.
# Esimerkiksi EFHK-koodia vastaava GET-pyyntö annetaan muodossa: http://127.0.0.1:3000/kenttä/EFHK.
# Vastauksen on oltava muodossa:
# {"ICAO":"EFHK", "Name":"Helsinki Vantaa Airport", "Municipality":"Helsinki"}.
import logging
import mysql.connector
from flask import Flask, Response
from flask_cors import CORS
import json
import config

app = Flask(__name__)

# Asennetaan CORS-proxy cross-domain pyyntöjen käsittelyä varten
# Tarvitaan myös kun Flask-palvelin on asennettu lokaalisti samalla koneelle mistä
# fetch-pyynnön tekevä web-sivu avataan

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.logger.setLevel(logging.INFO)

@app.route('/testi')
def testi():
    print("Testi")
    vastaus = {
        "status": "Testi"
    }
    json_vastaus = json.dumps(vastaus)
    return Response(response=json_vastaus, status=202, mimetype="application/json")

@app.route('/lentokentta/<icao>')
def kentta(icao):
    print("Kentta")
    app.logger.info("Kenttä")

    try:
        yhteys = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_game',
            user=config.user,
            password=config.pwd,
            autocommit=True
        )

        sql = f'SELECT ident, name, municipality FROM airport WHERE ident="{icao}"'
        print(sql)
        kursori = yhteys.cursor(dictionary=True)
        kursori.execute(sql)
        tulos = kursori.fetchone()
        print("Tulos: ", tulos)

        tilakoodi = 200
        if tulos:
            vastaus = {
                "status": tilakoodi,
                "ICAO": tulos['ident'],
                "Name": tulos['name'],
                "Municipality" : tulos['municipality']
            }
        else:
            raise ValueError

    except ValueError:
        tilakoodi = 400
        vastaus = {
            "status": tilakoodi,
            "teksti": "ICAO koodia vastaavaa lentokenttää ei löydy"
        }

    json_vastaus = json.dumps(vastaus)
    response = Response(response=json_vastaus, status=tilakoodi, mimetype="application/json")
    response.headers["Content-Type"] = "charset=utf-8"
    return response

@app.errorhandler(404)
def page_not_found(virhekoodi):
    tilakoodi = 404
    vastaus = {
        "status" : tilakoodi,
        "teksti" : "Virheellinen päätepiste"
    }
    json_vastaus = json.dumps(vastaus)
    return Response(response=json_vastaus, status=tilakoodi, content_type="application/json" )

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)

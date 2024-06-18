# Windows gitbash or linux build
python3 -m venv venv
source venv/**/activate
pip3 install Flask Flask-Cors mysql-connector-python mysql
export FLASK_APP=app.py
flask run --cert=resources/zbe976_cert.pem --key=resources/zbe976_key.pem --port=8080
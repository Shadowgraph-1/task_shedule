from flask import Flask
app = Flask(__name__)

@app.route('/home')
def home():
    return 'Добро пожаловать в TASK SHEDULE!'

@app.route('/about')
def about():
    return 'Раздел содержащий информацию "О нас"'

if __name__ == '__main__':
    app.debug = True
    app.run()
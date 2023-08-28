import flask 
import tensorflow as tf 
import json
import joblib


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'aljshfdkajsfh'
model = tf.keras.models.load_model('/usr/src/app/model')
scaler = joblib.load('/usr/src/app/model/scaler.joblib')

@app.route('/', methods=['GET', 'POST'])
def index():
    hardness = 0
    if flask.request.method == 'POST':
        flask.flash('Cчитаем...')
        X = [[float(flask.request.form['youngs']), float(flask.request.form['ultimate']), float(flask.request.form['yield']), float(flask.request.form['temperature']), float(flask.request.form['density']), float(flask.request.form['capacity'])]]
        print(X)
        scaled_X = scaler.transform(X)
        hardness = model.predict(scaled_X)[0][0]
    return flask.render_template('/usr/src/app/index.html', hardness=hardness)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    content = flask.request.json
    features = [
        float(content['youngs']),
        float(content['ultimate']),
        float(content['yield']),
        float(content['temperature']),
        float(content['density']),
        float(content['capacity'])
    ]
    prediction = {'prediction': f'{model.predict(scaler.transform([features]))[0][0]}'}
    return json.dumps(prediction)
    
@app.errorhandler(415)
def errorPage(error):
    return '<h1>Отправьте json запрос</h1>'

def main():
    app.run(debug=False)

if __name__ == '__main__':
    main()
    
    #print(model.predict([[1, 1, 1, 1, 1, 1]]))
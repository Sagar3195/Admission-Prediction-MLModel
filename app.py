#import  required dependencies
from flask import *
from flask_cors import CORS, cross_origin
import pickle

#initializing the Flask app
app = Flask(__name__)

@app.route('/', methods = ['GET']) #route to display  the home page
@cross_origin()
def homePage():
    return render_template('index.html')

@app.route('/predict', methods = ['POST', 'GET']) #route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #reading the inputs given by user
            gre_score = float(request.form['gre_score'])
            toefl_score = float(request.form['toefl_score'])
            university_rating = float(request.form['university_rating'])
            sop = float(request.form['sop'])
            lor = float(request.form['lor'])
            cgpa = float(request.form['cgpa'])
            is_research = request.form['research']
            if (is_research == 'yes'):
                research=1
            else:
                research=0

            filename = 'admission_model.pkl'
            model = pickle.load(open(filename, 'rb')) #loading the model file from the storage
            #now we do predictions using loaded model
            prediction = model.predict([[gre_score, toefl_score, university_rating, sop, lor, cgpa, research]])
            print("Prediction is : ", prediction)
            #showing prediction results in UI
            return render_template('results.html', prediction = round(100 * prediction[0]))
        except Exception as e:
            print("The Exception message is : ", e)
            return "Something is wrong"

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug= True)

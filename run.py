from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import TextField, SelectField, SubmitField, RadioField
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from random import randint
import yaml


# Fetch configuration information
env_vars = yaml.load(open('config.yaml').read())

app = Flask(__name__)
app.secret_key = 'SoMeThInG000SeCrEt'
csrf = CSRFProtect(app)

app.config['MONGO_DBNAME'] = env_vars['database']['name']
app.config['MONGO_USERNAME'] = env_vars['database']['username']
app.config['MONGO_PASSWORD'] = env_vars['database']['pw']
app.config['MONGO_URI'] = env_vars['database']['uri']

mongo = PyMongo(app)


def get_random_id(docids):
    id = randint(0, len(docids))
    return docids[id]


class verifyAnswers(FlaskForm):
    ''' Form class for verification questions. '''
    # Current test users
    name = SelectField('Current user', choices=[('jduda@usgs.gov', 'jduda@usgs.gov'), ('dwieferich@usgs.gov', 'dwieferich@usgs.gov'), ('bserna@usgs.gov', 'bserna@usgs.gov'), ('other', 'other')])
    p_dam = RadioField('Predicted Dam', choices=[('1', 'Correct'), ('0', 'Incorrect'), ('-1', 'Skip')])
    p_loc = RadioField('Predicted Dam', choices=[('1', 'Correct'), ('0', 'Incorrect'), ('-1', 'Skip')])
    p_yr = RadioField('Predicted Dam', choices=[('1', 'Correct'), ('0', 'Incorrect'), ('-1', 'Skip')])
    p_river = RadioField('Predicted Dam', choices=[('1', 'Correct'), ('0', 'Incorrect'), ('-1', 'Skip')])
    id = TextField()
    submit = SubmitField()


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/get', methods=['GET', 'POST'])
def get():
    name = verifyAnswers()  # Inst form
    if request.method == 'GET':
        docids = mongo.db.dams.distinct('_id')  # Fetch mongodb doc ids
        id = get_random_id(docids)  # Randomly find one to review
        name.id.data = id

        dam = mongo.db.dams.find_one({'_id': ObjectId(id)})

        # Attribute fields to bring over into the view for phrase context.
        pred_dam = dam['dam']
        pred_river = dam['river']
        pred_yr = dam['year_removed']
        pred_loc = dam['dam_location']
        phrase = dam['phrase']
        journal = dam['journal_title']
        authors = dam['journal_authors']

        return render_template('verify.html', dam=pred_dam, river=pred_river, yr=pred_yr, loc=pred_loc,  name=name, phrase=phrase, journal=journal, authors=str(' '.join(authors)), id=id)
    # Assign variables to the form data
    dam = name.p_dam.data
    loc = name.p_loc.data
    river = name.p_river.data
    yr = name.p_yr.data
    id = name.id.data
    usr = name.name.data

    # Update
    if '@' in usr:
        usr = usr.split('@')[0]
    try:
        mongo.db.dams.update_one({'_id': ObjectId(id)}, {'$set': {'dam_verified-' + usr: dam, 'dam_location_verified-' + usr: loc, 'river_verified-' + usr: river, 'year_verified-' + usr: yr}})
    except Exception as e:
        print(e)
        return('Sorry an error occured saving your results. Please contact us.')
    return render_template('index.html')


if __name__ == "__main__":
    app.run()

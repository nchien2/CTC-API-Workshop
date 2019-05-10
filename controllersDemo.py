from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired
app = Flask(__name__)

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class Form(FlaskForm):
    input = TextAreaField(
      'input', validators=[
        InputRequired(message='Insert text to analyze'),
      ],
      render_kw={'autofocus': True}
    )
    submit = SubmitField('Submit')


@app.route("/", methods = ['GET', 'POST'])
def hello():
    if(request.method == 'POST'):
        input = request.form
        getSentiment(input['input'])
        getEntities(input['input'])
        getSyntax(input['input'])
    return render_template(
        'template.html',
        form = Form()
    )

def getSyntax(input):
    #Detects parts of speech, punctuation, etc.

def getSentiment(input):
    #Uses google's pre-trained NLP algorithm to determine 'feeling' of text
    #Has a 'score' that corresponds to overall emotional leaning and 'magnitude'
    #that includes overall strength of emotion, both positive and negative.

def getEntities(input):
    #Classifies phrases in the text into entities, with different categories like
    #person, organization, location, etc. Also gives a measure of salience, or
    #the entities' importance for the text.


if __name__ == "__main__":
    app.run()
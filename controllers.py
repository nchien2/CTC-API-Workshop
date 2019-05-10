from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six

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

def getSentiment(input):
    # Instantiates a client
    client = language.LanguageServiceClient()

    # The text to analyze
    document = types.Document(
        content=input,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    print('Text: {}'.format(input))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))


def getEntities(input):
    # Instantiates a client
    client = language.LanguageServiceClient()

    # The text to analyze
    document = types.Document(
        content=input,
        type=enums.Document.Type.PLAIN_TEXT)


    entities = client.analyze_entities(document).entities

    for entity in entities:
        entity_type = enums.Entity.Type(entity.type)
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity_type.name))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))
        print(u'{:<16}: {}'.format('mid', entity.metadata.get('mid', '-')))

def getSyntax(input):
    client = language.LanguageServiceClient()

    if isinstance(input, six.binary_type):
        input = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=input,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    tokens = client.analyze_syntax(document).tokens

    # part-of-speech tags from enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

    for token in tokens:
        print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag],
                               token.text.content))

if __name__ == "__main__":
    app.run()

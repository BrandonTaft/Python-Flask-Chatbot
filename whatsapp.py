from flask import Flask, request
import requests
#webhook response to twilio must be in twilio markup language(twiml)
#twiml is XML-based language
#twilio helper library has classes that create the response for you
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    #access users incoming message with request object
    #convert to lowercase to avoid issues w/ different ways a word can come
    incoming_msg = request.values.get('Body', '').lower()

    #twiml response that includes text and media
    #twilio expects url instead of actual image
    resp = MessagingResponse()
    msg = resp.message()
    #chatbot logic- this searches incoming messages for specific keywords
    #the responded boolean tracks the case where message doesnt have any 
    #of the keywords and gives generic response
    responded = False
    if 'quote' in incoming_msg:
        # return a quote from api
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic from api
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)


if __name__ == '__main__':
    app.run()
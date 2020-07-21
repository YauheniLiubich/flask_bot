import flask
import requests

app = flask.Flask(__name__)

TG_TOKEN = '1399690604:AAFdK7tMVfnmJiZ2CncXxD6DVHvwXgq2dOw'
WEATHER_KEY = '20b2a4b7362b244f91683b1a1504f0e9'


def get_weather(query):
    params = {
        'access_key': WEATHER_KEY,
        'query': query
    }
    response = requests.get('http://api.weatherstack.com/current', params)
    print(response)
    print(response.json())
    # resp = response.json().get('current')
    # print(resp)
    if 'current' in response.json():
        return f"Сейчас в {query} {response.json()['current']['temperature']} градус(-а, -ов)"
    elif 'current' not in response.json():
        print('Ключа "current" нет')


@app.route('/', methods=['GET', 'POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        print(flask.request.json)
        """Для отправки сообщений нам нужно знать id чата. Его можно вытащить из тела Telegram-запроса."""
        chat_id = flask.request.json['message']['chat']['id']

        request_text = flask.request.json['message']['text']

        weather_response = get_weather(request_text)

        method = 'sendMessage'
        url = f'https://api.telegram.org/bot{TG_TOKEN}/{method}'
        data = {
            'chat_id': chat_id,
            'text': weather_response
        }
        requests.post(url, data)
    return ''


URL = 'https://207a22a1bd7a.ngrok.io'

if __name__ == '__main__':
    requests.get("https://api.telegram.org/bot{}/setWebhook?url={}".format(TG_TOKEN, URL))
    app.run()

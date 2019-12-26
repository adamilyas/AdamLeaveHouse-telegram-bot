from config import query_base
from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main_route():
    if request.method == 'POST':
        msg = request.get_json()
        print(msg)
        return Response('Ok', status=200)
    else:
        return "<h1>Main</h1>"

def create_send_message_url(chat_id, message):
    return f'{query_base}/sendMessage?chat_id={chat_id}&text={message}'    

if __name__ == "__main__":
    app.run(port=5000)
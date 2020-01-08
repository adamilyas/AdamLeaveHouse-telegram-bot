from api.config import *
from api.service import data_mall_service
from flask import Flask, request, Response
import requests as rq
import json
import os

app = Flask(__name__)

# read json
dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.join(dir_path, 'locations.json')

with open(file_name, "r") as locations_file:
    locations = json.load(locations_file)

print(locations)
# locations
help_string = """
/help - help

/details - bus stop id of locations

/add - To add bus stop, use the command: /add <location name> <bus stop id> 

/del - To delete bus stop, use command: /del <location name>

Available Bus Stops are: """
for location in locations:
    help_string += f' /{location}'

"""
To do:

Use DB instead of JSON
"""

@app.route("/", methods=['GET', 'POST'])
def main_route():
    if request.method == 'POST':
        msg = request.get_json()
        app.logger.debug(msg)

        chat_id = msg['message']['chat']['id']
        if TEXT in msg['message']:
            message_text = msg['message']['text']
        else:
            message_text = HELP

        message_text = message_text.replace(BOT_NAME, "")
        app.logger.debug((chat_id, message_text))

        # /details
        if DETAILS in message_text :
            message_to_send = get_details(locations)

        # /add
        elif ADD in message_text:
            args = message_text.split(" ")
            app.logger.debug(args)
            if len(args) != 3:
                message_to_send = "Format: /add <location name> <bus stop id>"

            elif args[1] in locations.keys():
                message_to_send = f'`{args[1]}` already exists. Please use another location name\n\n' + get_details(locations)

            else:
                locations[args[1]] = args[2]
                with open(file_name, "w") as new_file:
                    json.dump(locations, new_file)

                message_to_send = 'Updated Location List\n\n' + get_details(locations)

        # /delete
        elif DELETE in message_text:
            args = message_text.split(" ")
            app.logger.debug(args)
            if len(args) != 2:
                message_to_send = "Format: /del <location name>"
            elif args[1] not in locations.keys():
                message_to_send = f'`{args[1]}` doesnt exist. Please delete from the following list\n\n' + get_details(locations)
            else:
                del locations[args[1]]
                with open(file_name, "w") as new_file:
                    json.dump(locations, new_file)

                message_to_send = 'Updated Location List\n\n' + get_details(locations)


        # /help or /wrongLocation -> help string
        elif HELP in message_text:
            message_to_send = help_string

        # valid location
        elif message_text[1:] in locations.keys():
            bus_stop_id = locations[message_text[1:]]
            message_to_send = data_mall_service(bus_stop_id)

        # /invalid_command or /invalid_location
        elif  message_text[0] == '/':
            message_to_send = help_string

        # send message back to me.
        if message_to_send:
            send_message_url = create_send_message_url(chat_id, message_to_send)
            app.logger.debug(send_message_url)

            r = rq.post(send_message_url)
            app.logger.debug(r.content)
            
        return Response('Ok', status=200)
    else:
        return "<h1>Main</h1>"

def create_send_message_url(chat_id, message):
    return f'{query_base}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=markdown'    

def get_details(locations):
    details = "**Current Locations**: \n"
    for location in locations:
        details += f'\n/{location} : {locations[location]}'

    return details

if __name__ == "__main__":
    app.run(port=5000, debug=True)
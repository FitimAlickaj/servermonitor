import time
import requests
from requests.exceptions import HTTPError
from datetime import datetime
import socket
import multiprocessing
from termcolor import colored
import json


#Slack Info
slack_token = 'xxx token'
slack_channel = '#general'
slack_icon_emoji = ':eyes:'
slack_user_name = 'Support' # name of app in slack
def post_message_to_slack(text, blocks=None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': text,
        'icon_emoji': slack_icon_emoji,
        'username': slack_user_name,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()


# In case we have large list of servers we split in two so we can use multiprocess monitoring
list_one = ['https://github.com']
list_two = ['https://www.youtube.com']



temp_down = []
def processOne():
    fine_server = []
    try:
        for server in list_one:
            IPaddress=socket.gethostbyname(socket.gethostname())
            if IPaddress=="127.0.0.1":
                print("No internet, your localhost is "+ IPaddress)
                break
            else:
                try:
                    response = requests.get(server)
                    response.raise_for_status()
                    if response.status_code == 200:
                        fine_server.append(server)
                        print(server  + colored(" OK" , "green"))
                    #checking for Http errors
                except HTTPError as http_err:
                    if server in temp_down:
                        continue
                    else:
                        #post_message_to_slack(server) # Send msg to slack for down server
                        print(server + colored(" DOWN" , "red"))
                        temp_down.append(server)
                        #
                except Exception as error:
                        # checking for other problems
                    if server in temp_down:
                        continue
                    else:
                        #post_message_to_slack(server) # Send msg to slack for down server
                        print(server + colored(" DOWN" , "red"))
                        temp_down.append(server)
    except Exception as Baseerror:
        print("Crashed " + str(Baseerror))
    finally:
        for server in fine_server: 
            if server in temp_down:
                print("Fixed " + server)
                #post_message_to_slack(server) # If we want to send msg to slack for fixed server
                temp_down.remove(server)
        

    
def processTwo():
    fine_server = []
    try:
        for server in list_two:
            IPaddress=socket.gethostbyname(socket.gethostname())
            if IPaddress=="127.0.0.1":
                print("No internet, your localhost is "+ IPaddress)
                break
            else:
                try:
                    response = requests.get(server)
                    response.raise_for_status()
                    # checking if server is fine
                    if response.status_code == 200:
                        fine_server.append(server)
                        print(server  + colored(" OK" , "green") )
                # checking for http errors
                except HTTPError as http_err:
                    if server in temp_down:
                        continue
                    else:
                        #post_message_to_slack(server) # Send msg to slack for down server
                        print(server + colored(" DOWN" , "red"))
                        temp_down.append(server)
                    # checking for other problems
                except Exception as error:
                    if server in temp_down:
                        continue
                    else:
                        #post_message_to_slack(server) # Send msg to slack for down server
                        print(server + colored(" DOWN" , "red"))
                        temp_down.append(server)
    except Exception as Baseerror:
        print("Crashed " + str(Baseerror))
    finally:
        for server in fine_server: 
            if server in temp_down:
                print("Fixed " + server)
                temp_down.remove(server)
        
        




if __name__ == "__main__":
    p1 = multiprocessing.Process(target=processOne)
    p2 = multiprocessing.Process(target=processTwo)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("List One  " + colored("Done ", "cyan"))
    print("List Two  " + colored("Done ", "cyan"))

    

import constants
import jwt
import requests
import logging

from typing import Optional

from fastapi import FastAPI , Request, Header
from typing import Any, Dict, AnyStr, List, Union

from pydantic import BaseModel

app = FastAPI()
JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
# Main URL - which shows FAST apis is running
@app.get("/")
def read_root():
    return {"Test": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

#Defining the variables
class Item(BaseModel):
    message_uuid: str
    to: dict
    message: dict
        
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

#Function - auth_jwt(header_data) used to authenticate the request
def auth_jwt(header_data):
    try:
        jwt_tokken = header_data['authorization'].split(' ')[1]
        api_key = jwt.decode(jwt_tokken, "qcL8RVLb0ok8hg74KuUaBVI9rxu6FHxcUgEvRn0iZFTWAs9Sk7", algorithms=["HS256"])
        if api_key['api_key'] == constants.AUTH_SECURE_KEY:
            return True
        else:
            return False
    except Exception as err:
        print(err)
        return False

#Vonage webhook connected to below URL
@app.post("/whats_app")
def root(request: JSONObject,req: Request):
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
        
            auth_flag = auth_jwt(req.headers)
            if auth_flag == False:
                print("Invalid Key")
                logging.error('Security - Invalid Key')
                return "400"

            new_data = { key.decode(): val for key, val in request.items() }
            cust_message_uuid = new_data['message_uuid']
            #customer mobile number
            cust_no = new_data['from']['number']
            #customer message
            cust_msg = new_data['message']['content']['text']
            #joing the message customer and mobile number
            combined_msg = str(cust_msg) + '_' +str(cust_no)
            
            data = '{\n    "message":"'+str(combined_msg)+'",\n    "sender": "'+str(cust_no)+'" }'
            #getting chat bot response from chat bot rasa API
            response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=data)
            #formatting of response
            try:
                if response.text:
                    d = eval(response.text)
                    d[0]['text']
                    reply = [d[0]['text']]

            except Exception as err:
                    reply = ["Hmm... I am not sure I quite understand your query"]
                    print(err)
            #sending whats app message to user
            for msg in reply:
                    data_2 = '{\n    "from": { "type": "whatsapp", "number": "' + str(
                        constants.header_whats_no) + '" },\n    "to": { "type": "whatsapp", "number": "' + str(
                        cust_no) + '" },\n    "message": {\n      "content": {\n        "type": "text",\n        "text": "' + str(
                        msg['text']) + '"\n      }\n    }\n  }'
                    response = requests.post(constants.send_msg_url, headers=headers,
                                                                             data=data_2, auth=(constants.AUTH_SECURE_KEY, constants.api_secret))

             return "200"

#vonage webhook url for users status e.g message recevied to user and read by user (Blue tick) 
@app.post("/status")
def get_status(request: JSONObject):
    print(request)
    return "200"

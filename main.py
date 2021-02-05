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

@app.get("/")
def read_root():
    return {"Test": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

class Item(BaseModel):
    message_uuid: str
    to: dict
    message: dict

# example in ward message
# {'message_uuid': 'aaaaaaaa-bbbb-cccc-dddd-0123456789ab', 'timestamp': '2020-01-01T14:00:00.000Z', 
#'to': {'type': 'whatsapp', 'number': '447700900000'}, 
#'from': {'type': 'whatsapp', 'number': '447700900001'}, 
#'message': {'content': {'type': 'text', 'text': 'Hello From Vonage!'}}}

JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]
#auth request coming from vonage
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


@app.post("/whats_app")
def root(request: JSONObject,req: Request):
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
            #if you require the auth
            #auth_flag = auth_jwt(req.headers)
            # if auth_flag == False:
            #     print("Invalid Key")
            #     logging.error('Security - Invalid Key')
            #     return "400"
            #print(auth_flag,'auth_flagauth_flagauth_flagauth_flagauth_flag')
            new_data = { key.decode(): val for key, val in request.items() }
            #print(new_data)
            cust_message_uuid = new_data['message_uuid']
            cust_no = new_data['from']['number']
            #customer mobile number
            print(cust_no)
            cust_msg = new_data['message']['content']['text']
            print(cust_msg)

            #number plus message
            combined_msg = str(cust_msg) + '_' +str(cust_no)
            data = '{\n    "message":"'+str(combined_msg)+'",\n    "sender": "'+str(cust_no)+'" }'

            response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=data)
            print("resporesponseresponse",response)

            # reply from rasa chat bot, use this to show and send this output to whats app
            print(response.text)

            try:
                if response.text:
                    d = eval(response.text)
                    d[0]['text']
                    reply = [d[0]['text']]

            except Exception as err:
                    reply = ["Hmm... I am not sure I quite understand your query"]
                    print(err)

            return "200"


@app.post("/status")
def get_status(request: JSONObject):
    print(request)
    return "200"

@app.post("/test_api_res")
def sample(request: JSONObject):
    return 200
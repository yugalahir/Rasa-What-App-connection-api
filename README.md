# Rasa-What-App-connection-api
This is a python file which is build using FAST API and unicorn ASGI server. 
Here using this script can connect your rasa chat bot with whatApp (you have to use third party sms provider like , vonage, twillo. in my view Vonage is best)

steps 
1 Start your rasa chat bot ->  rasa run --debug (test your bot, and confirm rasa chatbot is working)
2 after that run this script-> uvicorn main:app --reload and this send request to rasa bot which running on 

All you need 
1 python 3.6 or above 
2 install fast api and uvicorn -> https://fastapi.tiangolo.com/
3 rasa chat bot installed - https://rasa.com/docs/rasa/installation/

Thank you

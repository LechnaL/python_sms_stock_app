#if any imports are underlined in red, remember to install the required packages
import requests
from twilio.rest import Client
from datetime import date, timedelta


#here you need to enter YOUR API keys for program to work properly
B_API_KEY = "[PLACEHOLDER FOR YOUR ALPHA VANTAGE API KEY]"
NEWS_API_KEY = "[PLACEHOLDER FOR YOUR NEWS API KEY]"


#here you need to enter YOUR twilio api SID and TOKEN for program to work properly
account_sid = "[PLACEHOLDER FOR YOUR TWILIO SID]"
auth_token = "[PLACEHOLDER FOR YOUR TWILIO TOKEN]"


yesterday_date = date.today() - timedelta(1)

article_params={
    "q":"tesla",#if you want to get articles about other company you will need to change that value
    "from":yesterday_date,
    "sortBy":"popularity",
    "apiKey":NEWS_API_KEY,

}


#funtion used to fetch the data
def getNewsAndFetch(good_news):

    N_API_CALL=requests.get("https://newsapi.org/v2/top-headlines?q=tesla&from=2023-02-22&to=2023-02-22&sortBy=popularity&apiKey=b99f57c22e5b425c9ffadf098af9b8a0",params=article_params)
    N_data=N_API_CALL.json()
    N_title=N_data["articles"][0]["title"]
    N_desc=N_data["articles"][0]["description"]
    N_url=N_data["articles"][0]["url"]

    client = Client(account_sid, auth_token)
    if good_news:
        message = client.messages.create(
            body=f"Tesla stock up 10% or more!\n{N_title}\n{N_desc}\n{N_url}",
            from_="+12345678910",#here you need to enter YOUR twilio phone number
            to="+12345678910",#here you need to enter YOUR phone number remember that number must be verified by twilio, or message wont be send
        )
    else:
        message = client.messages.create(
            body=f"Tesla stock down 10% or more!\n{N_title}\n{N_desc}\n{N_url}",
            from_="+12345678910",#here you need to enter YOUR twilio phone number
            to="+12345678910",#here you need to enter YOUR phone number remember that number must be verified by twilio, or message wont be send
        )
    print(message.status)
    print(message.sid)



#you can change the parameters to fit the company stock you want to follow
query_params = {
    "function":"GLOBAL_QUOTE",
    "symbol":"TSLA",
    "apikey":B_API_KEY,
}

#this API call should always trigger

API_CALL = requests.get("https://www.alphavantage.co/query", params=query_params)

data = API_CALL.json()

on_open = float(data["Global Quote"]["02. open"])
prev_close = float(data["Global Quote"]["08. previous close"])
print(on_open ,prev_close)


#check if the change in stock is big enough
if on_open>prev_close:
    dif = on_open - prev_close

    if prev_close/10 <= dif:
        getNewsAndFetch(True)


else:
    dif = prev_close - on_open
    if prev_close / 10 <= dif:
        getNewsAndFetch(False)




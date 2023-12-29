import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

ClientId = int(os.getenv("ClientId"))
UserId = os.getenv("UserId")
UserName = os.getenv("User-Name")
Password = os.getenv("Password")
API_Token = os.getenv("API-Token")

headers = {
    'Content-Type': 'application/json',
    'Authorization': API_Token,
    'API-Token': API_Token
}

'''
  https://ipapi.co/json/
  https://api.ipify.org?format=json
  https://ip.seeip.org/jsonip

'''

def get_ip_address():
    response = requests.get('https://api.seeip.org/jsonip')
    return json.loads(response.text.strip())

External_ip = get_ip_address()["ip"]
print(External_ip)


# Working - just get IP right
def balance_check():
    api_url = 'https://flight.srdvtest.com/v5/rest/Balance'
    payload_data = {
        "EndUserIp": External_ip,
        "ClientId": ClientId,
        "UserName": UserName,
        "Password": Password
    }

    try:
        response = requests.post(api_url, json=payload_data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return (f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return (f"Error: {e}")


def Flight_search():
    api_url = 'https://flight.srdvtest.com/v8/rest/Search'
    payload_data = {
        "EndUserIp": External_ip,
        "ClientId": ClientId,
        "UserName": UserName,
        "Password": Password,
        "AdultCount":"1",
        "ChildCount":"0",
        "InfantCount":"0",
        "JourneyType":"1",
        # 1 - oneway , 2 - return, 3 - multiCity, 4- advance search
        "Segments":[  
            {  
                "Origin":"DEL",
                "Destination":"BOM",
                "FlightCabinClass":"1",
                # 1 - all, 2 - economy, 3 - premium eco , 4 - business, 5 - premium, 6 -  First
                "PreferredDepartureTime":"2023-12-26T00:00:00",
                "PreferredArrivalTime":"2023-13-26T00:00:00"
            }
        ]
    }

    try:
        response = requests.post(api_url, json=payload_data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            with open('flight_Search.json', 'w') as f:
                json.dump(response_data, f)
            return response_data

        else:
            return (f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return (f"Error: {e}")


print(json.dumps(Flight_search(), indent=4))

def LLC_ticket_Req(search, user_args):
    api_url = 'https://flight.srdvtest.com/v8/rest/TicketLCC'
    passengers = []
    for i in user_args:
        passengers.append()
    payload_data = {
        "EndUserIp": External_ip,
        "ClientId": ClientId,
        "UserName": UserName,
        "Password": Password,
        "SrdvType": search["SrdvType"],
        "SrdvIndex": search["SrdvIndex"],
        "TraceId": search['TraceId'],
        "ResultIndex": search['ResultIndex'],
        "Passengers":[
            {
                "Title":"Mr",
                "FirstName":"SRDV",
                "LastName":"Support",
                "PaxType":"1",
                "DateOfBirth":"1992-03-12",
                "Gender":"1",
                "PassportNo":"",
                "PassportExpiry":"",
                "AddressLine1":"Test",
                "City":"Kolkata",
                "CountryCode":"IN",
                "CountryName":"India",
                "ContactNo":"9632587410",
                "Email":"support@srdvtechnologies.com",
                "IsLeadPax":"True",
                "Fare": {
                    "BaseFare": search['Fair']['BaseFair'],
                    "Tax": search['Fair']['Tax'],
                    "TransactionFee": search['Fair']['TransactionFee'],
                    "YQTax": search['Fair']['YQTax'],
                    "AdditionalTxnFeeOfrd": search['Fair']['AdditionalTxnFeeOfrd'],
                    "AdditionalTxnFeePub": search['Fair']['AdditionalTxnFeePub'],
                    "AirTransFee": search['Fair']['AirTransFee']
                }	
            },
            {
                "Title":"Master",
                "FirstName":"Srdvtechnologies",
                "LastName":"Support",
                "PaxType":"2",
                "DateOfBirth":"2015-03-12",
                "Gender":"1",
                "PassportNo":"",
                "PassportExpiry":"",
                "AddressLine1":"Test",
                "City":"Kolkata",
                "CountryCode":"IN",
                "CountryName":"India",
                "ContactNo":"9632587410",
                "Email":"support@srdvtechnologies.com",
                "IsLeadPax":"False",
                "Fare": {
                    "BaseFare": search['Fair']['BaseFair'],
                    "Tax": search['Fair']['Tax'],
                    "TransactionFee": search['Fair']['TransactionFee'],
                    "YQTax": search['Fair']['YQTax'],
                    "AdditionalTxnFeeOfrd": search['Fair']['AdditionalTxnFeeOfrd'],
                    "AdditionalTxnFeePub": search['Fair']['AdditionalTxnFeePub'],
                    "AirTransFee": search['Fair']['AirTransFee']
                }	
            }
        ]
    }

    try:
        response = requests.post(api_url, json=payload_data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            print("Response:", response_data)
            return response_data

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return (f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return (f"Error: {e}")


def Fair_rate():
    api_url = 'https://flight.srdvtest.com/v5/rest/Balance'
    payload_data = {
        "EndUserIp": External_ip,
        "ClientId": ClientId,
        "UserName": UserName,
        "Password": Password
    }

    try:
        response = requests.post(api_url, json=payload_data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            print("Response:", response_data)
            return response_data

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return (f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return (f"Error: {e}")


def func():
    api_url = 'your_api_url'

    payload_data = {
        'key1': 'value1',
        'key2': 'value2'
    }
    try:
        response = requests.post(api_url, json=payload_data)

        if response.status_code == 200:
            response_data = response.json()
            print("Response:", response_data)
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

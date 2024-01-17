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
    # 'Authorization': API_Token,
    'API-Token': API_Token
}



def get_ip_address():
    '''
    https://ipapi.co/json/
    https://api.ipify.org?format=json
    https://ip.seeip.org/jsonip

    '''
    response = requests.get('https://api.ipify.org?format=json')
    # response = requests.get('https://api.seeip.org/jsonip')
    return json.loads(response.text.strip())

# External_ip = get_ip_address()["ip"]
External_ip = '1.1.1.1'
print(External_ip)


# Working - just get IP right
def balance_check():
    api_url = 'https://flight.srdvtest.com/v5/rest/Balance'
    payload_data = {
        "EndUserIp": External_ip,
        "ClientId": str(ClientId),
        "UserName": UserName,
        "Password": Password,
    }

    try:
        print(payload_data)
        response = requests.post(
            api_url, json=json.dumps(payload_data), headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return (f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return (f"Error: {e}")
# print(balance_check())


def Flight_search(inp=None):
    api_url = 'https://flight.srdvtest.com/v8/rest/Search'
    head = {
        "EndUserIp": External_ip,
        "ClientId": str(ClientId),
        "UserName": UserName,
        "Password": Password,
    }
    if inp:
        payload_data = {**head, **inp}
        print(payload_data)
    else:
        data = {
            "AdultCount": "1",
            "ChildCount": "0",
            "InfantCount": "0",
            "JourneyType": "1",
            # 1 - oneway , 2 - return, 3 - multiCity, 4- advance search
            "Segments": [
                {
                    "Origin": "DEL",
                    "Destination": "BOM",
                    "FlightCabinClass": "1",
                    # 1 - all, 2 - economy, 3 - premium eco , 4 - business, 5 - premium, 6 -  First
                    "PreferredDepartureTime": "2024-01-26T00:00:00",
                    "PreferredArrivalTime": "2024-01-26T00:00:00"
                }
            ]
        }
        payload_data = {**head, **data}
        print(payload_data)

    try:
        print("headers\n", headers)
        response = requests.post(api_url, json=payload_data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            with open('flight_Search.json', 'w') as f:
                json.dump(response_data, f)
            return response_data

        else:
            return {"Error": f"{response.status_code} - {response.text}", "headers_passed": headers, "data_passed": payload_data}

    except requests.exceptions.RequestException as e:
        return {"Error": e, "headers_passed": headers, "data_passed": payload_data}
# print(json.dumps(Flight_search(), indent=4))


def LLC_ticket_Req(data):
    api_url = 'https://flight.srdvtest.com/v8/rest/TicketLCC'
    payload_data = {
        "EndUserIp": External_ip,
        "ClientId": ClientId,
        "UserName": UserName,
        "Password": Password,
    }
    merged_dict = dict(payload_data)
    merged_dict.update(data)

    fare_quote_data ={
        "SrdvType": data["SrdvType"],
        "SrdvIndex": data["SrdvIndex"],
        "TraceId": data["TraceId"],
        "ResultIndex": data["ResultIndex"]
    }
    resp = Fare_quote(fare_quote_data)
    print(resp)
    if resp['Error']['ErrorCode']!= '0':
        print(resp)
        return None,501
    updated_data = merged_dict
    for i in range(len(data['Passengers'])):
        updated_data["Passengers"][i]['Fare'] = resp['Results']['Fare']
    # try:
    print("request - ",json.dumps(updated_data),"\n\n")
    response = requests.post(api_url, json= json.dumps(updated_data), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        print("Response - ",response_data,"\n\n")
        with open('output.json', "w") as json_file:
            json.dump(response_data, json_file, indent=4)
        print("Headers - ",headers,"\n\n")
        try:
            with open("Flight_API/bookingSuccess.json", 'r') as file:
                data = json.load(file)
            print("done")
            return data
        except FileNotFoundError:
            print(f"File bookingSuccess.json not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in '{file_path}': {e}")
        return None
        return response_data

    else:
        print(f"Error: {response.status_code} - {response.text}")
        return (f"Error: {response.status_code} - {response.text}")

    # except requests.exceptions.RequestException as e:
    #     print(f"Error: {e}")
    #     return (f"Error: {e}")


def Fare_quote(data):
    api_url = 'https://flight.srdvtest.com/v8/rest/FareQuote'
    payload_data = {
        "EndUserIp": External_ip,
        "ClientId": str(ClientId),
        "UserName": UserName,
        "Password": Password
    }
    merged_dict = dict(payload_data)
    merged_dict.update(data)
    # print(merged_dict)
    # return None
    # try:
    response = requests.post(api_url, json= merged_dict, headers=headers)

    if response.status_code == 200:
        # print(response)
        try:
            response_data = response.json()
            # print("Response:", response_data)
            return response_data
        except Exception as e:
            print("error at fare quote",e)
            return response


    else:
        print(f"Error: {response.status_code} - {response.text}")
        return (f"Error: {response.status_code} - {response.text}")

    # except requests.exceptions.RequestException as e:
    #     print(f"Error: {e}")
    #     return (f"Error: {e}")


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

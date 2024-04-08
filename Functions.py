import firebase_admin
from firebase_admin import credentials, auth, firestore
from firebase_admin.exceptions import FirebaseError

from dotenv import load_dotenv
import requests
import os
import json
import random
import string

load_dotenv()


head = {
    "EndUserIp": '1.1.1.1',
    "ClientId": str(int(os.getenv("ClientId"))),
    "UserName": os.getenv("User-Name"),
    "Password": os.getenv("Password"),
}
headers = {
    'Content-Type': 'application/json',
    'API-Token': os.getenv("API-Token")
}


def get_ip_address():
    '''
    https://ipapi.co/json/
    https://api.ipify.org?format=json
    https://ip.seeip.org/jsonip
    '''

    response = requests.get('https://api.ipify.org?format=json')
    # response = requests.get('https://api.seeip.org/jsonip')
    print(response.text.strip())
    return json.loads(response.text.strip())


External = get_ip_address()["ip"]


def BookingFlow(data, Type, email):
    data = {"bookingData": data, "metadata": {
        "BookingType": Type, "email": email}}

    pass


class Hotels:
    def balance_check(self):
        api_url = 'https://hotel.srdvtest.com/v5/rest/Balance'
        payload_data = {
            "EndUserIp": External_ip,
            "ClientId": str(ClientId),
            "UserName": UserName,
            "Password": Password,
        }

        try:
            print(payload_data)
            response = requests.post(
                api_url, json=payload_data, headers=headers)

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

    def Hotel_search(self, inp=None):
        api_url = 'https://hotel.srdvtest.com/v5/rest/Search'
        if inp:
            payload_data = {**head, **inp}
            # print(payload_data)
        else:
            data = {
                "BookingMode": "5",
                "CheckInDate": "30/04/2020",
                "NoOfNights": 1,
                "CountryCode": "IN",
                "CityId": "130443",
                "ResultCount": None,
                "PreferredCurrency": "INR",
                "GuestNationality": "IN",
                "NoOfRooms": "1",
                "RoomGuests": [
                    {
                        "NoOfAdults": "1",
                        "NoOfChild": "0",
                        "ChildAge": []
                    }
                ],
                "PreferredHotel": "",
                "MaxRating": "5",
                "MinRating": "0",
                "ReviewScore": None,
                "IsNearBySearchAllowed": False
            }
            payload_data = {**head, **data}

        try:
            response = requests.post(
                api_url, json=payload_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                return response_data

            else:
                return {"Error": f"{response.status_code} - {response.text}", "headers_passed": headers, "data_passed": payload_data}

        except requests.exceptions.RequestException as e:
            return {"Error": e, "headers_passed": headers, "data_passed": payload_data}
    # print(json.dumps(Hotel_search(), indent=4))

    def HotelInfo(self, data):
        url = "https://hotel.srdvtest.com/v5/rest/GetHotelInfo"
        sampleData = {
            "TraceId": "1",
            "SrdvType": "SingleTB",
            "SrdvIndex": "SrdvTB",
            "ResultIndex": 9,
            "HotelCode": "92G|DEL",
        }
        if data:
            payload_data = {**head, **data}
        else:
            payload_data = {**head, **sampleData}

        try:
            # print("headers\n", headers)
            response = requests.post(
                url, json=payload_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                return response_data

            else:
                return {"Error": f"{response.status_code} - {response.text}", "headers_passed": headers, "data_passed": payload_data}

        except requests.exceptions.RequestException as e:
            return {"Error": e, "headers_passed": headers, "data_passed": payload_data}

    def RoomInfo(self, data):
        url = "https://hotel.srdvtest.com/v5/rest/GetHotelRoom"
        sampleData = {
            "TraceId": "1",
            "SrdvType": "SingleTB",
            "SrdvIndex": "SrdvTB",
            "ResultIndex": 9,
            "HotelCode": "92G|DEL",
        }
        if data:
            payload_data = {**head, **data}
            print(payload_data)
        else:
            payload_data = {**head, **sampleData}

        try:
            response = requests.post(url, json=payload_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                return response_data
            else:
                return {"Error": f"{response.status_code} - {response.text}", "headers_passed": headers, "data_passed": payload_data}
        except requests.exceptions.RequestException as e:
            return {"Error": e, "headers_passed": headers, "data_passed": payload_data}

    def BlockRoom(self, data):
        url = "https://hotel.srdvtest.com/v5/rest/BlockRoom"
        sampleData = {
            "TraceId": "1",
            "SrdvType": "SingleTB",
            "SrdvIndex": "SrdvTB",
            "ResultIndex": 9,
            "HotelCode": "92G|DEL",
            "HotelName": "The Manor",
            "GuestNationality": "IN",
            "NoOfRooms": "1",
            "ClientReferenceNo": 0,
            "IsVoucherBooking": True,
            "HotelRoomsDetails": [
                {
                    "ChildCount": 0,
                    "RequireAllPaxDetails": True,
                    "RoomId": 0,
                    "RoomStatus": 0,
                    "RoomIndex": 1,
                    "RoomTypeCode": "007:92G:228:SGLyDXzGRvALLvROzROz:N:828857$#$1",
                    "RoomTypeName": "SINGLE DELUXE",
                    "RatePlanCode": "007:92G:228:SGLyDXzGRvALLvROzROz:N:828857|1",
                    "RatePlan": 0,
                    "InfoSource": "OpenCombination",
                    "SequenceNo": "1",
                    "DayRates": [
                        {
                            "Amount": 1658.17,
                            "Date": "2020-04-30T00:00:00"
                        }
                    ],
                    "SupplierPrice": None,
                    "Price": {
                        "CurrencyCode": "INR",
                        "RoomPrice": 1658.17,
                        "Tax": 0,
                        "ExtraGuestCharge": 0,
                        "ChildCharge": 0,
                        "OtherCharges": 248.5,
                        "Discount": 0,
                        "PublishedPrice": 1906.67,
                        "PublishedPriceRoundedOff": 1907,
                        "OfferedPrice": 1906.67,
                        "OfferedPriceRoundedOff": 1907,
                        "AgentCommission": 0,
                        "AgentMarkUp": 0,
                        "ServiceTax": 44.75,
                        "TDS": 0,
                        "ServiceCharge": 0,
                        "TotalGSTAmount": 44.75,
                        "GST": {
                            "CGSTAmount": 0,
                            "CGSTRate": 0,
                            "CessAmount": 0,
                            "CessRate": 0,
                            "IGSTAmount": 44.75,
                            "IGSTRate": 18,
                            "SGSTAmount": 0,
                            "SGSTRate": 0,
                            "TaxableAmount": 248.7
                        }
                    },
                    "RoomPromotion": "",
                    "Amenities": [
                        "Room Only"
                    ],
                    "Amenity": [],
                    "SmokingPreference": "NoPreference",
                    "BedTypes": [],
                    "HotelSupplements": [],
                    "LastCancellationDate": "2020-04-16T23:59:59",
                    "CancellationPolicies": [
                        {
                            "Charge": 1658,
                            "ChargeType": 1,
                            "Currency": "INR",
                            "FromDate": "2020-04-17T00:00:00",
                            "ToDate": "2020-04-20T23:59:59"
                        },
                        {
                            "Charge": 100,
                            "ChargeType": 2,
                            "Currency": "INR",
                            "FromDate": "2020-04-21T00:00:00",
                            "ToDate": "2020-05-01T23:59:59"
                        },
                        {
                            "Charge": 100,
                            "ChargeType": 2,
                            "Currency": "INR",
                            "FromDate": "2020-04-30T00:00:00",
                            "ToDate": "2020-05-01T00:00:00"
                        }
                    ],
                    "CancellationPolicy": "SINGLE DELUXE#^#INR 1658.00 will be charged, If cancelled between 17-Apr-2020 00:00:00 and 20-Apr-2020 23:59:59.|100.00% of total amount will be charged, If cancelled between 21-Apr-2020 00:00:00 and 01-May-2020 23:59:59.|100.00% of total amount will be charged, If cancelled between 30-Apr-2020 00:00:00 and 01-May-2020 00:00:00.|#!#",
                    "Inclusion": [
                        "Room Only"
                    ]
                }
            ],
            # "EndUserIp": "1.1.1.1",
            # "ClientId": "180120",
            # "UserName": "Fairfly2",
            # "Password": "Fairfly@22"
        }
        if data:
            payload_data = {**head, **data}
        else:
            payload_data = {**head, **sampleData}

        try:
            # print("headers\n", headers)
            response = requests.post(
                url, json=payload_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                return response_data

            else:
                return {"Error": f"{response.status_code} - {response.text}", "headers_passed": headers, "data_passed": payload_data}

        except requests.exceptions.RequestException as e:
            return {"Error": e, "headers_passed": headers, "data_passed": payload_data}

    def BookRoom(self, data):
        url = "https://hotel.srdvtest.com/v5/rest/Book"
        sampleData = {
            "TraceId": "1",
            "SrdvType": "SingleTB",
            "SrdvIndex": "SrdvTB",
            "ResultIndex": 9,
            "HotelCode": "92G|DEL",
            "HotelName": "The Manor",
            "GuestNationality": "IN",
            "NoOfRooms": "1",
            "ClientReferenceNo": 0,
            "IsVoucherBooking": True,
            "HotelRoomsDetails": [
                {
                    "ChildCount": 0,
                    "RequireAllPaxDetails": True,
                    "RoomId": 0,
                    "RoomStatus": 0,
                    "RoomIndex": 1,
                    "RoomTypeCode": "007:92G:228:SGLyDXzGRvALLvROzROz:N:828857$#$1",
                    "RoomTypeName": "SINGLE DELUXE",
                    "RatePlanCode": "007:92G:228:SGLyDXzGRvALLvROzROz:N:828857|1",
                    "RatePlan": 0,
                    "InfoSource": "OpenCombination",
                    "SequenceNo": "1",
                    "DayRates": [
                        {
                            "Amount": 1658.17,
                            "Date": "2020-04-30T00:00:00"
                        }
                    ],
                    "SupplierPrice": None,
                    "Price": {
                        "CurrencyCode": "INR",
                        "RoomPrice": 1658.17,
                        "Tax": 0,
                        "ExtraGuestCharge": 0,
                        "ChildCharge": 0,
                        "OtherCharges": 248.5,
                        "Discount": 0,
                        "PublishedPrice": 1906.67,
                        "PublishedPriceRoundedOff": 1907,
                        "OfferedPrice": 1906.67,
                        "OfferedPriceRoundedOff": 1907,
                        "AgentCommission": 0,
                        "AgentMarkUp": 0,
                        "ServiceTax": 44.75,
                        "TDS": 0,
                        "ServiceCharge": 0,
                        "TotalGSTAmount": 44.75,
                        "GST": {
                            "CGSTAmount": 0,
                            "CGSTRate": 0,
                            "CessAmount": 0,
                            "CessRate": 0,
                            "IGSTAmount": 44.75,
                            "IGSTRate": 18,
                            "SGSTAmount": 0,
                            "SGSTRate": 0,
                            "TaxableAmount": 248.7
                        }
                    },
                    "RoomPromotion": "",
                    "Amenities": [
                        "Room Only"
                    ],
                    "Amenity": [],
                    "SmokingPreference": "NoPreference",
                    "BedTypes": [],
                    "HotelSupplements": [],
                    "LastCancellationDate": "2020-04-16T23:59:59",
                    "CancellationPolicies": [
                        {
                            "Charge": 1658,
                            "ChargeType": 1,
                            "Currency": "INR",
                            "FromDate": "2020-04-17T00:00:00",
                            "ToDate": "2020-04-20T23:59:59"
                        },
                        {
                            "Charge": 100,
                            "ChargeType": 2,
                            "Currency": "INR",
                            "FromDate": "2020-04-21T00:00:00",
                            "ToDate": "2020-05-01T23:59:59"
                        },
                        {
                            "Charge": 100,
                            "ChargeType": 2,
                            "Currency": "INR",
                            "FromDate": "2020-04-30T00:00:00",
                            "ToDate": "2020-05-01T00:00:00"
                        }
                    ],
                    "CancellationPolicy": "SINGLE DELUXE#^#INR 1658.00 will be charged, If cancelled between 17-Apr-2020 00:00:00 and 20-Apr-2020 23:59:59.|100.00% of total amount will be charged, If cancelled between 21-Apr-2020 00:00:00 and 01-May-2020 23:59:59.|100.00% of total amount will be charged, If cancelled between 30-Apr-2020 00:00:00 and 01-May-2020 00:00:00.|#!#",
                    "Inclusion": [
                        "Room Only"
                    ]
                }
            ],
            # "EndUserIp": "1.1.1.1",
            # "ClientId": "180120",
            # "UserName": "Fairfly2",
            # "Password": "Fairfly@22"
        }
        if data:
            payload_data = {**head, **data}
        else:
            payload_data = {**head, **sampleData}
        print(json.dumps(payload_data, indent=4))
        try:
            # print("headers\n", headers)
            response = requests.post(
                url, json=payload_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                return response_data

            else:
                return {"Error": f"{response.status_code} - {response.text}", "headers_passed": headers, "data_passed": payload_data}

        except requests.exceptions.RequestException as e:
            return {"Error": e, "headers_passed": headers, "data_passed": payload_data}


class Bus:
    def bus_balance_check(self):
        api_url = 'https://bus.srdvtest.com/v5/rest/Balance'
        payload_data = head

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

    def bus_city_list(self,):
        api_url = 'https://bus.srdvtest.com/v5/rest/GetBusCityList'
        payload_data = head
        try:
            # print(payload_data)
            response = requests.post(
                api_url, json=payload_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                return response_data

            else:
                print(f"Error: {response.status_code} - {response.text}")
                return (f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return (f"Error: {e}")

    # print(json.dumps(bus_city_list(), indent=4))

    def bus_search(self, inp=None):
        api_url = 'https://bus.srdvtest.com/v5/rest/Search'
        if inp:
            payload_data = {**head, **inp}
            print("payload", payload_data)
        else:
            data = {
                "source_city": "Mumbai",
                "source_code": "3534",
                "destination_city": "Pune",
                "destination_code": "9771",
                "depart_date": "2020-06-14"
            }
            payload_data = {**head, **data}
            # print(payload_data)
            # print("default payload", payload_data)

        try:
            # print("headers - ", headers)
            response = requests.post(
                api_url, json=payload_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                return response_data

            else:
                return {"Error": f"{response.status_code} - {response.text}", "headers_passed": headers, "data_passed": payload_data}

        except requests.exceptions.RequestException as e:
            return {"Error": e, "headers_passed": headers, "data_passed": payload_data}

    def bus_seat_layout(self, inp=None):
        url = 'https://bus.srdvtest.com/v5/rest/GetSeatLayOut'

        if inp:
            payload_data = {**head, **inp}
            print("payload", payload_data)

        else:
            data = {
                "TraceId": "1",
                "ResultIndex": "1"
            }
            payload_data = {**head, **data}

        try:
            print("headers - ", headers)
            response = requests.post(url, json=payload_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                return response_data

            else:
                return {"Error": f"{response.status_code} - {response.text}", "headers_passed": headers, "data_passed": payload_data}

        except requests.exceptions.RequestException as e:
            return {"Error": e, "headers_passed": headers, "data_passed": payload_data}

    # print(json.dumps(bus_search(), indent=4))
    def bus_boarding_point_details(self, inp=None):
        url = 'https://bus.srdvtest.com/v5/rest/GetBoardingPointDetails'

        if inp:
            payload_data = {**head, **inp}
            print("payload", payload_data)

        else:
            data = {
                "TraceId": "1",
                "ResultIndex": "1"
            }
            payload_data = {**head, **data}

        try:
            print("headers - ", headers)
            response = requests.post(url, json=payload_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                return response_data

            else:
                return {"Error": f"{response.status_code} - {response.text}", "headers_passed": headers, "data_passed": payload_data}

        except requests.exceptions.RequestException as e:
            return {"Error": e, "headers_passed": headers, "data_passed": payload_data}

    def Bus_Booking_Req(self, data):
        api_url = 'https://bus.srdvtest.com/v5/rest/Book'

        if data:
            payload_data = {**head, **data}
            print("payload", payload_data)
        else:
            return False

        resp = self.BlockBus(payload_data)
        if resp['Error']['ErrorCode'] != '0':
            print(resp)
            return None, 501
        response = requests.post(api_url, json=payload_data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if response_data['Error']['ErrorCode'] != '0':
                # print(resp)
                return ({"Error": response_data['Error']['ErrorCode'], "resp": response_data}), 501
            return response_data

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return (f"Error: {response.status_code} - {response.text}")

    def BlockBus(self, data):
        api_url = 'https://bus.srdvtest.com/v5/rest/Block'

        if data:
            payload_data = {**head, **data}
        else:
            return False
        response = requests.post(api_url, json=payload_data, headers=headers)

        if response.status_code == 200:
            try:
                response_data = response.json()
                return response_data
            except Exception as e:
                print("error at fare quote", e)
                return response

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return (f"Error: {response.status_code} - {response.text}")


class flight:
    def balance_check(self,):
        api_url = 'https://flight.srdvtest.com/v5/rest/Balance'
        payload_data = {**head}

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

    def Flight_search(self, inp=None):
        api_url = 'https://flight.srdvtest.com/v8/rest/Search'
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
            response = requests.post(
                api_url, json=payload_data, headers=headers)

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

    def LLC_ticket_Req(self, data):
        api_url = 'https://flight.srdvtest.com/v8/rest/TicketLCC'

        if data:
            payload_data = {**head, **data}
        else:
            return False

        fare_quote_data = {
            "SrdvType": data["SrdvType"],
            "SrdvIndex": data["SrdvIndex"],
            "TraceId": data["TraceId"],
            "ResultIndex": data["ResultIndex"]
        }
        resp = self.Fare_quote(fare_quote_data)
        if resp['Error']['ErrorCode'] != '0':
            print(resp)
            return None, 501
        for i in range(len(data['Passengers'])):
            payload_data["Passengers"][i]['Fare'] = resp['Results']['Fare']

        response = requests.post(api_url, json=payload_data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return {"Response": response_data, "req": payload_data, "headers": headers}
            return response_data

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return (f"Error: {response.status_code} - {response.text}")

    def Fare_quote(self, data):
        api_url = 'https://flight.srdvtest.com/v8/rest/FareQuote'
        if data:
            payload_data = {**head, **data}
        else:
            return False
        response = requests.post(api_url, json=payload_data, headers=headers)

        if response.status_code == 200:
            try:
                response_data = response.json()
                return response_data
            except Exception as e:
                print("error at fare quote", e)
                return response

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return (f"Error: {response.status_code} - {response.text}")


class firebase:
    def __init__(self) -> None:
        try:
            self.cred = credentials.Certificate(
                "fairflying_auth_firebase.json")
        except Exception as e:
            print(e)
            print("failed to get firebasse auth json from root dir")
            self.cred = credentials.Certificate(
                'backend/Flight_API/fairflying_auth_firebase.json')

        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def check_user_exists(self, uid):
        try:
            user = auth.get_user(uid)
            print(user)
            return True
        except FirebaseError as e:
            if e.code == 'user-not-found':
                print("User does not exist")
                return False
            else:
                # Handle other exceptions
                print("Error occurred:", e)
                return False

    def change_email_auth_password(self, uid, new_password):
        try:
            auth.update_user(
                uid,
                password=new_password
            )
            print("Password changed successfully.")
            return True
        except auth.AuthError as e:
            print("Error occurred:", e)
            return False

    def get_user_email(self, uid):
        try:
            user = auth.get_user(uid)
            return user.email
        except FirebaseError as e:
            if e.code == 'user-not-found':
                print("User does not exist")
            else:
                # Handle other exceptions
                print("Error occurred:", e)
            return None

    def store_user_data(self, uid, user_data):
        try:
            user_ref = self.db.collection('users').document(uid)
            user_ref.set(user_data)
            print("User data stored successfully.")
            return True
        except FirebaseError as e:
            print("Error occurred:", e)
            return False

    def get_user_data(self, uid):
        try:
            user_ref = self.db.collection('users').document(uid)
            user_data = user_ref.get()
            if user_data.exists:
                return user_data.to_dict()
            else:
                print("User data not found.")
                return None
        except FirebaseError as e:
            print("Error occurred:", e)
            return None

    def write_to_firestore(self, id, data, collection="user_data"):
        doc_ref = self.db.collection(collection).document(id)
        doc_ref.set(data)
        print("Document '{}' written to Firestore.".format(id))
        return True

    def read_from_firestore(self, custom_id, collection="user_data"):
        doc_ref = self.db.collection(collection).document(custom_id)
        doc = doc_ref.get()
        return doc.to_dict()

    def get_all_document_ids(self, collection="user_data"):
        docs = self.db.collection(collection).list_documents()
        return [doc.id for doc in docs]

    def generate_unique_id(self, length=9, collection="user_data"):
        existing_ids = set(self.get_all_document_ids(collection))
        new_id = ''.join(random.choices(
            string.ascii_letters + string.digits, k=length))
        while new_id in existing_ids:
            new_id = ''.join(random.choices(
                string.ascii_letters + string.digits, k=length))
        return new_id

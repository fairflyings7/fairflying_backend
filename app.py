
from flask import Flask, jsonify, request, redirect, send_file
from flask_cors import CORS
from flask_mail import Mail, Message

import razorpay

import io
import os
import json

from Functions import Hotels, Bus, flight, firebase
HOTELS = Hotels()
BUS = Bus()
FLIGHT = flight()
FIREBASE = firebase()
'''
booking flow

1. create order number -> save all the pre payment data associated to it, and mail it to user saying "booking innitiated on this order number"
2. complete payment / failed payment -> updated details of that order number, 
3. add section in db to save generated markdown (for future ticket invoice download)
4. mail user the success of oppeation with a link to download generated pdf invoice

'''

app = Flask(__name__)
CORS(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True   # Set it to False if you're using SSL
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")

mail = Mail(app)


def send_email(email, subject, body):
    try:
        message = Message(subject=subject, recipients=[email])
        message.body = body
        mail.send(message)
        return True
    except Exception as e:
        print("Error sending email:", str(e))
        return False


@app.route('/')
def health():
    return "hi", 200


@app.route('/check_flight_balace', methods=['GET'])
def flight_balance_check():
    res = FLIGHT.balance_check()
    return jsonify(res), 200


@app.route('/search_flights', methods=['POST'])
def search_flights():
    req = request.get_json()
    res = FLIGHT.Flight_search(req['data'])
    return jsonify(res), 200


@app.route('/book_flight', methods=['POST'])
def booking_function():
    res = request.get_json()
    data = res['data']

    res = FLIGHT.LLC_ticket_Req(data)
    return jsonify(res), 200


@app.route('/search_hotels', methods=['POST'])
def search_hotel():
    req = request.get_json()
    res = HOTELS.Hotel_search(req['data'])
    return jsonify(res), 200


@app.route('/hotelsRoomInfo', methods=['POST'])
def hotelRoomInfo():
    req = request.get_json()
    res = HOTELS.RoomInfo(req['data'])
    return jsonify(res), 200


@app.route('/hotelsInfo', methods=['POST'])
def hotelInfo():
    req = request.get_json()
    res = HOTELS.HotelInfo(req['data'])
    return jsonify(res), 200


@app.route('/hotelsbooking', methods=['POST'])
def hotelbooking():
    req = request.get_json()
    block = HOTELS.BlockRoom(req['data'])
    book = HOTELS.BookRoom(req['data'])
    return jsonify({"blockResponse": block, "bookResponse": book}), 200


@app.route('/search_bus', methods=['POST'])
def search_buses():
    req = request.get_json()
    res = BUS.bus_search(req['data'])
    return jsonify(res), 200


@app.route('/bus_city_list', methods=['GET'])
def bus_city_list():
    # req = request.get_json()
    res = BUS.bus_city_list()
    return res, 200


@app.route('/bus_seat_layout', methods=['POST'])
def bus_seat_layout():
    req = request.get_json()
    if not req:
        return jsonify({"desc": "requirment not fullfilled"}), 401

    res = BUS.bus_seat_layout(req)
    return res, 200


@app.route('/bus_points', methods=['POST'])
def bus_pt():
    req = request.get_json()
    if not req:
        return jsonify({"desc": "requirment not fullfilled"}), 401

    res = BUS.bus_boarding_point_details(req)
    return res, 200


@app.route('/create_payment_request', methods=['POST'])
def create_payment_request():
    res = request.get_json()
    auth = request.headers.get('Authorization')

    return jsonify({"resp": {"link": "https://google.com"}}), 200


@app.route('/check_payment_status', methods=['POST'])
def check_payment_status():
    res = request.get_json()

    return jsonify(True), 200


@app.route('/check_bus_balace', methods=['GET'])
def bus_balance_check():
    res = BUS.bus_balance_check()
    return jsonify(res), 200


@app.route('/check_hotel_balace', methods=['GET'])
def hotel_balance_check():
    res = HOTELS.balance_check()
    return jsonify(res), 200


@app.route('/cancellation', methods=['POST'])
def cancellation():
    res = request.get_json()

    return jsonify({}), 200


RAZOR_KEY = os.getenv('RAZORPAY_KEY', None)
RAZOR_SECRET = os.getenv('RAZORPAY_SECRET', None)

razorpay_client = razorpay.Client(
    auth=(RAZOR_KEY, RAZOR_SECRET))


@app.route("/razorpay_order", methods=['POST'])
def PaymentView():
    body = request.get_json()
    metadata = body["metadata"]
    razorpay_order = razorpay_client.order.create(
        {"amount": int(metadata["amount"]) * 100, "currency": "INR",
         "payment_capture": "1"}
    )
    newMetaData = {
        **metadata,
        "merchantId": RAZOR_KEY,
        "currency": 'INR',
        "orderId": razorpay_order["id"],
    }
    body = {
        **body,
        "metadata": newMetaData
    }

    FIREBASE.write_to_firestore(
        id=razorpay_order["id"], data=body, collection="payments")

    mail_body = 'An order is created at Fairflyings with this email address, incase of any doubt please refer to order ID ' + \
        razorpay_order["id"] + " to further refer to this payment"
    send_email(email=metadata["email"],
               subject="Order Created", body=mail_body)
    return jsonify(body), 200


@app.route("/razorpay_callback", methods=['POST'])
def CallbackView():
    try:
        response = request.get_json(force=True)
    except Exception as e:
        response = request.form.to_dict()

    if "razorpay_signature" in response:
        # Verifying Payment Signature
        data = razorpay_client.utility.verify_payment_signature(response)

        # if we get here True signature
        if data:
            payment_object = FIREBASE.read_from_firestore(
                custom_id=response['razorpay_order_id'], collection="payments")

            data = payment_object['data']
            if payment_object["type"] == "flight":
                # res = FLIGHT.LLC_ticket_Req(data)
                res = {"Error": {"ErrorCode": "0", "ErrorMessage": ""}, "TraceId": "174278", "ResponseStatus": "1", "SrdvType": "MixAPI", "Response": {"SrdvIndex": "2", "PNR": "TESTPNR", "BookingId": 2106, "SSRDenied": "", "SSRMessage": "", "Status": "1", "IsPriceChanged": false, "IsTimeChanged": false, "TicketStatus": "1", "FlightItinerary": {"BookingId": 2106, "IsManual": false, "PNR": "TESTPNR", "IsDomestic": "Not Set", "Source": "Publish", "Origin": "DEL", "Destination": "AMD", "AirlineCode": "6E", "LastTicketDate": "", "ValidatingAirlineCode": "", "AirlineRemark": [], "IsLCC": true, "NonRefundable": false, "FareType": "Publish", "CreditNoteNo": "", "Fare": {"Currency": "INR", "BaseFare": 3691, "Tax": 1465, "YQTax": 700, "AdditionalTxnFeeOfrd": 0, "AdditionalTxnFeePub": 0, "PGCharge": 0, "OtherCharges": 0, "PublishedFare": 5156, "OfferedFare": 5156, "CommissionEarned": 0, "TdsOnCommission": 0, "ServiceFee": 0, "TotalBaggageCharges": 0, "TotalMealCharges": 0, "TotalSeatCharges": 0, "TotalSpecialServiceCharges": 0}, "CreditNoteCreatedOn": "", "Passenger": [{"PaxId": "", "Title": "Mr", "FirstName": "First", "LastName": "Name", "PaxType": "1", "DateOfBirth": "", "Gender": "", "PassportNo": "", "AddressLine1": "", "City": "", "CountryCode": "", "CountryName": "", "Nationality": "", "ContactNo": "09870123654", "Email": "navneet@srdvtechnologies.com", "IsLeadPax": "", "FFAirlineCode": "", "FFNumber": "", "Fare": {"Currency": "", "BaseFare": "", "Tax": "", "YQTax": "", "AdditionalTxnFeeOfrd": "", "AdditionalTxnFeePub": "", "PGCharge": "", "OtherCharges": "", "PublishedFare": "", "OfferedFare": "", "ServiceFee": "", "TotalBaggageCharges": "", "TotalMealCharges": "", "TotalSeatCharges": "", "TotalSpecialServiceCharges": ""}, "Ticket": {"TicketId": "", "TicketNumber": "", "IssueDate": "", "ValidatingAirline": "", "Remarks": "", "ServiceFeeDisplayType": "", "Status": ""}, "SegmentAdditionalInfo": [{"FareBasis": "", "NVA": "", "NVB": "", "Baggage": "", "Meal": "", "Seat": "", "SpecialService": ""}]}], "CancellationCharges": "", "Segments": [
                    {"Baggage": "15 Kg (01 Piece only)", "CabinBaggage": "7 Kg", "TripIndicator": 1, "SegmentIndicator": 1, "DepTime": "2023-12-31T18:40", "ArrTime": "2023-12-31T20:05", "Airline": {"AirlineCode": "6E", "AirlineName": "IndiGo", "FlightNumber": "2501", "FareClass": "R", "OperatingCarrier": ""}, "AirlinePNR": "", "AccumulatedDuration": 245, "Origin": {"AirportCode": "DEL", "AirportName": "Delhi Indira Gandhi Intl", "Terminal": "Terminal 2", "CityCode": "DEL", "CityName": "Delhi", "CountryCode": "IN", "CountryName": "India"}, "Destination": {"AirportCode": "AMD", "AirportName": "Sardar Vallabh Bhai Patel Intl Arpt", "Terminal": "Terminal 1", "CityCode": "AMD", "CityName": "Ahmedabad", "CountryCode": "IN", "CountryName": "India"}, "Duration": 85, "GroundTime": 160, "Mile": "", "StopOver": "", "StopPoint": "", "StopPointArrivalTime": "", "StopPointDepartureTime": "", "Craft": "", "Remark": "", "IsETicketEligible": "", "FlightStatus": "", "Status": ""}, {"Baggage": "15 Kg (01 Piece only)", "CabinBaggage": "7 Kg", "TripIndicator": 1, "SegmentIndicator": 2, "DepTime": "2023-12-31T22:45", "ArrTime": "2024-01-01T00:10", "Airline": {"AirlineCode": "6E", "AirlineName": "IndiGo", "FlightNumber": "6794", "FareClass": "R", "OperatingCarrier": ""}, "AirlinePNR": "", "AccumulatedDuration": 330, "Origin": {"AirportCode": "AMD", "AirportName": "Sardar Vallabh Bhai Patel Intl Arpt", "Terminal": "Terminal 1", "CityCode": "AMD", "CityName": "Ahmedabad", "CountryCode": "IN", "CountryName": "India"}, "Destination": {"AirportCode": "BOM", "AirportName": "Chhatrapati Shivaji", "Terminal": "Terminal 2", "CityCode": "BOM", "CityName": "Mumbai", "CountryCode": "IN", "CountryName": "India"}, "Duration": 85, "GroundTime": "", "Mile": "", "StopOver": "", "StopPoint": "", "StopPointArrivalTime": "", "StopPointDepartureTime": "", "Craft": "", "Remark": "", "IsETicketEligible": "", "FlightStatus": "", "Status": ""}], "FareRules": [{"Origin": "", "Destination": "", "Airline": "", "FareBasisCode": "", "FareRuleDetail": "", "FareRestriction": ""}], "InvoiceNo": "", "InvoiceStatus": "", "InvoiceCreatedOn": "", "Remarks": "", "PartialSegmentCancellation": "Not Allowed"}}}
            elif payment_object["type"] == "hotel":
                # block = Hotels.BlockRoom(data)
                # book = Hotels.BookRoom(data)
                res = {
                    "block": {
                        "BlockRoomResult": {
                            "Error": {
                                "ErrorCode": 0,
                                "ErrorMessage": ""
                            },
                            "AvailabilityType": "Confirm",
                            "TraceId": "1",
                            "ResponseStatus": 1,
                            "GSTAllowed": False,
                            "IsPackageDetailsMandatory": False,
                            "IsPackageFare": False,
                            "IsPriceChanged": False,
                            "IsCancellationPolicyChanged": False,
                            "IsHotelPolicyChanged": True,
                            "HotelNorms": "india - land of mystries \"//\" \"  /// \"  |<ul><li>Check-in hour 14:00 - .  Valid From 2020-04-30 through 2020-05-01Identification card at arrival.  Valid From 2020-04-30 through 2020-05-01Minimum check-in age 18.  Valid From 2020-04-30 through 2020-05-01Car park YES (without additional debit notes).  Valid From 2020-04-30 through 2020-05-01</li><li>Amendments cannot be made against this booking once your booking has been requested.</li></ul>",
                            "HotelName": "Avtar",
                            "AddressLine1": "Road Pahar Ganj, 3425 DB Gupta Rd, Arya  110015 DELHI India",
                            "AddressLine2": "\n Phone No: 911123580007\n Fax : 911123587103",
                            "StarRating": 2,
                            "HotelPolicyDetail": "india - land of mystries \"//\" \"  /// \"  |<ul><li>Check-in hour 14:00 - .  Valid From 2020-04-30 through 2020-05-01Identification card at arrival.  Valid From 2020-04-30 through 2020-05-01Minimum check-in age 18.  Valid From 2020-04-30 through 2020-05-01Car park YES (without additional debit notes).  Valid From 2020-04-30 through 2020-05-01</li><li>Amendments cannot be made against this booking once your booking has been requested.</li></ul>",
                            "Latitude": "28.6443589",
                            "Longitude": "77.2128331",
                            "BookingAllowedForRoamer": False,
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
                            ]
                        }
                    },
                    "book": {
                        "BookResult": {
                            "Error": {
                                "ErrorCode": 0,
                                "ErrorMessage": ""
                            },
                            "VoucherStatus": True,
                            "ResponseStatus": 1,
                            "TraceId": "1",
                            "Status": 1,
                            "HotelBookingStatus": "Confirmed",
                            "InvoiceNumber": "MW/1920/17991",
                            "ConfirmationNo": "270-300706",
                            "BookingRefNo": "270-300706",
                            "BookingId": 1554760,
                            "IsPriceChanged": False,
                            "IsCancellationPolicyChanged": False
                        }
                    }
                }
            elif payment_object["type"] == "bus":
                # block = BUS.BlockBus(data)
                # block = BUS.Bus_Booking_Req(data)

                res = {
                    "block": {
                        "Error": {
                            "ErrorCode": 0,
                            "ErrorMessage": ""
                        },
                        "Result": {
                            "ResponseStatus": 1,
                            "ArrivalTime": "02/14/2020 12:45:00",
                            "BusType": "Leyland Non A/C Seater KingSize Family (2+2)",
                            "DepartureTime": "02/14/2020 21:45:00",
                            "ServiceName": "Seat Seller",
                            "TraceId": "1",
                            "TravelName": "TESTING ACCOUNT",
                            "BoardingPointdetails": {
                                "CityPointIndex": 1,
                                "CityPointLocation": "Kalamboli Mc Donolds Hotel",
                                "CityPointName": "Kalamboli Mc Donolds Hotel",
                                "CityPointTime": "2020-02-14T09:55:00"
                            },
                            "CancelPolicy": [
                                {
                                    "CancellationCharge": 10,
                                    "CancellationChargeType": 2,
                                    "PolicyString": "Till 16:45 on 13 Feb 2020",
                                    "FromDate": "2020-01-23T12:12:43",
                                    "ToDate": "2020-02-13T16:45:00"
                                },
                                {
                                    "CancellationCharge": 50,
                                    "CancellationChargeType": 2,
                                    "PolicyString": "Between 16:45 on 13 Feb 2020 - 04:45 on 14 Feb 2020",
                                    "FromDate": "2020-02-13T16:45:00",
                                    "ToDate": "2020-02-14T04:45:00"
                                },
                                {
                                    "CancellationCharge": 100,
                                    "CancellationChargeType": 2,
                                    "PolicyString": "After 04:45 on 14 Feb 2020",
                                    "FromDate": "2020-02-14T04:45:00",
                                    "ToDate": "2020-02-14T12:45:00"
                                }
                            ],
                            "Passenger": [
                                {
                                    "LeadPassenger": True,
                                    "Title": "Mr",
                                    "Address": "Modinagar",
                                    "Age": "22",
                                    "FirstName": "Amit",
                                    "Gender": "1",
                                    "IdNumber": None,
                                    "IdType": None,
                                    "Phoneno": "9643737502",
                                    "Seat": {
                                        "ColumnNo": "001",
                                        "Height": 1,
                                        "IsLadiesSeat": False,
                                        "IsMalesSeat": False,
                                        "IsUpper": False,
                                        "RowNo": "000",
                                        "SeatFare": 400,
                                        "SeatIndex": 2,
                                        "SeatName": "2",
                                        "SeatStatus": True,
                                        "SeatType": 1,
                                        "Width": 1,
                                        "Price": {
                                            "CurrencyCode": "INR",
                                            "BasePrice": 400,
                                            "Tax": 0,
                                            "OtherCharges": 0,
                                            "Discount": 0,
                                            "PublishedPrice": 400,
                                            "PublishedPriceRoundedOff": 400,
                                            "OfferedPrice": 380,
                                            "OfferedPriceRoundedOff": 380,
                                            "AgentCommission": 20,
                                            "AgentMarkUp": 0,
                                            "TDS": 8,
                                            "GST": {
                                                "CGSTAmount": 0,
                                                "CGSTRate": 0,
                                                "CessAmount": 0,
                                                "CessRate": 0,
                                                "IGSTAmount": 0,
                                                "IGSTRate": 18,
                                                "SGSTAmount": 0,
                                                "SGSTRate": 0,
                                                "TaxableAmount": 0
                                            }
                                        }
                                    }
                                },
                                {
                                    "LeadPassenger": False,
                                    "Title": "Mr",
                                    "Address": "Modinagar",
                                    "Age": "28",
                                    "FirstName": "ramesh",
                                    "Gender": "1",
                                    "IdNumber": None,
                                    "IdType": None,
                                    "Phoneno": "1234567890",
                                    "Seat": {
                                        "ColumnNo": "002",
                                        "Height": 1,
                                        "IsLadiesSeat": False,
                                        "IsMalesSeat": False,
                                        "IsUpper": False,
                                        "RowNo": "000",
                                        "SeatFare": 400,
                                        "SeatIndex": 3,
                                        "SeatName": "3",
                                        "SeatStatus": True,
                                        "SeatType": 1,
                                        "Width": 1,
                                        "Price": {
                                            "CurrencyCode": "INR",
                                            "BasePrice": 400,
                                            "Tax": 0,
                                            "OtherCharges": 0,
                                            "Discount": 0,
                                            "PublishedPrice": 400,
                                            "PublishedPriceRoundedOff": 400,
                                            "OfferedPrice": 380,
                                            "OfferedPriceRoundedOff": 380,
                                            "AgentCommission": 20,
                                            "AgentMarkUp": 0,
                                            "TDS": 8,
                                            "GST": {
                                                "CGSTAmount": 0,
                                                "CGSTRate": 0,
                                                "CessAmount": 0,
                                                "CessRate": 0,
                                                "IGSTAmount": 0,
                                                "IGSTRate": 18,
                                                "SGSTAmount": 0,
                                                "SGSTRate": 0,
                                                "TaxableAmount": 0
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    "book": {
                        "Error": {
                            "ErrorCode": 0,
                            "ErrorMessage": ""
                        },
                        "Result": {
                            "TraceId": "1",
                            "BusBookingStatus": "Confirmed",
                            "InvoiceAmount": 388,
                            "BusId": 11836,
                            "TicketNo": "25SYK4ET",
                            "TravelOperatorPNR": "25SYK4ET"
                        }
                    }
                }
            else:
                res = {"status": "null", "Desc": "type not selected"}

            payment_object = {
                **payment_object,
                "metadata": {
                    **payment_object["metadata"],
                    "status": "Success",
                    "payment_id": response['razorpay_payment_id'],
                    "signature_id": response['razorpay_signature'],
                },
                "Booking": res
            }

            FIREBASE.write_to_firestore(
                id=response["razorpay_order_id"], data=payment_object, collection="payments")

            mail_body = 'Your order by Fairflyings has been placed successfully. please use the order ID ' + \
                response['razorpay_order_id'] + \
                " to further refer to this payment"
            send_email(email=payment_object["metadata"]["email"],
                       subject="Order Successfull", body=mail_body)
            return redirect(os.getenv("WEB_URL")+"/booking-success?order_id=" + response['razorpay_order_id'])
        else:
            send_email(email=payment_object["metadata"]["email"], subject="Order Failed",
                       body="your recent order failed, if payment deducted please refer to order id sent to you for refund")
            return redirect(os.getenv("WEB_URL")+"/failure?order_id=" + response['razorpay_order_id'])

    else:
        error_metadata = json.loads(response.get('error[metadata]', '{}'))
        print(json.dumps(error_metadata, indent=4))
        payment_object = FIREBASE.read_from_firestore(
            custom_id=error_metadata['order_id'], collection="payments")
        payment_object = {
            **payment_object,
            "payment_id": error_metadata.get('payment_id'),
            "signature_id": "None",
            "status": "Failed",
            "error_status": {
                'error_code': response.get('error[code]'),
                'error_description': response.get('error[description]'),
                'error_source': response.get('error[source]'),
                'error_reason': response.get('error[reason]'),
            }
        }

        FIREBASE.write_to_firestore(
            id=error_metadata['order_id'], data=payment_object, collection="payments")

        send_email(email=payment_object["metadata"]["email"], subject="Order Failed",
                   body="your recent order failed, if payment deducted please refer to order id sent to you for refund")
        return redirect(os.getenv("WEB_URL")+"/failure?order_id=" + error_metadata['order_id'])


@app.route('/get-order-info', methods=['POST'])
def get_order_info():
    res = request.get_json()
    order_id = res['orderId']
    payment_object = FIREBASE.read_from_firestore(
        custom_id=order_id, collection="payments")

    return jsonify(payment_object), 200


@app.route('/get_pdf', methods=['post'])
def get_pdf():
    data = request.get_json()
    orderId = data['orderId']
    from report import flight_invoiceMD, get_pdf

    payment_object = FIREBASE.read_from_firestore(
        custom_id=orderId, collection="payments")
    markdown = flight_invoiceMD(payment_object["Booking"])
    pdf_content = get_pdf(markdown)
    if pdf_content is not None:
        return send_file(
            io.BytesIO(pdf_content),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='generated_pdf.pdf'
        )
    else:
        return "PDF generation failed.", 500
    # except Exception as e:
    #     print(e)
    #     return {"Error":"An error occurred while generating the PDF"}


if __name__ == '__main__':
    app.run(debug=True)

'''
company name
company add

pnr
booking id / TICKET NUMBER

passenger details
    name
    add
    email
    number etc

flight detials
    airline name
    logo
    numver
    from - to
    date arr-dep

    meal & bagage [default / custom]

price 
    base
    tax
    publishedFair {taken ferom customer}


    offered fair {deducted from our side}
'''

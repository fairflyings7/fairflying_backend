import requests
flight_booking_response = {'Error':
                           {'ErrorCode': '0', 'ErrorMessage': ''},
                           'TraceId': '133414',
                           'ResponseStatus': '1',
                           'SrdvType': 'MixAPI',
                           'Response': {
                               'SrdvIndex': '2',
                               'PNR': 'M1J4VP',
                               'BookingId': 204800,
                               'SSRDenied': '',
                               'SSRMessage': '',
                               'Status': '1',
                               'IsPriceChanged': False,
                               'IsTimeChanged': False,
                               'TicketStatus': '1',
                               'FlightItinerary': {
                                   'BookingId': 204800,
                                   'IsManual': False,
                                   'PNR': 'M1J4VP',
                                   'IsDomestic': 'Not Set',
                                   'Source': 'Other',
                                   'Origin': 'DEL',
                                   'Destination': 'COK',
                                   'AirlineCode': 'IX',
                                   'LastTicketDate': '',
                                   'ValidatingAirlineCode': '',
                                   'AirlineRemark': [],
                                   'IsLCC': True,
                                   'NonRefundable': False,
                                   'FareType': 'Other',
                                   'CreditNoteNo': '',
                                   'Fare': {
                                       'Currency': 'INR',
                                       'BaseFare': 700,
                                       'Tax': 711,
                                       'YQTax': 0,
                                       'AdditionalTxnFeeOfrd': 0,
                                       'AdditionalTxnFeePub': 0,
                                       'PGCharge': 0,
                                       'OtherCharges': 0,
                                       'PublishedFare': 1411,
                                       'OfferedFare': 1411,
                                       'CommissionEarned': 0,
                                       'TdsOnCommission': 0,
                                       'ServiceFee': 0,
                                       'TotalBaggageCharges': 0,
                                       'TotalMealCharges': 0,
                                       'TotalSeatCharges': 0,
                                       'TotalSpecialServiceCharges': 0
                                   },
                                   'CreditNoteCreatedOn': '',
                                   'Passenger': [
                                       {
                                           'PaxId': '',
                                           'Title': 'Mr',
                                           'FirstName': 'SRDV',
                                           'LastName': 'Support',
                                           'PaxType': '1',
                                           'DateOfBirth': '1992-03-12',
                                           'Gender': '',
                                           'PassportNo': '',
                                           'AddressLine1': '',
                                           'City': '',
                                           'CountryCode': '',
                                           'CountryName': '',
                                           'Nationality': '',
                                           'ContactNo': '9632587410',
                                           'Email': 'support@srdvtechnologies.com',
                                           'IsLeadPax': '',
                                           'FFAirlineCode': '',
                                           'FFNumber': '',
                                           'Fare': {
                                               'Currency': '',
                                               'BaseFare': '',
                                               'Tax': '',
                                               'YQTax': '',
                                               'AdditionalTxnFeeOfrd': '',
                                               'AdditionalTxnFeePub': '',
                                               'PGCharge': '',
                                               'OtherCharges': '',
                                               'PublishedFare': '',
                                               'OfferedFare': '',
                                               'ServiceFee': '',
                                               'TotalBaggageCharges': '',
                                               'TotalMealCharges': '',
                                               'TotalSeatCharges': '',
                                               'TotalSpecialServiceCharges': ''
                                           },
                                           'Ticket': {
                                               'TicketId': '',
                                               'TicketNumber': '',
                                               'IssueDate': '',
                                               'ValidatingAirline': '',
                                               'Remarks': '',
                                               'ServiceFeeDisplayType': '',
                                               'Status': ''
                                           },
                                           'SegmentAdditionalInfo': [
                                               {
                                                   'FareBasis': '',
                                                   'NVA': '',
                                                   'NVB': '',
                                                   'Baggage': '',
                                                   'Meal': '',
                                                   'Seat': '',
                                                   'SpecialService': ''
                                               }
                                           ]
                                       }
                                   ],
                                   'CancellationCharges': '',
                                   'Segments': [
                                       {
                                           'Baggage': '',
                                           'CabinBaggage': '7 Kg',
                                           'TripIndicator': 1,
                                           'SegmentIndicator': 1,
                                           'DepTime': '2024-01-21T14:00',
                                           'ArrTime': '2024-01-21T16:30',
                                           'Airline': {
                                               'AirlineCode': 'IX',
                                               'AirlineName': 'AI Express',
                                               'FlightNumber': '3434',
                                               'FareClass': 'LT',
                                               'OperatingCarrier': ''
                                           },
                                           'AirlinePNR': '',
                                           'AccumulatedDuration': 240,
                                           'Origin': {
                                               'AirportCode': 'DEL',
                                               'AirportName': 'Delhi Indira Gandhi Intl',
                                               'Terminal': 'Terminal 3',
                                               'CityCode': 'DEL',
                                               'CityName': 'Delhi',
                                               'CountryCode': 'IN',
                                               'CountryName': 'India'
                                           },
                                           'DPoint': '',
                                           'StopPointArrivalTime': '',
                                           'StopPointDepartureTime': '',
                                           'Craft': '',
                                           'Remark': '',
                                           'IsETicketEligible': '',
                                           'FlightStatus': '',
                                           'Status': ''
                                       }, {
                                           'Baggage': '',
                                           'CabinBaggage': '7 Kg',
                                           'TripIndicator': 1,
                                           'SegmentIndicator': 2,
                                           'DepTime': '2024-01-21T18:00',
                                           'ArrTime': '2024-01-21T19:00',
                                           'Airline': {
                                               'AirlineCode': 'IX',
                                               'AirlineName': 'AI Express',
                                               'FlightNumber': '8133',
                                               'FareClass': 'LT',
                                               'OperatingCarrier': ''
                                           },
                                           'AirlinePNR': '',
                                           'AccumulatedDuration': 300,
                                           'Origin': {
                                               'AirportCode': 'COK',
                                               'AirportName': 'Cochin Internation Arpt',
                                               'Terminal': '',
                                               'CityCode': 'COK',
                                               'CityName': 'Kochi',
                                               'CountryCode': 'IN',
                                               'CountryName': 'India'
                                           },
                                           'Destination': {
                                               'AirportCode': 'BLR',
                                               'AirportName': 'Bengaluru Intl Arpt',
                                               'Terminal': '',
                                               "CityCode": 'BLR',
                                               'CityName': 'Bengaluru',
                                               'CountryCode': 'IN',
                                               'CountryName': 'India'
                                           },
                                           'Duration': 60,
                                           'GroundTime': '',
                                           'Mile': '',
                                           'StopOver': '',
                                           'StopPoint': '',
                                           'StopPointArrivalTime': '',
                                           'StopPointDepartureTime': '',
                                           'Craft': '',
                                           'Remark': '',
                                           'IsETicketEligible': '',
                                           'FlightStatus': '',
                                           'Status': ''
                                       }
                                   ],
                                   'FareRules': [
                                       {
                                           'Origin': '',
                                           'Destination': '',
                                           'Airline': '',
                                           'FareBasisCode': '',
                                           'FareRuleDetail': '',
                                           'FareRestriction': ''
                                       }
                                   ],
                                   'InvoiceNo': '',
                                   'InvoiceStatus': '',
                                   'InvoiceCreatedOn': '',
                                   'Remarks': '',
                                   'PartialSegmentCancellation': 'Not Allowed'
                               }
                           }
                           }


def flight_invoiceMD(data):
    try:
        destination_airport_1st_segment = data['Response'][
            'FlightItinerary']['Segments'][0]['Destination']['AirportName']
    except:
        destination_airport_1st_segment = data['Response'][
            'FlightItinerary']['Segments'][1]['Destination']['AirportName']

    passenger_name = data['Response']['FlightItinerary']['Passenger'][0]['Title'] + ' ' + \
        data['Response']['FlightItinerary']['Passenger'][0]['FirstName'] + \
        ' ' + \
        data['Response']['FlightItinerary']['Passenger'][0]['LastName']
    markdown_template = f"""
# Flight Booking Invoice

**PNR:** {data['Response']['PNR']}  
**Booking ID:** {data['Response']['BookingId']}  

---

## Flight Details

**Airline:** {data['Response']['FlightItinerary']['Segments'][0]['Airline']['AirlineName']}  

**Flight Number (1st Segment):** {data['Response'][
    'FlightItinerary']['Segments'][0]['Airline']['FlightNumber']}  
- **Departure Airport:** {data['Response'][
    'FlightItinerary']['Segments'][0]['Origin']['AirportName']}  
- **Destination Airport:** {destination_airport_1st_segment}  
- **Departure Time (1st Segment):** {data['Response']['FlightItinerary']['Segments'][0]['DepTime']}  
- **Arrival Time (1st Segment):** {data['Response']['FlightItinerary']['Segments'][0]['ArrTime']}  

**Flight Number (2nd Segment):** {data['Response'][
    'FlightItinerary']['Segments'][1]['Airline']['FlightNumber']}  
- **Departure Airport:** {data['Response'][
    'FlightItinerary']['Segments'][1]['Origin']['AirportName']}  
- **Destination Airport:** {data['Response'][
    'FlightItinerary']['Segments'][1]['Destination']['AirportName']}  
- **Departure Time (2nd Segment):** {data['Response']['FlightItinerary']['Segments'][1]['DepTime']}  
-  **Arrival Time (2nd Segment):** {data['Response']['FlightItinerary']['Segments'][1]['ArrTime']}  

---

## Passenger Details

- **Name:** {passenger_name}
- **Contact No:** {data['Response']['FlightItinerary']['Passenger'][0]['ContactNo']}
- **Email:** {data['Response']['FlightItinerary']['Passenger'][0]['Email']}

---

## Fare Details

**Currency:** {data['Response']['FlightItinerary']['Fare']['Currency']}  
**Base Fare:** {data['Response']['FlightItinerary']['Fare']['BaseFare']}  
**Tax:** {data['Response']['FlightItinerary']['Fare']['Tax']}  
**Total Fare:** {data['Response']['FlightItinerary']['Fare']['PublishedFare']}  

---

## Additional Information

- **Cabin Baggage Allowance:** {data['Response']['FlightItinerary']['Segments'][0]['CabinBaggage']} (Per Segment)

---

## Important Notes

- **Ticket Status:** {data['Response']['TicketStatus']}
- **Ticket Type:** Electronic Ticket (E-Ticket)
- **Cancellation Charges:** {data['Response']['FlightItinerary']['CancellationCharges']} (As per provided information)

---

*Note: This invoice is based on the information available at the time of booking. Any changes or updates should be verified with the airline.*
"""

    return markdown_template


def bus_markdown(json_data):
    invoice = ""
    invoice = f"Booking ID: {json_data['metadata']['orderId']}\n"
    invoice += f"Customer Name: {json_data['metadata']['name']}\n"
    invoice += f"Contact: {json_data['metadata']['contact']}\n"
    invoice += f"Email: {json_data['metadata']['email']}\n"
    invoice += f"Total Amount: {json_data['metadata']['amount']} {json_data['metadata']['currency']}\n"
    invoice += "Bus Details:\n"
    invoice += f"- Travel Name: {json_data['Booking']['block']['Result']['TravelName']}\n"
    invoice += f"- Bus Type: {json_data['Booking']['block']['Result']['BusType']}\n"
    invoice += "Passengers:\n"
    for passenger in json_data['Booking']['block']['Result']['Passenger']:
        invoice += f"- {passenger['FirstName']} ({passenger['Title']}) - Age: {passenger['Age']}, Gender: {passenger['Gender']}, Seat: {passenger['Seat']['SeatName']}\n"

    return invoice


def hotel_markdown(json_data):
    invoice = ""
    invoice += "# Booking Details:\n"
    invoice = f" ## Booking ID: {json_data['Booking']['book']['BookResult']['BookingId']}\n"
    invoice = f" ## Invoice Number: {json_data['Booking']['book']['BookResult']['InvoiceNumber']}\n"
    invoice = f" ## Booking Reference Number: {json_data['Booking']['book']['BookResult']['BookingRefNo']}\n"
    invoice = f" ## Hotel Booking Status: {json_data['Booking']['book']['BookResult']['HotelBookingStatus']}\n"
    invoice += "\n"
    invoice += f"Customer Name: {json_data['metadata']['name']}\n"
    invoice += f"Contact: {json_data['metadata']['contact']}\n"
    invoice += f"Email: {json_data['metadata']['email']}\n"
    invoice += f"Total Amount: {json_data['metadata']['amount']} {json_data['metadata']['currency']}\n"
    invoice += "\n"
    invoice += "\n"
    invoice += "# Hotel Details:\n"
    invoice += f"- Hotel Name: {json_data['Booking']['block']['BlockRoomResult']['HotelName']}\n"
    invoice += f"- Hotel Address line 1: {json_data['Booking']['block']['BlockRoomResult']['AddressLine1']}\n"
    invoice += f"- Hotel Address line 2: {json_data['Booking']['block']['BlockRoomResult']['AddressLine2']}\n"
    invoice += "\n"
    invoice += "Room Details:\n"
    for passenger in json_data['Booking']['block']['BlockRoomResult']['HotelRoomsDetails']:
        invoice += f"   - Name - {passenger['RoomTypeName']}, Code - ({passenger['RoomTypeCode']}) - Id: {str(passenger['RoomId'])}\n"
        try:
            invoice += f"   - Cancellation Policy:\n    {passenger['CancellationPolicies']['CancellationPolicy']}\n"
        except:
            pass
    print(invoice)
    return invoice


def get_pdf(markdown_content="# Heading 1"):
    import requests

    url = "https://md-to-pdf.fly.dev"

    params = {
        "css": "",
        # Optional PDF conversion engine (weasyprint, wkhtmltopdf, pdflatex)
        "engine": "weasyprint"
    }

    response = requests.post(
        url, data={"markdown": markdown_content}, params=params)

    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}\n{response.text}")


def get_pdf_saving(markdown_content="# Heading 1", name="generatedPdf"):
    url = "https://md-to-pdf.fly.dev"
    params = {
        "css": "",
        # Optional PDF conversion engine (weasyprint, wkhtmltopdf, pdflatex)
        "engine": "weasyprint"
    }
    response = requests.post(
        url, data={"markdown": markdown_content}, params=params)
    if response.status_code == 200:
        with open(name+'.pdf', "wb") as f:
            f.write(response.content)
        print('PDF saved as "'+name+'.pdf"')
    else:
        print(f"Error: {response.status_code}\n{response.text}")


# get_pdf_saving(flight_invoiceMD(
#     flight_booking_response), name="flight_Invoice")

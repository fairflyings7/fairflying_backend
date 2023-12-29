from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST'])
def health():

    res = request.get_json()

@app.route('/search_flights', methods=['POST'])
def search_fn():
    res = request.get_json()
    print(res['data'])
    # data = {   
    # "AdultCount":"1",
    # "ChildCount":"0",
    # "InfantCount":"0",
    # "JourneyType":"1",
    # "Segments":[  
    #     {  
    #         "Origin":"DEL",
    #         "Destination":"BOM",
    #         "FlightCabinClass":"1",
    #         "PreferredDepartureTime":"2023-06-26T00:00:00",
    #         "PreferredArrivalTime":"2023-06-26T00:00:00"
    #     }
    #     ]
    # }
    import json
    with open("Flight_API/Search_Response.json", 'r') as file:
        json_data = json.load(file)
    return jsonify(json_data),200

@app.route('/book_flight', methods=['POST'])
def booking_function():
    res = request.get_json()
    user_res = {
        "Title":res["Title"],
        "FirstName":res["FirstName"],
        "LastName":res["LastName"],
        "PaxType":res["PaxType"],
        "DateOfBirth":res["DateOfBirth"],
        "Gender":res["Gender"],
        "PassportNo":res["PassportNo"], 
        "PassportExpiry":res["PassportExpiry"],
        "AddressLine1":res["AddressLine1"],
        "City":res["City"],
        "CountryCode":res["CountryCode"],
        "CountryName":res["CountryCode"],
        "ContactNo":res["ContactNo"],
        "Email":res["Email"],
        "IsLeadPax":res["IsLeadPax"],
    }
    return jsonify({}),200

@app.route('/check_balace', methods=['POST'])
def balance_check():
    res = request.get_json()
    
    return jsonify({}),200

@app.route('/fair_quote', methods=['POST'])
def fair_quote_check():
    res = request.get_json()
    
    return jsonify({}),200

@app.route('/cancellation', methods=['POST'])
def cancellation():
    res = request.get_json()
    
    return jsonify({}),200

@app.route('/ex', methods=['POST'])
def extra():
    res = request.get_json()
    
    return jsonify({}),200

if __name__ == '__main__':
    app.run(debug=True)

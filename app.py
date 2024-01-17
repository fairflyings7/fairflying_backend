from flask import Flask, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/')
def health():
    return "hi",200

@app.route('/search_flights', methods=['POST'])
def search_fn():
    req = request.get_json()
    # data = {   
    # "AdultCount":"1",
    # "ChildCount":"0",
    # "InfantCount":"0",
    # "JourneyType":"1",
    # "Segments":[  
    #      {  
    #         "Origin":"DEL",
    #         "Destination":"BOM",
    #         "FlightCabinClass":"1",
    #         "PreferredDepartureTime":"2023-06-26T00:00:00",
    #         "PreferredArrivalTime":"2023-06-26T00:00:00"
    #      }
    #   ]
    # }
    # import json
    # with open("Flight_API/Search_Response.json", 'r') as file:
    #     res = json.load(file)
    from api_func import Flight_search
    res = Flight_search(req['data']) 
    return jsonify(res),200

@app.route('/book_flight', methods=['POST'])
def booking_function():
    res = request.get_json()
    data = res['data']
    # print(data)
    # print(type(data))
    # user_res = {
    #     "Title":res["Title"],
    #     "FirstName":res["FirstName"],
    #     "LastName":res["LastName"],
    #     "PaxType":res["PaxType"],
    #     "DateOfBirth":res["DateOfBirth"],
    #     "Gender":res["Gender"],
    #     "PassportNo":res["PassportNo"], 
    #     "PassportExpiry":res["PassportExpiry"],
    #     "AddressLine1":res["AddressLine1"],
    #     "City":res["City"],
    #     "CountryCode":res["CountryCode"],
    #     "CountryName":res["CountryCode"],
    #     "ContactNo":res["ContactNo"],
    #     "Email":res["Email"],
    #     "IsLeadPax":res["IsLeadPax"],
    # }

    from api_func import LLC_ticket_Req
    res = LLC_ticket_Req(data)
    return jsonify(res),200

@app.route('/create_payment_request', methods=['POST'])
def create_payment_request():
    res = request.get_json()
    
    return jsonify({"resp":{"link":"https://google.com"}}),200
@app.route('/check_payment_status', methods=['POST'])
def check_payment_status():
    res = request.get_json()
    
    return jsonify(True),200

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

import razorpay
# Replace with your Razorpay API keys
# razorpay_client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY_ID", "YOUR_RAZORPAY_KEY_SECRET"))

# @app.route("/create-order", methods=["POST"])
# def create_order():
#     amount = int(float(request.json["amount"]) * 100)  # Convert to paise
#     order = razorpay_client.order.create({
#         "amount": amount,
#         "currency": "INR",
#         "receipt": "order_receipt_123",  # Replace with your unique identifier
#     })
#     return jsonify({"order_id": order["id"], "order_amount": order["amount"]})

# @app.route("/verify-payment", methods=["POST"])
# def verify_payment():
#     data = request.json
#     try:
#         razorpay_client.utility.verify_payment_signature(data)
#         # Payment successful, handle order fulfillment here
#         return jsonify({"status": "success"})
#     except:
#         # Payment verification failed
#         return jsonify({"status": "failure"}), 400

if __name__ == '__main__':
    app.run(debug=True)

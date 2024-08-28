
from flask import Flask, jsonify, request, redirect, send_file
from flask_cors import CORS
from flask_mail import Mail, Message

import razorpay

import io
import os
import json

from Functions import Hotels, Bus, flight, firebase, get_ip_address
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


@app.route('/get-device-ip')
def ipGetter():
    ip = get_ip_address()["ip"]
    return jsonify({"ip": ip}), 200


@app.route('/editData', methods=['POST'])
def editData():
    auth_header = request.headers.get('Authorization')
    print("Authorization Header:", auth_header)
    if not FIREBASE.check_user_exists(auth_header):
        return jsonify({"status": "fail", "Description": "user doesnt exist"}), 200

    data = request.get_json()
    # prev_data = FIREBASE.read_from_firestore(auth_header)
    # if (data["Creating"] == True):
    #     data["Creating"] = False
    # else:
    #     try:
    #         a = data["Name"]
    #     except:
    #         print("data got reset")
    #         return jsonify({"status": False, "desc": "data got reset"}), 400
    res = FIREBASE.write_to_firestore(auth_header, {"data": json.dumps(data)})
    if res:
        return jsonify({"status": res}), 200
    else:
        return jsonify({"status": res}), 501


@app.route('/get_user', methods=['GET'])
def get_items():
    auth_header = request.headers.get('Authorization')
    if not FIREBASE.check_user_exists(auth_header):
        return jsonify({"status": "fail", "Description": "user doesnt exist"}), 200
    res = FIREBASE.read_from_firestore(custom_id=auth_header)
    if res:
        try:
            if res["data"]:
                res = json.loads(res["data"])
        except:
            pass
    return jsonify(res), 200


@app.route('/check_flight_balace', methods=['GET'])
def flight_balance_check():
    res = FLIGHT.balance_check()
    return jsonify(res), 200


@app.route('/search_flights', methods=['POST'])
def search_flights():
    req = request.get_json()
    res = FLIGHT.Flight_search(req['data'])
    return jsonify(res), 200


@app.route('/fare-calander', methods=['POST'])
def flight_fair_Cal():
    req = request.get_json()
    res = FLIGHT.calandar_Fare(req['data'])
    return jsonify(res), 200


@app.route('/get-flight-details', methods=['POST'])
def flight_ssr():
    req = request.get_json()
    quote = FLIGHT.fare_quote(req['data'])
    Rule = FLIGHT.fare_rule(req['data'])
    ssr = FLIGHT.SSR(req['data'])
    seatMapDev = FLIGHT.SeatMap(req['data'])

    return jsonify({"rules": Rule, "quote": quote, "ssr": ssr, "seatMap": seatMapDev}), 200


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
    # print("Req", req, "\n")
    # print("Res", res, "\n")
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


@app.route('/busbooking', methods=['POST'])
def busbooking():
    req = request.get_json()
    block = BUS.BlockBus(req['data'])
    book = BUS.Bus_Booking_Req(req['data'])
    return jsonify({"blockResponse": block, "bookResponse": book}), 200


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
    import json
    # print("req")
    # print(json.dumps(body, indent=4))
    # print("res")

    # print(json.dumps(body, indent=4))
    FIREBASE.write_to_firestore(
        id=razorpay_order["id"], data={"unparsed_Data": json.dumps(body)}, collection="payments")

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

        print(response)

        print("Callback hit")

        print(data)
        # if we get here True signature
        if data:
            print(data)
            try:
                payment_object = FIREBASE.read_from_firestore(
                    custom_id=response['razorpay_order_id'], collection="payments")
            except:
                payment_object = json.loads(FIREBASE.read_from_firestore(
                    custom_id=response['razorpay_order_id'], collection="payments"))
            payment_object = json.loads(payment_object['unparsed_Data'])
            print(payment_object)
            data = payment_object['data']
            uid = payment_object['uid']
            # print(json.dumps(data, indent=4))
            if payment_object["type"] == "flight":
                res = FLIGHT.LLC_ticket_Req(data)
            # if payment_object["type"] == "flight_return":
            elif payment_object["type"] == "hotel":
                block = Hotels.BlockRoom(data)
                book = Hotels.BookRoom(data)
                res = {"block": block, "book": book}
            elif payment_object["type"] == "bus":
                block = BUS.BlockBus(data)
                book = BUS.Bus_Booking_Req(data)
                res = {
                    "block": block,
                    "book": book
                }
            elif payment_object["type"] == "flight_return":
                res1 = FLIGHT.LLC_ticket_Req(data[0])
                res2 = FLIGHT.LLC_ticket_Req(data[1])
                res = {"flight_1": res1, "flight_2": res2}
            else:
                res = {"status": "None", "Desc": "type not selected"}

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
            print("BOOKING SUCCESSS LOGS ================== ")
            print(json.dumps(payment_object, indent=4))

            FIREBASE.write_to_firestore(
                id=response["razorpay_order_id"], data={"data": json.dumps(payment_object)}, collection="payments")

            try:
                data2 = FIREBASE.read_from_firestore(
                    custom_id=uid, collection="user_data")
                try:
                    data2["payments"].append(payment_object)
                except Exception as e:
                    print(e)
                    data2["payments"] = [payment_object]
                FIREBASE.write_to_firestore(
                    id=uid, data={"data": json.dumps(data2)}, collection="user_data")
            except Exception as e:
                print(e)
                FIREBASE.write_to_firestore(
                    id=uid, data={"data": json.dumps(payment_object)}, collection="user_data")

            mail_body = 'Your order by Fairflyings has been placed successfully. please use the visit ' + \
                os.getenv("WEB_URL")+'/booking-success?order_id=' + \
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
        # print(json.dumps(error_metadata, indent=4))
        payment_object = json.loads(FIREBASE.read_from_firestore(
            custom_id=response['order_id'], collection="payments")['data'])
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
            id=error_metadata['order_id'], data={"data": json.dumps(payment_object)}, collection="payments")

        send_email(email=payment_object["metadata"]["email"], subject="Order Failed",
                   body="your recent order failed, if payment deducted please refer to order id sent to you for refund")
        return redirect(os.getenv("WEB_URL")+"/failure?order_id=" + error_metadata['order_id'])


@app.route('/get-order-info', methods=['POST'])
def get_order_info():
    res = request.get_json()
    order_id = res['orderId']
    # print(order_id)
    try:
        payment_object = json.loads(FIREBASE.read_from_firestore(
            custom_id=order_id, collection="payments")['data'])
    except:
        payment_object = FIREBASE.read_from_firestore(
            custom_id=order_id, collection="payments")

    payment_object = FIREBASE.read_from_firestore(
        custom_id=order_id, collection="payments")
    return jsonify(payment_object), 200


@app.route('/get_pdf', methods=['post'])
def get_pdf():
    data = request.get_json()
    orderId = data['orderId']
    from report import flight_invoiceMD, get_pdf, bus_markdown, hotel_markdown

    payment_object = json.loads(FIREBASE.read_from_firestore(
        custom_id=orderId, collection="payments")['data'])
    if payment_object['type'] == "flight":
        markdown = flight_invoiceMD(payment_object["Booking"])
    if payment_object['type'] == "hotel":
        markdown = hotel_markdown(payment_object)
    if payment_object['type'] == "bus":
        markdown = bus_markdown(payment_object)
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

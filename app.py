
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


@app.route('/fare-calander', methods=['POST'])
def flight_fair_Cal():
    req = request.get_json()
    res = FLIGHT.calandar_Fare(req['data'])
    return jsonify(res), 200


@app.route('/get-flight-details', methods=['POST'])
def flight_ssr():
    req = request.get_json()
    Rule = FLIGHT.fare_rule(req['data'])
    quote = FLIGHT.fare_quote(req['data'])
    ssr = FLIGHT.SSR(req['data'])
    seatMapDev = FLIGHT.SeatMap(req['data'])
    seatMap = flight_seat_layout()

    return jsonify({"rules":Rule,"quote":quote,"ssr":ssr,"seatMap":seatMap,"seatMapDev":seatMapDev}), 200


def flight_seat_layout():
    res = {"Error": {"ErrorCode": 0,"ErrorMessage": ""},"TraceId": "174278","SrdvType": "MixAPI","SrdvIndex": "2","ResultIndex": "5-5668111542_36DELAMD6E2501AMDBOM6E6794~36270019929212","Results": [{"FromAirportCode": "AMD","FromCity": "Ahmedabad","ToAirportCode": "BOM","ToCity": "Mumbai","AirlineName": "IndiGo","AirlineCode": "6E","AirlineNumber": "6794","TotalRow": 31,"TotalColumn": 7,"Seats": {"Row1": {"Column1": {"SeatNumber": "1A","IsBooked": True,"IsLegroom": True,"IsAisle": None,"Amount": 1500,"Code": "1ASeKey310"},"Column2": {"SeatNumber": "1B","IsBooked": False,"IsLegroom": True,"IsAisle": None,"Amount": 1200,"Code": "1BSeKey310"},"Column3": {"SeatNumber": "1C","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1500,"Code": "1CSeKey310"},"Column5": {"SeatNumber": "1D","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1500,"Code": "1DSeKey310"},"Column6": {"SeatNumber": "1E","IsBooked": False,"IsLegroom": True,"IsAisle": None,"Amount": 1200,"Code": "1ESeKey310"},"Column7": {"SeatNumber": "1F","IsBooked": False,"IsLegroom": True,"IsAisle": None,"Amount": 1500,"Code": "1FSeKey310"}},"Row2": {"Column1": {"SeatNumber": "2A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 400,"Code": "2ASeKey310"},"Column2": {"SeatNumber": "2B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 400,"Code": "2BSeKey310"},"Column3": {"SeatNumber": "2C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 400,"Code": "2CSeKey310"},"Column5": {"SeatNumber": "2D","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 400,"Code": "2DSeKey310"},"Column6": {"SeatNumber": "2E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 400,"Code": "2ESeKey310"},"Column7": {"SeatNumber": "2F","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 400,"Code": "2FSeKey310"}},"Row3": {"Column1": {"SeatNumber": "3A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 400,"Code": "3ASeKey310"},"Column2": {"SeatNumber": "3B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 400,"Code": "3BSeKey310"},"Column3": {"SeatNumber": "3C","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 400,"Code": "3CSeKey310"},"Column5": {"SeatNumber": "3D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 400,"Code": "3DSeKey310"},"Column6": {"SeatNumber": "3E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 400,"Code": "3ESeKey310"},"Column7": {"SeatNumber": "3F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 400,"Code": "3FSeKey310"}},"Row4": {"Column1": {"SeatNumber": "4A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "4ASeKey310"},"Column2": {"SeatNumber": "4B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "4BSeKey310"},"Column3": {"SeatNumber": "4C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "4CSeKey310"},"Column5": {"SeatNumber": "4D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "4DSeKey310"},"Column6": {"SeatNumber": "4E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "4ESeKey310"},"Column7": {"SeatNumber": "4F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "4FSeKey310"}},"Row5": {"Column1": {"SeatNumber": "5A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "5ASeKey310"},"Column2": {"SeatNumber": "5B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "5BSeKey310"},"Column3": {"SeatNumber": "5C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "5CSeKey310"},"Column5": {"SeatNumber": "5D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "5DSeKey310"},"Column6": {"SeatNumber": "5E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "5ESeKey310"},"Column7": {"SeatNumber": "5F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "5FSeKey310"}},"Row6": {"Column1": {"SeatNumber": "6A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "6ASeKey310"},"Column2": {"SeatNumber": "6B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "6BSeKey310"},"Column3": {"SeatNumber": "6C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "6CSeKey310"},"Column5": {"SeatNumber": "6D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "6DSeKey310"},"Column6": {"SeatNumber": "6E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "6ESeKey310"},"Column7": {"SeatNumber": "6F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "6FSeKey310"}},"Row7": {"Column1": {"SeatNumber": "7A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "7ASeKey310"},"Column2": {"SeatNumber": "7B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "7BSeKey310"},"Column3": {"SeatNumber": "7C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "7CSeKey310"},"Column5": {"SeatNumber": "7D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "7DSeKey310"},"Column6": {"SeatNumber": "7E","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "7ESeKey310"},"Column7": {"SeatNumber": "7F","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "7FSeKey310"}},"Row8": {"Column1": {"SeatNumber": "8A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "8ASeKey310"},"Column2": {"SeatNumber": "8B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "8BSeKey310"},"Column3": {"SeatNumber": "8C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "8CSeKey310"},"Column5": {"SeatNumber": "8D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "8DSeKey310"},"Column6": {"SeatNumber": "8E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "8ESeKey310"},"Column7": {"SeatNumber": "8F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "8FSeKey310"}},"Row9": {"Column1": {"SeatNumber": "9A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "9ASeKey310"},"Column2": {"SeatNumber": "9B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "9BSeKey310"},"Column3": {"SeatNumber": "9C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "9CSeKey310"},"Column5": {"SeatNumber": "9D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "9DSeKey310"},"Column6": {"SeatNumber": "9E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "9ESeKey310"},"Column7": {"SeatNumber": "9F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "9FSeKey310"}},"Row10": {"Column1": {"SeatNumber": "10A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "10ASeKey310"},"Column2": {"SeatNumber": "10B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "10BSeKey310"},"Column3": {"SeatNumber": "10C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "10CSeKey310"},"Column5": {"SeatNumber": "10D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 320,"Code": "10DSeKey310"},"Column6": {"SeatNumber": "10E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "10ESeKey310"},"Column7": {"SeatNumber": "10F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 320,"Code": "10FSeKey310"}},"Row11": {"Column1": {"SeatNumber": "11A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "11ASeKey310"},"Column2": {"SeatNumber": "11B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "11BSeKey310"},"Column3": {"SeatNumber": "11C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "11CSeKey310"},"Column5": {"SeatNumber": "11D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "11DSeKey310"},"Column6": {"SeatNumber": "11E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "11ESeKey310"},"Column7": {"SeatNumber": "11F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "11FSeKey310"}},"Row12": {"Column1": {"SeatNumber": "12A","IsBooked": False,"IsLegroom": True,"IsAisle": None,"Amount": 1200,"Code": "12ASeKey310"},"Column2": {"SeatNumber": "12B","IsBooked": False,"IsLegroom": True,"IsAisle": None,"Amount": 1200,"Code": "12BSeKey310"},"Column3": {"SeatNumber": "12C","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1200,"Code": "12CSeKey310"},"Column5": {"SeatNumber": "12D","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1200,"Code": "12DSeKey310"},"Column6": {"SeatNumber": "12E","IsBooked": False,"IsLegroom": True,"IsAisle": None,"Amount": 1200,"Code": "12ESeKey310"},"Column7": {"SeatNumber": "12F","IsBooked": False,"IsLegroom": True,"IsAisle": None,"Amount": 1200,"Code": "12FSeKey310"}},"Row13": {"Column1": {"SeatNumber": "13A","IsBooked": False,"IsLegroom": True,"IsAisle": None,"Amount": 1200,"Code": "13ASeKey310"},"Column2": {"SeatNumber": "13B","IsBooked": False,"IsLegroom": True,"IsAisle": None,"Amount": 1200,"Code": "13BSeKey310"},"Column3": {"SeatNumber": "13C","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1200,"Code": "13CSeKey310"},"Column5": {"SeatNumber": "13D","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1200,"Code": "13DSeKey310"},"Column6": {"SeatNumber": "13E","IsBooked": False,"IsLegroom": True,"IsAisle": None,"Amount": 1200,"Code": "13ESeKey310"},"Column7": {"SeatNumber": "13F","IsBooked": False,"IsLegroom": True,"IsAisle": None,"Amount": 1200,"Code": "13FSeKey310"}},"Row14": {"Column1": {"SeatNumber": "14A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "14ASeKey310"},"Column2": {"SeatNumber": "14B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "14BSeKey310"},"Column3": {"SeatNumber": "14C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "14CSeKey310"},"Column5": {"SeatNumber": "14D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "14DSeKey310"},"Column6": {"SeatNumber": "14E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "14ESeKey310"},"Column7": {"SeatNumber": "14F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "14FSeKey310"}},"Row15": {"Column1": {"SeatNumber": "15A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "15ASeKey310"},"Column2": {"SeatNumber": "15B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "15BSeKey310"},"Column3": {"SeatNumber": "15C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "15CSeKey310"},"Column5": {"SeatNumber": "15D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "15DSeKey310"},"Column6": {"SeatNumber": "15E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "15ESeKey310"},"Column7": {"SeatNumber": "15F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "15FSeKey310"}},"Row16": {"Column1": {"SeatNumber": "16A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "16ASeKey310"},"Column2": {"SeatNumber": "16B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "16BSeKey310"},"Column3": {"SeatNumber": "16C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "16CSeKey310"},"Column5": {"SeatNumber": "16D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "16DSeKey310"},"Column6": {"SeatNumber": "16E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "16ESeKey310"},"Column7": {"SeatNumber": "16F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "16FSeKey310"}},"Row17": {"Column1": {"SeatNumber": "17A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "17ASeKey310"},"Column2": {"SeatNumber": "17B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "17BSeKey310"},"Column3": {"SeatNumber": "17C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "17CSeKey310"},"Column5": {"SeatNumber": "17D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "17DSeKey310"},"Column6": {"SeatNumber": "17E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "17ESeKey310"},"Column7": {"SeatNumber": "17F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "17FSeKey310"}},"Row18": {"Column1": {"SeatNumber": "18A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "18ASeKey310"},"Column2": {"SeatNumber": "18B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "18BSeKey310"},"Column3": {"SeatNumber": "18C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "18CSeKey310"},"Column5": {"SeatNumber": "18D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "18DSeKey310"},"Column6": {"SeatNumber": "18E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "18ESeKey310"},"Column7": {"SeatNumber": "18F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "18FSeKey310"}},"Row19": {"Column1": {"SeatNumber": "19A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "19ASeKey310"},"Column2": {"SeatNumber": "19B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "19BSeKey310"},"Column3": {"SeatNumber": "19C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "19CSeKey310"},"Column5": {"SeatNumber": "19D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "19DSeKey310"},"Column6": {"SeatNumber": "19E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "19ESeKey310"},"Column7": {"SeatNumber": "19F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "19FSeKey310"}},"Row20": {"Column1": {"SeatNumber": "20A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "20ASeKey310"},"Column2": {"SeatNumber": "20B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "20BSeKey310"},"Column3": {"SeatNumber": "20C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "20CSeKey310"},"Column5": {"SeatNumber": "20D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "20DSeKey310"},"Column6": {"SeatNumber": "20E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "20ESeKey310"},"Column7": {"SeatNumber": "20F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 250,"Code": "20FSeKey310"}},"Row21": {"Column1": {"SeatNumber": "21A","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "21ASeKey310"},"Column2": {"SeatNumber": "21B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "21BSeKey310"},"Column3": {"SeatNumber": "21C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "21CSeKey310"},"Column5": {"SeatNumber": "21D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "21DSeKey310"},"Column6": {"SeatNumber": "21E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "21ESeKey310"},"Column7": {"SeatNumber": "21F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "21FSeKey310"}},"Row22": {"Column1": {"SeatNumber": "22A","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "22ASeKey310"},"Column2": {"SeatNumber": "22B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "22BSeKey310"},"Column3": {"SeatNumber": "22C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "22CSeKey310"},"Column5": {"SeatNumber": "22D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "22DSeKey310"},"Column6": {"SeatNumber": "22E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "22ESeKey310"},"Column7": {"SeatNumber": "22F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "22FSeKey310"}},"Row23": {"Column1": {"SeatNumber": "23A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "23ASeKey310"},"Column2": {"SeatNumber": "23B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "23BSeKey310"},"Column3": {"SeatNumber": "23C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "23CSeKey310"},"Column5": {"SeatNumber": "23D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "23DSeKey310"},"Column6": {"SeatNumber": "23E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "23ESeKey310"},"Column7": {"SeatNumber": "23F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "23FSeKey310"}},"Row24": {"Column1": {"SeatNumber": "24A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "24ASeKey310"},"Column2": {"SeatNumber": "24B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "24BSeKey310"},"Column3": {"SeatNumber": "24C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "24CSeKey310"},"Column5": {"SeatNumber": "24D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "24DSeKey310"},"Column6": {"SeatNumber": "24E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "24ESeKey310"},"Column7": {"SeatNumber": "24F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "24FSeKey310"}},"Row25": {"Column1": {"SeatNumber": "25A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "25ASeKey310"},"Column2": {"SeatNumber": "25B","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "25BSeKey310"},"Column3": {"SeatNumber": "25C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "25CSeKey310"},"Column5": {"SeatNumber": "25D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "25DSeKey310"},"Column6": {"SeatNumber": "25E","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "25ESeKey310"},"Column7": {"SeatNumber": "25F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "25FSeKey310"}},"Row26": {"Column1": {"SeatNumber": "26A","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "26ASeKey310"},"Column2": {"SeatNumber": "26B","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "26BSeKey310"},"Column3": {"SeatNumber": "26C","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "26CSeKey310"},"Column5": {"SeatNumber": "26D","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "26DSeKey310"},"Column6": {"SeatNumber": "26E","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "26ESeKey310"},"Column7": {"SeatNumber": "26F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "26FSeKey310"}},"Row27": {"Column1": {"SeatNumber": "27A","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "27ASeKey310"},"Column2": {"SeatNumber": "27B","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "27BSeKey310"},"Column3": {"SeatNumber": "27C","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "27CSeKey310"},"Column5": {"SeatNumber": "27D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "27DSeKey310"},"Column6": {"SeatNumber": "27E","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "27ESeKey310"},"Column7": {"SeatNumber": "27F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "27FSeKey310"}},"Row28": {"Column1": {"SeatNumber": "28A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "28ASeKey310"},"Column2": {"SeatNumber": "28B","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "28BSeKey310"},"Column3": {"SeatNumber": "28C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "28CSeKey310"},"Column5": {"SeatNumber": "28D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "28DSeKey310"},"Column6": {"SeatNumber": "28E","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "28ESeKey310"},"Column7": {"SeatNumber": "28F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "28FSeKey310"}},"Row29": {"Column1": {"SeatNumber": "29A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "29ASeKey310"},"Column2": {"SeatNumber": "29B","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "29BSeKey310"},"Column3": {"SeatNumber": "29C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "29CSeKey310"},"Column5": {"SeatNumber": "29D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "29DSeKey310"},"Column6": {"SeatNumber": "29E","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "29ESeKey310"},"Column7": {"SeatNumber": "29F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "29FSeKey310"}},"Row30": {"Column1": {"SeatNumber": "30A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "30ASeKey310"},"Column2": {"SeatNumber": "30B","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "30BSeKey310"},"Column3": {"SeatNumber": "30C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "30CSeKey310"},"Column5": {"SeatNumber": "30D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "30DSeKey310"},"Column6": {"SeatNumber": "30E","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "30ESeKey310"},"Column7": {"SeatNumber": "30F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "30FSeKey310"}},"Row31": {"Column1": {"SeatNumber": "31A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "31ASeKey310"},"Column2": {"SeatNumber": "31B","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "31BSeKey310"},"Column3": {"SeatNumber": "31C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "31CSeKey310"},"Column5": {"SeatNumber": "31D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "31DSeKey310"},"Column6": {"SeatNumber": "31E","IsBooked": True,"IsLegroom": False,"IsAisle": None,"Amount": 0,"Code": "31ESeKey310"},"Column7": {"SeatNumber": "31F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "31FSeKey310"}}}},{"FromAirportCode": "DEL","FromCity": "Delhi","ToAirportCode": "AMD","ToCity": "Ahmedabad","AirlineName": "IndiGo","AirlineCode": "6E","AirlineNumber": "2501","TotalRow": 39,"TotalColumn": 7,"Seats": {"Row1": {"Column1": {"SeatNumber": "1A","IsBooked": True,"IsLegroom": True,"IsAisle": False,"Amount": 1500,"Code": "1ASeKey309"},"Column2": {"SeatNumber": "1B","IsBooked": False,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "1BSeKey309"},"Column3": {"SeatNumber": "1C","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1500,"Code": "1CSeKey309"},"Column5": {"SeatNumber": "1D","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1500,"Code": "1DSeKey309"},"Column6": {"SeatNumber": "1E","IsBooked": False,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "1ESeKey309"},"Column7": {"SeatNumber": "1F","IsBooked": False,"IsLegroom": True,"IsAisle": False,"Amount": 1500,"Code": "1FSeKey309"}},"Row2": {"Column1": {"SeatNumber": "2A","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 400,"Code": "2ASeKey309"},"Column2": {"SeatNumber": "2B","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 400,"Code": "2BSeKey309"},"Column3": {"SeatNumber": "2C","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 400,"Code": "2CSeKey309"},"Column5": {"SeatNumber": "2D","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 400,"Code": "2DSeKey309"},"Column6": {"SeatNumber": "2E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 400,"Code": "2ESeKey309"},"Column7": {"SeatNumber": "2F","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 400,"Code": "2FSeKey309"}},"Row3": {"Column1": {"SeatNumber": "3A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 400,"Code": "3ASeKey309"},"Column2": {"SeatNumber": "3B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 400,"Code": "3BSeKey309"},"Column3": {"SeatNumber": "3C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 400,"Code": "3CSeKey309"},"Column5": {"SeatNumber": "3D","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 400,"Code": "3DSeKey309"},"Column6": {"SeatNumber": "3E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 400,"Code": "3ESeKey309"},"Column7": {"SeatNumber": "3F","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 400,"Code": "3FSeKey309"}},"Row4": {"Column1": {"SeatNumber": "4A","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "4ASeKey309"},"Column2": {"SeatNumber": "4B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "4BSeKey309"},"Column3": {"SeatNumber": "4C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "4CSeKey309"},"Column5": {"SeatNumber": "4D","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "4DSeKey309"},"Column6": {"SeatNumber": "4E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "4ESeKey309"},"Column7": {"SeatNumber": "4F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "4FSeKey309"}},"Row5": {"Column1": {"SeatNumber": "5A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "5ASeKey309"},"Column2": {"SeatNumber": "5B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "5BSeKey309"},"Column3": {"SeatNumber": "5C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "5CSeKey309"},"Column5": {"SeatNumber": "5D","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "5DSeKey309"},"Column6": {"SeatNumber": "5E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "5ESeKey309"},"Column7": {"SeatNumber": "5F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "5FSeKey309"}},"Row6": {"Column1": {"SeatNumber": "6A","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "6ASeKey309"},"Column2": {"SeatNumber": "6B","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "6BSeKey309"},"Column3": {"SeatNumber": "6C","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "6CSeKey309"},"Column5": {"SeatNumber": "6D","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "6DSeKey309"},"Column6": {"SeatNumber": "6E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "6ESeKey309"},"Column7": {"SeatNumber": "6F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "6FSeKey309"}},"Row7": {"Column1": {"SeatNumber": "7A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "7ASeKey309"},"Column2": {"SeatNumber": "7B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "7BSeKey309"},"Column3": {"SeatNumber": "7C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "7CSeKey309"},"Column5": {"SeatNumber": "7D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "7DSeKey309"},"Column6": {"SeatNumber": "7E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "7ESeKey309"},"Column7": {"SeatNumber": "7F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "7FSeKey309"}},"Row8": {"Column1": {"SeatNumber": "8A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "8ASeKey309"},"Column2": {"SeatNumber": "8B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "8BSeKey309"},"Column3": {"SeatNumber": "8C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "8CSeKey309"},"Column5": {"SeatNumber": "8D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "8DSeKey309"},"Column6": {"SeatNumber": "8E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "8ESeKey309"},"Column7": {"SeatNumber": "8F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "8FSeKey309"}},"Row9": {"Column1": {"SeatNumber": "9A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "9ASeKey309"},"Column2": {"SeatNumber": "9B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "9BSeKey309"},"Column3": {"SeatNumber": "9C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "9CSeKey309"},"Column5": {"SeatNumber": "9D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "9DSeKey309"},"Column6": {"SeatNumber": "9E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "9ESeKey309"},"Column7": {"SeatNumber": "9F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "9FSeKey309"}},"Row10": {"Column1": {"SeatNumber": "10A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "10ASeKey309"},"Column2": {"SeatNumber": "10B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "10BSeKey309"},"Column3": {"SeatNumber": "10C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "10CSeKey309"},"Column5": {"SeatNumber": "10D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "10DSeKey309"},"Column6": {"SeatNumber": "10E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "10ESeKey309"},"Column7": {"SeatNumber": "10F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "10FSeKey309"}},"Row11": {"Column1": {"SeatNumber": "11A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "11ASeKey309"},"Column2": {"SeatNumber": "11B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "11BSeKey309"},"Column3": {"SeatNumber": "11C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "11CSeKey309"},"Column5": {"SeatNumber": "11D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "11DSeKey309"},"Column6": {"SeatNumber": "11E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "11ESeKey309"},"Column7": {"SeatNumber": "11F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "11FSeKey309"}},"Row12": {"Column1": {"SeatNumber": "12A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "12ASeKey309"},"Column2": {"SeatNumber": "12B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "12BSeKey309"},"Column3": {"SeatNumber": "12C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "12CSeKey309"},"Column5": {"SeatNumber": "12D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "12DSeKey309"},"Column6": {"SeatNumber": "12E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "12ESeKey309"},"Column7": {"SeatNumber": "12F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "12FSeKey309"}},"Row13": {"Column1": {"SeatNumber": "13A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "13ASeKey309"},"Column2": {"SeatNumber": "13B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "13BSeKey309"},"Column3": {"SeatNumber": "13C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "13CSeKey309"},"Column5": {"SeatNumber": "13D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "13DSeKey309"},"Column6": {"SeatNumber": "13E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "13ESeKey309"},"Column7": {"SeatNumber": "13F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "13FSeKey309"}},"Row14": {"Column1": {"SeatNumber": "14A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "14ASeKey309"},"Column2": {"SeatNumber": "14B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "14BSeKey309"},"Column3": {"SeatNumber": "14C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "14CSeKey309"},"Column5": {"SeatNumber": "14D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "14DSeKey309"},"Column6": {"SeatNumber": "14E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "14ESeKey309"},"Column7": {"SeatNumber": "14F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "14FSeKey309"}},"Row15": {"Column1": {"SeatNumber": "15A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "15ASeKey309"},"Column2": {"SeatNumber": "15B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "15BSeKey309"},"Column3": {"SeatNumber": "15C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "15CSeKey309"},"Column5": {"SeatNumber": "15D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "15DSeKey309"},"Column6": {"SeatNumber": "15E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "15ESeKey309"},"Column7": {"SeatNumber": "15F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "15FSeKey309"}},"Row16": {"Column1": {"SeatNumber": "16A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "16ASeKey309"},"Column2": {"SeatNumber": "16B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "16BSeKey309"},"Column3": {"SeatNumber": "16C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "16CSeKey309"},"Column5": {"SeatNumber": "16D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 350,"Code": "16DSeKey309"},"Column6": {"SeatNumber": "16E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "16ESeKey309"},"Column7": {"SeatNumber": "16F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 350,"Code": "16FSeKey309"}},"Row17": {"Column1": {"SeatNumber": "17A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "17ASeKey309"},"Column2": {"SeatNumber": "17B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "17BSeKey309"},"Column3": {"SeatNumber": "17C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "17CSeKey309"},"Column5": {"SeatNumber": "17D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "17DSeKey309"},"Column6": {"SeatNumber": "17E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "17ESeKey309"},"Column7": {"SeatNumber": "17F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "17FSeKey309"}},"Row18": {"Column1": {"SeatNumber": "18A","IsBooked": True,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "18ASeKey309"},"Column2": {"SeatNumber": "18B","IsBooked": True,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "18BSeKey309"},"Column3": {"SeatNumber": "18C","IsBooked": True,"IsLegroom": True,"IsAisle": True,"Amount": 1200,"Code": "18CSeKey309"},"Column5": {"SeatNumber": "18D","IsBooked": True,"IsLegroom": True,"IsAisle": True,"Amount": 1200,"Code": "18DSeKey309"},"Column6": {"SeatNumber": "18E","IsBooked": True,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "18ESeKey309"},"Column7": {"SeatNumber": "18F","IsBooked": True,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "18FSeKey309"}},"Row19": {"Column1": {"SeatNumber": "19A","IsBooked": False,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "19ASeKey309"},"Column2": {"SeatNumber": "19B","IsBooked": False,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "19BSeKey309"},"Column3": {"SeatNumber": "19C","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1200,"Code": "19CSeKey309"},"Column5": {"SeatNumber": "19D","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1200,"Code": "19DSeKey309"},"Column6": {"SeatNumber": "19E","IsBooked": False,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "19ESeKey309"},"Column7": {"SeatNumber": "19F","IsBooked": False,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "19FSeKey309"}},"Row20": {"Column1": {"SeatNumber": "20A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "20ASeKey309"},"Column2": {"SeatNumber": "20B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "20BSeKey309"},"Column3": {"SeatNumber": "20C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "20CSeKey309"},"Column5": {"SeatNumber": "20D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "20DSeKey309"},"Column6": {"SeatNumber": "20E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "20ESeKey309"},"Column7": {"SeatNumber": "20F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "20FSeKey309"}},"Row21": {"Column1": {"SeatNumber": "21A","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "21ASeKey309"},"Column2": {"SeatNumber": "21B","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "21BSeKey309"},"Column3": {"SeatNumber": "21C","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "21CSeKey309"},"Column5": {"SeatNumber": "21D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "21DSeKey309"},"Column6": {"SeatNumber": "21E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "21ESeKey309"},"Column7": {"SeatNumber": "21F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "21FSeKey309"}},"Row22": {"Column1": {"SeatNumber": "22A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "22ASeKey309"},"Column2": {"SeatNumber": "22B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "22BSeKey309"},"Column3": {"SeatNumber": "22C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "22CSeKey309"},"Column5": {"SeatNumber": "22D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "22DSeKey309"},"Column6": {"SeatNumber": "22E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "22ESeKey309"},"Column7": {"SeatNumber": "22F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "22FSeKey309"}},"Row23": {"Column1": {"SeatNumber": "23A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "23ASeKey309"},"Column2": {"SeatNumber": "23B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "23BSeKey309"},"Column3": {"SeatNumber": "23C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "23CSeKey309"},"Column5": {"SeatNumber": "23D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "23DSeKey309"},"Column6": {"SeatNumber": "23E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "23ESeKey309"},"Column7": {"SeatNumber": "23F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "23FSeKey309"}},"Row24": {"Column1": {"SeatNumber": "24A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "24ASeKey309"},"Column2": {"SeatNumber": "24B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "24BSeKey309"},"Column3": {"SeatNumber": "24C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "24CSeKey309"},"Column5": {"SeatNumber": "24D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "24DSeKey309"},"Column6": {"SeatNumber": "24E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "24ESeKey309"},"Column7": {"SeatNumber": "24F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "24FSeKey309"}},"Row25": {"Column1": {"SeatNumber": "25A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "25ASeKey309"},"Column2": {"SeatNumber": "25B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "25BSeKey309"},"Column3": {"SeatNumber": "25C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "25CSeKey309"},"Column5": {"SeatNumber": "25D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "25DSeKey309"},"Column6": {"SeatNumber": "25E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "25ESeKey309"},"Column7": {"SeatNumber": "25F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "25FSeKey309"}},"Row26": {"Column1": {"SeatNumber": "26A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "26ASeKey309"},"Column2": {"SeatNumber": "26B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "26BSeKey309"},"Column3": {"SeatNumber": "26C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "26CSeKey309"},"Column5": {"SeatNumber": "26D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "26DSeKey309"},"Column6": {"SeatNumber": "26E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "26ESeKey309"},"Column7": {"SeatNumber": "26F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "26FSeKey309"}},"Row27": {"Column1": {"SeatNumber": "27A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "27ASeKey309"},"Column2": {"SeatNumber": "27B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "27BSeKey309"},"Column3": {"SeatNumber": "27C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "27CSeKey309"},"Column5": {"SeatNumber": "27D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 250,"Code": "27DSeKey309"},"Column6": {"SeatNumber": "27E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "27ESeKey309"},"Column7": {"SeatNumber": "27F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 250,"Code": "27FSeKey309"}},"Row28": {"Column1": {"SeatNumber": "28A","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "28ASeKey310"},"Column2": {"SeatNumber": "28B","IsBooked": False,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "28BSeKey309"},"Column3": {"SeatNumber": "28C","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1200,"Code": "28CSeKey309"},"Column5": {"SeatNumber": "28D","IsBooked": False,"IsLegroom": True,"IsAisle": True,"Amount": 1200,"Code": "28DSeKey309"},"Column6": {"SeatNumber": "28E","IsBooked": False,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "28ESeKey309"},"Column7": {"SeatNumber": "28F","IsBooked": False,"IsLegroom": False,"IsAisle": None,"Amount": 150,"Code": "28FSeKey310"}},"Row29": {"Column1": {"SeatNumber": "29A","IsBooked": False,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "29ASeKey309"},"Column2": {"SeatNumber": "29B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "29BSeKey309"},"Column3": {"SeatNumber": "29C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "29CSeKey309"},"Column5": {"SeatNumber": "29D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "29DSeKey309"},"Column6": {"SeatNumber": "29E","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "29ESeKey309"},"Column7": {"SeatNumber": "29F","IsBooked": False,"IsLegroom": True,"IsAisle": False,"Amount": 1200,"Code": "29FSeKey309"}},"Row30": {"Column1": {"SeatNumber": "30A","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "30ASeKey309"},"Column2": {"SeatNumber": "30B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "30BSeKey309"},"Column3": {"SeatNumber": "30C","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "30CSeKey309"},"Column5": {"SeatNumber": "30D","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "30DSeKey309"},"Column6": {"SeatNumber": "30E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "30ESeKey309"},"Column7": {"SeatNumber": "30F","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "30FSeKey309"}},"Row31": {"Column1": {"SeatNumber": "31A","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "31ASeKey309"},"Column2": {"SeatNumber": "31B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "31BSeKey309"},"Column3": {"SeatNumber": "31C","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "31CSeKey309"},"Column5": {"SeatNumber": "31D","IsBooked": True,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "31DSeKey309"},"Column6": {"SeatNumber": "31E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "31ESeKey309"},"Column7": {"SeatNumber": "31F","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "31FSeKey309"}},"Row32": {"Column1": {"SeatNumber": "32A","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "32ASeKey309"},"Column2": {"SeatNumber": "32B","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "32BSeKey309"},"Column3": {"SeatNumber": "32C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "32CSeKey309"},"Column5": {"SeatNumber": "32D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "32DSeKey309"},"Column6": {"SeatNumber": "32E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "32ESeKey309"},"Column7": {"SeatNumber": "32F","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "32FSeKey309"}},"Row33": {"Column1": {"SeatNumber": "33A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "33ASeKey309"},"Column2": {"SeatNumber": "33B","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "33BSeKey309"},"Column3": {"SeatNumber": "33C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "33CSeKey309"},"Column5": {"SeatNumber": "33D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "33DSeKey309"},"Column6": {"SeatNumber": "33E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 99,"Code": "33ESeKey309"},"Column7": {"SeatNumber": "33F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "33FSeKey309"}},"Row34": {"Column1": {"SeatNumber": "34A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "34ASeKey309"},"Column2": {"SeatNumber": "34B","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "34BSeKey309"},"Column3": {"SeatNumber": "34C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "34CSeKey309"},"Column5": {"SeatNumber": "34D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "34DSeKey309"},"Column6": {"SeatNumber": "34E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "34ESeKey309"},"Column7": {"SeatNumber": "34F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "34FSeKey309"}},"Row35": {"Column1": {"SeatNumber": "35A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "35ASeKey309"},"Column2": {"SeatNumber": "35B","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "35BSeKey309"},"Column3": {"SeatNumber": "35C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "35CSeKey309"},"Column5": {"SeatNumber": "35D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "35DSeKey309"},"Column6": {"SeatNumber": "35E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "35ESeKey309"},"Column7": {"SeatNumber": "35F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "35FSeKey309"}},"Row36": {"Column1": {"SeatNumber": "36A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "36ASeKey309"},"Column2": {"SeatNumber": "36B","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "36BSeKey309"},"Column3": {"SeatNumber": "36C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "36CSeKey309"},"Column5": {"SeatNumber": "36D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "36DSeKey309"},"Column6": {"SeatNumber": "36E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "36ESeKey309"},"Column7": {"SeatNumber": "36F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "36FSeKey309"}},"Row37": {"Column1": {"SeatNumber": "37A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "37ASeKey309"},"Column2": {"SeatNumber": "37B","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "37BSeKey309"},"Column3": {"SeatNumber": "37C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "37CSeKey309"},"Column5": {"SeatNumber": "37D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "37DSeKey309"},"Column6": {"SeatNumber": "37E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "37ESeKey309"},"Column7": {"SeatNumber": "37F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "37FSeKey309"}},"Row38": {"Column1": {"SeatNumber": "38A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "38ASeKey309"},"Column2": {"SeatNumber": "38B","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "38BSeKey309"},"Column3": {"SeatNumber": "38C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "38CSeKey309"},"Column5": {"SeatNumber": "38D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "38DSeKey309"},"Column6": {"SeatNumber": "38E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "38ESeKey309"},"Column7": {"SeatNumber": "38F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "38FSeKey309"}},"Row39": {"Column1": {"SeatNumber": "39A","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "39ASeKey309"},"Column2": {"SeatNumber": "39B","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "39BSeKey309"},"Column3": {"SeatNumber": "39C","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "39CSeKey309"},"Column5": {"SeatNumber": "39D","IsBooked": False,"IsLegroom": False,"IsAisle": True,"Amount": 150,"Code": "39DSeKey309"},"Column6": {"SeatNumber": "39E","IsBooked": True,"IsLegroom": False,"IsAisle": False,"Amount": 0,"Code": "39ESeKey309"},"Column7": {"SeatNumber": "39F","IsBooked": False,"IsLegroom": False,"IsAisle": False,"Amount": 150,"Code": "39FSeKey309"}}}}]}
    return res


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
    # print(json.dumps(body, indent=4))
    FIREBASE.write_to_firestore(
        id=razorpay_order["id"], data={"data": json.dumps(body)}, collection="payments")

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
            payment_object = json.loads(FIREBASE.read_from_firestore(
                custom_id=response['razorpay_order_id'], collection="payments")['data'])
            data = payment_object['data']
            # print(json.dumps(data, indent=4))
            if payment_object["type"] == "flight":
                print(data)
                res = FLIGHT.LLC_ticket_Req(data)
                # res = {
                #     "Error":
                #     {
                #         "ErrorCode": "0",
                #         "ErrorMessage": ""
                #     },
                #     "TraceId": "174278",
                #     "ResponseStatus": "1",
                #     "SrdvType": "MixAPI",
                #     "Response": {
                #         "SrdvIndex": "2",
                #         "PNR": "TESTPNR",
                #         "BookingId": 2106,
                #         "SSRDenied": "",
                #         "SSRMessage": "",
                #         "Status": "1",
                #         "IsPriceChanged": False,
                #         "IsTimeChanged": False,
                #         "TicketStatus": "1",
                #         "FlightItinerary": {
                #             "BookingId": 2106,
                #             "IsManual": False,
                #             "PNR": "TESTPNR",
                #             "IsDomestic": "Not Set",
                #             "Source": "Publish",
                #             "Origin": "DEL",
                #             "Destination": "AMD",
                #             "AirlineCode": "6E",
                #             "LastTicketDate": "",
                #             "ValidatingAirlineCode": "",
                #             "AirlineRemark": [],
                #             "IsLCC": True,
                #             "NonRefundable": False,
                #             "FareType": "Publish",
                #             "CreditNoteNo": "",
                #             "Fare": {
                #                 "Currency": "INR",
                #                 "BaseFare": 3691,
                #                 "Tax": 1465,
                #                 "YQTax": 700,
                #                 "AdditionalTxnFeeOfrd": 0,
                #                 "AdditionalTxnFeePub": 0,
                #                 "PGCharge": 0,
                #                 "OtherCharges": 0,
                #                 "PublishedFare": 5156,
                #                 "OfferedFare": 5156,
                #                 "CommissionEarned": 0,
                #                 "TdsOnCommission": 0,
                #                 "ServiceFee": 0, "TotalBaggageCharges": 0,
                #                 "TotalMealCharges": 0,
                #                 "TotalSeatCharges": 0,
                #                 "TotalSpecialServiceCharges": 0
                #             }, "CreditNoteCreatedOn": "", "Passenger": [{"PaxId": "", "Title": "Mr", "FirstName": "First", "LastName": "Name", "PaxType": "1", "DateOfBirth": "", "Gender": "", "PassportNo": "", "AddressLine1": "", "City": "", "CountryCode": "", "CountryName": "", "Nationality": "", "ContactNo": "09870123654", "Email": "navneet@srdvtechnologies.com", "IsLeadPax": "", "FFAirlineCode": "", "FFNumber": "", "Fare": {"Currency": "", "BaseFare": "", "Tax": "", "YQTax": "", "AdditionalTxnFeeOfrd": "", "AdditionalTxnFeePub": "", "PGCharge": "", "OtherCharges": "", "PublishedFare": "", "OfferedFare": "", "ServiceFee": "", "TotalBaggageCharges": "", "TotalMealCharges": "", "TotalSeatCharges": "", "TotalSpecialServiceCharges": ""}, "Ticket": {"TicketId": "", "TicketNumber": "", "IssueDate": "", "ValidatingAirline": "", "Remarks": "", "ServiceFeeDisplayType": "", "Status": ""}, "SegmentAdditionalInfo": [{"FareBasis": "", "NVA": "", "NVB": "", "Baggage": "", "Meal": "", "Seat": "", "SpecialService": ""}]}], "CancellationCharges": "", "Segments": [

                #                 {"Baggage": "15 Kg (01 Piece only)", "CabinBaggage": "7 Kg", "TripIndicator": 1, "SegmentIndicator": 1, "DepTime": "2023-12-31T18:40", "ArrTime": "2023-12-31T20:05", "Airline": {"AirlineCode": "6E", "AirlineName": "IndiGo", "FlightNumber": "2501", "FareClass": "R", "OperatingCarrier": ""}, "AirlinePNR": "", "AccumulatedDuration": 245, "Origin": {"AirportCode": "DEL", "AirportName": "Delhi Indira Gandhi Intl", "Terminal": "Terminal 2", "CityCode": "DEL", "CityName": "Delhi", "CountryCode": "IN", "CountryName": "India"}, "Destination": {"AirportCode": "AMD", "AirportName": "Sardar Vallabh Bhai Patel Intl Arpt", "Terminal": "Terminal 1", "CityCode": "AMD", "CityName": "Ahmedabad", "CountryCode": "IN", "CountryName": "India"}, "Duration": 85, "GroundTime": 160, "Mile": "", "StopOver": "", "StopPoint": "", "StopPointArrivalTime": "", "StopPointDepartureTime": "", "Craft": "", "Remark": "", "IsETicketEligible": "", "FlightStatus": "", "Status": ""}, {"Baggage": "15 Kg (01 Piece only)", "CabinBaggage": "7 Kg", "TripIndicator": 1, "SegmentIndicator": 2, "DepTime": "2023-12-31T22:45", "ArrTime": "2024-01-01T00:10", "Airline": {"AirlineCode": "6E", "AirlineName": "IndiGo", "FlightNumber": "6794", "FareClass": "R", "OperatingCarrier": ""}, "AirlinePNR": "", "AccumulatedDuration": 330, "Origin": {"AirportCode": "AMD", "AirportName": "Sardar Vallabh Bhai Patel Intl Arpt", "Terminal": "Terminal 1", "CityCode": "AMD", "CityName": "Ahmedabad", "CountryCode": "IN", "CountryName": "India"}, "Destination": {"AirportCode": "BOM", "AirportName": "Chhatrapati Shivaji", "Terminal": "Terminal 2", "CityCode": "BOM", "CityName": "Mumbai", "CountryCode": "IN", "CountryName": "India"}, "Duration": 85, "GroundTime": "", "Mile": "", "StopOver": "", "StopPoint": "", "StopPointArrivalTime": "", "StopPointDepartureTime": "", "Craft": "", "Remark": "", "IsETicketEligible": "", "FlightStatus": "", "Status": ""}], "FareRules": [{"Origin": "", "Destination": "", "Airline": "", "FareBasisCode": "", "FareRuleDetail": "", "FareRestriction": ""}], "InvoiceNo": "", "InvoiceStatus": "", "InvoiceCreatedOn": "", "Remarks": "", "PartialSegmentCancellation": "Not Allowed"}}}
            elif payment_object["type"] == "hotel":
                block = Hotels.BlockRoom(data)
                book = Hotels.BookRoom(data)
                res = {"block": block, "book": book}
                # res = {
                #     "block": {
                #         "BlockRoomResult": {
                #             "Error": {
                #                 "ErrorCode": 0,
                #                 "ErrorMessage": ""
                #             },
                #             "AvailabilityType": "Confirm",
                #             "TraceId": "1",
                #             "ResponseStatus": 1,
                #             "GSTAllowed": False,
                #             "IsPackageDetailsMandatory": False,
                #             "IsPackageFare": False,
                #             "IsPriceChanged": False,
                #             "IsCancellationPolicyChanged": False,
                #             "IsHotelPolicyChanged": True,
                #             "HotelNorms": "india - land of mystries \"//\" \"  /// \"  |<ul><li>Check-in hour 14:00 - .  Valid From 2020-04-30 through 2020-05-01Identification card at arrival.  Valid From 2020-04-30 through 2020-05-01Minimum check-in age 18.  Valid From 2020-04-30 through 2020-05-01Car park YES (without additional debit notes).  Valid From 2020-04-30 through 2020-05-01</li><li>Amendments cannot be made against this booking once your booking has been requested.</li></ul>",
                #             "HotelName": "Avtar",
                #             "AddressLine1": "Road Pahar Ganj, 3425 DB Gupta Rd, Arya  110015 DELHI India",
                #             "AddressLine2": "\n Phone No: 911123580007\n Fax : 911123587103",
                #             "StarRating": 2,
                #             "HotelPolicyDetail": "india - land of mystries \"//\" \"  /// \"  |<ul><li>Check-in hour 14:00 - .  Valid From 2020-04-30 through 2020-05-01Identification card at arrival.  Valid From 2020-04-30 through 2020-05-01Minimum check-in age 18.  Valid From 2020-04-30 through 2020-05-01Car park YES (without additional debit notes).  Valid From 2020-04-30 through 2020-05-01</li><li>Amendments cannot be made against this booking once your booking has been requested.</li></ul>",
                #             "Latitude": "28.6443589",
                #             "Longitude": "77.2128331",
                #             "BookingAllowedForRoamer": False,
                #             "HotelRoomsDetails": [
                #                 {
                #                     "ChildCount": 0,
                #                     "RequireAllPaxDetails": True,
                #                     "RoomId": 0,
                #                     "RoomStatus": 0,
                #                     "RoomIndex": 1,
                #                     "RoomTypeCode": "007:92G:228:SGLyDXzGRvALLvROzROz:N:828857$#$1",
                #                     "RoomTypeName": "SINGLE DELUXE",
                #                     "RatePlanCode": "007:92G:228:SGLyDXzGRvALLvROzROz:N:828857|1",
                #                     "RatePlan": 0,
                #                     "InfoSource": "OpenCombination",
                #                     "SequenceNo": "1",
                #                     "DayRates": [
                #                         {
                #                             "Amount": 1658.17,
                #                             "Date": "2020-04-30T00:00:00"
                #                         }
                #                     ],
                #                     "SupplierPrice": None,
                #                     "Price": {
                #                         "CurrencyCode": "INR",
                #                         "RoomPrice": 1658.17,
                #                         "Tax": 0,
                #                         "ExtraGuestCharge": 0,
                #                         "ChildCharge": 0,
                #                         "OtherCharges": 248.5,
                #                         "Discount": 0,
                #                         "PublishedPrice": 1906.67,
                #                         "PublishedPriceRoundedOff": 1907,
                #                         "OfferedPrice": 1906.67,
                #                         "OfferedPriceRoundedOff": 1907,
                #                         "AgentCommission": 0,
                #                         "AgentMarkUp": 0,
                #                         "ServiceTax": 44.75,
                #                         "TDS": 0,
                #                         "ServiceCharge": 0,
                #                         "TotalGSTAmount": 44.75,
                #                         "GST": {
                #                             "CGSTAmount": 0,
                #                             "CGSTRate": 0,
                #                             "CessAmount": 0,
                #                             "CessRate": 0,
                #                             "IGSTAmount": 44.75,
                #                             "IGSTRate": 18,
                #                             "SGSTAmount": 0,
                #                             "SGSTRate": 0,
                #                             "TaxableAmount": 248.7
                #                         }
                #                     },
                #                     "RoomPromotion": "",
                #                     "Amenities": [
                #                         "Room Only"
                #                     ],
                #                     "Amenity": [],
                #                     "SmokingPreference": "NoPreference",
                #                     "BedTypes": [],
                #                     "HotelSupplements": [],
                #                     "LastCancellationDate": "2020-04-16T23:59:59",
                #                     "CancellationPolicies": [
                #                         {
                #                             "Charge": 1658,
                #                             "ChargeType": 1,
                #                             "Currency": "INR",
                #                             "FromDate": "2020-04-17T00:00:00",
                #                             "ToDate": "2020-04-20T23:59:59"
                #                         },
                #                         {
                #                             "Charge": 100,
                #                             "ChargeType": 2,
                #                             "Currency": "INR",
                #                             "FromDate": "2020-04-21T00:00:00",
                #                             "ToDate": "2020-05-01T23:59:59"
                #                         },
                #                         {
                #                             "Charge": 100,
                #                             "ChargeType": 2,
                #                             "Currency": "INR",
                #                             "FromDate": "2020-04-30T00:00:00",
                #                             "ToDate": "2020-05-01T00:00:00"
                #                         }
                #                     ],
                #                     "CancellationPolicy": "SINGLE DELUXE#^#INR 1658.00 will be charged, If cancelled between 17-Apr-2020 00:00:00 and 20-Apr-2020 23:59:59.|100.00% of total amount will be charged, If cancelled between 21-Apr-2020 00:00:00 and 01-May-2020 23:59:59.|100.00% of total amount will be charged, If cancelled between 30-Apr-2020 00:00:00 and 01-May-2020 00:00:00.|#!#",
                #                     "Inclusion": [
                #                         "Room Only"
                #                     ]
                #                 }
                #             ]
                #         }
                #     },
                #     "book": {
                #         "BookResult": {
                #             "Error": {
                #                 "ErrorCode": 0,
                #                 "ErrorMessage": ""
                #             },
                #             "VoucherStatus": True,
                #             "ResponseStatus": 1,
                #             "TraceId": "1",
                #             "Status": 1,
                #             "HotelBookingStatus": "Confirmed",
                #             "InvoiceNumber": "MW/1920/17991",
                #             "ConfirmationNo": "270-300706",
                #             "BookingRefNo": "270-300706",
                #             "BookingId": 1554760,
                #             "IsPriceChanged": False,
                #             "IsCancellationPolicyChanged": False
                #         }
                #     }
                # }
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

            FIREBASE.write_to_firestore(
                id=response["razorpay_order_id"], data={"data": json.dumps(payment_object)}, collection="payments")

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
    try:
        payment_object = json.loads(FIREBASE.read_from_firestore(
            custom_id=order_id, collection="payments")['data'])
    except:
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

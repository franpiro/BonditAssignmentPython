from datetime import datetime
from flask import Flask, request
import csv

app = Flask(__name__)

@app.route('/flights', methods = ['POST'])
def update_flight():
    updated_flights = read_csv_flights()
    write_csv_flights(updated_flights)
    return "Flights.csv updated successfully"

@app.route('/flights', methods = ['GET'])
def get_flight():
    id = request.args.get('id')
    flight = get_flight_by_id(id)
    if (flight):
        return flight
    else:
        return "Record not found", 400

def read_csv_flights():
    updated_flights = []
    with open('Flights.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        updated_flights.append(next(csv_reader, None))
        successTotal = 0
        for row in csv_reader:
            if (((datetime.strptime(row[2], '%H:%M') - datetime.strptime(row[1], '%H:%M')).total_seconds() / 60.0 >= 180) and successTotal <= 20):
                row[3] = 'success'
                successTotal = successTotal + 1
            else:
                row[3] = 'fail'
            updated_flights.append(row)
    updated_flights[1:] = sorted(updated_flights[1:], key=lambda x: x[1])
    return updated_flights

def write_csv_flights(updated_flights):
    with open('Flights.csv', 'w', newline='') as csv_file:
        csv_write = csv.writer(csv_file, delimiter=',')
        csv_write.writerows(updated_flights)

def get_flight_by_id(id):
    with open('Flights.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = next(csv_reader, None)
        try:
            flight = next(filter(lambda p: id == p[0], csv_reader))
            return dict(zip(header, flight))
        except:
            return {}
         
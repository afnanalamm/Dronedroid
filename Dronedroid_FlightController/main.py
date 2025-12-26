import serial
import time
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import logging

logging.getLogger('werkzeug').setLevel(logging.ERROR)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Required for SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False)

controllerSerial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)    # this line is for RPi/Linux. Change ACM to correct port arduino is connected to
# controllerSerial = serial.Serial('COM3', 9600, timeout=1) # this line is for Windows. Change COM3 to correct port arduino is connected to
time.sleep(2)


@socketio.on('accel')
def handle_accel(data):
    x = data.get('x', 0) # get x value from data. The 0 is a default value in case x is not provided
    y = data.get('y', 0) 
    timestamp = time.strftime('%H:%M:%S') + f'.{int(time.time() * 1000) % 1000:03d}'
    print(f"[{timestamp}] {x:.2f} {y:.2f}")

    try:
        if x is not None and y is not None:
            # send as: x,y\n
            x = round(x, 2) # round to 2 decimal places
            y = round(y, 2)

            x *= 100  # scale to get integer values
            y *= 100

            serial_data = f"{x},{y}\n" #serial_data = f"{x}, {y}\n"
            print(serial_data.encode('ascii'))

            controllerSerial.write(serial_data.encode('ascii'))
            controllerSerial.flush()
    except KeyboardInterrupt:
        print("\nExiting.")

    return jsonify({"status": "ok", "received": {"x": x, "y": y}})


# Optional: Handle connections for debugging
# @socketio.on('connect')
# def connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def disconnect():
#     print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=False)




# import serial
# import time
# from flask import Flask, request

# app = Flask(__name__) #creating an instance of the flask app
# controllerSerial = serial.Serial(port= '/dev/ttyACM0',baudrate= 9600, timeout=1) # attachingg to arduino via serial
# time.sleep(2) # give arduino time to reset after connecting via serial

# @app.route('/receiveInput', methods=["POST"])
# def receiveInput():
#     print("Type text to display on LCD (Ctrl+C to exit)")

#     try:
#         while True:
#             input = request
#             # firstChar = request[0] # get the first character from the request to print 
#             controllerSerial.write(input.encode("ascii"))

#     except Exception as e:
#         print(f"Error: {e}")

#     finally:
#         controllerSerial.close()

# # run the flask app
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5001, debug=True)

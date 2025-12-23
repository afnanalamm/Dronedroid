import serial
import time
from flask import Flask, request, jsonify
import logging

logging.getLogger('werkzeug').setLevel(logging.ERROR)



app = Flask(__name__)

# rpiSerial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)    # this line is for RPi/Linux. Change ACM to correct port arduino is connected to
# rpiSerial = serial.Serial('COM3', 9600, timeout=1) # this line is for Windows. Change COM3 to correct port arduino is connected to
# time.sleep(2)

@app.route('/receiveInput', methods=['POST'])
def receive_input():
    data = request.get_json()
    # print(data)

    # EXPECTING: { "x": <float>, "y": <float> }
    x = data.get("x")
    y = data.get("y")

    try:
        if x is not None and y is not None:
            # send as: x,y\n
            x = round(x, 2)
            y = round(y, 2)
            serial_data = f"{x} {y}"
            print(serial_data.encode('ascii'))

            # rpiSerial.write(serial_data.encode('ascii'))
            # rpiSerial.flush()
    except KeyboardInterrupt:
        print("\nExiting.")

    return jsonify({"status": "ok", "received": {"x": x, "y": y}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)




# import serial
# import time
# from flask import Flask, request

# app = Flask(__name__) #creating an instance of the flask app
# rpiSerial = serial.Serial(port= '/dev/ttyACM0',baudrate= 9600, timeout=1) # attachingg to arduino via serial
# time.sleep(2) # give arduino time to reset after connecting via serial

# @app.route('/receiveInput', methods=["POST"])
# def receiveInput():
#     print("Type text to display on LCD (Ctrl+C to exit)")

#     try:
#         while True:
#             input = request
#             # firstChar = request[0] # get the first character from the request to print 
#             rpiSerial.write(input.encode("ascii"))

#     except Exception as e:
#         print(f"Error: {e}")

#     finally:
#         rpiSerial.close()

# # run the flask app
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5001, debug=True)

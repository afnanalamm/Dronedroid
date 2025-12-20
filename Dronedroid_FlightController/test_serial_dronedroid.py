import serial
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

rpiSerial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

@app.route('/receiveInput', methods=['POST'])
def receive_input():
    data = request.get_json()
    print(data)
    text = data["text"]
    
    
    try:
        if text:
            rpiSerial.write(text.encode('ascii'))
            rpiSerial.flush()
    except KeyboardInterrupt:
        print("\nExiting.")

    return jsonify({"status": "ok", "received": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)




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
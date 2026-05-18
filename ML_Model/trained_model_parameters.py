import serial
import time
import numpy as np

# ===== MODEL PARAMETERS =====

w = np.array([
    [-1.95906435,  0.13935992],
    [ 0.1653572 ,  0.35332168],
    [ 1.79370709, -0.49268199]
])

b = np.array([
    94.1027715,
   -8.1825106,
   -85.92026089
])

# ===== PREDICTION FUNCTION =====

def predict(h, t):

    x = np.array([h, t])

    scores = np.dot(w, x) + b

    return np.argmax(scores)

# ===== SERIAL SETUP =====

ser = serial.Serial('COM5', 9600)   # CHANGE COM PORT
time.sleep(2)

print("System started...")

# ===== MAIN LOOP =====

while True:

    try:

        line = ser.readline().decode(errors='ignore').strip()

        # Ignore invalid lines
        if ',' not in line:
            continue

        # Parse sensor data
        h, t = map(float, line.split(','))

        # ML prediction
        level = predict(h, t)

        print(f"H:{h:.2f}, T:{t:.2f} → Level: {level}")

        # Send level back to Arduino
        ser.write(f"{level}\n".encode())

    except Exception as e:

        print("Error:", e)

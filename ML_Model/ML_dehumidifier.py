import serial
import time
import numpy as np

# ===== TRAINED PARAMETERS =====

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

# ===== PREDICTION =====

def predict(h, t):

    x = np.array([h, t])

    scores = np.dot(w, x) + b

    return np.argmax(scores)

# ===== SERIAL =====

ser = serial.Serial('COM5', 9600)
time.sleep(2)

print("System started...")

# ===== LOOP =====

while True:

    try:

        line = ser.readline().decode(errors='ignore').strip()

        if ',' not in line:
            continue

        h, t = map(float, line.split(','))

        level = predict(h, t)

        print(f"H:{h:.2f}, T:{t:.2f} → Level: {level}")

        ser.write(f"{level}\n".encode())

    except Exception as e:

        print("Error:", e)

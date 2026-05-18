import numpy as np
from sklearn.linear_model import LogisticRegression

np.random.seed(42)

humidity = []
temperature = []
labels = []

# ===== GENERATE DATA =====

for hour in range(168):   # 1 week hourly data

    h = 50 + 10*np.sin(hour/12) + np.random.normal(0, 2)
    t = 28 + 4*np.sin(hour/24) + np.random.normal(0, 1)

    humidity.append(h)
    temperature.append(t)

    # ===== LABELING LOGIC =====

    if h < 45:
        labels.append(0)

    elif h < 60:
        labels.append(1)

    else:
        labels.append(2)

# ===== DATASET =====

X = np.column_stack((humidity, temperature))
y = np.array(labels)

print("Class distribution:", np.bincount(y))

# ===== TRAIN MODEL =====

model = LogisticRegression(
    multi_class='multinomial',
    max_iter=1000
)

model.fit(X, y)

# ===== RESULTS =====

print("\n=== DATA SAMPLE ===")
print(X[:10])

print("\n=== LABEL SAMPLE ===")
print(y[:10])

print("\n=== WEIGHTS ===")
print(model.coef_)

print("\n=== BIAS ===")
print(model.intercept_)

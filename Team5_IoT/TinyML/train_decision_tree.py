import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import export_text

# ==============================
# 1. Đọc Dataset
# ==============================

data = pd.read_csv("smart_agriculture_dataset.csv")

print("===== 5 dòng đầu =====")
print(data.head())

# ==============================
# 2. Feature & Label
# ==============================

X = data[["Temperature", "Humidity", "Soil"]]
y = data["NeedWater"]

# ==============================
# 3. Train/Test
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print()
print("Train:", len(X_train))
print("Test :", len(X_test))

# ==============================
# 4. Decision Tree
# ==============================

model = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

model.fit(X_train, y_train)

# ==============================
# 5. Predict
# ==============================

y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)

print()
print("=========================")
print("Accuracy:", round(acc * 100, 2), "%")

# ==============================
# 6. Lưu Model
# ==============================

joblib.dump(model, "decision_tree.pkl")

print()
print("Đã lưu decision_tree.pkl")

# ==============================
# 7. Hiển thị cây
# ==============================

tree_rules = export_text(
    model,
    feature_names=list(X.columns)
)

print()
print("=========================")
print(tree_rules)

# ==============================
# 8. Lưu cây ra file txt
# ==============================

with open("tree_rules.txt", "w", encoding="utf-8") as f:
    f.write(tree_rules)

print()
print("Đã lưu tree_rules.txt")
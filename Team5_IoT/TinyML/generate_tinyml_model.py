import joblib
from sklearn.tree import _tree

# ============================
# Load Decision Tree
# ============================

model = joblib.load("decision_tree.pkl")

tree = model.tree_

feature_names = [
    "temperature",
    "humidity",
    "soil"
]

# ============================
# Hàm sinh code Python
# ============================

def recurse(node, depth):

    indent = "    " * depth

    if tree.feature[node] != _tree.TREE_UNDEFINED:

        feature = feature_names[tree.feature[node]]
        threshold = tree.threshold[node]

        code = ""

        code += f"{indent}if {feature} <= {threshold:.2f}:\n"
        code += recurse(tree.children_left[node], depth + 1)

        code += f"{indent}else:\n"
        code += recurse(tree.children_right[node], depth + 1)

        return code

    else:

        value = tree.value[node][0]

        prediction = value.argmax()

        return f"{indent}return {prediction}\n"

# ============================
# Sinh file tinyml_model.py
# ============================

python_code = "def predict(temperature, humidity, soil):\n"

python_code += recurse(0, 1)

with open("tinyml_model.py", "w", encoding="utf8") as f:

    f.write(python_code)

print("--------------------------------")
print("tinyml_model.py generated!")
print("--------------------------------")
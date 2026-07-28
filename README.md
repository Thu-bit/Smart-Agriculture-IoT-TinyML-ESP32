# Smart Agriculture Monitoring System using ESP32, Blynk IoT and TinyML

## Overview

This project is an IoT-based smart agriculture monitoring system using ESP32, Blynk IoT and TinyML. The system monitors environmental parameters such as temperature, air humidity and soil moisture, allowing users to remotely monitor and control irrigation through the Blynk application.

The project supports two operating modes:

- **AUTO:** ESP32 uses the TinyML model to automatically determine whether irrigation is required.
- **MANUAL:** The user manually controls the water pump through the Blynk application.

In addition, the system supports email notifications through Blynk Cloud when predefined events occur.

---

# Project Structure

```
Team5_IoT
│
├── ESP32/
│   ├── main.py
│   ├── boot.py
│   ├── BlynkLib.py
│   ├── tinyml_model.py
│   └── README.md
│
├── TinyML/
│   ├── train_decision_tree.py
│   ├── generate_tinyml_model.py
│   ├── smart_agriculture_dataset.csv
│   ├── decision_tree.pkl
│   ├── smart_agriculture_model.pkl
│   ├── tinyml_model.py
│   └── README.md
│
└── Report/
```

---

# Folder Description

## ESP32

This folder contains the MicroPython source code used to run the actual embedded system on the ESP32.

Main functions:

- Read sensor data
- Connect to WiFi
- Communicate with Blynk Cloud
- Execute TinyML inference
- Control the relay and water pump
- Support AUTO and MANUAL operating modes

This is the folder required to deploy and run the real project.

---

## TinyML

This folder contains the research and development process of the TinyML model.

It includes:

- Dataset generation
- Decision Tree training using Scikit-learn
- Model evaluation
- Exporting the trained Decision Tree
- Converting the trained model into MicroPython (if-else rules)

These files are provided for documentation and research purposes only.

They are **NOT required** to run the ESP32 project.

The ESP32 only uses the generated **tinyml_model.py** inside the ESP32 folder for inference.

---

# How to Run

## Step 1

Flash MicroPython firmware to ESP32.

---

## Step 2

Open the **ESP32** folder using Thonny IDE.

---

## Step 3

Configure:

- WiFi SSID
- WiFi Password
- Blynk Template ID
- Blynk Auth Token

inside **main.py**

---

## Step 4

Upload all files inside the ESP32 folder to the ESP32 board.

Required files:

- boot.py
- main.py
- BlynkLib.py
- tinyml_model.py

---

## Step 5

Restart ESP32.

The system will:

- connect to WiFi
- connect to Blynk Cloud
- read sensors
- execute TinyML inference
- update Dashboard
- control the relay

---

# TinyML Workflow

Dataset

↓

Train Decision Tree (Scikit-learn)

↓

Evaluate Model

↓

Export Decision Tree

↓

Convert to MicroPython

↓

tinyml_model.py

↓

Deploy to ESP32

↓

Inference

↓

Relay Control

---

# Authors

Group 5

Embedded Systems & IoT Project

Van Lang University

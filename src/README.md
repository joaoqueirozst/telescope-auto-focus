# Telescope Automatic Focus Adjustment System

Automatic telescope lens focusing system developed using `Python`, `C++`, `ESP32`, and `Socket Communication` for real-time focus optimization through computer vision techniques.

The project performs automatic lens adjustment by analyzing image sharpness captured by a camera connected to the telescope system. Communication between the `Python Server` and the `ESP32 Client` is established through TCP sockets, enabling remote motor control and autonomous focus correction.

The system uses focus metrics based on the variance of the `Laplacian` operator to determine the sharpest image and automatically position the telescope lens at the best focal point.

---

# Project Structure

```bash
src/
├── README.md
├── requirements.txt
├── server.py
└── client.cpp
```

---

# System Overview

The project is divided into two main modules:

- `Server (Python)`:
  Responsible for image acquisition, focus analysis, and communication with the ESP32 device.

- `Client (ESP32/C++)`:
  Responsible for controlling the stepper motor attached to the telescope lens.

The server captures images from the camera, evaluates the focus quality, and sends movement commands to the ESP32 through socket communication. The ESP32 then adjusts the lens position accordingly.

---

# Focus Estimation

The focus quality is estimated using the variance of the `Laplacian` operator:

```python
cv2.Laplacian()
```

This method evaluates image sharpness by measuring high-frequency components. Higher variance values indicate sharper and better-focused images.

---

# Socket Communication

Communication between the `Python Server` and the `ESP32 Client` is performed using TCP sockets.

The server sends motor position commands:

```python
conn.send(str(position).encode())
```

The ESP32 receives the position value and adjusts the motor accordingly.

After movement completion, the ESP32 sends confirmation:

```cpp
client.println("ok");
```

This guarantees synchronized communication between both systems.

---

# Hardware Requirements

To run the project, you will need:

- Telescope lens system;
- `ESP32`;
- Stepper motor driver;
- Stepper motor;
- Camera or webcam;
- Wi-Fi network.

---

# Installing Python and the Arduino IDE

To install Python, access the link https://www.python.org/downloads/. For installing the Arduino IDE and ESP32 dependencies, access the tutorial suggested on the lab's website ([ESP32 Installation](https://www.eletroifes.com.br/home)) and follow the step-by-step instructions.

# requirements.txt

Create a file named:

```bash
requirements.txt
```

Containing:

```txt
opencv-python
```

Install automatically using:

```bash
pip install -r requirements.txt
```

---

# ESP32 Wi-Fi Configuration

Inside `client.cpp`, configure:

```cpp
const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* host = "SERVER_IP";
```

Example:

```cpp
const char* ssid = "MyWiFi";
const char* password = "12345678";
const char* host = "192.168.0.0";
```

---

# Server Configuration

Inside `server.py`, configure:

```python
host = 'YOUR_SERVER_IP'
port = 8000
```

Example:

```python
host = '192.168.0.0'
port = 8000
```

The server and ESP32 must be connected to the same Wi-Fi network.

---

# Running the Project

## 1. Upload the Client Code to ESP32 and start the Python Server

Open `client.cpp` inside Arduino IDE and upload the code to the ESP32 board. Next, run the server code.

```bash
python server.py
```

or:

```bash
python3 server.py
```

---

## 2. Start the ESP32 System

After powering the ESP32:

- The device connects to Wi-Fi;
- Establishes socket communication with the server;
- Initializes motor calibration;
- Starts automatic focus adjustment.

---

# Focus Adjustment Workflow

The system workflow follows these steps:

- Camera captures image;
- Focus metric is computed;
- Server determines if focus quality improved;
- Position command is sent to ESP32;
- Stepper motor moves the lens;
- New image is captured;
- Best focal position is selected automatically.

---

# Observations
For this project, the selected focus threshold value was `62`, which was experimentally defined according to the image acquisition conditions used during development. However, this value may vary depending on factors such as camera quality, sensor characteristics, optical configuration, environmental lighting conditions, and image noise. Therefore, users may need to calibrate and adjust the threshold according to their own telescope setup and acquisition environment in order to achieve more accurate focus estimation results.

```python
threshold = 62
```

# Author

Developed by João Pedro, with [Lab Penguin](https://github.com/Lab-Penguin).

# JAKA Mini 2 Object Detection and Pick-and-Place System

## Project Overview

This project integrates a **JAKA Mini 2 robotic arm**, **ROS2 Humble**, **Python**, and **YOLOv8** to detect objects using a webcam and command the robot to move toward the detected object.

The system consists of three main components:

* **YOLO Object Detection (`app.py`)**

  * Detects objects from the webcam in real time.
  * Allows the user to select which object class to track.
  * Converts image coordinates into centered pixel coordinates.
  * Publishes the detected object's coordinates on a ROS2 topic.

* **Coordinate Receiver (`send_detected_coords_loop.py`)**

  * Subscribes to the published object coordinates.
  * Converts pixel coordinates into robot joint values.
  * Sends movement commands to the JAKA robot continuously.

* **JAKA ROS2 Driver**

  * Establishes communication between ROS2 and the physical JAKA Mini 2 robot.

---

# Software Requirements

## Operating System

* Ubuntu 22.04
* ROS2 Humble

## Python

* Python 3.10+

## Required Python Packages

Install the required packages:

```bash
pip install ultralytics
pip install opencv-python
```

If needed:

```bash
pip install numpy
```

---

# Hardware Requirements

* JAKA Mini 2 Robot
* Ethernet connection between PC and robot
* Webcam
* Virtual Machine (Ubuntu)

---

# Important Configuration Before Launching

## 1. Connect to the Robot First

**Important**

The computer **must already be connected to the JAKA robot before starting the Ubuntu Virtual Machine.**

If the VM is started before the robot connection is established, ROS2 may not detect the robot correctly.

---

## 2. VirtualBox Network Settings

Open:

```
VirtualBox
→ Settings
→ Network
```

Select:

```
Bridged Adapter
```

Do **NOT** use:

* NAT
* Host-Only

The VM must be on the same network as the robot.

---

## 3. Enable Webcam

Before starting Ubuntu:

```
VirtualBox
→ Devices
→ Webcam
```

Enable the webcam.

Without this step:

* OpenCV will not detect the camera.
* YOLO will not receive any image.

---

## 4. Check USB Devices

If additional USB devices are used, enable them from:

```
Devices
→ USB
```

before running the project.

---

# Launch Order

The programs **must** be started in the following order.

---

## Step 1 — Start the JAKA Driver

```bash
ros2 launch jaka_driver robot_start.launch.py ip:=10.5.5.100
```

Wait until the driver connects successfully.

Do **not** continue until the robot is connected.

---

## Step 2 — Start the Coordinate Sender

Open a new terminal:

```bash
python3 send_detected_coords_loop.py
```

This node waits for object detections and sends movement commands to the robot.

---

## Step 3 — Start Object Detection

Open another terminal:

```bash
python3 app.py
```

This launches:

* Webcam
* YOLO detector
* Object selection

After selecting the desired object, the coordinates are continuously published to ROS2.

---

# Returning the Robot to the Home Position

To move the robot back to the zero position, run:

```bash
ros2 service call /jaka_driver/joint_move jaka_msgs/srv/Move "{
  pose: [0, 0, 0, 0, 0, 0],
  has_ref: false,
  ref_joint: [0],
  mvvelo: 0.5,
  mvacc: 0.5,
  mvtime: 0.0,
  mvradii: 0.0,
  coord_mode: 0,
  index: 0
}"
```

---

# Project Workflow

```
Webcam
     │
     ▼
YOLOv8 Detection
     │
     ▼
Object Selection
     │
     ▼
Pixel Coordinates
     │
     ▼
ROS2 PoseArray Topic
     │
     ▼
send_detected_coords_loop.py
     │
     ▼
Pixel-to-Joint Conversion
     │
     ▼
JAKA ROS2 Driver
     │
     ▼
JAKA Mini 2 Robot
```

---

# ROS2 Communication

## Published Topic

```
/detected_objects_xy
```

Message type:

```
geometry_msgs/PoseArray
```

Each detected object contains:

* X coordinate
* Y coordinate

---

# Main Files

## app.py

Responsibilities:

* Open webcam
* Load YOLO model
* Detect objects
* Ask the user which object to track
* Convert image coordinates
* Publish coordinates to ROS2

---

## send_detected_coords_loop.py

Responsibilities:

* Subscribe to detected coordinates
* Convert pixels to robot joint values
* Send joint commands
* Keep the robot following the selected object

---

# Coordinate Mapping

The detected object position is converted from:

```
Camera Pixels
        ↓
Centered Pixel Coordinates
        ↓
Joint Angles
        ↓
Robot Motion
```

The mapping was calibrated experimentally to match the camera view with the robot workspace.

---

# Notes

* The robot must be powered on before launching the driver.
* Ensure the robot IP address is correct (`10.5.5.100` by default).
* Wait for a successful connection before launching the remaining nodes.
* Always connect the robot before starting the virtual machine.
* Always use **Bridged Adapter** networking.
* Make sure the webcam is enabled from the VirtualBox **Devices** menu.
* Verify any required USB devices are attached to the VM.
* Start the nodes in the correct order:

  1. JAKA Driver
  2. `send_detected_coords_loop.py`
  3. `app.py`
* If the camera cannot be opened, verify that the webcam is attached to the virtual machine and not in use by another application.

---

# Technologies Used

* ROS2 Humble
* Python 3
* OpenCV
* Ultralytics YOLOv8
* JAKA ROS2 Driver
* JAKA Mini 2 Robot
* VirtualBox
* Ubuntu 22.04

---

# Future Improvements

* Automatic camera calibration.
* Conversion from image coordinates to real-world Cartesian coordinates.
* Object grasping using an end-effector.
* Multi-object prioritization.
* Dynamic obstacle avoidance.
* Improved workspace calibration for higher positioning accuracy.

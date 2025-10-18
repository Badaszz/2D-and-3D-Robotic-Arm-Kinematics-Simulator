# 2D and 3D Robotic Arm Kinematics Simulator

This repository contains two interactive Python simulators that demonstrate **forward and inverse kinematics** for a robotic arm.

- 🟢 `only_python.py` → 2-link **2D robotic arm** (forward + inverse kinematics)
- 🔵 `only_python_3d.py` → 3-link **3D robotic arm** (forward kinematics)

Both are implemented purely in **Python**, using `matplotlib` for visualization and `numpy` for mathematical computation.

---

## 🧠 Project Overview

This project is designed to visualize the relationship between **joint angles** (control inputs) and **end-effector position** (output) in robotic manipulators.

It demonstrates:

- ✅ **Forward Kinematics:** computing end-effector position from joint angles  
- ✅ **Inverse Kinematics (2D only):** computing joint angles for a target point  
- ✅ **Interactive Control:** sliders for adjusting joint angles  
- ✅ **Visualization:** dynamic, real-time plotting of the arm’s movement  

---

## 📂 Files in This Repository

| File | Description |
|------|--------------|
| `only_python.py` | 2D two-link robotic arm with sliders and mouse-click inverse kinematics |
| `only_python_3d.py` | 3D three-link robotic arm with sliders for joint control |
| `README.md` | This documentation file |

---

## 🧩 Requirements

Before running the scripts, install the following dependencies:

```bash
pip install numpy matplotlib

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

# Arm parameters
L1, L2, L3 = 2.0, 1.5, 1.0  # Lengths of arm segments

# Initial joint angles (radians)
theta1, theta2, theta3 = np.pi / 4, np.pi / 4, np.pi / 4 # 45 degrees each

# Create 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.1, bottom=0.35)

# Set workspace limits
# Place origin at the edge/corner of the plotting box by making the axis minimum 0
max_range = L1 + L2 + L3 + 0.5  # total reach plus small margin
ax.set_xlim([0, max_range])
ax.set_ylim([0, max_range])
ax.set_zlim([0, max_range])
ax.set_box_aspect([1, 1, 1])
ax.view_init(elev=25, azim=45)
ax.set_title('3D ARM Simulator\n(Click to set target position)')

# Arm line
line, = ax.plot([], [], [], 'o-', lw=3, color='royalblue')

def forward_kinematics(theta1, theta2, theta3):
    """
    Computes joint positions for a simple 3-link 3D arm
    with base rotation (theta1) and planar bending (theta2, theta3)
    """
    # Joint 1 (base rotation)
    x1 = L1 * np.cos(theta2) * np.cos(theta1)
    y1 = L1 * np.cos(theta2) * np.sin(theta1)
    z1 = L1 * np.sin(theta2)

    # Joint 2
    x2 = x1 + L2 * np.cos(theta2 + theta3) * np.cos(theta1)
    y2 = y1 + L2 * np.cos(theta2 + theta3) * np.sin(theta1)
    z2 = z1 + L2 * np.sin(theta2 + theta3)

    # End effector
    return np.array([[0, x1, x2],
                     [0, y1, y2],
                     [0, z1, z2]])

def update(val):
    t1 = s_theta1.val
    t2 = s_theta2.val
    t3 = s_theta3.val
    pts = forward_kinematics(t1, t2, t3)
    line.set_data(pts[0, :], pts[1, :])
    line.set_3d_properties(pts[2, :])
    fig.canvas.draw_idle()

# Sliders
ax_theta1 = plt.axes([0.2, 0.25, 0.65, 0.03])
ax_theta2 = plt.axes([0.2, 0.2, 0.65, 0.03])
ax_theta3 = plt.axes([0.2, 0.15, 0.65, 0.03])

s_theta1 = Slider(ax_theta1, 'Base θ1', -np.pi, np.pi, valinit=theta1)
s_theta2 = Slider(ax_theta2, 'Shoulder θ2', -np.pi/2, np.pi/2, valinit=theta2)
s_theta3 = Slider(ax_theta3, 'Elbow θ3', -np.pi/2, np.pi/2, valinit=theta3)

s_theta1.on_changed(update)
s_theta2.on_changed(update)
s_theta3.on_changed(update)

update(None)
plt.show()

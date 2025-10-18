import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Wedge  # Added to draw angle arcs

# Arm parameters
L1 = 4.0  # Length of first arm segment
L2 = 3.5  # Length of second arm segment

fig, ax = plt.subplots() # Create figure and axis
plt.subplots_adjust(bottom=0.3)
ax.set_xlim(-7.5, 7.5) # Set x-axis limits
ax.set_ylim(-7.5, 7.5) # Set y-axis limits
ax.set_aspect('equal') # Equal aspect ratio
# Keep the axes frame but hide ticks and tick labels
ax.set_xticks([])
ax.set_yticks([])
ax.tick_params(left=False, bottom=False)
for spine in ax.spines.values():
    spine.set_visible(True)
ax.set_title('2D ARM Simulator\n(Click to set target position)')
# ax.axis('off')  # hide axes, ticks and frame

# Add an empty message text (top-center of the axes, in axes coords)
msg = ax.text(0.5, 0.95, '', transform=ax.transAxes, ha='center', va='top', color='red', fontsize=12)

# show theta values (degrees) on the plot (bottom-left)
theta1_text = ax.text(0.02, 0.08, '', transform=ax.transAxes, ha='left', va='bottom', color='blue', fontsize=10)
theta2_text = ax.text(0.02, 0.02, '', transform=ax.transAxes, ha='left', va='bottom', color='blue', fontsize=10)

# Initial angles
theta1, theta2 = np.pi/4, np.pi/4 # 45 degrees each
line, = plt.plot([], [], 'o-', lw=4) # Line object for the arm

# reference point markers and arc patch placeholders
origin_point, = ax.plot([0], [0], 'ko', markersize=6)          # origin marker
joint_point, = ax.plot([], [], 'ko', markersize=6)             # first joint marker
arc1 = None  # arc at origin for theta1
arc2 = None  # arc at joint for theta2

def forward_kinematics(theta1, theta2):
    # Function to compute forward kinematics 
    # With the control inputs theta1 and theta2 (in radians)
    x1 = L1 * np.cos(theta1) # x-coordinate of first joint
    y1 = L1 * np.sin(theta1) # y-coordinate of first joint
    x2 = x1 + L2 * np.cos(theta1 + theta2) # x-coordinate of second joint
    y2 = y1 + L2 * np.sin(theta1 + theta2) # y-coordinate of second joint
    return [0, x1, x2], [0, y1, y2]

def update(val):
    global arc1, arc2 # Use global arc variables to modify them
    t1 = s_theta1.val # Get current value of theta1 from slider
    t2 = s_theta2.val # Get current value of theta2 from slider
    x, y = forward_kinematics(t1, t2) # Compute forward kinematics
    line.set_data(x, y) # Update arm/line data
    msg.set_text('')   # clear any previous message when updating via sliders
    # update degree displays
    theta1_text.set_text(f"Theta1: {np.degrees(t1):.1f}°")
    theta2_text.set_text(f"Theta2: {np.degrees(t2):.1f}°")

    # update reference markers
    x1, y1 = x[1], y[1]   # coordinates of first joint
    joint_point.set_data([x1], [y1])

    # remove previous arcs if present
    if arc1 is not None:
        try:
            arc1.remove()
        except Exception:
            pass
        arc1 = None
    if arc2 is not None:
        try:
            arc2.remove()
        except Exception:
            pass
        arc2 = None

    # draw small arcs (as Wedge outlines) to show angles
    # arc at origin showing theta1 relative to +x axis
    deg_t1 = np.degrees(t1)
    if deg_t1 >= 0:
        start1, end1 = 0, deg_t1
    else:
        start1, end1 = deg_t1, 0
    arc1 = Wedge((0, 0), 1.0, start1, end1, width=0.25, facecolor='none', edgecolor='black', lw=2, zorder=3)
    ax.add_patch(arc1)

    # arc at first joint showing the angle between link1 and link2
    start2 = np.degrees(t1)
    end2 = np.degrees(t1 + t2)
    # normalize small arc direction/extent for nicer visuals
    arc2 = Wedge((x1, y1), 0.8, start2, end2, width=0.25, facecolor='none', edgecolor='black', lw=2, zorder=3)
    ax.add_patch(arc2)

    fig.canvas.draw_idle()

# Add sliders
ax_theta1 = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_theta2 = plt.axes([0.2, 0.1, 0.65, 0.03])
s_theta1 = Slider(ax_theta1, 'Theta1', -np.pi, np.pi, valinit=theta1)
s_theta2 = Slider(ax_theta2, 'Theta2', -np.pi, np.pi, valinit=theta2)
s_theta1.on_changed(update)
s_theta2.on_changed(update)

# Inverse kinematics
def on_click(event):
    # Function to handle mouse click events for inverse kinematics
    if event.inaxes != ax:
        # If click is outside the arm's axes message out of reach and return
        msg.set_text("Target out of reach!")
        fig.canvas.draw_idle() # Redraw canvas to show message
        return
    x, y = event.xdata, event.ydata
    cos_t2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    if abs(cos_t2) > 1:
        msg.set_text("Target out of reach!")
        fig.canvas.draw_idle()
        return
    # clear any previous message when reachable
    msg.set_text('')
    sin_t2 = np.sqrt(1 - cos_t2**2) # Elbow-down solution
    theta2 = np.arctan2(sin_t2, cos_t2) # Compute theta2 for the elbow-down solution
    theta1 = np.arctan2(y, x) - np.arctan2(L2*np.sin(theta2), L1 + L2*np.cos(theta2)) # Compute theta1 
    s_theta1.set_val(theta1) # Update sliders
    s_theta2.set_val(theta2)
    update(None) # Update arm position with new angles

fig.canvas.mpl_connect('button_press_event', on_click) # Connect click event to inverse kinematics function

# Initialize
update(None) # Initial update to draw the arm
plt.show()

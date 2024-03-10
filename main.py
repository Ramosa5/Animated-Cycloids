import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

R = 9
r = 3
rotations = 20 * np.pi
precision = 1000
boundary = 20
t = np.linspace(0, rotations, precision)
t_lab = np.linspace(-2, -1, precision)
point_x = []
point_y = []
choice = input("Wybierz co narysowac (c - cykloida, e - epicykloida, h - hipocykloida, z - zajeciowa): ")

if choice == "c":
    # cykloida
    cycl_x = r * (t - np.sin(t))
    cycl_y = r * (1 - np.cos(t))
elif choice == "e":
    # epicykloida
    cycl_x = (R + r) * np.cos(t) - r * np.cos(((R + r) / r) * t)
    cycl_y = (R + r) * np.sin(t) - r * np.sin(((R+r)/r)*t)
    stable_x = R * np.cos(t)
    stable_y = R * np.sin(t)
elif choice == "h":
    # hipocykloida
    cycl_x = (R - r) * np.cos(t) + r * np.cos(((R - r) / r) * t)
    cycl_y = (R - r) * np.sin(t) - r * np.sin(((R - r) / r) * t)
    stable_x = R * np.cos(t)
    stable_y = R * np.sin(t)
elif choice == "z":
    # zajeciowa
    r = 0.1
    boundary = 4
    poly_x = t_lab
    x = t_lab
    poly_y = (14 * x * np.exp(-8 * x)) / (1e6 * (4 * x + 13 * np.exp(x)))
    cycl_x = poly_x + r * (t_lab - np.sin(t_lab)) - r
    cycl_y = poly_y + (r * (1 - np.cos(t_lab))) - r

fig, ax = plt.subplots()
cycl, = ax.plot([], [], lw=1)
moving, = ax.plot([], [], lw=1)
stable, = ax.plot([], [], lw=1)
poli, = ax.plot([], [], lw=1)

def init():
    cycl.set_data([], [])
    if choice == 'h' or choice == 'e':
        stable.set_data(stable_x, stable_y)
    elif choice == 'z':
        poli.set_data(poly_x, poly_y)
    moving.set_data([], [])
    return cycl, moving


def animate_hipo(i):
    cycl.set_data(cycl_x[:i], cycl_y[:i])
    angle = i * (rotations / precision)

    center_x = (R - r) * np.cos(angle)
    center_y = (R - r) * np.sin(angle)

    moving_x = center_x + r * np.cos(t)
    moving_y = center_y + r * np.sin(t)
    moving.set_data(moving_x, moving_y)
    return cycl, moving


def animate_epi(i):
    cycl.set_data(cycl_x[:i], cycl_y[:i])
    angle = i * (rotations / precision)

    center_x = (R + r) * np.cos(angle)
    center_y = (R + r) * np.sin(angle)

    moving_x = center_x + r * np.cos(t)
    moving_y = center_y + r * np.sin(t)
    moving.set_data(moving_x, moving_y)
    return cycl, moving


def animate_cycloid(i):
    cycl.set_data(cycl_x[:i], cycl_y[:i])
    angle = i * (rotations / precision)

    center_x = r * angle
    center_y = r

    moving_x = center_x + r * np.cos(t)
    moving_y = center_y + r * np.sin(t)
    moving.set_data(moving_x, moving_y)
    return cycl, moving


def animate_lab(i):
    angle = i/(2*np.pi)

    center_x = poly_x[i] - r
    center_y = poly_y[i]

    moving_x = center_x + r * np.cos(t)
    moving_y = center_y + r * np.sin(t)
    moving.set_data(moving_x, moving_y)
    point_x.append(center_x + r * np.cos(angle))
    point_y.append(center_y + r * np.sin(angle))
    cycl.set_data(point_x[:i], point_y[:i])
    return cycl, moving


if choice == "c":
    ani = animation.FuncAnimation(fig, animate_cycloid, init_func=init, frames=len(t), interval=20, blit=True)
elif choice == "e":
    ani = animation.FuncAnimation(fig, animate_epi, init_func=init, frames=len(t), interval=20, blit=True)
elif choice == "h":
    ani = animation.FuncAnimation(fig, animate_hipo, init_func=init, frames=len(t), interval=20, blit=True)
elif choice == "z":
    ani = animation.FuncAnimation(fig, animate_lab, init_func=init, frames=len(t), interval=20, blit=True)


plt.xlim(-boundary, boundary)
if choice == "z":
    plt.ylim(-10, 40)
else:
    plt.ylim(-boundary, boundary)
    plt.axis('equal')
plt.grid()

plt.show()

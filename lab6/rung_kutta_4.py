import numpy as np
from matplotlib import pyplot as plt


def f_x(x, t):
    """
    Euler's method
    """
    return -x**3 + np.sin(t)


def main():
    """
    """
    a = 0.0         # Start of interval
    b = 10.0        # End of interval
    N = 1000        # Number of steps
    h = (b-a)/N     # Size of single step
    x = 0.0         # Initial condition

    tpoints = np.arange(a, b, h)
    xpoints = []
    # loop over time interval
    for t in tpoints:
        xpoints.append(x)
        # Calculate the 4th Order Rung-Kutta
        k1 = h*f_x(x,t)
        k2 = h*f_x(x + 0.5*k1, t + 0.5*h)
        k3 = h*f_x(x + 0.5*k2, t + 0.5*h)
        k4 = h*f_x(x+k3, t+h)
        x += (k1 + 2*k2 + 2*k3 + k4)/6

    # Plot Values
    plt.plot(tpoints, xpoints)
    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.show()


# Call main
main()

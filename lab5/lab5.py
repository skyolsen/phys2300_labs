'''
Assignment to simulate projectile motion with and without air resistance
'''
from vpython import *
from math import sin, cos
import argparse
import sys
import matplotlib.pylab as plt



def set_scene(data):
    """
    Set Vpython Scene
    :data: dictionary to hold data
    :return: Nothing
    """
    scene.title = "Assignment 5: Projectile motion"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1
    # Set background: floor, table, etc
    ground=box(pos=vec(0,-1,0), size=vec(data['grnd_size'],1,4))

def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    ball_nd = sphere(pos=vector(-data['grnd_size']/2, data['init_height'], 0),
                        radius=1, color=color.cyan, make_trail=True)

    # Follow the movement of the ball
    scene.camera.follow(ball_nd)

    # Set initial velocity & position
    ball_nd.m = data['ball_mass']
    ball_nd.v = (vec(data['init_velocity']*cos(data['theta']*pi/180), data['init_velocity']*sin(data['theta']*pi/180),0))  #velocity of ball
    
    #set gravity force vector (accelleration in only the y direction)
    fgrav = vec(0, data['gravity'], 0)

    # set time to 0, and add first time and position entry to list
    t = 0
    data['pm_t'].append(t)
    data['pm_posy'].append(ball_nd.pos.y)

    # Animate
    while ball_nd.pos.y >= 0:
        rate(100)
        force = data['ball_mass']*fgrav #Calculate Force (vector): F=M*A
        ball_nd.v = ball_nd.v+(force/data['ball_mass'])*data['deltat']  #V = v0+a*dt. (force/ball_mass = acceleration)
        ball_nd.pos = ball_nd.pos + ball_nd.v*data['deltat'] #X= x0+v*dt
        
        #Add time and append time and height to lists
        t = t+data['deltat']
        data['pm_t'].append(t)
        data['pm_posy'].append(ball_nd.pos.y)


def motion_drag(data):
    """
    Create animation for projectile motion with no dragging force
    :data: dictionary to hold data
    :return: Nothing
    """

    ball_nd = sphere(pos=vector(-data['grnd_size']/2, data['init_height'], 0),
                        radius=1, color=color.red, make_trail=True)
    
    # Follow the movement of the ball
    scene.camera.follow(ball_nd)
   
    # Set initial velocity & position
    ball_nd.m = data['ball_mass']
    ball_nd.v = (vec(data['init_velocity']*cos(data['theta']*pi/180), data['init_velocity']*sin(data['theta']*pi/180),0))  #velocity of ball
   
    #set gravity force vector (accelleration in only the y direction)
    fgrav = vec(0, data['gravity'], 0)

    # set time to 0 and add first time and position point to list
    t = 0
    data['pmdrag_t'].append(t)
    data['pmdrag_posy'].append(ball_nd.pos.y)

    # Animate
    while ball_nd.pos.y >= 0:
        rate(100)
        force = data['ball_mass']*fgrav #Calculate Force (vector): F=M*A
        fdx = data['alpha'] * (ball_nd.v.x)**2 #Calculate Fd air resistance in x direction (-1/2*p*Cd*A*Vx^2 )
        fdy = data['alpha'] * (ball_nd.v.y)**2 #Calculate Fd air resistance in y direction (-1/2*p*Cd*A*Vy^2 )
        fd = vec(fdx,fdy,0) # Set Fd air resistance force (vector)
        totf = force+fd #Add the force of gravity and the force of air resistance (vector)

        ball_nd.v = ball_nd.v+(totf/data['ball_mass']*data['deltat']) #V = v0+a*dt. (force/ball_mass = acceleratioin)
        ball_nd.pos = ball_nd.pos + ball_nd.v*data['deltat'] #X= x0+v*dt
        
        #Add time and append time and height to lists
        t = t+data['deltat']
        data['pmdrag_t'].append(t)
        data['pmdrag_posy'].append(ball_nd.pos.y)


def plot_data(data):
    """
    Set Vpython Scene
    :data: dictionary to hold data
    :return: Nothing
    """
    plt.figure()
    # Plot = Row, Col, selected sublot
    #plt.subplot(2, 1, 1)                # select first subplot
    plt.title("Projectile Motion")
    plt.plot(data['pm_t'], data['pm_posy'], '-b', label='No Air Resistance')   
    plt.plot(data['pmdrag_t'], data['pmdrag_posy'], '-r', label='With Air Resistance')       
    plt.ylabel("Height (m)")
    plt.xlabel("Time (s)")
    plt.legend()
    plt.show()      # display plot



def myhelp():
    """
    Help Function
    """
    print("Usage: ", sys.argv[0], "<VELOCITY> <POSITION> [HEIGHT]")
    exit(0)

def main():
    """
    """

    # if len(sys.argv) < 3:
    #     print("Error")
    #     myhelp()

    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description="Projectile Motion Demo")

    parser.add_argument("--velocity", "-v", action="store", dest="velocity", type=float, default=20, required=True, help="Velocity in m/s - (Default: 20.0)")
    parser.add_argument("--angle", "-a", action="store", dest="angle", type=float, default=40, required=True, help="Angle in Meters - (Default: 40.0)")
    parser.add_argument("--height", "-ht", action="store", dest="height", type=float, default=1.2, help="Height in Meters - (Default: 1.2)")


    args = parser.parse_args()
    print(args.velocity)

    # Set Variables
    data = {}       # empty dictionary for all data and variables
    data['init_height'] = args.height   # y-axis
    data['init_velocity'] = args.velocity  # m/s
    data['theta'] = args.angle       # degrees
    # Constants
    data['rho'] = 1.225  # kg/m^3
    data['Cd'] = 0.5    # coefficient friction
    data['deltat'] = 0.005
    data['gravity'] = -9.8  # m/s^2

    data['ball_mass'] = 0.145  # kg
    data['ball_radius'] = 0.075  # meters
    data['ball_area'] = pi * data['ball_radius']**2
    data['alpha'] = data['rho'] * data['Cd'] * data['ball_area'] / -2.0 #rho = air densitiy. Cd = dragCoeffecient. A = ball area
    #data['beta'] = data['alpha'] / data['ball_mass']

    # List to hold plot points
    data['pm_t'] = []
    data['pm_posy'] = []
    data['pmdrag_t'] = []
    data['pmdrag_posy'] = []

    data['grnd_size'] = 100
    # Set Scene
    set_scene(data)
    # 2) No Drag Animation
    motion_no_drag(data)
    # 3) Drag Animation
    motion_drag(data)
    # 4) Plot Information: extra credit
    plot_data(data)


if __name__ == "__main__":
    main()
    exit(0)

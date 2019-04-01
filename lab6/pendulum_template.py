import numpy as np
from matplotlib import pyplot as plt
from vpython import *
from math import sin, cos
#import argparse

g = 9.81    # m/s**2
l = 0.1     # meters length
W = 0.002   # arm radius
R = .01     # ball radius
m1 = .1 #ball mass in kg
framerate = 100
steps_per_frame = 10
dt = 0.01 # time interval


def set_scene():
        """
        Add title and caption to scene
        """
        scene.title = "Assignment 6: Pendulum"
#     scene.width = 600
#     scene.heigth = 1200
#     scene.center=vector(0,.01,0)
        scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
        To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
        On a two-button mouse, middle is left + right.
        Touch screen: pinch/extend to zoom, swipe or two-finger rotate.
        """

def f(r):
        """
        Pendulum formula with drag
        """
        theta = r[0] # Angular positions theta(0)
        omega = r[1] # Angular speed omega(w)
        ftheta = omega
        fomega = -(g/l)*np.sin(theta)-1.5*omega # Angular acceleration alpha(oc) - cw
    
        return np.array([ftheta, fomega])
   


def motion(data):
        """
        Create vpython objects. Loop over time interval. Runk Kutta pendulum formula. Animate and update vpython positions
        :data: dictionary to hold data
        :return: Nothing
        """
        #Roof and Cylindar Pivot Pisition
        data['p'] = vec(0,0,0) 
        
        #Vpython objects 
        sky=box(pos=data['p'],size=vec(.01,0.01,.01), color=color.green)
        ball=sphere(pos=vec(data['x'], data['y'],0),radius=R, color=color.blue)
        arm=cylinder(pos=data['p'],axis=ball.pos-data['p'],radius=W,color=color.red)

         #Vpython objects
        ball2=sphere(pos=vec(data['x2'], data['y2'],0),radius=R, color=color.yellow)
        arm2=cylinder(pos=data['p'],axis=ball2.pos-data['p'],radius=W,color=color.red)

        # Loop over some time interval
        t = 0 # time
        while t < 50:
                
                rate(framerate)

                # F = f(data['r'])
                # data['r'][1] += data['h']*F[1]   #OMEGA
                # data['r'][0] += data['h']* data['r'][1]   #THETA

                # F = f(data['r2'])
                # data['r2'][1] += data['h2']*F[1]   #OMEGA
                # data['r2'][0] += data['h2']* data['r2'][1]   #THETA

                #Use the 4'th order Runga-Kutta approximation Ball 1
                k1 = data['h']*f(data['r'])
                k2 = data['h']*f(data['r']+0.5*k1)
                k3 = data['h']*f(data['r']+0.5*k2)
                k4 = data['h']*f(data['r']+k3)
                data['r'] += (k1 + 2*k2 + 2*k3 + k4)/6

                #Use the 4'th order Runga-Kutta approximation Ball 1
                k1 = data['h2']*f(data['r2'])
                k2 = data['h2']*f(data['r2']+0.5*k1)
                k3 = data['h2']*f(data['r2']+0.5*k2)
                k4 = data['h2']*f(data['r2']+k3)
                data['r2'] += (k1 + 2*k2 + 2*k3 + k4)/6

                # Lists of change in Theta and Time for Graph
                data['time'].append(t)#
                data['theta'].append(data['r'][0])#
                data['time2'].append(t)#
                data['theta2'].append(data['r2'][0])#


                t += dt
        #        # Update x and y positions
                data['x'] = l*np.sin(data['r'][0])
                data['y'] = -l*np.cos(data['r'][0])
                data['x2'] = l*np.sin(data['r2'][0])
                data['y2'] = -l*np.cos(data['r2'][0])
                
                # Update the pendulum's bob
                ball.pos = vec(data['x'],data['y'],0)
                # Update the cylinder axis
                arm.axis=ball.pos-arm.pos

                # Update the pendulum's bob
                ball2.pos = vec(data['x2'],data['y2'],0)
                # Update the cylinder axis
                arm2.axis=ball2.pos-arm2.pos

               
def plot_data(data):
        """
        Set Vpython Scene
        :data: dictionary to hold data
        :return: Nothing
        """
        plt.figure()
        # Plot = Row, Col, selected sublot
        #plt.subplot(2, 1, 1)                
        plt.title("Pendulum: Theta over Time")
        plt.plot(data['time'], data['theta'], '-b', label='Ball 1: theta = 179')   
        plt.plot(data['time2'], data['theta2'], '-r', label='Ball 2: theta = 90')         
        plt.ylabel("Theta (rad)")
        plt.xlabel("Time")
        plt.legend()
        plt.show()      # display plot

def myhelp():
        """
        Help Function
        """
        print("Usage: ", sys.argv[0], "Pendulum Simulation")
        exit(0)

def main():
        """
        Set Initial Parameters, then simulate pendulum animation
        :data: dictionary to hold data
        :return: Nothing
        """
        # Set up initial values

        # empty dictionary for all data and variables
        data = {}      
        data['time'] = []
        data['theta'] = []
        data['time2'] = []
        data['theta2'] = []

        # Initial conditions 1
        data['h'] = 1.0/(framerate * steps_per_frame) # Size of step
        data['r'] = np.array([179*np.pi/180, 0], float) #r = Angles that ball is dropped from (initial upper angle from vertical)

        # Initial 1 x and y 
        data['x'] = l*np.sin( data['r'][0]) 
        data['y'] = -l*np.cos(data['r'][0]) 

        # Initial conditions 2
        data['h2'] = 1.0/(framerate * steps_per_frame) # Size of step
        data['r2'] = np.array([90*np.pi/180, 0], float) #r = Angles that ball is dropped from (initial upper angle from vertical)

        # Initial x2 and y2 
        data['x2'] = l*np.sin( data['r'][0]) 
        data['y2'] = -l*np.cos(data['r'][0])


        #1) Set Scene
        set_scene()
        #2) Ball Animation
        motion(data)
        #3) Plot Information
        plot_data(data)
    

    


if __name__ == "__main__":
        main()
        exit(0)
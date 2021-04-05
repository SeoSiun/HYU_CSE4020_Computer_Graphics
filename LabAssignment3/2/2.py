import glfw
from OpenGL.GL import *
import numpy as np

global gComposedM

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gComposedM
    if key == glfw.KEY_W:
        if action==glfw.PRESS or action==glfw.REPEAT:
            M=np.array([[1., 0.,0.],
                        [0., .9,0.],
                        [0.,0.,1.]])
            gComposedM=M @ gComposedM
    elif key== glfw.KEY_E:
        if action==glfw.PRESS or action==glfw.REPEAT:
            M=np.array([[1.,0.,0.],
                       [0.,1.1,0.],
                       [0.,0.,1.]])
            gComposedM=M@gComposedM
    elif key== glfw.KEY_S:
        if action==glfw.PRESS or action==glfw.REPEAT:
            M=np.array([[np.cos(np.pi/18),-np.sin(np.pi/18),0.],
                      [np.sin(np.pi/18),np.cos(np.pi/18),0.],
                      [0.,0.,1.]])
            gComposedM=M@gComposedM
    elif key== glfw.KEY_D:
        if action==glfw.PRESS or action==glfw.REPEAT:
            M=np.array([[np.cos(-1*np.pi/18),-np.sin(-1*np.pi/18),0.],
                      [np.sin(-1*np.pi/18),np.cos(-1*np.pi/18),0.],
                      [0.,0.,1.]])
            gComposedM=M@gComposedM
    elif key== glfw.KEY_X:
        if action==glfw.PRESS or action==glfw.REPEAT:
            M=np.array([[1.,0.,0.1],
                       [0.,1.,0.],
                       [0.,0.,1.]])
            gComposedM=M@gComposedM
    elif key== glfw.KEY_C:
        if action==glfw.PRESS or action==glfw.REPEAT:
            M=np.array([[1.,0.,-0.1],
                       [0.,1.,0.],
                       [0.,0.,1.]])
            gComposedM=M@gComposedM
    elif key== glfw.KEY_R:
        if action==glfw.PRESS or action==glfw.REPEAT:
            M=np.array([[-1.,0.,0.],
                       [0.,-1.,0.],
                       [0.,0.,1.]])
            gComposedM=M@gComposedM
    elif key== glfw.KEY_1:
        if action==glfw.PRESS or action==glfw.REPEAT:
            gComposedM=np.identity(3)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2019019016", None,None)
    if not window:
        glfw.terminate()
        return
    
    global gComposedM
    gComposedM= np.identity(3)
    glfw.set_key_callback(window,key_callback)
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render(gComposedM)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()


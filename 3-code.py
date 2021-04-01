###################################################
# [Practice] Uniform Scale
import glfw
from OpenGL.GL import *
import numpy as np

def render(M):
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

    # draw triangle - p'=Mp
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv(M @ np.array([0.0,0.5]))
    glVertex2fv(M @ np.array([0.0,0.0]))
    glVertex2fv(M @ np.array([0.5,0.0]))
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640,640,"2D Trans", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        M = np.array([[2.,0.],
                      [0.,2.]])
        render(M)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

###################################################
# [Practice] Animate It!
def main():
    if not glfw.init():
        return
    window = glfw.create_window(640,640,"2D Trans", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    # set the number of screen refresh to wait before calling glfw.swap_buffer().
    # if your monitor refresh rate is 60Hz, the while loop is repeated every 1/60 sec
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # get the current time, in seconds
        t = glfw.get_time()

        s = np.sin(t)
        M = np.array([[s,0.],
                      [0.,s]])
        render(M)

        glfw.swap_buffers(window)
    glfw.terminate()

###################################################
# [Practice] Nonuniform Scale, Rotation, Reflection, Shear
    while not glfw.window_should_close(window):
        glfw.poll_events()
        t = glfw.get_time()

        # nonuniform scale
        s = np.sin(t)
        M = np.array([[s,0.],
                      [0.,s*.5]])
        # rotation
        th = t
        M = np.array([[np.cos(th), -np.sin(th)],
                      [np.sin(th), np.cos(th)]])
        # reflection
        M = np.array([[-1.,0.],
                      [0.,1.]])
        # shear
        a = np.sin(t)
        M = np.array([[1.,a],
                      [0.,1.]])

        render(M)
        glfw.swap_buffers(window)

###################################################
# [Practice] Translation
def render(u):
    # ...
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv(np.array([0.0,0.5]) + u)
    glVertex2fv(np.array([0.0,0.0]) + u)
    glVertex2fv(np.array([0.5,0.0]) + u)
    glEnd()

def main():
    # ...
    while not glfw.window_should_close(window):
        glfw.poll_events()
        t = glfw.get_time()

        u = np.array([np.sin(t), 0.])
        render(u)
        # ...

###################################################
# [Practice] Affine Transformation
def render(M, u):
    # ...
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv(M @ np.array([0.0,0.5]) + u)
    glVertex2fv(M @ np.array([0.0,0.0]) + u)
    glVertex2fv(M @ np.array([0.5,0.0]) + u)
    glEnd()

def main():
    # ...
    while not glfw.window_should_close(window):
        glfw.poll_events()
        t = glfw.get_time()

        th = t
        R = np.array([[np.cos(th), -np.sin(th)],
                      [np.sin(th), np.cos(th)]])
        u = np.array([np.sin(t), 0.])
        render(R, u)
        # ...

###################################################
# [Practice] Composition
def main():
    # ...
    while not glfw.window_should_close(window):
        glfw.poll_events()

        S = np.array([[1.,0.],
                      [0.,2.]])

        th = np.radians(60)
        R = np.array([[np.cos(th), -np.sin(th)],
                      [np.sin(th), np.cos(th)]])

        u = np.zeros(2)

        # compare results of these two lines
        render(R @ S, u)
        # render(S @ R, u)

        # ...

###################################################
# [Practice] Homogeneous Coordinates
def render(M):
    # ...
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (M @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (M @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (M @ np.array([.5,.0,1.]))[:-1] )
    glEnd()

def main():
    # ...
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # rotate 60 deg about z axis
        th = np.radians(60)
        R = np.array([[np.cos(th), -np.sin(th),0.],
                      [np.sin(th), np.cos(th),0.],
                      [0.,         0.,        1.]])

        # translate by (.4, .1)
        T = np.array([[1.,0.,.4],
                      [0.,1.,.1],
                      [0.,0.,1.]])

        render(R)
        # render(T)
        # render(T @ R)
        # render(R @ T)
        # ...


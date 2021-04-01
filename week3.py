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

    # [Practice] Nonuniform Scale, Rotation, Reflection, Shear
    while not glfw.window_should_close(window):
        glfw.poll_events()
        t = glfw.get_time()

        # nonuniform scale
        #s = np.sin(t)
        #M = np.array([[s,0.],[0.,s*.5]])

        # rotation
        #th = t
        #M = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])

        # reflection
        #M = np.array([[-1.,0.],[0.,1.]])

        # shear
        #a = np.sin(t)
        #M = np.array([[1.,a],[0.,1.]])

	#indentity
        M = np.identity(2, dtype=int)

        render(M)
        glfw.swap_buffers(window)

if __name__ == "__main__":
    main()
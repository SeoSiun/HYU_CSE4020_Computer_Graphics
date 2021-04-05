import glfw
from OpenGL.GL import *
import numpy as np


def render():
    global keyPressed
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    for i in range(0,12):
        glVertex2f(np.cos(i*30*np.pi/180),np.sin(i*30*np.pi/180))
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(0.0,0.0)
    glVertex2f(np.cos(keyPressed*30*np.pi/180),np.sin(keyPressed*30*np.pi/180))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global keyPressed
    if key==glfw.KEY_1:
        keyPressed=2
    elif key==glfw.KEY_2:
        keyPressed=1
    elif key==glfw.KEY_3:
        keyPressed=0
    elif key==glfw.KEY_4:
        keyPressed=11
    elif key==glfw.KEY_5:
        keyPressed=10
    elif key==glfw.KEY_6:
        keyPressed=9
    elif key==glfw.KEY_7:
        keyPressed=8
    elif key==glfw.KEY_8:
        keyPressed=7
    elif key==glfw.KEY_9:
        keyPressed=6
    elif key==glfw.KEY_0:
        keyPressed=5
    elif key==glfw.KEY_Q:
        keyPressed=4
    elif key==glfw.KEY_W:
        keyPressed=3
    

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2019019016", None,None)
    if not window:
        glfw.terminate()
        return

    global keyPressed
    keyPressed=3
    glfw.set_key_callback(window,key_callback)


    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        render()

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

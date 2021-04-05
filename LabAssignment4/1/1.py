import glfw
from OpenGL.GL import *
import numpy as np


def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    
    glColor3ub(255, 255, 255)

    global keyList
    if keyList[0]!='1':
        keys = list(reversed(keyList));
        for key in keys:
            if key=='Q':
                glTranslatef(-0.1, 0,0)
            elif key=='E':
                glTranslatef(0.1,0,0)
            elif key=='A':
                glRotatef(10,0,0,1)
            elif key=='D':
                glRotatef(-10,0,0,1)
        

    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global keyList
    if key == glfw.KEY_Q:
        if action==glfw.PRESS or action==glfw.REPEAT:
            if keyList[0]=='1':
                keyList[0]='Q'
            else:
                keyList.append('Q');
    elif key== glfw.KEY_E:
        if action==glfw.PRESS or action==glfw.REPEAT:
            if keyList[0]=='1':
                keyList[0]='E'
            else:
                keyList.append('E');
    elif key== glfw.KEY_A:
        if action==glfw.PRESS or action==glfw.REPEAT:
            if keyList[0]=='1':
                keyList[0]='A'
            else:
                keyList.append('A');
    elif key== glfw.KEY_D:
        if action==glfw.PRESS or action==glfw.REPEAT:
            if keyList[0]=='1':
                keyList[0]='D'
            else:
                keyList.append('D');
    elif key== glfw.KEY_1:
        if action==glfw.PRESS or action==glfw.REPEAT:
            keyList=['1'];
            

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2019019016", None,None)
    if not window:
        glfw.terminate()
        return
    
    global keyList
    keyList=['1']
    glfw.set_key_callback(window,key_callback)
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

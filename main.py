import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# draw a cube of side 1, centered at the origin.
def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)

    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-1.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,-1.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,-1]))
    glVertex3fv(np.array([0.,0.,1.]))
    glColor3ub(102,102,102)
    for i in range(-50,51):
        glVertex3fv(np.array([0.5*i,0.,1000.]))
        glVertex3fv(np.array([0.5*i,0.,-1000.]))
        glVertex3fv(np.array([1000.,0.,0.5*i]))
        glVertex3fv(np.array([-1000.,0.,0.5*i]))
    glEnd()

def render():
    global cam
    global isOrtho
    global tpoint
    global elev
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()
    
    if isOrtho:
        glOrtho(-5,5,-5,5,-10,10)
    else:
        gluPerspective(45, 1, 1,10)

    if elev%360 >=0 and elev%360 <180:
        y=1
    else:
        y=-1


    gluLookAt(cam[0],cam[1],cam[2],tpoint[0],tpoint[1],tpoint[2],0,y,0)


    drawFrame()
    glColor3ub(255, 255, 255)
    drawUnitCube()

def key_callback(window, key, scancode, action, modes):
    global isOrtho
    if key==glfw.KEY_V:
        if action == glfw.PRESS:
            isOrtho = not isOrtho
        
       
def cursor_callback(window, xpos, ypos_):
    global leftPressed
    global rightPressed
    global pressPoint
    global cam
    global tpoint
    global elev
    global azim
    global d
    
    currentPoint = np.array([xpos, ypos_])
    
    if leftPressed or rightPressed:
        v = currentPoint - pressPoint
        azim -= 0.01 * v[0]
        elev -= 0.01 * v[1]
        print("azim : ",azim ,", elev: ",elev)

        a=np.radians(azim%360)
        e=np.radians(elev%360)
        tmp = np.array([d*np.sin(a)*np.cos(e),d*np.sin(e),d*np.cos(e)*np.cos(a)])
        if rightPressed:
            tpoint -= (tmp-cam)
        cam = tmp
        
 
def button_callback(window,button,action,mod):
    global leftPressed
    global rightPressed
    global pressPoint

    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            leftPressed=True
            pressPoint = np.array(glfw.get_cursor_pos(window))
        elif action == glfw.RELEASE:
            leftPressed=False

    if button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            rightPressed = True
            pressPoint = np.array(glfw.get_cursor_pos(window))
        elif action == glfw.RELEASE:
            rightPressed = False
            


def scroll_callback(window, xoffset, yoffset):
    global d
    global azim
    global radians
    global cam
    
    d += yoffset
    a=np.radians(azim%360)
    e=np.radians(elev%360)
    cam = np.array([d*np.sin(a)*np.cos(e),d*np.sin(e),d*np.cos(e)*np.cos(a)])

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800,800,'ClassAssignment1', None,None)
    if not window:
        glfw.terminate()
        return
    
    global leftPressed
    leftPressed = False
    global rightPressed
    rightPressed = False
    global isOrtho
    isOrtho=False
    global elev
    elev = 35.264
    global azim
    azim = 45
    global d
    d = 5.196
    global cam
    cam= np.array([3.,3.,3.])
    global tpoint
    tpoint = np.array([0.,0.,0.])

    glfw.set_key_callback(window,key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window,scroll_callback)
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

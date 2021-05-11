import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo

gCamAng = 0.
gCamHeight = 1.


def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -1 ,  1 ,  1 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  1 ,  1 ,  1 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  1 , -1 ,  1 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -1 , -1 ,  1 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -1 ,  1 , -1 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  1 ,  1 , -1 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  1 , -1 , -1 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([3.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,3.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,3.]))
    glEnd()

def draw(R,R_):
    R1 = np.identity(4)
    R1[:3,:3]=R
    R2 = np.identity(4)
    R2[:3,:3]=R_

    J1 = R1
    
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    T1 = np.identity(4)
    T1[0][3] = 1.
    J2 = R1 @ T1 @ R2

    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

def getR(x,y,z):
    x=np.radians(x)
    y=np.radians(y)
    z=np.radians(z)

    Rx = np.array([[1,0,0],
                   [0, np.cos(x), -np.sin(x)],
                   [0, np.sin(x), np.cos(x)]])
    Ry = np.array([[np.cos(y), 0, np.sin(y)],
                   [0,1,0],
                   [-np.sin(y), 0, np.cos(y)]])
    Rz = np.array([[np.cos(z), -np.sin(z), 0],
                   [np.sin(z), np.cos(z), 0],
                   [0,0,1]])
    return Rx@Ry@Rz


def l2norm(v):
    return np.sqrt(np.dot(v, v))

def normalized(v):
    l = l2norm(v)
    return 1/l * np.array(v)

def lerp(v1, v2, t):
    return (1-t)*v1 + t*v2

def exp(rv):
    th = l2norm(rv)
    u = normalized(rv)
    cos = np.cos(th)
    sin = np.sin(th)
    return np.array([[cos+u[0]*u[0]*(1-cos), u[0]*u[1]*(1-cos)-u[2]*sin, u[0]*u[2]*(1-cos)+u[1]*sin],
                     [u[1]*u[0]*(1-cos)+u[2]*sin, cos+u[1]*u[1]*(1-cos), u[1]*u[2]*(1-cos)-u[0]*sin],
                     [u[2]*u[0]*(1-cos)-u[1]*sin, u[2]*u[1]*(1-cos)+u[0]*sin, cos+u[2]*u[2]*(1-cos)]])

def log(R):
    tr = R[0,0]+R[1,1]+R[2,2]
    if tr == 3:
        w=np.array([0,0,0])
        th=0
    elif tr==-1:
        th=np.pi
        v1 = np.array([R[0,2],R[1,2],R[2,2]+1]/np.sqrt(2*(1+R[2,2])))
        v2 = np.array([R[0,1],R[1,1]+1,R[2,1]]/np.sqrt(2*(1+R[1,1])))
        v3 = np.array([R[0,0]+1,R[1,0],R[2,0]]/np.sqrt(2*(1+R[0,0])))
        if v1 != [0,0,0]:
            w=v1
        elif v2 != [0,0,0]:
            w=v2
        elif v3 != [0,0,0]:
            w=v3
    else:
        th = np.arccos((tr-1)/2)
        w = np.array([R[2,1]-R[1,2],R[0,2]-R[2,0],R[1,0]-R[0,1]])/(2*np.sin(th))

    w=normalized(w)
    return w*th

def slerp(R1,R2,t):
    if t==0:
        return R1
    return R1 @ exp(t*log((R1.T)@R2))
    

def render(t):
    global gCamAng, gCamHeight,cnt
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    # draw global frame
    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    objectColor = (1.,0.,0.,1.)
    specularObjectColor = (1.,0.,0.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    R1_0 = getR(20,30,30)
    R2_0 = getR(15,30,25)
    draw(R1_0,R2_0)

    objectColor = (1.,1.,0.,1.)
    specularObjectColor = (1.,1.,0.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    R1_20 = getR(45,60,40)
    R2_20 = getR(25,40,40)
    draw(R1_20,R2_20)

    objectColor = (0.,1.,0.,1.)
    specularObjectColor = (0.,1.,0.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    R1_40 = getR(60,70,50)
    R2_40 = getR(40,60,50)
    draw(R1_40,R2_40)

    objectColor = (0.,0.,1.,1.)
    specularObjectColor = (0.,0.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    R1_60 = getR(80,85,70)
    R2_60 = getR(55,80,65)
    draw(R1_60,R2_60)

    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    if cnt<=20:
        R1=slerp(R1_0,R1_20,cnt/20)
        R2=slerp(R2_0,R2_20,cnt/20)
    elif cnt<=40:
        R1=slerp(R1_20,R1_40,(cnt-20)/20)
        R2=slerp(R2_20,R2_40,(cnt-20)/20)
    elif cnt<=60:
        R1=slerp(R1_40,R1_60,(cnt-40)/20)
        R2=slerp(R2_40,R2_60,(cnt-40)/20)
        if cnt==60:
            cnt=-1
    draw(R1,R2)
    cnt+=1

    glDisable(GL_LIGHTING)


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray,cnt
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2019019016', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    cnt=0
    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        t = glfw.get_time()
        render(t)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()


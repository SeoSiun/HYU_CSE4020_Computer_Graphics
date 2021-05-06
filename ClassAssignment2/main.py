import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

global varr

def getAngle(a):
    if a<0:
        return 360+a
    elif a>360:
        return a-360
    else:
        return a

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glColor3ub(102,102,102)
    for i in range(-60,60):
        glVertex3fv(np.array([0.5*i,0.,1000.]))
        glVertex3fv(np.array([0.5*i,0.,-1000.]))
        glVertex3fv(np.array([1000.,0.,0.5*i]))
        glVertex3fv(np.array([-1000.,0.,0.5*i]))
    glEnd()

def render():
    global isOrtho, isSingleMesh, isWireFrame
    global tpoint
    global elev, azim
    global v, u
    global harr
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if isWireFrame:
        glDisable(GL_LIGHTING)
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    else:
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    glLoadIdentity()
    
    if isOrtho:
        glOrtho(-5,5,-5,5,-10,10)
    else:
        gluPerspective(45, 1, 1,10)

    a=np.radians(azim)
    e=np.radians(elev)
    cpoint = np.array([tpoint[0]+d*np.sin(a)*np.cos(e),tpoint[1]+d*np.sin(e),tpoint[2]+d*np.cos(e)*np.cos(a)])
    if elev<=90 or elev>270:
        up = np.array([0.,1.,0.])
    else:
        up = np.array([0.,-1.,0.])

    
    gluLookAt(cpoint[0],cpoint[1],cpoint[2],tpoint[0],tpoint[1],tpoint[2],up[0],up[1],up[2])

    w = (cpoint-tpoint) / np.sqrt(np.dot(cpoint-tpoint,cpoint-tpoint))
    u = np.cross(up,w) / np.sqrt(np.dot(np.cross(up,w),np.cross(up,w)))
    v = np.cross(w,u)

    glDisable(GL_LIGHTING)
    drawFrame()

    if not isWireFrame:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)
        glEnable(GL_NORMALIZE)
        

        glPushMatrix()
        lightPos = (10.,10.,0.,0.)
        glLightfv(GL_LIGHT0,GL_POSITION,lightPos)

        lightColor = (0.,0.,1.,1.)
        ambientLightColor = (.0,.0,.1,1.)
        glLightfv(GL_LIGHT0,GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT0,GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT0,GL_AMBIENT, ambientLightColor)
        glPopMatrix()

        glPushMatrix()
        lightPos = (-10.,0.,0.,0.)
        glLightfv(GL_LIGHT1,GL_POSITION,lightPos)

        lightColor = (1.,0.,0.,1.)
        ambientLightColor = (.1,.0,.0,1.)
        glLightfv(GL_LIGHT1,GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT1,GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT1,GL_AMBIENT, ambientLightColor)
        glPopMatrix()

        glPushMatrix()
        lightPos = (-10.,0.,-10.,0.)
        glLightfv(GL_LIGHT2,GL_POSITION,lightPos)

        lightColor = (0.,1.,0.,1.)
        ambientLightColor = (.0,.1,.0,1.)
        glLightfv(GL_LIGHT2,GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT2,GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT2,GL_AMBIENT, ambientLightColor)
        glPopMatrix()

        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS,10)
        glMaterialfv(GL_FRONT, GL_SPECULAR,specularObjectColor)

    glColor3ub(255,255,255)
    if len(varr)!=0 and isSingleMesh:
        draw(varr)
    elif not isSingleMesh:
        draw(harr[0])
        draw(harr[1])
        draw(harr[2])
        draw(harr[3])
        

def draw(varr):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize,
                    ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES,0,int(varr.size/6))


def key_callback(window, key, scancode, action, modes):
    global isOrtho,isSingleMesh,isWireFrame
    
    if key==glfw.KEY_V:
        if action == glfw.PRESS:
            isOrtho = not isOrtho
    if key==glfw.KEY_H:
        if action == glfw.PRESS:
            isSingleMesh = not isSingleMesh
    if key==glfw.KEY_Z:
        if action == glfw.PRESS:
            isWireFrame = not isWireFrame
        
       
def cursor_callback(window, xpos, ypos_):
    global leftPressed, rightPressed
    global pressPoint
    global tpoint
    global elev, azim
    global v,u
    
    currentPoint = np.array([xpos, ypos_])

    if leftPressed:
        diff = currentPoint - pressPoint
        azim -= 0.005 * diff[0]
        azim = getAngle(azim)
        elev += 0.005 * diff[1]
        elev = getAngle(elev)

    elif rightPressed:
        diff=currentPoint - pressPoint
        tpoint = tpoint + v*diff[1]*0.0002 - u*diff[0]*0.0002
        
 
def button_callback(window,button,action,mod):
    global leftPressed, rightPressed
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
    d -= yoffset

def drop_callback(window, paths):
    global varr
    
    vertex = []
    normal = []
    varr = []
    face=0
    face3=0
    face4=0
    faceMoreThan4=0
    
    f = open(paths[0])
    name = paths[0].split('\\')
    print("File name : " ,name[len(name)-1])
    while True:
        line = f.readline()
        if not line: break
        
        s = line.split()
        if s[0] == 'v':
            vertex.append((float(s[1]),float(s[2]),float(s[3])))
        elif s[0] == 'vn':
            normal.append((float(s[1]),float(s[2]),float(s[3])))
        elif s[0] == 'f':
            pair = []
            face+=1
            for i in range(1,len(s)):
                v,t,n = s[i].split('/')
                pair.append((int(n)-1,int(v)-1))
            pair = np.array(pair)
            for i in range(1,len(s)-2):
                varr.append(normal[pair[0,0]])
                varr.append(vertex[pair[0,1]])
                varr.append(normal[pair[i,0]])
                varr.append(vertex[pair[i,1]])
                varr.append(normal[pair[i+1,0]])
                varr.append(vertex[pair[i+1,1]])
            if len(s)-1==3:
                face3+=1
            elif len(s)-1==4:
                face4+=1
            else:
                faceMoreThan4+=1
    f.close()
    varr = np.array(varr,'float32') 
    print("Total number of faces : ",face)
    print("Number of faces with 3 vertices : ",face3)
    print("Number of faces with 4 vertices : ",face4)
    print("Number of faces with moer than 4 vertices : ",faceMoreThan4,"\n")

def hierarchical():
    global harr
    
    harr=[]
    vertex=[]
    normal=[]
    temp=[]
    
    f=open("leg.obj")
    while True:
        line = f.readline()
        if not line: break
        
        s = line.split()
        if s[0] == 'o' and len(temp)!=0:
            print(line)
            print(temp)
            harr.append(temp)
            temp=[]
            vertex=[]
            normal=[]
        elif s[0] == 'v':
            vertex.append((float(s[1]),float(s[2]),float(s[3])))
        elif s[0] == 'vn':
            normal.append((float(s[1]),float(s[2]),float(s[3])))
        elif s[0] == 'f':
            pair = []
            for i in range(1,len(s)):
                v,t,n = s[i].split('/')
                pair.append((int(n)-1,int(v)-1))
            pair = np.array(pair)
            for i in range(1,len(s)-2):
                temp.append(normal[pair[0,0]])
                temp.append(vertex[pair[0,1]])
                temp.append(normal[pair[i,0]])
                temp.append(vertex[pair[i,1]])
                temp.append(normal[pair[i+1,0]])
                temp.append(vertex[pair[i+1,1]])
    harr.append(temp)
    harr=np.array(harr)
    print(harr)
    f.close()
    

def main():
    global leftPressed, rightPressed
    global isOrtho, isSingleMesh,isWireFrame
    global elev, azim
    global d
    global tpoint
    global varr
    global harr

    
    if not glfw.init():
        return
    window = glfw.create_window(900,900,'ClassAssignment2', None,None)
    if not window:
        glfw.terminate()
        return

    leftPressed = False
    rightPressed = False
    isOrtho=False
    isSingleMesh = True
    elev = 35.264
    azim = 45
    d = 5.196
    tpoint = np.array([0.,0.,0.])
    varr=[]
    isWireFrame=True
    hierarchical()

    glfw.set_key_callback(window,key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window,scroll_callback)
    glfw.set_drop_callback(window,drop_callback)
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

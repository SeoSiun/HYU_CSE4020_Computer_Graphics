import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

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
    global isOrtho, isSingleMesh, isWireFrame, isForce
    global tpoint
    global elev, azim
    global v, u
    global varr,iarr,vertex,avrNorm,harr, hiarr,hvarr,havrNorm
    
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
        gluPerspective(50, 3/2, 1,10)

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
        glEnable(GL_LIGHT3)

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

        glPushMatrix()
        lightPos = (10.,10.,10.,1.)
        glLightfv(GL_LIGHT3,GL_POSITION,lightPos)

        lightColor = (1.,1.,1.,1.)
        ambientLightColor = (.1,.1,.1,1.)
        glLightfv(GL_LIGHT3,GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT3,GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT3,GL_AMBIENT, ambientLightColor)
        glPopMatrix()


    if len(varr)!=0 and isSingleMesh:
        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS,10)
        glMaterialfv(GL_FRONT, GL_SPECULAR,specularObjectColor)
        
        glColor3ub(255,255,255)
        if not isForce:
            draw(varr)
        else:
            drawSmooth(vertex,avrNorm,iarr)
        
    elif not isSingleMesh:
        t=glfw.get_time()
        
#body.obj
        # body
        glPushMatrix()
        glTranslatef(0,.0,2*np.sin(t/2))
        direction=np.cos(t/2)/abs(np.cos(t/2))

        objectColor = (.7,.7,.7,1.)
        specularObjectColor = (.07,.07,.07,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS,10)
        glMaterialfv(GL_FRONT, GL_SPECULAR,specularObjectColor)
        
        glPushMatrix()
        glColor3ub(180,180,180)
        if not isForce:
            draw(harr[4])
        else:
            drawSmooth(hvarr[0],havrNorm[0],hiarr[4])
        glPopMatrix()

        objectColor = (.5,.5,1.,1.)
        specularObjectColor = (.05,.05,.1,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS,10)
        glMaterialfv(GL_FRONT, GL_SPECULAR,specularObjectColor)

        #back wheel
        glPushMatrix()
        glTranslatef(0.,-.08,-0.7)
        glRotatef(t*(180/np.pi),direction,0,0)
        glTranslatef(0.,.08,0.7)
        glColor3ub(130,130,255)
        if not isForce:
            draw(harr[0])
            draw(harr[1])
        else:
            drawSmooth(hvarr[0],havrNorm[0],hiarr[0])
            drawSmooth(hvarr[0],havrNorm[0],hiarr[1])
        glPopMatrix()

        #front wheel
        glPushMatrix()
        glTranslatef(0.,-.02,0.8)
        glRotatef(t*(180/np.pi),direction,0,0)
        glTranslatef(0.,.02,-0.8)
        glColor3ub(130,130,255)
        if not isForce:
            draw(harr[2])
            draw(harr[3])
        else:
            drawSmooth(hvarr[0],havrNorm[0],hiarr[2])
            drawSmooth(hvarr[0],havrNorm[0],hiarr[3])
        glPopMatrix()


#circle.obj
        #circle
        glPushMatrix()
        glTranslatef(0.,1.42,-.1)
        glRotatef(90+30*np.sin(t/3),0,1,0)

        objectColor = (.25,.25,.6,1.)
        specularObjectColor = (.025,.025,.06,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS,10)
        glMaterialfv(GL_FRONT, GL_SPECULAR,specularObjectColor)

        glPushMatrix()
        glColor3ub(80,80,150)
        if not isForce:
            draw(harr[5])
        else:
            drawSmooth(hvarr[1],havrNorm[1],hiarr[5])
        glPopMatrix()

#fork.obj
        #first
        glPushMatrix()
        glColor3ub(130,130,255)
        
        objectColor = (.53,.53,1.,1.)
        specularObjectColor = (.053,.053,.1,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS,10)
        glMaterialfv(GL_FRONT, GL_SPECULAR,specularObjectColor)
        
        glPushMatrix()
        glTranslatef(0.,.15,0.)
        glRotatef(10*np.sin(t/2),0,0,1)

        if not isForce:
            draw(harr[8])
        else:
            drawSmooth(hvarr[2],havrNorm[2],hiarr[8])

        #second
        glPushMatrix()
        glTranslatef(-.64,.33,0)
        glRotatef(20*np.sin(t/3),0,0,1)
        glTranslatef(.64,-.33,0)

        if not isForce:
            draw(harr[7])
        else:
            drawSmooth(hvarr[2],havrNorm[2],hiarr[7])

        #bucket
        glPushMatrix()
        glTranslatef(-1.6,.22,0.)
        glRotatef(20*np.sin(t/3),0,0,1)
        glTranslatef(1.6,-.22,0.)
        
        if not isForce:
            draw(harr[6])
        else:
            drawSmooth(hvarr[2],havrNorm[2],hiarr[6])

        glPopMatrix()
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()
        

def draw(varr):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize,
                    ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES,0,int(varr.size/6))

def drawSmooth(varr,avrNorm,iarr):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3,GL_FLOAT, 3*varr.itemsize, varr)
    glNormalPointer(GL_FLOAT, 3*avrNorm.itemsize, avrNorm)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)
    
def key_callback(window, key, scancode, action, modes):
    global isOrtho,isSingleMesh,isWireFrame, isForce
    
    if key==glfw.KEY_V:
        if action == glfw.PRESS:
            isOrtho = not isOrtho
    if key==glfw.KEY_H:
        if action == glfw.PRESS:
            isSingleMesh = False
    if key==glfw.KEY_Z:
        if action == glfw.PRESS:
            isWireFrame = not isWireFrame
    if key==glfw.KEY_S:
        if action == glfw.PRESS:
            isForce = not isForce
        
       
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
    global varr,isSingleMesh,iarr,vertex,avrNorm
    vertex = []
    normal = []
    norm = []
    pairs=[]
    face=0
    face3=0
    face4=0
    faceMoreThan4=0
    vertexCnt=0
    
    f = open(paths[0])
    name = paths[0].split('\\')
    print("File name : " ,name[len(name)-1])
    while True:
        line = f.readline()
        if not line: break
        
        s = line.split()
        if s[0] == 'v':
            vertexCnt+=1
            vertex.append(np.array((float(s[1]),float(s[2]),float(s[3]))))
        elif s[0] == 'vn':
            normal.append((float(s[1]),float(s[2]),float(s[3])))
        elif s[0] == 'f':
            for i in range(vertexCnt):
                norm.append([])
            vertexCnt=0
            pair = []
            face+=1
            for i in range(1,len(s)):
                v,t,n = s[i].split('/')
                pair.append((int(n)-1,int(v)-1))
            pairs.append(np.array(pair))
            if len(s)-1==3:
                face3+=1
            elif len(s)-1==4:
                face4+=1
            else:
                faceMoreThan4+=1
    f.close()

    
    varr,iarr,norm=makeVarr(normal,vertex,pairs,norm)
    avrNorm = averageNorm(norm)
    varr = np.array(varr,'float32')
    iarr = np.array(iarr,'float32')
    vertex=np.array(vertex,'float32')
    avrNorm=np.array(avrNorm,'float32')
    
    print("Total number of faces : ",face)
    print("Number of faces with 3 vertices : ",face3)
    print("Number of faces with 4 vertices : ",face4)
    print("Number of faces with moer than 4 vertices : ",faceMoreThan4,"\n")
    isSingleMesh = True


def initHierarchical():
    global harr,fharr,hiarr,hvarr,havrNorm
    harr=[]
    fharr=[]
    hiarr=[]
    hvarr=[]
    havrNorm=[]

    f=open("body.obj")
    v,n=parseOBJ(f)
    hvarr.append(v)
    havrNorm.append(n)
    f.close()
    
    f=open("circle.obj")
    v,n=parseOBJ(f)
    hvarr.append(v)
    havrNorm.append(n)
    f.close()
    
    f=open("fork.obj")
    v,n=parseOBJ(f)
    hvarr.append(v)
    havrNorm.append(n)
    f.close()


def parseOBJ(f):
    global harr, hiarr
    vertex=[]
    normal=[]
    norm = []
    pairs=[]
    vertexCnt=0
    
    while True:
        line = f.readline()
        if not line: break
        
        s = line.split()

        if s[0] == 'o' and len(pairs)!=0:
            varr,iarr,norm=makeVarr(normal,vertex,pairs,norm)
            harr.append(np.array(varr,'float32'))
            hiarr.append(np.array(iarr,'float32'))
            pairs=[]
        elif s[0] == 'v':
            vertexCnt+=1
            vertex.append(np.array((float(s[1]),float(s[2]),float(s[3]))))
        elif s[0] == 'vn':
            normal.append((float(s[1]),float(s[2]),float(s[3])))
        elif s[0] == 'f':
            for i in range(vertexCnt):
                norm.append([])
            vertexCnt=0
            pair = []
            tmp=[]
            for i in range(1,len(s)):
                v,t,n = s[i].split('/')
                pair.append((int(n)-1,int(v)-1))
            pairs.append(np.array(pair))

    varr,iarr,norm=makeVarr(normal,vertex,pairs,norm)
    havrNorm = averageNorm(norm)
    harr.append(np.array(varr,'float32'))
    hiarr.append(np.array(iarr,'float32'))
    return np.array(vertex,'float32'),np.array(havrNorm,'float32')

def normalized(v):
    l = np.sqrt(np.dot(v, v))
    return (1/l) * np.array(v)
    
def makeVarr(normal,vertex,pairs,norm):
    varr=[]
    iarr=[]
    for pair in pairs:
        for i in range(1,len(pair)-1):
            varr.append(normal[pair[0,0]])
            varr.append(vertex[pair[0,1]])
            varr.append(normal[pair[i,0]])
            varr.append(vertex[pair[i,1]])
            varr.append(normal[pair[i+1,0]])
            varr.append(vertex[pair[i+1,1]])

            iarr.append(pair[0,1])
            iarr.append(pair[i,1])
            iarr.append(pair[i+1,1])

            v1 = vertex[pair[i,1]]-vertex[pair[0,1]]
            v2 = vertex[pair[i+1,1]]-vertex[pair[0,1]]
            tmp=[0,0,0]
            tmp[0]=v1[1]*v2[2]-v1[2]*v2[1]
            tmp[1]=v1[2]*v2[0]-v1[0]*v2[2]
            tmp[2]=v1[0]*v2[1]-v1[1]*v2[0]
            tmp =normalized(tmp)
            
            norm[pair[0,1]].append(tmp)
            norm[pair[i,1]].append(tmp)
            norm[pair[i+1,1]].append(tmp)
            
    return varr,iarr,norm

def averageNorm(norm):
    avrNorm=[]
    for i in range(0,len(norm)):
        tmp=[0,0,0]
        for j in range(0,len(norm[i])):
            tmp[0] += norm[i][j][0]
            tmp[1] += norm[i][j][1]
            tmp[2] += norm[i][j][2]
        avrNorm.append(normalized(tmp))
    return avrNorm
    

def main():
    global leftPressed, rightPressed
    global isOrtho, isSingleMesh,isWireFrame, isForce
    global elev, azim
    global d
    global tpoint
    global varr
    global harr

    
    if not glfw.init():
        return
    window = glfw.create_window(1500,1000,'ClassAssignment2', None,None)
    if not window:
        glfw.terminate()
        return

    leftPressed = False
    rightPressed = False
    isOrtho=False
    isSingleMesh = True
    isForce=False
    elev = 35.264
    azim = 45
    d = 5.196
    tpoint = np.array([0.,0.,0.])
    varr=[]
    isWireFrame=True
    initHierarchical()

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

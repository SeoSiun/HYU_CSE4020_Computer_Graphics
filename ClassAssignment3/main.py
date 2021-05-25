import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Joint:
    def __init__(self, name, offset, chan, parent):
        self.name = name
        self.child = []
        self.channel = chan
        self.offset = offset
        self.parent = parent
        self.chanValue = []
        self.matrix=[]
        ############
        self.R =[]
        self.T=[]
        self.rate=0
        ##############
        posmat = np.identity(4)
        posmat[:3,3] = self.offset
        if self.parent!=None:
            self.posmat=self.parent.posmat @ posmat
        else: self.posmat=posmat
        
    def addChild(self,child):
        self.child.append(child)

    def addChanValue(self,value):
        self.chanValue.append(value)

    def getParent(self):
        return self.parent

    def getName(self):
        return self.name

    def getChanNum(self):
        return len(self.channel)

    def getChild(self):
        return self.child

    def getPosmat(self):
        return self.posmat

    def getOffset(self):
        return self.offset*self.rate

    def getR(self,f):
        return self.R[f]

    def getT(self,f):
        return self.T[f]

    def setRate(self,rate):
        self.rate=rate
        
    def setMat(self,fnum):
        for i in range(0,fnum):
            if self.parent!=None:
                self.matrix.append(self.parent.matrix[i] @ self.getMat(i))
            else:
                self.matrix.append(self.getMat(i))

    def getMat(self,f):
        T=np.identity(4)
        R=np.identity(3)

        for i,chan in enumerate(self.channel):
            value = self.chanValue[f][i]
            if chan=="XPOSITION" or chan =="Xposition":
                T[0,3]=value*self.rate
            elif chan=="YPOSITION" or chan =="Yposition":
                T[1,3]=value*self.rate
            elif chan=="ZPOSITION" or chan =="Zposition":
                T[2,3]=value*self.rate
            elif chan=="XROTATION" or chan =="Xrotation":
                value = np.radians(value)
                R = R @ np.array([[1,0,0],
                                 [0, np.cos(value), -np.sin(value)],
                                 [0, np.sin(value), np.cos(value)]])
            elif chan=="YROTATION" or chan =="Yrotation":
                value = np.radians(value)
                R = R @ np.array([[np.cos(value), 0, np.sin(value)],
                                  [0,1,0],
                                  [-np.sin(value), 0, np.cos(value)]])
            elif chan=="ZROTATION" or chan =="Zrotation":
                value = np.radians(value)
                R = R @ np.array([[np.cos(value), -np.sin(value), 0],
                                  [np.sin(value), np.cos(value), 0],
                                  [0,0,1]])
        offset = np.identity(4)
        offset[:3,3] = self.offset
        tmp = np.identity(4)
        tmp[:3,:3] = R

        #################
        self.R.append(tmp)
        self.T.append(T)
        #################

        return offset @ T @ tmp
    
    def getMatrix(self,f):
        return self.matrix[f]

def getAngle(a):
    if a<0:
        return 360+a
    elif a>360:
        return a-360
    else:
        return a

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(180,180,180)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([.1,0.,0.]))
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,.1,0.]))
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,.1]))

    glColor3ub(102,102,102)
    for i in range(-60,60):
        glVertex3fv(np.array([0.5*i,0.,1000.]))
        glVertex3fv(np.array([0.5*i,0.,-1000.]))
        glVertex3fv(np.array([1000.,0.,0.5*i]))
        glVertex3fv(np.array([-1000.,0.,0.5*i]))
    glEnd()

def drawBvh(joint):
    if len(joint.getChild())==0 or joint.getName() == "end": return
    
    child = joint.getChild()
    offset = joint.getOffset()

    glPushMatrix()
    glTranslatef(offset[0],offset[1],offset[2])
    for i in range(0,len(child)):
        # line   
        #glVertex3fv((joint.getPosmat()@np.array([0.,0.,0.,1.]))[:-1])
        #glVertex3fv((child[i].getPosmat()@np.array([0.,0.,0.,1.])) [:-1])

        drawCube(child[i].getOffset())
        drawBvh(child[i])
    glPopMatrix()

def animateBvh(joint,f):
    if len(joint.getChild())==0 or joint.getName() == "end": return
    
    child = joint.getChild()
    offset = np.identity(4)
    offset[:3,3] = joint.getOffset()

    glPushMatrix()
    glMultMatrixf((offset@joint.getT(f)@joint.getR(f)).T)

    for i in range(0,len(child)):
        #line
        #glVertex3fv((joint.getMatrix(f) @ np.array([0.,0.,0.,1.])) [:-1] )
        #glVertex3fv((child[i].getMatrix(f) @ np.array([0.,0.,0.,1.])) [:-1])

        # cube
        drawCube(child[i].getOffset())
        animateBvh(child[i],f)
        
    glPopMatrix()

def drawCube(offset):
    global isAnimating
    y=np.array([0.,1.,0.])
    cos = np.dot(y,offset) / (np.sqrt(np.dot(offset, offset)) * np.sqrt(np.dot(y, y)))
    cross=np.cross(y,offset)
    
    glPushMatrix()
    glRotatef(np.degrees(np.arccos(cos)), cross[0],cross[1],cross[2])
    c = np.identity(4)
    c[1,3] = np.sqrt(np.dot(offset, offset))

    glBegin(GL_QUADS)
    glColor3ub(0,0,255)

    glNormal3f(0,-1,0)
    glVertex3fv(np.array([.02,.0,.02]))
    glVertex3fv(np.array([.02,.0,-.02]))
    glVertex3fv(np.array([-.02,.0,-.02]))
    glVertex3fv(np.array([-.02,.0,.02]))

    glNormal3f(1,0,0)
    glVertex3fv(np.array([.02,.0,.02]))
    glVertex3fv(np.array([.02,.0,-.02]))
    glVertex3fv((c @ np.array([.02,.0,-.02,1.])) [:-1])
    glVertex3fv((c @ np.array([.02,.0,.02,1.])) [:-1])

    glNormal3f(0,0,-1)
    glVertex3fv(np.array([.02,.0,-.02]))
    glVertex3fv( np.array([-.02,.0,-.02]))
    glVertex3fv((c @ np.array([-.02,.0,-.02,1.])) [:-1])
    glVertex3fv((c @ np.array([.02,.0,-.02,1.])) [:-1])

    glNormal3f(-1,0,0)
    glVertex3fv(np.array([-.02,.0,-.02]))
    glVertex3fv(np.array([-.02,.0,.02]))
    glVertex3fv((c @  np.array([-.02,.0,.02,1.])) [:-1])
    glVertex3fv((c @ np.array([-.02,.0,-.02,1.])) [:-1])

    glNormal3f(0,0,1)
    glVertex3fv(np.array([-.02,.0,.02]))
    glVertex3fv(np.array([.02,.0,.02]))
    glVertex3fv((c @  np.array([.02,.0,.02,1.])) [:-1])
    glVertex3fv((c @ np.array([-.02,.0,.02,1.])) [:-1])

    glNormal3f(0,1,0)
    glVertex3fv((c @ np.array([.02,.0,.02,1.])) [:-1])
    glVertex3fv((c @ np.array([.02,.0,-.02,1.])) [:-1])
    glVertex3fv((c @ np.array([-.02,.0,-.02,1.])) [:-1])
    glVertex3fv((c @ np.array([-.02,.0,.02,1.])) [:-1])

    glEnd()

    glPopMatrix()

    
def render(f):
    global isOrtho, isAnimating
    global tpoint
    global elev, azim
    global v, u
    global root
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
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

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    
    lightPos = (10.,10.,0.,0.)
    glLightfv(GL_LIGHT0,GL_POSITION,lightPos)

    lightColor = (0.,0.,1.,1.)
    ambientLightColor = (.0,.0,.1,1.)
    glLightfv(GL_LIGHT0,GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0,GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0,GL_AMBIENT, ambientLightColor)

    lightPos = (0.,0.,10.,0.)
    glLightfv(GL_LIGHT1,GL_POSITION,lightPos)

    lightColor = (1.,0.,0.,1.)
    ambientLightColor = (.1,.0,.0,1.)
    glLightfv(GL_LIGHT1,GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1,GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1,GL_AMBIENT, ambientLightColor)

    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (.1,.1,.1,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS,10)
    glMaterialfv(GL_FRONT, GL_SPECULAR,specularObjectColor)
        
    
    if root != None:
        if not isAnimating: drawBvh(root)
        else: animateBvh(root,f)

def key_callback(window, key, scancode, action, modes):
    global isOrtho,isAnimating
    if key==glfw.KEY_V:
        if action == glfw.PRESS:
            isOrtho = not isOrtho
    if key==glfw.KEY_SPACE and action==glfw.PRESS:
        isAnimating = not isAnimating
       
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

def drop_callback(window,paths):
    global root, ftime, start, fnum
    root=None
    curparent = None
    tmp = None
    name=""
    offset=[]
    chan=[]
    isEnd=False
    jnum=0
    start=0
    m=0
    
    f = open(paths[0])
    
    while True:
        line = f.readline()
        
        s=line.split()
        if s[0] == "MOTION":
            s = f.readline().split()
            fnum = int(s[1])
            s = f.readline().split()
            ftime = float(s[2])

            for i in range(0,fnum):
                s = f.readline().split()
                start=0
                setChanValues(s,root)
            if m>1: setMat(root,fnum,1/m)
            else: setMat(root,fnum,1)
            break;
        elif s[0] == "ROOT" or s[0] == "JOINT":
            name = s[1]
            jnum+=1
        elif s[0] == '{':
          pass
        elif s[0] == "OFFSET":
            if float(s[1])!=0 or float(s[2])!=0 or float(s[3])!=0:
                if m<abs(float(s[1])): m=abs(float(s[1]))
                if m<abs(float(s[2])): m=abs(float(s[2]))
                if m<abs(float(s[3])): m=abs(float(s[3]))       
            offset = np.array((float(s[1]), float(s[2]), float(s[3])))
            if isEnd:
                tmp = Joint("end",offset,[],curparent)
                curparent.addChild(tmp)
                curparent=tmp
                isEnd=False
        elif s[0] == "CHANNELS":
            chan=[]
            for i in range(0,int(s[1])):
                chan.append(s[2+i])
            tmp = Joint(name,offset,chan,curparent)
            if root == None: root = tmp
            elif curparent!= None: curparent.addChild(tmp)
            curparent=tmp
        elif s[0] == '}' and curparent!=None:
            curparent = curparent.getParent()
        elif s[0] == "End":
            isEnd=True
            
    name = paths[0].split('\\')
    print("File name: ", name[len(name)-1])
    print("Number of frames: ", fnum)
    print("FPS: ", 1/ftime)
    print("Number of joints: ", jnum)
    printAllJoint(root)
        
        
def setChanValues(s,joint):
    global start

    if len(joint.getChild())==0 or joint.getName() == "end":
        return

    tmp = []
    for i in range(0,joint.getChanNum()):
        tmp.append(float(s[i+start]))
    joint.addChanValue(np.array(tmp))
    
    start = start + joint.getChanNum()
    child = joint.getChild()
    
    for i in range(0,len(child)):
        setChanValues(s,child[i])
   
def printAllJoint(joint):
    print(joint.getName())
    child = joint.getChild()
    if len(child) == 0 or child[0].getName() == "end":
        return
    for i in range(0,len(child)):
        printAllJoint(child[i])

def setMat(joint,fnum,rate):
    joint.setRate(rate)
    joint.setMat(fnum)
    child = joint.getChild()
    for i in range(0,len(child)):
        setMat(child[i],fnum,rate)

    if len(child)==0 or joint.getName() == "end": return


def main():
    global leftPressed, rightPressed
    global isOrtho, isAnimating
    global elev, azim
    global d
    global tpoint
    global root
    global fnum

    if not glfw.init():
        return
    window = glfw.create_window(900,900,'BVH Viewer', None,None)
    if not window:
        glfw.terminate()
        return

    leftPressed = False
    rightPressed = False
    isOrtho=False
    isAnimating=False
    elev = 35.264
    azim = 45
    d = 5.196
    tpoint = np.array([0.,0.,0.])
    root=None
    fnum=0
    f=0

    glfw.set_key_callback(window,key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window,scroll_callback)
    glfw.set_drop_callback(window,drop_callback)
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.swap_interval(1)
        if fnum==f:
            f=0
        render(f)
        f+=1
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

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
        self.arr=[]
        self.R =[]
        self.T=[]
        
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

    def getOffset(self):
        return self.offset

    def getR(self,f):
        if f==-1:
            return np.identity(4)
        return self.R[f]

    def getT(self,f):
        if f==-1:
            return np.identity(4)
        return self.T[f]

    def getOffsetM(self):
        offset = np.identity(4)
        offset[:3,3] = self.offset
        return offset

    def getArr(self,i):
        return self.arr[i]

    def addArr(self,arr):
        self.arr.append(arr)
        
    def setMat(self,fnum):
        for i in range(0,fnum):
            T=np.identity(4)
            R=np.identity(3)

            for j,chan in enumerate(self.channel):
                value = self.chanValue[i][j]
                if chan=="XPOSITION" or chan =="Xposition":
                    T[0,3]=value
                elif chan=="YPOSITION" or chan =="Yposition":
                    T[1,3]=value
                elif chan=="ZPOSITION" or chan =="Zposition":
                    T[2,3]=value
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
            tmp = np.identity(4)
            tmp[:3,:3] = R
            self.R.append(tmp)
            self.T.append(T)

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

def drawBvh(joint,f):
    global isOBJ
    if len(joint.getChild())==0 or joint.getName() == "end": return
    
    child = joint.getChild()

    glPushMatrix()

    glMultMatrixf((joint.getOffsetM()@joint.getT(f)@joint.getR(f)).T)

    for i in range(0,len(child)):
        if isOBJ:
            drawOBJ(child[i].getOffset(),joint.getArr(i))
        else:
            glBegin(GL_LINES)
            glColor(255,255,255)
            glVertex3fv(np.array([0.,0.,0.,1.]) [:-1] )
            glVertex3fv((child[i].getOffsetM() @ np.array([0.,0.,0.,1.])) [:-1] )
            glEnd()
        drawBvh(child[i],f)
    glPopMatrix()
        
def drawOBJ(offset,varr):
    y=np.array([0.,1.,0.])
    cos = np.dot(y,offset) / (np.sqrt(np.dot(offset, offset)) * np.sqrt(np.dot(y, y)))
    cross=np.cross(y,offset)
    
    glPushMatrix()   
    glRotatef(np.degrees(np.arccos(cos)), cross[0],cross[1],cross[2])
    glScalef(.1,.1,.1)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize,varr)
    glVertexPointer(3,GL_FLOAT, 6*varr.itemsize,ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES,0,int(varr.size/6))

    glPopMatrix() 

def render(f):
    global isOrtho, isAnimating, isOBJ
    global tpoint
    global elev, azim
    global v, u
    global root
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    if isOBJ:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL )
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE )
        
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

    if isOBJ:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)

        lightPos = (10.,10.,10.,0.)
        glLightfv(GL_LIGHT0,GL_POSITION,lightPos)

        lightColor = (1.,0.,0.,1.)
        ambientLightColor = (.1,.0,.0,1.)
        glLightfv(GL_LIGHT0,GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT0,GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT0,GL_AMBIENT, ambientLightColor)

        lightPos = (-10.,10.,-10.,0.)
        glLightfv(GL_LIGHT1,GL_POSITION,lightPos)

        lightColor = (0.,1.,0.,1.)
        ambientLightColor = (.0,.1,.0,1.)
        glLightfv(GL_LIGHT1,GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT1,GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT1,GL_AMBIENT, ambientLightColor)

        lightPos = (10.,10.,-10.,0.)
        glLightfv(GL_LIGHT2,GL_POSITION,lightPos)

        lightColor = (0.,0.,1.,1.)
        ambientLightColor = (.0,.0,.1,1.)
        glLightfv(GL_LIGHT2,GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT2,GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT2,GL_AMBIENT, ambientLightColor)

        objectColor = (.8,.8,.8,1.)
        specularObjectColor = (.08,.08,.08,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE,objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS,10)
        glMaterialfv(GL_FRONT, GL_SPECULAR,specularObjectColor)
        
    if root != None:  
        if isScale:
            glPushMatrix()
            glScalef(.05,.05,.05)
            
        if not isAnimating:
            drawBvh(root,-1)
        else:
            drawBvh(root,f)
            
        if isScale: glPopMatrix()

def key_callback(window, key, scancode, action, modes):
    global isOrtho,isAnimating, f
    if key==glfw.KEY_V:
        if action == glfw.PRESS:
            isOrtho = not isOrtho
    if key==glfw.KEY_SPACE and action==glfw.PRESS:
        if not isAnimating:
            loadMotion()
            isAnimating = True
            f=0
       
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
    global root, ftime, start, fnum,isOBJ, isScale, file, isAnimating
    root=None
    curparent = None
    tmp = None
    name=""
    offset=[]
    chan=[]
    isEnd=False
    jnum=0
    start=0
    isAnimating=False
    
    file = open(paths[0])
    name = paths[0].split('\\')
    name = name[len(name)-1]
    if name=="sample-walk.bvh" or name=="sample-spin.bvh":
        isOBJ=True
    else: isOBJ=False
    if name=="Sophie_Excited-01.bvh":
        isScale=True
    else: isScale=False
    
    while True:
        line = file.readline()
        
        s=line.split()
        if s[0] == "MOTION":
            s = file.readline().split()
            fnum = int(s[1])
            s = file.readline().split()
            ftime = float(s[2])
            break;
        elif s[0] == "ROOT" or s[0] == "JOINT":
            name = s[1]
            jnum+=1
        elif s[0] == '{':
          pass
        elif s[0] == "OFFSET":      
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
                        
    print("File name: ", name)
    print("Number of frames: ", fnum)
    print("FPS: ", 1/ftime)
    print("Number of joints: ", jnum)
    printAllJoint(root)
    

def loadMotion():
    global fnum,file,root,start

    for i in range(0,fnum):
        s = file.readline().split()
        start=0
        setChanValues(s,root)
    setMat(root,fnum)
        
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

def setMat(joint,fnum):
    joint.setMat(fnum)
    child = joint.getChild()
    for i in range(0,len(child)):
        setMat(child[i],fnum)
    if len(child)==0 or joint.getName() == "end": return

def printAllJoint(joint):
    global isOBJ
    if isOBJ:
        findArr(joint)
    print(joint.getName())
    child = joint.getChild()
    if len(child) == 0 or child[0].getName() == "end":
        return
    for i in range(0,len(child)):
        printAllJoint(child[i])

def findArr(joint):
    name = joint.getName()

    if name == "Hips":
        joint.addArr(parseOBJ("hips.obj"))
        joint.addArr(parseOBJ("rightHipLeg.obj"))
        joint.addArr(parseOBJ("leftHipLeg.obj"))
    elif name == "Spine":
        joint.addArr(parseOBJ("spine.obj"))
        joint.addArr(parseOBJ("rightSpineArm.obj"))
        joint.addArr(parseOBJ("leftSpineArm.obj"))
    elif name == "Head":
        joint.addArr(parseOBJ("head.obj"))
    elif name == "RightArm":
        joint.addArr(parseOBJ("rightArm.obj"))
    elif name == "RightForeArm":
        joint.addArr(parseOBJ("rightForeArm.obj"))
    elif name == "RightHand":
        joint.addArr(parseOBJ("rightHand.obj"))
    elif name == "LeftArm":
        joint.addArr(parseOBJ("leftArm.obj"))
    elif name == "LeftForeArm":
        joint.addArr(parseOBJ("leftForeArm.obj"))
    elif name == "LeftHand":
        joint.addArr(parseOBJ("leftHand.obj"))
    elif name == "RightUpLeg":
        joint.addArr(parseOBJ("rightUpLeg.obj"))
    elif name == "RightLeg":
        joint.addArr(parseOBJ("rightLeg.obj"))
    elif name == "RightFoot":
        joint.addArr(parseOBJ("rightFoot.obj"))
    elif name == "LeftUpLeg":
        joint.addArr(parseOBJ("leftUpLeg.obj"))
    elif name == "LeftLeg":
        joint.addArr(parseOBJ("leftLeg.obj"))
    elif name == "LeftFoot":
        joint.addArr(parseOBJ("leftFoot.obj"))
        
def parseOBJ(filename):
    arr=[]
    vertex=[]
    normal=[]
    pairs=[]
    
    f=open(filename)
    
    while True:
        line = f.readline()
        if not line: break
        
        s = line.split()

        if s[0] == 'v':
            vertex.append(np.array((float(s[1]),float(s[2]),float(s[3]))))
        elif s[0] == 'vn':
            normal.append((float(s[1]),float(s[2]),float(s[3])))
        elif s[0] == 'f':
            pair = []
            tmp=[]
            for i in range(1,len(s)):
                v,t,n = s[i].split('/')
                pair.append((int(n)-1,int(v)-1))
            pairs.append(np.array(pair))

    varr=makeVarr(normal,vertex,pairs)

    return np.array(varr,'float32')

def makeVarr(normal,vertex,pairs):
    varr=[]
    for pair in pairs:
        for i in range(1,len(pair)-1):
            varr.append(normal[pair[0,0]])
            varr.append(vertex[pair[0,1]])
            varr.append(normal[pair[i,0]])
            varr.append(vertex[pair[i,1]])
            varr.append(normal[pair[i+1,0]])
            varr.append(vertex[pair[i+1,1]])          
    return varr


def main():
    global leftPressed, rightPressed
    global isOrtho, isAnimating,isOBJ, isScale
    global elev, azim
    global d
    global tpoint
    global root
    global fnum, f

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
    isOBJ=False
    isScale=False

    glfw.set_key_callback(window,key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window,scroll_callback)
    glfw.set_drop_callback(window,drop_callback)
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        if fnum==f:
            f=0
        render(f)
        f+=1
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

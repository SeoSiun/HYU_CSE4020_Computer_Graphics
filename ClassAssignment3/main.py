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
        if parent!=None:
            self.globalPos = parent.getGlobalPos() + self.offset
        else: self.globalPos = self.offset
        
    def addChild(self,child):
        self.child.append(child)

    def setChanValue(self,value):
        self.cahnValue = value

    def getParent(self):
        return self.parent

    def getName(self):
        return self.name

    def getChanNum(self):
        return len(self.channel)

    def getChild(self):
        return self.child

    def getGlobalPos(self):
        return self.globalPos

def getAngle(a):
    if a<0:
        return 360+a
    elif a>360:
        return a-360
    else:
        return a

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(102,102,102)
    for i in range(-60,60):
        glVertex3fv(np.array([0.5*i,0.,1000.]))
        glVertex3fv(np.array([0.5*i,0.,-1000.]))
        glVertex3fv(np.array([1000.,0.,0.5*i]))
        glVertex3fv(np.array([-1000.,0.,0.5*i]))
    glEnd()

def drawBvh(joint):
    if joint.getName() == "end": return
    
    child = joint.getChild()
    for i in range(0,len(child)):
        glVertex3fv(joint.getGlobalPos())
        glVertex3fv(child[i].getGlobalPos())
        drawBvh(child[i])
    return
    

def render():
    global isOrtho
    global tpoint
    global elev, azim
    global v, u
    global root
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
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

    drawFrame()
    if root != None:
        glBegin(GL_LINES)
        glColor3ub(0,0,255)
        drawBvh(root)
        glEnd()

def key_callback(window, key, scancode, action, modes):
    global isOrtho
    if key==glfw.KEY_V:
        if action == glfw.PRESS:
            isOrtho = not isOrtho
        
       
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
    global root, ftime, start
    root=None
    curparent = None
    tmp = None
    name=""
    offset=[]
    chan=[]
    isEnd=False
    
    f = open(paths[0])
    
    while True:
        line = f.readline()
        
        s=line.split()
        if s[0] == "MOTION":
            s = f.readline().split()
            frames = int(s[1])
            s = f.readline().split()
            ftime = float(s[2])

            for i in range(0,frames):
                s = f.readline().split()
                start=0
                setChanValues(s,root)
            break;
        elif s[0] == "ROOT" or s[0] == "JOINT":
            name = s[1]
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
        
        
def setChanValues(s,joint):
    global start

    if joint.getName == "end":
        return
    
    tmp = []
    for i in range(start,joint.getChanNum()):
        tmp.append(float(s[i]))
    joint.setChanValue(tmp)
    
    start = start + joint.getChanNum()
    child = joint.getChild()
    
    for i in range(0,len(child)):
        setChanValues(s,child[i])
   
        

def main():
    global leftPressed, rightPressed
    global isOrtho
    global elev, azim
    global d
    global tpoint
    global root
    
    if not glfw.init():
        return
    window = glfw.create_window(800,800,'BVH Viewer', None,None)
    if not window:
        glfw.terminate()
        return

    leftPressed = False
    rightPressed = False
    isOrtho=False
    elev = 35.264
    azim = 45
    d = 5.196
    tpoint = np.array([0.,0.,0.])
    root=None

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

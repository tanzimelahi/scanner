import math
from subprocess import Popen, PIPE
from os import remove
import random
#constants
XRES = 500
YRES = 500
MAX_COLOR = 255
RED = 0
GREEN = 1
BLUE = 2

DEFAULT_COLOR = [0, 0, 0]

def new_screen( width = XRES, height = YRES ):
    screen = []
    for y in range( height ):
        row = []
        screen.append( row )
        for x in range( width ):
            screen[y].append( DEFAULT_COLOR[:] )
    return screen
def z_buffer():
    buffer=[]
    for y in range(YRES):
        row=[]
        buffer.append(row)
        for x in range(XRES):
            buffer[y].append(float('-inf'))
    return buffer
def plot( screen,buffer,x,y,z,color ):
    newy = YRES - 1 - y
    if ( x < XRES and newy < YRES ):
        if buffer[int(newy)][int(x)]<z:
            screen[int(newy)][int(x)] = color[:]
            buffer[int(newy)][int(x)]=z

def clear_screen( screen,buffer ):  # sets the screen and buffer to default values
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            screen[y][x] = DEFAULT_COLOR[:]
    for y in range(len(buffer)):
        for x in range(len(buffer[y])):
            buffer[y][x]=float('-inf')

def save_ppm( screen, fname ):
    f = open( fname, 'wb' )
    ppm = 'P6\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    f.write(ppm.encode())
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            f.write( bytes(pixel) )
    f.close()

def save_ppm_ascii( screen, fname ):
    f = open( fname, 'w' )
    ppm = 'P3\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    for y in range( len(screen) ):
        row = ''
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            row+= str( pixel[ RED ] ) + ' '
            row+= str( pixel[ GREEN ] ) + ' '
            row+= str( pixel[ BLUE ] ) + ' '
        ppm+= row + '\n'
    f.write( ppm )
    f.close()

def save_extension( screen, fname ):
    ppm_name = fname[:fname.find('.')] + '.ppm'
    save_ppm_ascii( screen, ppm_name )
    p = Popen( ['convert', ppm_name, fname ], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)

def display( screen ):
    ppm_name = 'pic.ppm'
    save_ppm_ascii( screen, ppm_name )
    p = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)

#commands from here:
#for the first two octants, the x0 must be smaller than x1
def firstoct(screen,buffer,x0,y0,z0,x1,y1,z1,color):#oct 1 and 5
    x=x0
    y=y0
    A=y1-y0
    B=-(x1-x0)
    d=2*A+B
    dz=(z1-z0)/(x1-x0+1)
    z=z0
    while x<x1:
        plot(screen,buffer,x,y,z,color)
        if d>=0:
            y+=1
            d=d+2*B
        x=x+1
        d=d+2*A
        z+=dz
    plot(screen,buffer,x1,y1,z1,color)
def secondoct(screen,buffer,x0,y0,z0,x1,y1,z1,color):#oct 2 and 6
    x=x0
    y=y0
    A=y1-y0
    B=-(x1-x0)
    d=A+2*B
    z=z0
    dz=(z1-z0)/(y1-y0+1)
    while y<y1:
        plot(screen,buffer,x,y,z,color)
        if d<=0:
            d=d+2*A
            x+=1
        y=y+1
        d=d+2*B
        z+=dz
    plot(screen,buffer,x1,y1,z1,color)
def thirdoct(screen,buffer,x0,y0,z0,x1,y1,z1,color):#oct 3 and 7 remember the x0 and x1 hierarchy is reversed for this one
    x=x0
    y=y0
    A=y1-y0
    B=-(x1-x0)
    d=A+2*B
    z=z0
    dz=(z1-z0)/(y1-y0+1)
    while y<y1:
        plot(screen,buffer,x,y,z,color)
        if d>=0:
            x=x-1
            d=d-2*A
        y=y+1
        d=d+2*B
        z+=dz
    plot(screen,buffer,x1,y1,z1,color)
def fourthoct(screen,buffer,x0,y0,z0,x1,y1,z1,color): #oct 4 and 8
    x=x0
    y=y0
    A=y1-y0
    B=-(x1-x0)
    d=A+2*B
    z=z0
    dz=(z1-z0)/(x1-x0+1)
    while x<x1:
        plot(screen,buffer,x,y,z,color)
        if d<=0:
            y=y-1
            d=d-2*B
        x=x+1
        d=d+2*A
        z+=dz
    plot(screen,buffer,x1,y1,z1,color)
def oneSlopePos(screen,buffer,x0,y0,z0,x1,y1,z1,color):
    x=x0
    y=y0
    z=z0
    dz=(z1-z0)/(x1-x0+1)
    while x<=x1:
        plot(screen,buffer,x,y,z,color)
        x+=1
        y+=1
        z+=dz
        

def oneSlopeNeg(screen,buffer,x0,y0,z0,x1,y1,z1,color):
    x=x0
    y=y0
    z=z0
    dz=(z1-z0)/(x1-x0+1)
    while x<=x1:
        plot(screen,buffer,x,y,z,color)
        x+=1
        y-=1
        z+=dz
def zeroSlope(screen,buffer,x0,y0,z0,x1,y1,z1,color):
    x=x0
    y=y0
    z=z0
    dz=(z1-z0)/(x1-x0+1)
    while(x<=x1):
        plot(screen,buffer,x,y,z,color)
        x+=1
        z+=dz
def undefinedSlope(screen,buffer,x0,y0,z0,x1,y1,z1,color):
    x=x0
    y=y0
    z=z0
    dz=(z1-z0)/(y1-y0+1)
    while y<=y1:
        plot(screen,buffer,x,y,z,color)
        y+=1
        z+=dz

def drawline(screen,buffer,x0,y0,z0,x1,y1,z1,color):# whenever possible x0 must be greater than x1(left to right orientation)
    if(x0>x1):
        store=x0
        x0=x1
        x1=store
        storage=y0
        y0=y1
        y1=storage
        store=z0
        z0=z1
        z1=store
    if(x0==x1):
        if(y1<y0):
            store=y0
            y0=y1
            y1=store
            store=z0
            z0=z1
            z1=store
        undefinedSlope(screen,buffer,x0,y0,z0,x1,y1,z1,color)
    elif(y0==y1):
        zeroSlope(screen,buffer,x0,y0,z0,x1,y1,z1,color)
    elif abs(x1-x0)>=abs(y1-y0):
        if y1>y0:
            firstoct(screen,buffer,x0,y0,z0,x1,y1,z1,color)
        else:
            fourthoct(screen,buffer,x0,y0,z0,x1,y1,z1,color)
    else:
        if y1>y0:
            secondoct(screen,buffer,x0,y0,z0,x1,y1,z1,color)
        else:
            thirdoct(screen,buffer,x1,y1,z1,x0,y0,z0,color)



def new_matrix(rows = 4, cols = 4):
    m = []
    for c in range( cols ):
        m.append( [] )
        for r in range( rows ):
            m[c].append( 0 )
    return m
def update_matrix(row,column,matrix,value):
    matrix[column][row]=value
def up(matrix,row,column,value):
    matrix[column][row]=value
def print_matrix(matrix):
    result=""
    row=len(matrix[0])
    col=len(matrix)
    for x in range(row):
        for y in range(col):
            add=str(matrix[y][x])
            if len(add)==1:
                result+=add+"   "
            elif len(add)==2:
                result+=add+"  "
            else:
                result+=add+" "
        result+="\n"
    print(result)
        


def ident(matrix):
    row=len(matrix[0])
    col=row
    for x in range(row):
        for y in range(col):
            if(x==y):
                matrix[y][x]=1
            else:
                matrix[y][x]=0
def matrix_multiplication(m1,m2): #this func works fine
    result=new_matrix(len(m1[0]),len(m2))
    for secondCol in range(len(m2)):
        for y in range(len(m1[0])):
            add=0
            for x in range(len(m1)):
                add+=(m1[x][y]*m2[secondCol][x])
            result[secondCol][y]=add
    for x in range(len(m2)):
        m2[x]=result[x]

def empty_matrix():
    m = []
    m.append( [] )
    return m
#test cases


#that ends here
def add_point(matrix,x,y,z=0):
    if len(matrix[0])==0:
        matrix[0].append(x)
        matrix[0].append(y)
        matrix[0].append(z)
        matrix[0].append(1)
    else:
        matrix.append([])
        matrix[len(matrix)-1].append(x)
        matrix[len(matrix)-1].append(y)
        matrix[len(matrix)-1].append(z)
        matrix[len(matrix)-1].append(1)
        
def update_point(matrix,x,y,z,unit=1):  #same as add_point but can modify the '1's used as helper func for rotation
    if len(matrix[0])==0:
        matrix[0].append(x)
        matrix[0].append(y)
        matrix[0].append(z)
        matrix[0].append(unit)
    else:
        matrix.append([])
        matrix[len(matrix)-1].append(x)
        matrix[len(matrix)-1].append(y)
        matrix[len(matrix)-1].append(z)
        matrix[len(matrix)-1].append(unit)
    
def add_edge(matrix,x0,y0,z0,x1,y1,z1):
    add_point(matrix,x0,y0,z0)
    add_point(matrix,x1,y1,z1)
def add_polygon(matrix,x0,y0,z0,x1,y1,z1,x2,y2,z2):
    add_point(matrix,x0,y0,z0)
    add_point(matrix,x1,y1,z1)
    add_point(matrix,x2,y2,z2)

def dot_product(vector1,vector2):
    return (vector1[0]*vector2[0]+vector1[1]*vector2[1]+vector1[2]*vector2[2])

def vector_substraction(vector1,vector2):
    return [vector1[0]-vector2[0],vector1[1]-vector2[1],vector1[2]-vector2[2]]

def cross_product(a,b):# a and b are vectors []
    return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
#print(cross_product([2,4,3],[1,2,4]))

def surface_normal(polygon_matrix,index):  #one change made here that is different from notes
    a=vector_substraction(polygon_matrix[index+1],polygon_matrix[index])
    b=(vector_substraction(polygon_matrix[index+2],polygon_matrix[index]))  #returned surface normal to its regular note form
    #print(cross_product(a,b))
    return cross_product(a,b)

def backface_culling(n,v):# n being the normal of a triangle and v the  z unit vector
    result=dot_product(n,v)
    return True
    if (result>0):
        return True
    else:
        return False

def ytop(matrix,step): #helper func for add_polygons
    result=step+2
    y_top=matrix[result][1]
    if(matrix[step+1][1]>y_top):
        y_top=matrix[step+1][1]
        result=step+1
    if(matrix[step][1]>y_top):
        y_top=matrix[step][1]
        result=step
    return y_top
def ytop_step(matrix,step):
    result=step+2
    y_top=matrix[result][1]
    if(matrix[step+1][1]>y_top):
        y_top=matrix[step+1][1]
        result=step+1
    if(matrix[step][1]>y_top):
        y_top=matrix[step][1]
        result=step
    return result

def xtop(matrix,step):
    result=step+2
    y_top=matrix[result][1]
    if(matrix[step+1][1]>y_top):
        y_top=matrix[step+1][1]
        result=step+1
    if(matrix[step][1]>y_top):
        y_top=matrix[step][1]
        result=step
    x_top=matrix[result][0]
    return x_top
def ybot(matrix,step):
    bottom=step+2
    y_bottom=matrix[bottom][1]
    if(matrix[step+1][1]<y_bottom):
        y_bottom=matrix[step+1][1]
        bottom=step+1
    if(matrix[step][1]<y_bottom):
        y_bottom=matrix[step][1]
        bottom=step
    return y_bottom
def ybot_step(matrix,step):
    bottom=step+2
    y_bottom=matrix[bottom][1]
    if(matrix[step+1][1]<y_bottom):
        y_bottom=matrix[step+1][1]
        bottom=step+1
    if(matrix[step][1]<y_bottom):
        y_bottom=matrix[step][1]
        bottom=step
    return bottom

def xbot(matrix,step):
    bottom=step+2
    y_bottom=matrix[bottom][1]
    if(matrix[step+1][1]<y_bottom):
        y_bottom=matrix[step+1][1]
        bottom=step+1
    if(matrix[step][1]<y_bottom):
        y_bottom=matrix[step][1]
        bottom=step
    x_bottom=matrix[bottom][0]
    return x_bottom

def zbot(matrix,step):    
    bottom=step+2
    y_bottom=matrix[bottom][1]
    if(matrix[step+1][1]<y_bottom):
        y_bottom=matrix[step+1][1]
        bottom=step+1
    if(matrix[step][1]<y_bottom):
        y_bottom=matrix[step][1]
        bottom=step
    x_bottom=matrix[bottom][0]
    z_bottom=matrix[bottom][2]
    return z_bottom

def ztop(matrix,step):
    result=step+2
    y_top=matrix[result][1]
    if(matrix[step+1][1]>y_top):
        y_top=matrix[step+1][1]
        result=step+1
    if(matrix[step][1]>y_top):
        y_top=matrix[step][1]
        result=step
    x_top=matrix[result][0]
    z_top=matrix[result][2]
    return z_top

    
    

def add_polygons(screen,buffer,matrix,color):
    step=0
    col=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    while(step<len(matrix)):
        if step%2==0:
             col=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        normal=surface_normal(matrix,step)
        if(backface_culling(normal,[0,0,1])):
            drawline(screen,buffer,matrix[step][0],matrix[step][1],matrix[step][2],matrix[step+1][0],matrix[step+1][1],matrix[step+1][2],col)
            drawline(screen,buffer,matrix[step+1][0],matrix[step+1][1],matrix[step+1][2],matrix[step+2][0],matrix[step+2][1],matrix[step+2][2],col)
            drawline(screen,buffer,matrix[step+2][0],matrix[step+2][1],matrix[step+2][2],matrix[step][0],matrix[step][1],matrix[step][2],col)
            
            yb=ybot(matrix,step)     #scanline conversion starts here
            yt=ytop(matrix,step)
            xt=xtop(matrix,step)
            xb=xbot(matrix,step)
            zb=zbot(matrix,step)
            zt=ztop(matrix,step)
            xm=0
            zm=0
            ym=0
            if matrix[step+2][1]!=yb and matrix[step+2][1]!=yt:
                ym=matrix[step+2][1]
                xm=matrix[step+2][0]
                zm=matrix[step+2][2]
            elif matrix[step+1][1]!=yb and matrix[step+1][1]!=yt:
                ym=matrix[step+1][1]
                xm=matrix[step+1][0]
                zm=matrix[step+1][2]
            elif matrix[step][1]!=yb and matrix[step][1]!=yt:
                ym=matrix[step][1]
                xm=matrix[step][0]
                zm=matrix[step][2]
            else:
                b=0
                t=0
                if(matrix[step][1]==yb):
                    b+=1
                elif(matrix[step][1]==yt):
                    t+=1
                if(matrix[step+1][1]==yb):
                     b+=1
                elif(matrix[step+1][1]==yt):
                    t+=1
                if(matrix[step+2][1]==yb):
                    b+=1
                elif(matrix[step+2][1]==yt):
                    t+=1
                if(t>=2):
                    count=ytop_step(matrix,step)
                    if step!=count and matrix[step][1]==yt:
                        xm=matrix[step][0]
                        ym=matrix[step][1]
                        zm=matrix[step][2]
                    elif (step+1)!=count and matrix[step+1][1]==yt:
                        xm=matrix[step+1][0]
                        ym=matrix[step+1][1]
                        zm=matrix[step+1][2]
                    else:
                        xm=matrix[step+2][0]
                        ym=matrix[step+2][1]
                        zm=matrix[step+2][2]
                if(b>=2):
                    count=ybot_step(matrix,step)
                    if step!=count and matrix[step][1]==yb:
                        xm=matrix[step][0]
                        ym=matrix[step][1]
                        zm=matrix[step][2]
                    elif (step+1)!=count and matrix[step+1][1]==yb:
                        xm=matrix[step+1][0]
                        ym=matrix[step+1][1]
                        zm=matrix[step+1][2]
                    else:
                        xm=matrix[step+2][0]
                        ym=matrix[step+2][1]
                        zm=matrix[step+2][2]

            dx=(xt-xb)/(yt-yb+1)
            dx1=(xm-xb)/(ym-yb+1)
            dx1_1=(xt-xm)/(yt-ym+1)
            dz0=(zt-zb)/(yt-yb+1)
            dz1=(zm-zb)/(ym-yb+1)
            dz1_1=(zt-zm)/(yt-ym+1)
            x0=xb
            x1=xb
            z0=zb
            z1=zb
            y=yb
            while(y<=ym):
                drawline(screen,buffer,x0,y,z0,x1,y,z1,col)
                x0+=dx
                x1+=dx1
                z0+=dz0
                z1+=dz1
                y+=1
            
            dx1=dx1_1
            x1=xm
            z1=zm
            dz1=dz1_1
            while(y<=yt):
                drawline(screen,buffer,x0,y,z0,x1,y,z1,col)
                x0+=dx
                x1+=dx1
                z0+=dz0
                z1+=dz1
                y+=1                       #scanline conversino ends here
                
        step+=3                   


def add_lines(screen,buffer,matrix,color):
    step=0
    while(step<len(matrix)):
        #print("x0:"+str(matrix[step][0])+"  "+"y0:"+str(matrix[step][1])+"  "+"x1:"+str(matrix[step+1][0])+"  "+"y1:"+str(matrix[step+1][1]))
        drawline(screen,buffer,matrix[step][0],matrix[step][1],matrix[step][2],matrix[step+1][0],matrix[step+1][1],matrix[step+1][2],color)
        step+=2
def scale(sx,sy,sz):
    info=[sx,sy,sz]
    matrix=new_matrix(4,4)
    ident(matrix)
    for col in range(len(matrix)-1):
        for row in range(len(matrix[0])-1):
            if row==col:
                matrix[col][row]=info[col]

    return matrix
def move(a,b,c):
    info=[a,b,c]
    matrix=new_matrix(4,4)
    ident(matrix)
    for row in range(len(matrix)-1):
        matrix[3][row]=info[row]
    return matrix



def x_rotation(angle):
    angle=math.radians(angle)
    matrix=empty_matrix()
    update_point(matrix,1,0,0,0)
    update_point(matrix,0,math.cos(angle),1*math.sin(angle),0)
    update_point(matrix,0,-1*math.sin(angle),math.cos(angle),0)
    update_point(matrix,0,0,0,1)
    return matrix
     
    

def y_rotation(angle):
    angle=math.radians(angle)
    matrix=empty_matrix()
    update_point(matrix,math.cos(angle),0,-1*math.sin(angle),0)
    update_point(matrix,0,1,0,0)
    update_point(matrix,1*math.sin(angle),0,math.cos(angle),0)
    update_point(matrix,0,0,0,1)
    return matrix



def z_rotation(angle):
    angle=math.radians(angle)
    matrix=empty_matrix()
    update_point(matrix,math.cos(angle),1*math.sin(angle),0,0)
    update_point(matrix,-1*math.sin(angle),math.cos(angle),0,0)
    update_point(matrix,0,0,1,0)
    update_point(matrix,0,0,0,1)
    return matrix
   

    
def rotation (angle,axis_of_rotation):
    if(axis_of_rotation=="x"):
        return x_rotation(angle)
    elif axis_of_rotation=="y":
        return y_rotation(angle)
    else:
        return z_rotation(angle)

def bezier(matrix,x0,y0,x1,y1,x2,y2,x3,y3):
    ax=-x0+3*x1-3*x2+x3
    bx=3*x0-6*x1+3*x2
    cx=-3*x0+3*x1
    dx=x0
    ay=-y0+3*y1-3*y2+y3
    by=3*y0-6*y1+3*y2
    cy=-3*y0+3*y1
    dy=y0
    t=0
    input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
    input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
    t+=0.0001
    new_input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
    new_input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
    add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
    input_x=new_input_x
    input_y=new_input_y
    t+=0.0001
    while(t<=1):
        new_input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
        new_input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
        add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
        input_x=new_input_x
        input_y=new_input_y
        t+=0.0001
    
def hermite(matrix,x0,y0,x1,y1,rx0,ry0,rx1,ry1):
    my_matrix=empty_matrix()
    m2x=empty_matrix()
    add_point(m2x,x0,x1,rx0)
    update_matrix(3,0,m2x,rx1)
    add_point(my_matrix,2,-3,0)
    add_point(my_matrix,-2,3,0)
    add_point(my_matrix,1,-2,1)
    add_point(my_matrix,1,-1,0)
    info=[1,0,0,0]
    for x in range(4):
        update_matrix(3,x,my_matrix,info[x])
    matrix_multiplication(my_matrix,m2x)
    ax=m2x[0][0]
    bx=m2x[0][1]
    cx=m2x[0][2]
    dx=m2x[0][3]
    m2y=empty_matrix()
    add_point(m2y,y0,y1,ry0)
    update_matrix(3,0,m2y,ry1)
    matrix_multiplication(my_matrix,m2y)
    ay=m2y[0][0]
    by=m2y[0][1]
    cy=m2y[0][2]
    dy=m2y[0][3]
    t=0
    input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
    input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
    t+=0.0001
    new_input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
    new_input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
    add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
    input_x=new_input_x
    input_y=new_input_y
    t+=0.0001
    while(t<=1):
        new_input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
        new_input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
        add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
        input_x=new_input_x
        input_y=new_input_y
        t+=0.0001
def circle(matrix,cx,cy,cz,r,step=1000):
    i=0
    t=0
    input_x=int(math.cos(math.pi*2*t)*r+cx)
    input_y=int(math.sin(math.pi*2*t)*r+cy)
    i+=1
    t=i/step
    new_input_x=int(math.cos(math.pi*2*t)*r+cx)
    new_input_y=int(math.sin(math.pi*2*t)*r+cy)
    add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
    input_x=new_input_x
    input_y=new_input_y
    i+=1
    while(i<=step):
        t=i/step
        new_input_x=int(math.cos(math.pi*2*t)*r+cx)
        new_input_y=int(math.sin(math.pi*2*t)*r+cy)
        add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
        input_x=new_input_x
        input_y=new_input_y
        i+=1
     
def apply(transform,edge):
    matrix_multiplication(transform,edge)


def parser(fl_name,screen,buffer,color,edge,triangle_matrix,stack):
    fl=open(fl_name,"r")
    data=fl.readlines()
    i=0
    while(i<len(data)):
        #print(data[i].strip())
        if data[i].strip()=="line":
            coords=data[i+1].split()
            x0=int(coords[0])
            y0=int(coords[1])
            z0=int(coords[2])
            x1=int(coords[3])
            y1=int(coords[4])
            z1=int(coords[5])
            add_edge(edge,x0,y0,z0,x1,y1,z1)
            apply(stack[-1],edge)
            add_lines(screen,buffer,edge,color)
            edge=empty_matrix()
        elif data[i].strip()=="clear":
            clear_screen(screen,buffer)
        elif data[i].strip()=="scale":
            coords=data[i+1].split()
            sx=int(coords[0])
            sy=int(coords[1])
            sz=int(coords[2])
            transform=scale(sx,sy,sz)
            apply(stack[-1],transform)
            stack[-1]=transform
        elif data[i].strip()=="circle":
            coords=data[i+1].split()
            x=int(coords[0])
            y=int(coords[1])
            z=int(coords[2])
            r=int(coords[3])
            circle(edge,x,y,z,r)
            apply(stack[-1],edge)
            add_lines(screen,buffer,edge,color)
            edge=empty_matrix()
        elif data[i].strip()=="move":
            coords=data[i+1].split()
            a=int(coords[0])
            b=int(coords[1])
            c=int(coords[2])
            transform=move(a,b,c)
            apply(stack[-1],transform)
            stack[-1]=transform
        elif data[i].strip()=="rotate":
            coords=data[i+1].split()
            angle=int(coords[1])
            axis=coords[0]
            transform=rotation(angle,axis)
            apply(stack[-1],transform)
            stack[-1]=transform
        elif data[i].strip()=="save":
            coords=data[i+1].split()
            save_ppm(screen,coords[0])
        elif data[i].strip()=="display":
            display(screen)
        elif data[i].strip()=="sphere":
            coords=data[i+1].split()
            x=int(coords[0])
            y=int(coords[1])
            z=int(coords[2])
            r=int(coords[3])
            sphere(triangle_matrix,x,y,z,r)
            apply(stack[-1],triangle_matrix)
            add_polygons(screen,buffer,triangle_matrix,color)
            triangle_matrix=empty_matrix()
        elif data[i].strip()=="box":
             coords=data[i+1].split()
             x=int(coords[0])
             y=int(coords[1])
             z=int(coords[2])
             x_width=int(coords[3])
             y_width=int(coords[4])
             z_width=int(coords[5])
             box(triangle_matrix,x,y,z,x_width,y_width,z_width)
             apply(stack[-1],triangle_matrix)
             add_polygons(screen,buffer,triangle_matrix,color)
             triangle_matrix=empty_matrix()
        elif data[i].strip()=="torus":
            coords=data[i+1].split()
            x=int(coords[0])
            y=int(coords[1])
            z=int(coords[2])
            r=int(coords[3])
            R=int(coords[4])
            torus(triangle_matrix,x,y,z,r,R)
            apply(stack[-1],triangle_matrix)
            add_polygons(screen,buffer,triangle_matrix,color)
            triangle_matrix=empty_matrix()
        elif data[i].strip()=="push":
            push(stack)
        elif data[i].strip()=="pop":
            stack.pop()
        i+=1
   
        
        
def line_box(matrix,x,y,z,x_width,y_width,z_width): #changes made in line_box y+ switched to y-
    add_edge(matrix,x,y,z,x+x_width,y,z)#1 and 3
    add_edge(matrix,x,y,z,x,y-y_width,z)#1 and 2
    add_edge(matrix,x,y-y_width,z,x+x_width,y-y_width,z)# 2 and 4
    add_edge(matrix,x+x_width,y,z,x+x_width,y-y_width,z)#3 and 4
    add_edge(matrix,x,y,z,x,y,z+z_width)#1 and 6
    add_edge(matrix,x,y-y_width,z,x,y-y_width,z+z_width)#2 and 5
    add_edge(matrix,x,y-y_width,z+z_width,x,y,z+z_width)#5 and 6
    add_edge(matrix,x,y,z+z_width,x+x_width,y,z+z_width)#6 and 7
    add_edge(matrix,x,y-y_width,z+z_width,x+x_width,y-y_width,z+z_width)#5 and 8
    add_edge(matrix,x+x_width,y-y_width,z+z_width,x+x_width,y,z+z_width)#8 and 7
    add_edge(matrix,x+x_width,y,z,x+x_width,y,z+z_width)#3 and 7
    add_edge(matrix,x+x_width,y-y_width,z,x+x_width,y-y_width,z+z_width)#4 and 8

def box(matrix,x,y,z,x_width,y_width,z_width):
    add_polygon(matrix,x,y-y_width,z,x+x_width,y-y_width,z,x+x_width,y,z)#2,4,3
    add_polygon(matrix,x,y-y_width,z,x+x_width,y,z,x,y,z)#2,3,1
    add_polygon(matrix,x,y-y_width,z-z_width,x,y-y_width,z,x,y,z)#5,2,1
    add_polygon(matrix,x,y-y_width,z-z_width,x,y,z,x,y,z-z_width)#5,1,6
    add_polygon(matrix,x+x_width,y-y_width,z-z_width,x+x_width,y-y_width,z,x+x_width,y,z)#7,4,3
    add_polygon(matrix,x+x_width,y-y_width,z-z_width,x+x_width,y,z,x+x_width,y,z-z_width)#7,3,8
    add_polygon(matrix,x,y-y_width,z-z_width,x+x_width,y-y_width,z-z_width,x+x_width,y,z-z_width)#5,7,8
    add_polygon(matrix,x,y-y_width,z-z_width,x+x_width,y,z-z_width,x,y,z-z_width)#5,8,6
    add_polygon(matrix,x,y,z,x+x_width,y,z,x+x_width,y,z-z_width)#1,3,8
    add_polygon(matrix,x,y,z,x+x_width,y,z-z_width,x,y,z-z_width)#1,8,6
    add_polygon(matrix,x,y-y_width,z,x+x_width,y-y_width,z,x+x_width,y-y_width,z-z_width)#2,4,7
    add_polygon(matrix,x,y-y_width,z,x+x_width,y-y_width,z-z_width,x,y-y_width,z-z_width)#2,7,5




#def sphere(matrix,cx,cy,cz,radius,step=100):
    

def line_sphere(matrix,cx,cy,cz,radius,step=10):
    rot=0
    t=0
    i=0
    j=0
    x0=radius*math.cos(2*math.pi*0)+cx
    y0=radius*math.sin(2*math.pi*0)*math.cos(math.pi*0)+cy
    z0=radius*math.sin(2*math.pi*0)*math.sin(math.pi*0)+cz
    i+=1
    while j<=step:
        rot=j/step
        while i<=step:
            print(i)
            t=i/step
            x=radius*math.cos(1*math.pi*t)+cx
            y=radius*math.sin(1*math.pi*t)*math.cos(2*math.pi*rot)+cy
            z=radius*math.sin(1*math.pi*t)*math.sin(2*math.pi*rot)+cz
            add_edge(matrix,x0,y0,z0,x,y,z)
            x0=x
            y0=y
            z0=z
            i+=1
        i=0
        j+=1


def sphere(matrix,cx,cy,cz,radius,step=20):# n is 1+step
    rot=0
    t=0
    i=0
    j=0
    n=step+1
    edge=empty_matrix()
    while (j<=step):
        rot=j/step
        while(i<=step):
            t=i/step
            x=radius*math.cos(1*math.pi*t)+cx
            y=radius*math.sin(1*math.pi*t)*math.cos(2*math.pi*rot)+cy
            z=radius*math.sin(1*math.pi*t)*math.sin(2*math.pi*rot)+cz
            add_point(edge,x,y,z)
            i+=1
        if(j>=1):
            k=0
            while(k<step):
                if(k!=step-1):
                    x=edge[(j-1)*(n)+k][0]
                    y=edge[(j-1)*(n)+k][1]
                    z=edge[(j-1)*(n)+k][2]
                    x1=edge[(j-1)*(n)+k+1+n][0]
                    y1=edge[(j-1)*n+k+1+n][1]
                    z1=edge[(j-1)*n+k+1+n][2]
                    x2=edge[(j-1)*n+k+1][0]
                    y2=edge[(j-1)*n+k+1][1]
                    z2=edge[(j-1)*n+k+1][2]
                    add_polygon(matrix,x,y,z,x1,y1,z1,x2,y2,z2)
                if(k!=0):
                    x1=edge[(j-1)*n+k+n][0]
                    y1=edge[(j-1)*n+k+n][1]
                    z1=edge[(j-1)*n+k+n][2]
                    x2=edge[(j-1)*n+k+n+1][0]
                    y2=edge[(j-1)*n+k+n+1][1]
                    z2=edge[(j-1)*n+k+n+1][2]
                    add_polygon(matrix,x,y,z,x1,y1,z1,x2,y2,z2)
                k+=1
                
        i=0
        j+=1
            
def line_torus(matrix,cx,cy,cz,r,R,step=100):
    rot=0
    t=0
    i=0
    j=0
    x0=math.cos(rot)*(r*math.cos(t)+R)+cx
    y0=math.sin(t)*r+cy
    z0=-1*math.sin(rot)*(r*math.cos(t)+cx+R)+cz
    i+=1
    while j<=step:
        rot=j/step
        while i<=step:
            t=i/step
            x=math.cos(2*math.pi*rot)*(r*math.cos(2*math.pi*t)+R)+cx
            y=r*math.sin(2*math.pi*t)+cy
            z=-1*math.sin(2*math.pi*rot)*(r*math.cos(2*math.pi*t)+R)+cz
            add_edge(matrix,x0,y0,z0,x,y,z)
            x0=x
            y0=y
            z0=z
            i+=1
            
        i=0
        j+=1

def torus(matrix,cx,cy,cz,r,R,step=20):
    rot=0
    t=0
    i=0
    j=0
    edge=empty_matrix()
    n=step+1
    while j<=step:
        rot=j/step
        while i<=step:
            t=i/step
            x=math.cos(2*math.pi*rot)*(r*math.cos(2*math.pi*t)+R)+cx
            y=r*math.sin(2*math.pi*t)+cy
            z=-1*math.sin(2*math.pi*rot)*(r*math.cos(2*math.pi*t)+R)+cz
            add_point(edge,x,y,z)
            i+=1
        if j>=1:
            k=0
            while(k<step):
                 x=edge[(j-1)*(n)+k][0]
                 y=edge[(j-1)*(n)+k][1]
                 z=edge[(j-1)*(n)+k][2]
                 x1=edge[(j-1)*(n)+k+n][0]
                 y1=edge[(j-1)*(n)+k+n][1]
                 z1=edge[(j-1)*(n)+k+n][2]
                 x2=edge[(j-1)*(n)+k+n+1][0]
                 y2=edge[(j-1)*(n)+k+n+1][1]
                 z2=edge[(j-1)*(n)+k+n+1][2]
                 add_polygon(matrix,x,y,z,x1,y1,z1,x2,y2,z2)
                 x1=edge[(j-1)*(n)+k+n+1][0]
                 y1=edge[(j-1)*(n)+k+n+1][1]
                 z1=edge[(j-1)*(n)+k+n+1][2]
                 x2=edge[(j-1)*(n)+k+1][0]
                 y2=edge[(j-1)*(n)+k+1][1]
                 z2=edge[(j-1)*(n)+k+1][2]
                 add_polygon(matrix,x,y,z,x1,y1,z1,x2,y2,z2)
                 k+=1
        
        i=0
        j+=1
            
    
def pop(stack):
    stack.pop()
def push(stack):
    matrix=new_matrix()
    i=0
    while i<4:
        j=0
        while j<4:
            up(matrix,i,j,stack[-1][j][i])
            j+=1
        i+=1
    stack.append(matrix)
  
    
screen=new_screen()
buffer=z_buffer()
edge=empty_matrix()
triangle_matrix=empty_matrix()
transform=new_matrix()
ident(transform)
coord=[transform]
parser("script.txt",screen,buffer,[255,0,0],edge,triangle_matrix,coord)
print("sphere.png")
print("second_sphere.png")
print("box.png")
print("torus.png")
print("second_torus.png")
print("robot.png")




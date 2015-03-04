import pyfits as pf
import numpy as np
import matplotlib.pyplot as plt
#from bsub import bsub

## Implementing Code for 1D in a 2D Array ##

def posit(m,n,o,p):

    A=[]
    B=[]
    b=np.arange(0)
    Y=np.arange(0)
    X=np.arange(0)

    F=f[m:n,o:p] # Lines are Y, Cols are X

# Finding centroid for Y (Line Value) #

    for i in np.arange(o,p+1):

        y_1=f[m:n+1,i] # Creating a list of y values selected from m to n, to each col (from o to p)

        for j in y_1:

            b=np.append(b,list(f[:,i]).index(j)) ## getting information about the pixel of high intensities

        for k in b:
            if k > m and k < n+1:
                B.append(k)

        c=np.arange(0)
        d=np.arange(0)

        for l in B:

            c=np.append(c,f[l,i]*l)  ## Nominator of the mean. y[i] correspond to the intensity related to the pixel i.

            d=np.append(d,f[l,i])  ## Denominator of the mean.
        
        if c.sum()/d.sum() != 0.0: 
            Y=np.append(Y,c.sum()/d.sum())


# Finding centroid for X (COL Value) #

    bx=np.arange(0)
    Bx=[]

    for r in np.arange(m,n+1):

        x_1=f[r,o:p+1] # Creating a list of x values selected from o to p, to each line (from m to n)

        for s in x_1:

            bx=np.append(bx,list(f[r,:]).index(s)) ## getting information about the pixel of high intensities

        for t in bx:
            if t > o and t < p+1:
                Bx.append(t)

        cx=np.arange(0)
        dx=np.arange(0)

        for u in Bx:

            cx=np.append(cx,f[r,u]*u)  ## Nominator of the mean. y[i] correspond to the intensity related to the pixel i.

            dx=np.append(dx,f[r,u])  ## Denominator of the mean.
    
        if cx.sum()/dx.sum() != 0.0:            
            X=np.append(X,cx.sum()/dx.sum())

    #print 'X value is', np.mean(X)

    return np.mean(X), np.mean(Y)


## Centroid ##

path  = '/home/leonardo/lab3data/101613/'

AST_x=np.zeros_like(np.empty([136,1]))
AST_y=np.zeros_like(np.empty([136,1]))

file=0
n=input('File (113,114,115,116,117 or 118): ')
for item in (n,):
    myfits1='d'+str(item)+'.fits' # dafne R
    fits1=path+myfits1
    f=pf.getdata(fits1)
    f[:,256]=(f[:,255]+f[:,257])/2. # getting rid of bad column
    hdr=pf.getheader(fits1)

    u=np.zeros_like(np.empty([1024,2]))

    W=np.arange(0)

    for i in np.arange(1024):
        y=f[i,:] 

        u[i,0]=list(y).index(np.max(y))    # X
        u[i,1]=i  # Y

    u[0,1]=0.0

    x=list(u[:,0])
    y=[]

    X=[]
    Y=[]
    j=0

    i=0
    while i < len(x)-1:
        if x[i+1]!=x[i]:
            X.append(x[i])
            Y.append(u[i,1])
        i=i+1


    X0=[X[0]]
    k=0
    while k < len(X)-1:
        if np.abs(X[k+1]-X[k])>5.0:
            X0.append(X[k+1])
        k=k+1

    Y0=[]
    for i in X0:
        Y0.append(u[list(u[:,0]).index(i),1])

    print
    print 'Calculating for file', item
    print

    for i in np.arange(len(X0)):
        m= Y0[i]-3.
        n= Y0[i]+3.
        o= X0[i]-3.
        p= X0[i]+3.

        AST_x[i,file]=posit(m,n,o,p)[0]
        AST_y[i,file]=posit(m,n,o,p)[1]


    file=file+1


## Ploting ##

# First Plot
plt.figure()
imp=plt.imshow(f, cmap='gray_r', vmin=0.0, vmax=15000.)
plt.colorbar()
plt.scatter(X0,Y0, s=160, facecolors='none', edgecolors='r')
plt.show()

# Second Plot
ast_x=[]

for i in np.arange(len(AST_x)):
    if AST_x[i,0] != 0.:
        ast_x.append(AST_x[i,0])
ast_y=[]

for i in np.arange(len(AST_y)):
    if AST_y[i,0] != 0.:
        ast_x.append(AST_y[i,0])

plt.figure()
imp=plt.imshow(f, cmap='gray_r', vmin=0.0, vmax=15000.)
plt.colorbar()
plt.scatter(AST_x,AST_y, s=160, facecolors='none', edgecolors='g')
plt.show()

    

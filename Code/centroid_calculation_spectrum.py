##Tryal to get the max of a pick##

import matplotlib.pyplot as plt
import numpy as np

data=np.genfromtxt('neon_0000.txt', skip_header=17, skip_footer=1) ##register the data

x=data[:,0]  ##array of pixels
y=data[:,1]  ##array of intensities

X=list(x)  ##list of pixels
Y=list(y)  ##list of intensities

### Begin Programm ###

a=np.arange(0)
A=[]
b=np.arange(0)
B=[]
c=np.arange(0)
C=[]


n=input('x min: ')
m=input('x max: ')

for i in np.arange(n,m+1):
    
    A.append(Y[i])

for j in A:

     b=np.append(b,Y.index(j)) ## getting information about the pixel of high intensities

for u in b:
    if u > n and u < m+1:
        B.append(u)

     #b=np.append(b,x[Y.index(n)]*n) ## pixel times it's intensity (to be used in the nominator)

     #c=np.append(c,n) ## creating an array of the intensities (to be used in the denominator)

## Working with the pixel array ## 

#e=[]

#for k in d:

    #e.append(k + int(b.mean()))  ## creating a pixel array related to d and the mean of a

f=np.arange(0)
g=np.arange(0)

for l in B:

    f=np.append(f,y[l]*l)  ## Nominator of the mean. y[i] correspond to the intensity related to the pixel i.


    g=np.append(g,y[l])  ## Denominator of the mean.

print

print 'Pixels: ', b  ## values for the found pixels

print

print 'Pixel Average: ', f.sum()/g.sum()  ## output of pixel location due to the mean


### Graph Part ###

plt.plot(data[:,0], data[:,1], 'b-')

plt.axvline(n, color='g')

plt.axvline(m, color='g')

plt.axvline(x=f.sum()/g.sum(), color='r')

plt.axis([1300,2000,0,3000])

plt.xlabel('Pixel')

plt.ylabel('Intensity [ADU]')

plt.title('Intensity x Pixel Position for Neon')

plt.show()

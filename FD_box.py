"""
D E P A R T E M E N   F I S I K A - U G M
Bulaksumur Yogyakarta, Kabupaten Sleman 55281
-------------------------------------------------------------------------------
Author  : Reizkian Yesaya .R
Email   : reizkianyesaya@gmail.com
Program : 
Created : Mon May 27 23:56:10 2019
"""
import numpy as np
import matplotlib.pyplot as plt

#Parameter Numerik
N=71
L=1
dx = L/(N-1)
dy = L/(N-1)
dt = 0.001

#Parameter Fisis
N_time = 20         # untuk menghitung 1 detik
N_ptime = 50        # step-time untuk tekanan
vis = 0.001         # viskositas kinematik
rho = 1             # massa jenis
nu = vis/rho

#Deklarasi Variabel Ruang
axes1 = np.linspace(0,L,N)
axes2 = np.linspace(-L,0,N)
x,y = np.meshgrid(axes1,axes1) 

u = np.zeros([N,N]) #kecepatan arah-x
v = np.zeros([N,N]) #kecepatan arah-y
P = np.zeros([N,N]) #Tekanan
b = np.zeros([N,N]) #source Tekanan

P[0,:] = 10 
#Definisi Objek
lx=0.2
ly=0.5
position_x=0.4
position_y=0.2
Nx=N
Ny=N
Lx=L
Ly=L
Nax = round(position_x*Nx/Lx)
Nay = round(position_y*Ny/Ly)
Nbx = round( (position_x+lx) * Nx/Lx)
Nby = round( (position_y+ly) * Ny/Ly)

def PressureBoundary():
    P[:,0]  = P[:,1]    # dP/dy = 0  pada y = 0
    P[:,-1] = P[:,-2]   # dP/dy = 0  pada y = 1
def VelocityBoundary():    
    u[:,-1] = 0  #u(x,y=1) = 0
    u[:,0]  = 0  #u(x,y=0) = 0
    u[0,:]  = 0  #u(x=0,y) = 0
    u[-1,:] = 0  #u(x=1,y) = 0
        
    v[:,-1] = 0  #u(x,y=1) = 0
    v[:,0]  = 0  #u(x,y=0) = 0
    v[0,:]  = 0  #u(x=0,y) = 0
    v[-1,:] = 0  #u(x=1,y) = 0
    
#Syarat Batas Tekanan pada objek
def PressureBoundary_Object():
    P[Nax,Nay:Nby] = P[Nax-1,Nay:Nby] #tembok kiri
    P[Nbx,Nay:Nby] = P[Nbx+1,Nay:Nby] #tembok kanan
    P[Nax:Nbx,Nay] = P[Nax:Nbx,Nay-1] #tembok bawah
    P[Nax:Nbx,Nby] = P[Nax:Nbx,Nby+1] #tembok atas


def VelocityBoundary_Object():
    for i in range(Nax,Nbx):
        for j in range(Nay,Nby):
            u[i,j]=0
            v[i,j]=0
            
# Mulai Iterasi
#------------------------------------------------------------------------------
for n in range(N_time):
    percentage = n*100/N_time
    print("RUNNIG =",percentage, "%")
    
    for i in range (1,N-1):
        for j in range (1,N-1):
            u_xcd = ( u[i+1,j] - u[i-1,j] ) / 2 / dx  # du/dx central difference 
            u_ycd = ( u[i,j+1] - u[i,j-1] ) / 2 / dx  # du/dy central difference
            v_xcd = ( v[i+1,j] - v[i-1,j] ) / 2 / dx  # dv/dx central difference
            v_ycd = ( v[i,j+1] - v[i,j-1] ) / 2 / dx  # dv/dy central difference
            b[i,j] = rho*(u_xcd+v_ycd)/dt - rho*(u_xcd**2+v_ycd**2+2*u_ycd*v_xcd)
    
    for t in range(N_ptime):
        for i in range (1,N-1):
            for j in range (1,N-1):
                P_xx = (P[i+1,j] + P[i-1,j]) * (dy**2) # turunan P dua kali x
                P_yy = (P[i,j+1] + P[i,j-1]) * (dx**2) # turunan P dua kali y
                P[i,j] = (P_xx + P_yy - b[i,j]*(dx**2)*(dy**2)) / (dx**2+dy**2) /2
        #Syarat Batas Tekanan
        PressureBoundary()
        PressureBoundary_Object()
        
    un = u.copy()
    vn = v.copy()   
    for i in range(1,N-1):
        for j in range(1,N-1):
            u_x = (un[i,j] - un[i-1,j]) / dx # u turunan x
            u_y = (un[i,j] - un[i,j-1]) / dy # u turunan y   
            v_x = (vn[i,j] - vn[i-1,j]) / dx # v turunan x
            v_y = (vn[i,j] - vn[i,j-1]) / dy # v turunan y           
            
            P_x = (P[i+1,j] - P[i-1,j]) / 2 / dx # P turunan x
            P_y = (P[i,j+1] - P[i,j-1]) / 2 / dy # P turunan y
            
            u_xx = (un[i+1,j] - 2*u[i,j] + un[i-1,j]) / (dx**2) # u turunan x, dua kali
            u_yy = (un[i,j+1] - 2*u[i,j] + un[i,j-1]) / (dx**2) # u turunan y, dua kali
            v_xx = (vn[i+1,j] - 2*v[i,j] + vn[i-1,j]) / (dy**2) # v turunan x, dua kali
            v_yy = (vn[i,j+1] - 2*v[i,j] + vn[i,j-1]) / (dy**2) # v turunan y, dua kali
            
            u[i,j] = un[i,j] + dt*(-u[i,j]*u_x - v[i,j]*u_y - (P_x/rho) + vis*(u_xx+u_yy))
            v[i,j] = vn[i,j] + dt*(-u[i,j]*v_x - v[i,j]*v_y - (P_y/rho) + vis*(v_xx+v_yy))
            
    VelocityBoundary()
    VelocityBoundary_Object()
#------------------------------------------------------------------------------
#Selesai Iterasi


#CODE untuk plot
U=u.T
V=v.T
Pn=P.T

VelocityMagnitude = np.sqrt(U**2+V**2)

#Constructing Plot
total_time = N_time*dt
colorMagnitude = "jet"
colorPressure = "jet"
titleVelocity = "MAGNITUDE KECEPATAN" " (t= 1 s)"
titlePressure = "MEDAN SKALAR TEKANAN" " (t= 1 s)"

fig1 =  plt.figure()
plt.pcolor(x,y,VelocityMagnitude, cmap=colorMagnitude)
plt.colorbar()
plt.quiver(x,y,U,V)
plt.xlabel("x")
plt.ylabel("y")
plt.title(titleVelocity )
plt.show()

fig2 =  plt.figure()
plt.pcolor(x,y,VelocityMagnitude, cmap=colorMagnitude)
plt.colorbar()
plt.streamplot(x,y,U,V, color='k')
plt.xlabel("x")
plt.ylabel("y")
plt.title(titleVelocity)
plt.show()

fig3 =  plt.figure()
plt.pcolor(x,y,Pn, cmap=colorPressure)
plt.colorbar()
plt.quiver(x,y,U,V)
plt.xlabel("x")
plt.ylabel("y")
plt.title(titlePressure)
plt.show()

fig4 =  plt.figure()
plt.pcolor(x,y,Pn, cmap=colorPressure)
plt.colorbar()
plt.streamplot(x,y,U,V, color='k')
plt.xlabel("x")
plt.ylabel("y")
plt.title(titlePressure)
plt.show()
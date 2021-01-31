
import random
import numpy
import math
from solution import solution
import time
from operator import itemgetter


Max_iter=150; #max iterasyon sayısı
NumOfRuns=30  #toplam çalıştırma
SearchAgents_no=10 #Gri kurt sayilari
upper=[99,99,200,200] #kurtların pozisyonlarının üst limiti - problemdeki değişkenlerin üst limiti
lower=[0,0,10,10] #kurtların pozisyonlarının alt limiti - problemdeki değişkenlerin alt limiti
dim=len(upper) #değişken sayısı - problemde 4 adet değişken vardır
min_1= numpy.random.uniform(0, 0, ((NumOfRuns),5 ))
min_2 = numpy.random.uniform(0, 0, (Max_iter,5 ))

def objf(x):
    # if mantıksal sınamada g1,g2,g3,g4 şartları sağladığında maliyeti hesaplayacaktır
    if 0>=((0.0193*x[2])-x[0]) and 0 >= ((0.00954*x[2])-x[2]) and 0>=(1296000-((4/3)*math.pi*(x[2]**3))-(math.pi*(x[2]**2)*x[3])) and 0>=(x[3]-240):
        m= 0.6224*x[0]*x[2]*x[3]+1.7781*x[1]*(x[2]**2)+3.1661*(x[0]**2)*x[3]+19.84*(x[0]**2)*x[2]
        return m
    else:#şartlar sağlamadığında ceza olarak sonsuz sayı (inf) dönecektir
        return float("inf")

def GWO(objf,lb,ub,dim,SearchAgents_no,Max_iter):


    # alpha, beta, and delta_pozisyonlarını belirle
    Alpha_pos=numpy.zeros(dim)
    Alpha_score=float("inf")
    
    Beta_pos=numpy.zeros(dim)
    Beta_score=float("inf")
    
    Delta_pos=numpy.zeros(dim)
    Delta_score=float("inf")

    Positions = numpy.random.uniform(0, 1, (SearchAgents_no,dim ))

    #gri kurtların pozisyonları rastgele alt ve üst sınırları gözeterek belirlenmektedir.
    for i in range(0, SearchAgents_no):
        for j in range(0, dim):
            Positions[i][j] = Positions[i][j] * (ub[j] - lb[j]) + lb[j]



    for i in range(0, SearchAgents_no):
        for j in range(0, dim):
            Positions[i][j] = numpy.clip(Positions[i][j], lb[j], ub[j])
            # üst ve alt limitlerin dışına çıkan gri kurtları üst limiti aştıysa üst limite,
            # alt limiti aştıysa alt limite getirilir.
        # uygunluk fonksiyonunu hesaplar
        fitness=objf(Positions[i,:])

            # Alpha, beta ve deltayı güncelle
        if fitness<Alpha_score :
                Alpha_score=fitness; # alpha'yı güncelle
                Alpha_pos=Positions[i,:]

        if (fitness>Alpha_score and fitness<Beta_score ):
                Beta_score=fitness  # beta'yı güncelle
                Beta_pos=Positions[i,:]

        if (fitness>Alpha_score and fitness>Beta_score and fitness<Delta_score):
                Delta_score=fitness # delta'yı güncelle
                Delta_pos=Positions[i,:]

    for l in range(0, Max_iter):
        a = 2 - l * ((2) / Max_iter);  # a doğrusal olarak 2'den 0'a düşer
        # Tüm gri kurtların pozisyonlarını güncelle
        for i in range(0,SearchAgents_no):
            for j in range (0,dim):     
                           
                r1=random.random() # r1 [0,1] arasında  rastgele oluşturulmuştur
                r2=random.random() # r2 [0,1] arasında  rastgele oluşturulmuştur
                
                A1=2*a*r1-a; # 3.Denklem
                C1=2*r2; # 4.Denklem
                
                D_alpha=abs(C1*Alpha_pos[j]-Positions[i][j]); # 5.Denklem -1. bölüm
                X1=Alpha_pos[j]-A1*D_alpha; # 5.Denklem -1. bölüm
                           
                r1=random.random()
                r2=random.random()
                
                A2=2*a*r1-a; # 3.Denklem
                C2=2*r2; # 4.Denklem
                
                D_beta=abs(C2*Beta_pos[j]-Positions[i][j]); # 5.Denklem -2. bölüm
                X2=Beta_pos[j]-A2*D_beta; # 5.Denklem -2. bölüm
                
                r1=random.random()
                r2=random.random() 
                
                A3=2*a*r1-a; # 3.Denklem
                C3=2*r2; # 4.Denklem
                
                D_delta=abs(C3*Delta_pos[j]-Positions[i][j]); # 5.Denklem -3. bölüm
                X3=Delta_pos[j]-A3*D_delta; # 5.Denklem -3. bölüm
                
                Positions[i][j]=(X1+X2+X3)/3  # 7.Denklem
                Positions[i][j] = numpy.clip(Positions[i][j], lb[j], ub[j])
                # üst ve alt limitlerin dışına çıkan gri kurtları üst limiti aştıysa üst limite,
                # alt limiti aştıysa alt limite getirilir.
        for v in range(0, SearchAgents_no):
            for b in range(0, dim):

                fitness = objf(Positions[v,:])
                # Her bir kurt için uygunluk fonksiyonunu hesaplar
                # Alpha, Beta, ve Delta'yı güncelle
                if fitness < Alpha_score:
                    Alpha_score = fitness;  # alpha'yı güncelle
                    Alpha_pos = Positions[v, :]

                    min_2[l][0] = Alpha_score
                    min_2[l][1]=Alpha_pos[0]
                    min_2[l][2]=Alpha_pos[1]
                    min_2[l][3]=Alpha_pos[2]
                    min_2[l][4]=Alpha_pos[3]

                if (fitness > Alpha_score and fitness < Beta_score):
                    Beta_score = fitness  # beta'yı güncelle
                    Beta_pos = Positions[v, :]

                if (fitness > Alpha_score and fitness > Beta_score and fitness < Delta_score):
                    Delta_score = fitness  # delta'yı güncelle
                    Delta_pos = Positions[v, :]

q=0
w=1
for k in range(0, NumOfRuns):
    GWO(objf, lower,upper, dim, SearchAgents_no, Max_iter)

    for x in range(0,len(min_2)):
        if min_2[x][0]==0:
            min_2[x][0] = float("inf")
    min_2 = sorted(min_2, key=lambda x: x[0])
    for t in range(q, w):
        min_1[t][0]=min_2[0][0]
        min_1[t][1] = min_2[0][1]
        min_1[t][2] = min_2[0][2]
        min_1[t][3] = min_2[0][3]
        min_1[t][4] = min_2[0][4]
        w=w+1
        q=q+1

min_1=sorted(min_1, key=lambda x: x[0])
print("=Basınçlı Kap Tasarımı=")
print("Minimum Maliyet                = "+str(min_1[0][0]))
print("Ts(kabuğun kalınlığı)          = "+str(min_1[0][1]))
print("Th(kafasının kalınlığı)        = "+str(min_1[0][2]))
print("R (iç yarı çap)                = "+str(min_1[0][3]))
print("L(silindirik bölümün uzunluğu) = "+str(min_1[0][4]))
x=numpy.zeros(5)
x[0]=min_1[0][1]
x[1]=min_1[0][2]
x[2]=min_1[0][3]
x[3]=min_1[0][4]
kt=min_1[0][0]
m= 0.6224*x[0]*x[2]*x[3]+1.7781*x[1]*(x[2]**2)+3.1661*(x[0]**2)*x[3]+19.84*(x[0]**2)*x[2]

if 0>=((0.0193*x[2])-x[0]) and 0 >= ((0.00954*x[2])-x[2]) and 0>=(1296000-((4/3)*math.pi*(x[2]**3))-(math.pi*(x[2]**2)*x[3])) and 0>=(x[3]-240  ):
    print("--Doğrulaması Yapıldı--")
    print(str(kt))
    print(str(m))

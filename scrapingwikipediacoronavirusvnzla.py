# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 22:08:23 2020

@author: piki1
"""
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url='https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Venezuela'
html = urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")

casosdias=soup('span',{'style':'width: 3.5em;padding:0 0.3em 0 0; text-align:right; display: inline-block;'})

#cantidad de casos en venezuela  por día

cantidad=[]

count=0
for tag in casosdias:
    try:
        cases=int(tag.contents[0])
    except:
        n=count-1
        cases=int(casosdias[n].contents[0])
    cantidad.append(cases)
    count+=1
#La cantidad es la suma acumulativa, hay que diferenciar i - i-1
PorDia=[]
PorDia.append(cantidad[0])
for i in range(1,len(cantidad)):
    dia=cantidad[i]-cantidad[i-1]
    PorDia.append(dia)


#Fechas por dia
Fechas=[]
dates=soup('td',{'style':'padding-left:0.4em; padding-right:0.4em; text-align:center'})

for tag in dates[0::3]:
    date=str(tag.contents[0])
    if '2020' in date:
        Fechas.append(date)
    else:
        date='20-03-2020'
        Fechas.append(date)
    


#Estados y cantidad por estados

Estados=[]
tags1=soup('table',{'class':'wikitable sortable col3der'}) 
tags2=tags1[0]('a',title=True) #no importa que tenga title pero que tenga ese atributo

for tag in tags2:
    Estados.append(str(tag.contents[0]))

CasosPorEstado=[]
tags3=tags1[0]('td')
for tag in tags3[1::3]:
    CasosPorEstado.append(int(tag.contents[0]))


#DataFrames:
    
Cases=pd.DataFrame(columns=['Dates','CasesPerDay','AcumulativeSum'])

Cases['Dates']=Fechas
Cases['CasesPerDay']=PorDia
Cases['AcumulativeSum']=cantidad

Cases_States=pd.DataFrame(columns=['state','CasesPerState'])

Cases_States['state']=Estados
Cases_States['CasesPerState']=CasosPorEstado


Cases.to_csv('./Cases.csv')
Cases_States.to_csv('./Cases_States.csv')


#Recuperados,muertes,total:
td=[]
tags=soup('table',{'style':'width:22.7em; line-height: 1.4em; text-align:left; padding:.23em;'})
tags1=tags[0]('tr')
for tag in tags1:
    td.append(tag('td'))
    
td1=[]  
for i in range(0,len(td)):
    if len(td[i])!=0:
        td1.append(td[i])
        
Total=int(td1[13][0].contents[0])
Muertes=int(td1[14][0].contents[0])
Recuperados=int(td1[15][0].contents[0])
Activos=Total-Recuperados    
 
       
Status=pd.DataFrame(columns=['status','total'])
Status['status']=['Total','Active','Death','Recovered']
Status['total']=[Total,Activos,Muertes,Recuperados]

Status.to_csv('./Status.csv') 


#Imagen:

imgurl ="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/COVID-19_Outbreak_Cases_in_Venezuela.svg/500px-COVID-19_Outbreak_Cases_in_Venezuela.svg.png"

urlretrieve(imgurl, "venezuela.png")

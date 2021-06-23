import requests
from bs4 import BeautifulSoup
import csv
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from collections import Counter



url = "https://www.tripadvisor.com.mx/Hotel_Review-g292027-d674247-Reviews-Tranquility_Bay_Beach_Retreat-Trujillo_Colon_Department.html#REVIEWS"

comentarios = []
# Itera por páginas de comentarios
for i in range(2): 
    print(f"Consiguiendo los comentarios de la página {i+1}")
    # solicitud GET a la página
    r = requests.get(url) 
    # Estructuración del contenido de la página
    soup = BeautifulSoup(r.content, "html.parser") 
    # Conseguir los elementos html de los comentarios
    comentarios_pagina = soup.findAll("q", attrs={'class': 'IRsGHoPm'})
    # Conseguir el texto de los comentarios 
    comentarios_pagina = [ c.text for c in comentarios_pagina] 
    # Guardo los comentarios en una lista
    comentarios += comentarios_pagina 


    # Conseguir el url de la pagina siguiente
    url =  "https://www.tripadvisor.com.mx" + soup.find("a", attrs={"class": "ui_button nav next primary"})["href"] 

# Guarda los comentarios en un csv
with open("comentarios.txt", "w+",encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["comentarios"])
    for c in comentarios:
        writer.writerow([c]) 

lista = []
lista2 = []
lista3 = []
lista4 = []
lista5 = []
ss = SnowballStemmer("spanish")

with open('comentarios.txt','r',encoding="utf-8") as file:
    reader = csv.reader(file)
    
    next(reader)
    
    for r in reader:
        lista.append(r)
        
    lista2 = [x for x in lista if x != []]
     
    
    for i in range(len(lista2)):
        lista3.append(word_tokenize(lista2[i][0]))
        
    for r in range(len(lista3)):
        for t in range(len(lista3[r])):
            lista4.append(ss.stem(lista3[r][t]))
      
with open("stemming.txt", "w+",encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["reducir"])
    for c in lista4:
        writer.writerow([c]) 

for i in range(len(lista3)):
    lista5.append(list(map(str.lower , lista3[i])))
    

####################### STOP_WORDS ############################        
lista_sw = []

for i in range(len(lista5)):
    texto = lista5[i]
    #texto = word_tokenize(lista2[i][0]) 
    sw=[w for w in texto if not w in stopwords.words('Spanish')]
    lista_sw.append(sw)
     
stopw = []
for i in range(len(lista_sw)) :
    cuerpo = " ".join(lista_sw[i])
    stopw.append(cuerpo)

with open("stop-words.txt", "w+",encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["palabras-vacias"])
    for c in stopw:
        writer.writerow([c]) 
        
#################### Diccionario de frecuencia #################  
frecuencia = []

for i in range(len(lista_sw)):
    list1 = lista_sw[i]
    counts = Counter(list1)
    mayor = max(counts.keys())
    frecuencia.append(mayor)

print("")
print("Las palabras con mayor frecuencis fueron:")
print("")
print(frecuencia)






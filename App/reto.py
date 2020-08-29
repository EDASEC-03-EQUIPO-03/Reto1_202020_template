"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv

from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt
from Sorting import selectionsort as sort 
from time import process_time 

def cmp1(element1,element2):
    if element1 == element2["nombre"]:
        return True

def less(element1, element2):
    if float(element1["vote_count"]) < float(element2["vote_count"]):
        return True

def less2(element1, element2):
    if float(element1["vote_average"]) < float(element2["vote_average"]):
        return True
    return False

def greater1(element1, element2):
    if float(element1['vote_count']) > float(element2['vote_count']):
        return True
    return False

def greater2(element1, element2):
    if float(element1['vote_average']) > float(element2['vote_average']):
        return True
    return False

def greater_director(element1, element2):
    if float(element1['conteo']) > float(element2['conteo']):
        return True
    return False
def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking")
    print("0- Salir")

def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1



def loadCSVFile (file, cmpfunction):
    lst=lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        with open(  cf.data_dir + file, encoding="utf-8") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst


def loadMovies ():
    lst = loadCSVFile("theMoviesdb/SmallMoviesDetailsCleaned.csv",compareRecordIds)
    lst2 = loadCSVFile("theMoviesdb/MoviesCastingRaw-small.csv",compareRecordIds)
    print("Datos cargados, " + str(lt.size(lst)) + " pelicualas cargadas.")
    print("Datos cargados, " + str(lt.size(lst2)) + " datos del casting.")
    return lst,lst2

def Ranking_de_peliculas(lista,tipo_votacion,orden,num_peliculas):
    if lista['size']==0:
        print("La lista esta vacía")  
        return 0
    else:

        
        lista_final=lt.newList("ARRAY_LIST")
        if tipo_votacion=="vote_count" and orden.lower() == "peores" :
            sort.selectionSort(lista,less)
            iterador= it.newIterator(lista)
            counter=1
            while it.hasNext(iterador) and counter<=int(num_peliculas):
                element=it.next(iterador)
                lt.addLast(lista_final,element)
                
                counter+=1
            
        elif tipo_votacion=="vote_count" and orden.lower() == "mejores" :
            sort.selectionSort(lista,greater1)
            iterador= it.newIterator(lista)
            counter=1
            while it.hasNext(iterador) and counter<=int(num_peliculas):
                element=it.next(iterador)
                lt.addLast(lista_final,element)
                counter+=1

        elif tipo_votacion=="vote_average" and orden.lower() == "peores":
            sort.selectionSort(lista,less2)
            iterador= it.newIterator(lista)
            counter=1
            while it.hasNext(iterador) and counter<=int(num_peliculas):
                element=it.next(iterador)
                lt.addLast(lista_final,element)
                counter+=1
        
        elif tipo_votacion=="vote_average" and orden.lower() == "mejores":
            sort.selectionSort(lista,greater2)
            iterador= it.newIterator(lista)
            counter=1
            while it.hasNext(iterador) and counter<=int(num_peliculas):
                element=it.next(iterador)
                lt.addLast(lista_final,element)
                counter+=1

        
    
    return lista_final

def conocer_a_director(lista,lista2,nombre_director):
    if lista['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        counter=0
        votos_p=0
        lista_final=lt.newList("ARRAY-LIST")
        iterador=it.newIterator(lista)
        while it.hasNext(iterador):
            element=it.next(iterador)
            
            
            if element["director_name"].lower()==nombre_director.lower():
                id1=element["id"]
                iterador2=it.newIterator(lista2)
                while it.hasNext(iterador2):
                    element2=it.next(iterador2)
                    id2=element2["id"]
                    if id1==id2:
                        lt.addLast(lista_final,element2)
                        counter+=1
                        voto=float(element2["vote_average"])
                        votos_p+=voto
    promedio=votos_p/counter
    
    return lista_final,counter,promedio

def conocer_un_actor(lista,lista2,nombre_actor):
    if lista['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        autor = {'Nombre':nombre_actor, "Peliculas":None,  "Directores":None}
        peliculas= lt.newList("ARRAY_LIST")
        Directores= lt.newList("ARRAY_LIST",cmpfunction=cmp1)
        conteo=0
        sumatoria=0
        iterador=it.newIterator(lista)
        while it.hasNext(iterador):
            elemento=it.next(iterador)
            encontre=False
            i=1
            while i<=5 and not encontre:
                actor=elemento["actor"+str(i)+"_name"]
                if actor.lower ()== nombre_actor.lower():
                    encontre=True
                i+=1
            if encontre==True:
                id1=elemento["id"]
                director=elemento["director_name"]
                iterador2=it.newIterator(lista2)
                encontro2=False
                while it.hasNext(iterador2) and not encontro2:
                    elemento2=it.next(iterador2) 
                    id2=elemento2["id"]
                    if id1==id2:
                        encontro2=True
                        lt.addLast(peliculas,elemento2)
                        conteo+=1
                        sumatoria+=float(elemento2["vote_average"])
                        iterador4=it.newIterator(Directores)
                        encontro3=False
                        while it.hasNext(iterador4) and not encontro3:
                            elemento4=it.next(iterador4)
                            if director==elemento4["nombre"]:
                                encontro3=True
                        if encontro3 == False:
                            lt.addLast(Directores,{"nombre":director,"conteo":0})
                        iterador3=it.newIterator(Directores)
                        while it.hasNext(iterador3):
                            elemento3=it.next(iterador3)
                            if director==elemento3["nombre"]:
                                elemento3["conteo"]+=1
    
                    
        sort.selectionSort(Directores,greater_director)
        mas=lt.getElement(Directores,1)
        autor["Peliculas"]=peliculas
        autor["Directores"]=Directores
        promedio=sumatoria/conteo

    return autor,mas,conteo,promedio


         
    #def conocer_un_actor()                  

def conocer_genero(lista,genero):

    if lista['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        Generos=lt.newList("ARRAY_LIST")
        suma=0
        iterador= it.newIterator(lista)
        
        while it.hasNext(iterador):
            element=it.next(iterador)
            genero_lista=element["genres"]
            if genero.lower() in genero_lista.lower():
                lt.addLast(Generos,element)
                suma+=float(element["vote_average"])
                
    
    promedio=suma/lt.size(Generos)
    return Generos,lt.size(Generos),promedio

def ranking_genero(lista,genero,tipo_votacion,orden,num_peliculas):
    
    if lista['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        lista_final=lt.newList("ARRAY_LIST")
        peliculas,tamaño,promedio=conocer_genero(lista,genero)
        iterador=it.newIterator(peliculas)
        if tipo_votacion=="vote_count" and orden.lower() == "peores" :
            sort.selectionSort(peliculas,less)
            lista_final=lt.subList(peliculas,1,int(num_peliculas))
            iterador= it.newIterator(lista_final)
            counter=0
            while it.hasNext(iterador):
                element=it.next(iterador)
                counter+=float(element["vote_count"])
            
        elif tipo_votacion=="vote_count" and orden.lower() == "mejores" :
            sort.selectionSort(peliculas,greater1)
            lista_final=lt.subList(peliculas,1,int(num_peliculas))
            iterador= it.newIterator(lista_final)
            counter=0
            while it.hasNext(iterador):
                element=it.next(iterador)
                counter+=float(element["vote_count"])

        elif tipo_votacion=="vote_average" and orden.lower() == "peores":
            sort.selectionSort(peliculas,less2)
            lista_final=lt.subList(peliculas,1,int(num_peliculas))
            iterador= it.newIterator(lista_final)
            counter=0
            while it.hasNext(iterador):
                element=it.next(iterador)
                counter+=float(element["vote_average"])
        
        elif tipo_votacion=="vote_average" and orden.lower() == "mejores":
            sort.selectionSort(peliculas,greater2)
            lista_final=lt.subList(peliculas,1,int(num_peliculas))
            iterador= it.newIterator(lista_final)
            counter=0
            while it.hasNext(iterador):
                element=it.next(iterador)
                counter+=float(element["vote_count"])
        
    promedio=counter/lt.size(lista_final)
    return lista_final,promedio 



def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """


    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:

            if int(inputs[0])==1: #opcion 1
                lst1,lst2 = loadMovies()

            elif int(inputs[0])==2: #opcion 2
                tipo_votacion=input("Ingrese el tipo de votacion al que quiere acceder (vote_count/vote_average):\n")
                orden=input("Ingrese si quiere ver las mejores o peores peliculas (mejores/peores):\n")
                numero_peliculas=input("ingrese el numero de peliculas que desea ver:\n")
                me_pe=Ranking_de_peliculas(lst1,tipo_votacion,orden,numero_peliculas)
            
                print("Se tiene un numero de las",numero_peliculas,orden,"peliculas de acuerdo a",tipo_votacion,"\n")
                iterador=it.newIterator(me_pe)
                while it.hasNext(iterador):
                    elemento=it.next(iterador)
                    print(elemento,"\n","-------------------"*7)

            elif int(inputs[0])==3: #opcion 3
                Nombre_director=input("Ingrese el nombre del director que desea conocer:\n")
                peliculas,numero,promedio=conocer_a_director(lst2,lst1,Nombre_director)
                print("Se tiene un numero de ",numero,"peliculas de el director",Nombre_director,"Las cuales son:","\n")
                iterador=it.newIterator(peliculas)
                while it.hasNext(iterador):
                    elemento=it.next(iterador)
                    print(elemento,"\n","-------------------"*7)

                print("Y el promedio de calificacion de sus peliculas es:",promedio)

            elif int(inputs[0])==4: #opcion 4
                Nombre_actor=input("Ingrese el nombre del actor que desea conocer:\n")
                actor,director,conteo,promedio=conocer_un_actor(lst2,lst1,Nombre_actor)
                print("Se tienen un numero de",conteo,"peliculas de el actor",Nombre_actor,"Las cuales son\n")
                iterador=it.newIterator(actor["Peliculas"])
                while it.hasNext(iterador):
                    elemento=it.next(iterador)
                    print(elemento,"\n","-------------------"*7)
                print("El promedio de votacion de sus peliculas es:",promedio,"y el director con mayores colaboraciones es:",director["nombre"])
                print(actor["Directores"])

            elif int(inputs[0])==5: #opcion 5
                Genero=input("Ingrese el genero de interes:\n")
                Generos,tamaño,promedio=conocer_genero(lst1,Genero)
                iterador=it.newIterator(Generos)
                while it.hasNext(iterador):
                    elemento=it.next(iterador)
                    print(elemento,"\n","-------------------"*7)
                print("Se tienen un numero de",tamaño,"peliculas, de acuerdo al genero",Genero)
                print("Y su promedio de votacion (vote average) es:",promedio)

            elif int(inputs[0])==6: #opcion 6
                genero=input("Ingrese el genero de interes:\n")
                tipo_votacion=input("Ingrese el tipo de votacion al que quiere acceder (vote_count/vote_average):\n")
                orden=input("Ingrese si quiere ver las mejores o peores peliculas (mejores/peores):\n")
                numero_peliculas=input("ingrese el numero de peliculas que desea ver:\n")
                peliculas,promedio=ranking_genero(lst1,genero,tipo_votacion,orden,numero_peliculas)
                print("Estas son las",numero_peliculas,orden,"peliculas de el genero",genero,"de acuerdo a",tipo_votacion,"\n")
                iterador=it.newIterator(peliculas)
                while it.hasNext(iterador):
                    elemento=it.next(iterador)
                    print(elemento,"\n","-------------------"*7)
                print("Y su promedio de votacion es:",promedio)

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()
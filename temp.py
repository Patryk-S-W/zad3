# -*- coding: utf-8 -*-
###############################################################################
#
# Python 3
#
# Wcięcia realizowane są czterema spacjami.
#
# Doinstalowanie bibliotek numpy i matplotlib:
# pip install numpy
# pip install matplotlib
#
# Uruchamianie skryptu:
# python dane.py
# albo wymuszając Pythona 3 gdy nie jest on domyślny:
# py -3 dane.py
#
###############################################################################
#
# Plik dane.csv zawiera dane zbierane na węźle ciepłowniczym przez 
# przedsiębiorstwo dostarczające ciepło do budynku (patrz opisy kolumn w pliku). 
# Niniejszy skrypt dokonuje podstawowej analizy wybranych danych z pliku.
#
# A.
# Wczytanie obserwacji dla wybranych zmiennych.
#
# B.
# Sprawdzenie podstawowych statystyk dla poszczególnych zmiennych.
# Wykreślenie histogramów.
#
# C.
# Identyfikacja zmiennych, w których występują potencjalnie błędne dane (obserwacje)
# lub braki danych. Naprawa danych.
#
# D.
# Obliczenie unormowanych korelacji pomiędzy poszczególnymi zmiennymi.
#
# E.
# Przeprowadzenie regresji liniowej dla wybranych zmiennych, wraz z wykresami.
#
###############################################################################
#
# W skrypcie znajdują się zadania do wykonania (w sumie za 3p.)
#
###############################################################################

import csv
import numpy as np
import matplotlib.pyplot as plt
#######################
# A. Wczytanie danych #
#######################
  
przeplyw = []        # Przepływ wody przez węzeł [l/h]
temp_zas = []        # Temperatura zasilania (temperatura wody na wejściu do węzła) [C]
temp_pow = []        # Temperatura powrotu (temperatura wody na wyjściu z węzła) [C]
roznica_temp = []    # Różnica temperatur, wynikająca z oddanej energii w węźle [C]
moc = []             # Moc oddana w węźle [kW]
    
try:
    plik = open('dane.csv', 'rt')
except FileNotFoundError:
    print("Nie ma pliku")
    raise SystemExit


dane = csv.reader(plik, delimiter=',')
next(dane)                # Opuszczamy pierwszy wiersz - nagłówek
for obserwacja in dane:   # Iterujemy po poszczególnych obserwacjach
    przeplyw.append(float(obserwacja[6]))
    temp_zas.append(float(obserwacja[7]))
    temp_pow.append(float(obserwacja[8]))
    roznica_temp.append(float(obserwacja[9]))
    moc.append(float(obserwacja[12]))
plik.close()

### ZADANIE (0.2p.) ###
# Zabezpieczyć powyższe wczytywanie danych przed:
# (1) brakiem pliku dane.csv,
# (2) danymi, których nie da się przekonwertować na liczby
# W obu przypadkach skrypt powinien wyświetlić komunikat i zakończyć działanie.
### KONIEC ###

# Odwracamy dane na listach (żeby były ułożone chronologicznie)    
przeplyw.reverse()
moc.reverse()
temp_zas.reverse()
temp_pow.reverse()
roznica_temp.reverse()
        
# Tworzymy słownik: kluczem jest nazwa zmiennej a wartością - zmienna
zmienne = {"temp_zas":temp_zas, "temp_pow":temp_pow, "roznica_temp":roznica_temp, "przeplyw":przeplyw, "moc":moc}


######################################
# B. Podstawowe statystyki i wykresy #
######################################
    
# Iterujemy po słowniku, wyświetlając statystyki dla poszczególnych zmiennych
for nazwa,zmienna in zmienne.items():
    print()
    print("Zmienna:",nazwa)
    print("MIN:", min(zmienna))   
    print("MAX:", max(zmienna))
    print("ŚREDNIA:", np.mean(zmienna))
    print("MEDIANA:", np.median(zmienna))
    print("ZAKRES:", np.ptp(zmienna))
    print("ODCHYLENIE STANDARDOWE:", np.std(zmienna))
    print("WARIANCJA:", np.var(zmienna))
    print("PERCENTYL 90%:", np.percentile(zmienna,90) )
    print("HISTOGRAM:", np.histogram(zmienna))

    # Czcionka do wykresów, z polskimi znakami.
    plt.rc('font', family='Arial')

    # Wykres - histogram
    plt.hist(zmienna, 100)
    plt.title('Histogram dla: ' + nazwa)
    plt.xlabel('Przedział')
    plt.ylabel('Liczba obserwacji')
    plt.show()

    
############################################
# C. Analiza anomalii i czyszczenie danych # 
############################################

# Zidentyfikowaliśmy problem - "dziwne", znacząco za duże niektóre wartości dla zmiennych:
zmienne_do_naprawienia = {"roznica_temp":roznica_temp, "przeplyw":przeplyw, "moc":moc}

### ZADANIE (0.5p.) ###
# Zrealizować automatyczne dodawanie "podejrzanych" zmiennych do słownika "zmienne_do_naprawienia",
# na podstawie analizy statystyk danej zmiennej.
### KONIEC ###

print()
print("CZYSZCZENIE DANYCH")

for nazwa,zmienna in zmienne_do_naprawienia.items():
    for index,wartosc in enumerate(zmienna): # Iterujemy po wszystkich obserwacjach
        # Zakładamy (na podstawie analizy danych), że anomalia to wartość powyżej 10000
        if (wartosc > 10000): 
            print("Dla zmiennej {} pod indeksem {} znaleziono anomalię o wartości {}".format(nazwa, index, wartosc))
            # Wstawiamy medianę:
            mediana = np.median(zmienna)
            print("Naprawiam. Stara wartość: {}, nowa wartość: {}".format(zmienna[index], mediana))
            zmienna[index] = mediana

### ZADANIE (0.2p.) ###
# Znaleźć inną metodę wyznaczania progu anomalii w powyższej pętli tak, aby nie była to
# "hardkodowana" wartość 10000, ale liczba wyznaczana indywidualnie dla każdej zmiennej.
### KONIEC ###
from matplotlib.backends.backend_pdf import PdfPages

# Statystyki dla naprawionych zmiennych
for nazwa,zmienna in zmienne.items():
    print()
    print("Zmienna (naprawiona):",nazwa)
    print("MIN:", min(zmienna))   
    print("MAX:", max(zmienna))
    print("ŚREDNIA:", np.mean(zmienna))
    print("MEDIANA:", np.median(zmienna))
    print("ZAKRES:", np.ptp(zmienna))
    print("ODCHYLENIE STANDARDOWE:", np.std(zmienna))
    print("WARIANCJA:", np.var(zmienna))
    print("PERCENTYL 90%:", np.percentile(zmienna,90)) 
    print("HISTOGRAM:", np.histogram(zmienna))
    with PdfPages("{}.pdf".format(nazwa)) as pdf:
        plt.hist(zmienna, 100)
        plt.title('Histogram dla: ' + nazwa)
        plt.xlabel('Przedział')
        plt.ylabel('Liczba obserwacji')
        pdf.savefig()
        plt.show()
        
### ZADANIE (0.4p.) ###
# Zapisać naprawione dane do pliku dane-naprawione.csv, zachowując zgodność z plikiem oryginalnym.
### KONIEC ###

### ZADANIE (0.5p.) ###
# Zapisać powyższe statystyki i wykresy do plików PDF, osobnych dla poszczególnych zmiennych
# (można wykorzystać dowolny moduł/bibliotekę).
### KONIEC ###


#########################################
# D. Badanie korelacji między zmiennymi #
#########################################
       
print()      
print("KORELACJE")

# Piszemy funkcję, która zwróci korelację unormowaną między zestawami danych
def ncorrelate(a,b):
    '''Funkcja zwraca unormowaną wartość korelacji'''
    a = (a - np.mean(a)) / (np.std(a) * len(a))
    b = (b - np.mean(b)) / np.std(b)
    return np.correlate(a, b)[0]

# --- Częsć pomocnicza, wyjasniająca pojęcie korelacji --- 
# Przykłady korelacji:    
a = range(100)     # [0, 1, 2, 3...] 
# 1. Spodziewamy się wyniku: 1 (bardzo silna korelacja między danymi)
b = range (1,101)  # [1, 2, 3, 4...]
print("Przykład 1. a, b skorelowane:", ncorrelate(a, b))

a = range(100)     # [0, 1, 2, 3...] 
b = [0.1]*100 # Wypełniamy liczbami zmiennoprzecinkowymi, żeby w ncorrelate nie wystąpiło dzielenie przez zero
# 2. Spodziewamy się wyniku: około 0 (bardzo słaba korelacja między danymi)    
print("Przykład 2. a, b nieskorelowane:", ncorrelate(a, b))
print()
# --- koniec częsć pomocnicza ---

### ZADANIE (0.2p.) ###
# Poszukać funkcji z pakietu numpy, która wykonuje identyczne zadanie jak
# funkcja ncorrelate() i ją wykorzystać.
### KONIEC ###

# Badamy korelacje między wszystkimi (różnymi od siebie) zmiennymi
for nazwa1,zmienna1 in zmienne.items():
    for nazwa2,zmienna2 in zmienne.items():
        if nazwa1 != nazwa2:
            print("Korelacja między", nazwa1,"a", nazwa2,"wynosi:", end=" ")
            print(ncorrelate(zmienna1,zmienna2))

### ZADANIE (0.4p.) ###
# Zebrać powyższe wyniki korelacji w dwuwymiarowej liście postaci:
# [[zmienna1, zmienna2, korelacja], [..., ..., ...], ... ] tak, aby elementy tej listy
# były posortowane malejąco wg. wartości korelacji.
### KONIEC ###
            
# Przykładowe wykresy

# 1. Zmienne z dużą korelacją dodatnią: moc, przeplyw

# Wykres liniowy
plt.plot(range(len(moc)), moc, "x")
plt.plot(range(len(przeplyw)), przeplyw, "+")
plt.title("Duża korelacja dodatnia")
plt.ylabel('x: moc; +: przeplyw')
plt.xlabel('Numer obserwacji')
plt.show()

# Dla lepszej ilustracji: wycinek danych.
# Zmienna moc przemnożnona przez 10, aby lepiej było widać korelację.
plt.plot(range(len(moc[1000:1100])), [i*10 for i in moc[1000:1100]])
plt.plot(range(len(przeplyw[1000:1100])), przeplyw[1000:1100])
plt.title("Duża korelacja dodatnia. Zmienna moc przemnożona przez 10.")
plt.ylabel('dół: moc; góra: przeplyw')
plt.xlabel('Numer obserwacji')
plt.show()

# Wykres zależności przeplyw od moc
plt.plot(moc, przeplyw, '.')
plt.title("Duża korelacja dodatnia")
plt.xlabel('moc')
plt.ylabel('przeplyw')
plt.show()

# 2. Zmienne skorelowane ujemnie: roznica_temp, temp_pow

# Wykres liniowy
plt.plot(range(len(roznica_temp)), roznica_temp, "x")
plt.plot(range(len(temp_pow)), temp_pow, "+")
plt.title("Średnia korelacja ujemna")
plt.ylabel('x: roznica_temp; +: temp_pow')
plt.xlabel('Numer obserwacji')
plt.show()

# Dla lepszej ilustracji: wycinek danych
plt.plot(range(len(roznica_temp[1000:1100])), roznica_temp[1000:1100])
plt.plot(range(len(temp_pow[1000:1100])), temp_pow[1000:1100])
plt.title("Średnia korelacja ujemna.")
plt.ylabel('dol: roznica_temp; gora: temp_pow')
plt.xlabel('Numer obserwacji')
plt.show()

# Wykres zależności temp_pow od roznica_temp
plt.plot(roznica_temp, temp_pow, '.')
plt.title("Średnia korelacja ujemna.")
plt.xlabel('roznica_temp')
plt.ylabel('temp_pow')
plt.show()


#######################
# E. Regresja liniowa #
#######################

# Analiza przeprowadzona tylko dla jednej zmiennej, temp_zas

print()
print("REGRESJA LINIOWA")
# Wybieramy zmienną temp_zas w funkcji numeru obserwacji
x = range(len(temp_zas))
y = temp_zas
# Liczymy współczynniki regresji - prostej
a,b = np.polyfit(x,y,1)  # Wielomian 1 rzędu - prosta
print("Wzór prostej: y(x) =",a,"* x +",b)
# Wyliczamy punkty prostej otrzymanej w wyniku regresji
yreg =  [a*i + b for i in x] 
# Wykresy
plt.plot(x,y)
plt.plot(x,yreg)
plt.title("Regresja liniowa dla całosci danych zmiennej temp_zas")
plt.xlabel('Numer obserwacji')
plt.ylabel('temp_zas')
plt.show()

# Teraz dzielimy na trzy zakresy (odpowiadające poszczególnym okresom grzewczym):
# [0:11000], [11000:20000], [20000:do końca]
# (granice zakresów zostały określone na podstawie powyższego wykresu)
# i liczymy regresję w tych zakresach. 


x1 = x[:11150]
y1 = temp_zas[:11150]
a1,b1 = np.polyfit(x1,y1,1) 
print("Wzór prostej: y(x) =",a1,"* x +",b1)
yreg1 =  [a1*i + b1 for i in x1] 

x2 = x[11150:20000]
y2 = temp_zas[11150:20000]
a2,b2 = np.polyfit(x2,y2,1) 
print("Wzór prostej: y(x) =",a2,"* x +",b2)
yreg2 =  [a2*i + b2 for i in x2] 

x3 = x[20000:]
y3 = temp_zas[20000:]
a3,b3 = np.polyfit(x3,y3,1)
print("Wzór prostej: y(x) =",a3,"* x +",b3)
yreg3 =  [a3*i + b3 for i in x3] 

# Wykres trzech prostych regresji dla poszczególnych fragmentów
plt.plot(x,y)
plt.plot(x1,yreg1)
plt.plot(x2,yreg2)
plt.plot(x3,yreg3)
plt.title("Regresja liniowa dla podzakresów zmiennej temp_zas")
plt.xlabel('Numer obserwacji')
plt.ylabel('temp_zas')
plt.show()

### ZADANIE (0.4p.) ###
# Przeprowadzić regresję wielomianową wielomianem 2 stopnia dla zmiennej temp_zas.
# Narysować wykres otrzymanej krzywej na tle zmiennej temp_zas.

print()
print("REGRESJA WIELOMIANOWA")
# Wybieramy zmienną temp_in w funkcji numeru obserwacji
x = range(len(temp_zas))
y = temp_zas
# Liczymy współczynniki regresji - prostej
print("{}".format(np.polyfit(x,y,2)))
a,b, c = np.polyfit(x,y,2)  # Wielomian 1 rzędu - prosta
print("Wzór prostej: y(x) =",a,"* x +",b)
# Wyliczamy punkty prostej otrzymanej w wyniku regresji
yreg =  [a*(i**2) + b*i + c  for i in x]
# Wykresy
plt.plot(x,y)
plt.plot(x,yreg)
plt.title("Regresja wielomianowa dla całosci danych zmiennej temp_zas")
plt.xlabel('Numer obserwacji')
plt.ylabel('temp_zas')
plt.show()

### KONIEC ###

# Regresja liniowa dla zmiennych z dużą korelacją dodatnią: moc, przeplyw
a,b = np.polyfit(moc,przeplyw,1)  # Wielomian 1 rzędu - prosta
yreg =  [a*i + b for i in moc] 
# Wykresy
plt.plot(moc,przeplyw,".")
plt.plot(moc,yreg)
plt.title("Regresja liniowa")
plt.xlabel('moc')
plt.ylabel('przeplyw')
plt.show()

# Regresja liniowa dla zmiennych ze słabą korelacją ujemną: roznica_temp, temp_pow
a,b = np.polyfit(roznica_temp,temp_pow,1)  # Wielomian 1 rzędu - prosta
yreg =  [a*i + b for i in roznica_temp] 
# Wykresy
plt.plot(roznica_temp,temp_pow,".")
plt.plot(roznica_temp,yreg)
plt.title("Regresja liniowa")
plt.xlabel('roznica_temp')
plt.ylabel('temp_pow')
plt.show()

# Predykcja danych z losowej listy
roznica_temp = []	
import random
for i in range(20):
	roznica_temp.append(random.randint(0,100))
	
# Wyliczenie wyników na podstawie regresji i zapis do listy
predykcja = [[i, a*i+b] for i in roznica_temp]
print("Wyniki predykcji [roznica_temp, temp_pow]:",predykcja)

### ZADANIE (0.2p.) ###
# Zapisać wyniki powyższej predykcji do pliku YAML: predykcja.yaml, w formacie:
# predykcje:
#   - roznica_temp: X1
#     temp_pow: Y1
#   - roznica_temp: X2
#     temp_pow: Y2
#   ...
### KONIEC ###

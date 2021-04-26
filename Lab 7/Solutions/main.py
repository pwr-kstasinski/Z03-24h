from tkinter import *
from tkinter.ttk import Combobox
import requests
import json
import os
import io
from PIL import Image, ImageTk
import tkinter as tk
from urllib.request import urlopen


API_key = "3f686ccab03e14e9629ac212bbeab5e9"
gui = Tk()
gui.title("Weather forecast")
gui.geometry('600x350')
lat = "51.107883"
lon = "17.038538"
day = 0
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=minutely,alerts&appid=%s" % (lat, lon, API_key)
response = requests.get(url)
json.data = json.loads(response.text)

forecastDays = []
forecastDaysTemperature = []
forecastNightsTemperature = []
URLPictures = []
myPages = []
myPictures = []
PILImages = []
TKImages = []
Labels = []
forecastsClouds = []

def placeData(fcastD, fcastT, fcastTN, pic_url, my_page, my_picture, pil_img, tk_img, label, fcastW, day):
    if(day == 0):
        fcastD.configure(text="Today")
    elif(day == 1):
        fcastD.configure(text="Tomorrow")
    else:
        fcastD.configure(text="Overmorrow")
    fcastT.configure(text=int(json.data["daily"][day]["temp"]["day"]) - 273)
    #print(fcastT)
    fcastTN.configure(text=int(json.data["daily"][day]["temp"]["night"]) - 273)
    pic_url = "http://openweathermap.org/img/w/" + json.data["daily"][day]["weather"][0]["icon"] + ".png"
    my_page = urlopen(pic_url)
    my_picture = io.BytesIO(my_page.read())
    pil_img = Image.open(my_picture)
    tk_img = ImageTk.PhotoImage(pil_img)
    label.configure(image=tk_img)
    label.image = tk_img
    fcastW.configure(text=str(json.data["daily"][day]["clouds"]) + "%")

def changeCity(event):
    if CityChoices.get() == "Wroclaw":
        lat = "51.107883"
        lon = "17.038538"
    elif CityChoices.get() == "Warsaw":
        lat = "52.229676"
        lon = "21.012229"
    elif CityChoices.get() == "Berlin":
        lat = "52.520008"
        lon = "13.404954"
    elif CityChoices.get() == "Moscow":
        lat = "55.75000000"
        lon = "37.618323"
    elif CityChoices.get() == "London":    
        lat = "51.509865"
        lon = "-0.118092"
    elif CityChoices.get() == "Kair":
        lat = "30.033333"
        lon = "31.233334"
    elif CityChoices.get() == "Helsinki":
        lat = "60.192059"
        lon = "24.945831"

    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=minutely,alerts&appid=%s" % (lat, lon, API_key)
    response = requests.get(url)
    json.data = json.loads(response.text)
    #for k in data["daily"][day]["temp"]:
    #    print(k['temp'])
        
    placeData(forecastDays[0], forecastDaysTemperature[0], forecastNightsTemperature[0], URLPictures[0], myPages[0], myPictures[0], PILImages[0], TKImages[0], Labels[0], forecastsClouds[0], 0)
    placeData(forecastDays[1], forecastDaysTemperature[1], forecastNightsTemperature[1], URLPictures[1], myPages[1], myPictures[1], PILImages[1], TKImages[1], Labels[1], forecastsClouds[1], 1)
    placeData(forecastDays[2], forecastDaysTemperature[2], forecastNightsTemperature[2], URLPictures[2], myPages[2], myPictures[2], PILImages[2], TKImages[2], Labels[2], forecastsClouds[2], 2)
    
    


    
lbl = Label(gui, text="Enter city", font=("Arial Bold", 18))  
lbl.grid(column=1, row=0)   
lbl3 = Label(gui)  
lbl3.grid(column=0, row=3, pady=(30, 10))
lbl4 = Label(gui, text="Forecast", font=("Arial Bold", 28))  
lbl4.grid(column=1, row=3, pady=(30, 10))
lbl5 = Label(gui)  
lbl5.grid(column=2, row=3, pady=(30, 10))


CityChoices = Combobox(gui, font=("Arial Bold", 20), state='readonly', width = 20)  
CityChoices['values'] = ("Wroclaw", "Warsaw", "Berlin", "Moscow", "London", "Kair", "Helsinki")  
CityChoices.current(0)
CityChoices.grid(column=1, row=1, padx=(10, 10)) 
CityChoices.bind("<<ComboboxSelected>>", changeCity)




forecastDays.append(Label(gui, text="Today", font=("Arial Bold", 18)))
forecastDays[0].grid(column=0, row=4, padx=(10, 10))
forecastDaysTemperature.append(Label(gui, text=int(json.data["daily"][0]["temp"]["day"]) - 273, font=("Arial Bold", 18)))  
forecastDaysTemperature[0].grid(column=0, row=5, padx=(10, 10))
forecastNightsTemperature.append(Label(gui, text=int(json.data["daily"][0]["temp"]["night"]) -273, font=("Arial Bold", 12)))  
forecastNightsTemperature[0].grid(column=0, row=6, padx=(10, 10))


forecastDays.append(Label(gui, text="Tomorrow", font=("Arial Bold", 18)))  
forecastDays[1].grid(column=1, row=4, padx=(10, 10))
forecastDaysTemperature.append(Label(gui, text=int(json.data["daily"][1]["temp"]["day"]) - 273, font=("Arial Bold", 18)))  
forecastDaysTemperature[1].grid(column=1, row=5, padx=(10, 10))
forecastNightsTemperature.append(Label(gui, text=int(json.data["daily"][1]["temp"]["night"]) - 273, font=("Arial Bold", 12)))
forecastNightsTemperature[1].grid(column=1, row=6, padx=(10, 10))

forecastDays.append(Label(gui, text="Overmorrow", font=("Arial Bold", 18)))  
forecastDays[2].grid(column=2, row=4, padx=(10, 10))
forecastDaysTemperature.append(Label(gui, text=int(json.data["daily"][2]["temp"]["day"]) - 273, font=("Arial Bold", 18)))  
forecastDaysTemperature[2].grid(column=2, row=5, padx=(10, 10))
forecastNightsTemperature.append(Label(gui, text=int(json.data["daily"][2]["temp"]["night"]) - 273, font=("Arial Bold", 12)))  
forecastNightsTemperature[2].grid(column=2, row=6, padx=(10, 10))

URLPictures.append("http://openweathermap.org/img/w/" + json.data["daily"][0]["weather"][0]["icon"] + ".png")
myPages.append(urlopen(URLPictures[0]))
myPictures.append(io.BytesIO(myPages[0].read()))
PILImages.append(Image.open(myPictures[0]))
TKImages.append(ImageTk.PhotoImage(PILImages[0]))
Labels.append(Label(gui, image=TKImages[0]))
Labels[0].image = TKImages[0]
Labels[0].grid(column=0, row=7, sticky='ew')

URLPictures.append("http://openweathermap.org/img/w/" + json.data["daily"][1]["weather"][0]["icon"] + ".png")
myPages.append(urlopen(URLPictures[1]))
myPictures.append(io.BytesIO(myPages[1].read()))
PILImages.append(Image.open(myPictures[1]))
TKImages.append(ImageTk.PhotoImage(PILImages[1]))
Labels.append(Label(gui, image=TKImages[1]))
Labels[1].image = TKImages[1]
Labels[1].grid(column=1, row=7, sticky='ew')


URLPictures.append("http://openweathermap.org/img/w/" + json.data["daily"][2]["weather"][0]["icon"] + ".png")
myPages.append(urlopen(URLPictures[2]))
myPictures.append(io.BytesIO(myPages[2].read()))
PILImages.append(Image.open(myPictures[2]))
TKImages.append(ImageTk.PhotoImage(PILImages[2]))
Labels.append(Label(gui, image=TKImages[2]))
Labels[2].image = TKImages[2]
Labels[2].grid(column=2, row=7, sticky='ew')

forecastsClouds.append(Label(gui, text=str(json.data["daily"][0]["clouds"]) + "%", font=("Arial Bold", 18)))  
forecastsClouds[0].grid(column=0, row=8, padx=(10, 10))
forecastsClouds.append(Label(gui, text=str(json.data["daily"][1]["clouds"]) + "%", font=("Arial Bold", 18))) 
forecastsClouds[1].grid(column=1, row=8, padx=(10, 10))
forecastsClouds.append(Label(gui, text=str(json.data["daily"][2]["clouds"]) + "%", font=("Arial Bold", 18))) 
forecastsClouds[2].grid(column=2, row=8, padx=(10, 10))

hourly = json.data["hourly"]
print(hourly)

gui.mainloop()
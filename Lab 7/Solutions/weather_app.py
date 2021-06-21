import requests
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
import datetime

api_key = 'c53023dd1d38441eb0a098bd83edd201'

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
overmorrow = tomorrow + datetime.timedelta(days=1)
now = datetime.datetime.now()
next_hour = now.hour + 1


def search_weather():
    city = city_name.get()

    r = requests.get('https://api.weatherbit.io/v2.0//forecast/daily?city=' + city + '&key=' + api_key)

    datum = r.json()

    if datum:
        temperature_today['text'] = str(datum['data'][0]['temp']) + "   °C"
        temperature_tomorrow['text'] = str(datum['data'][1]['temp']) + "   °C"
        temperature_overmorrow['text'] = str(datum['data'][2]['temp']) + "   °C"

        min_temperature_today['text'] = str(datum['data'][0]['min_temp']) + "   °C"
        min_temperature_tomorrow['text'] = str(datum['data'][1]['min_temp']) + "   °C"
        min_temperature_overmorrow['text'] = str(datum['data'][2]['min_temp']) + "   °C"

        pop_today['text'] = str(datum['data'][0]['pop']) + "   %"
        pop_tomorrow['text'] = str(datum['data'][1]['pop']) + "   %"
        pop_overmorrow['text'] = str(datum['data'][2]['pop']) + "   %"

        icon_today_name = str(datum['data'][0]['weather']['icon'])
        icon_tomorrow_name = str(datum['data'][1]['weather']['icon'])
        icon_overmorrow_name = str(datum['data'][2]['weather']['icon'])
        icon_today = ImageTk.PhotoImage(Image.open("C:/Users/polit/Desktop/ikony/icons/" + icon_today_name + ".png"))
        icon_tomorrow = ImageTk.PhotoImage(Image.open("C:/Users/polit/Desktop/ikony/icons/" + icon_tomorrow_name + ".png"))
        icon_overmorrow = ImageTk.PhotoImage(Image.open("C:/Users/polit/Desktop/ikony/icons/" + icon_overmorrow_name + ".png"))
        icon_today_label['image'] = icon_today
        icon_tomorrow_label['image'] = icon_tomorrow
        icon_overmorrow_label['image'] = icon_overmorrow
        icon_today_label.photo = icon_today
        icon_tomorrow_label.photo = icon_tomorrow
        icon_overmorrow_label.photo = icon_overmorrow


def make_graph(day):
    city = city_name.get()

    r = requests.get('https://api.weatherbit.io/v2.0/forecast/hourly?city=' + city + '&key=' + api_key + '&hours=48')

    datum = r.json()

    temperatures = []
    hours = []
    plt.xticks(np.arange(0, 25))
    if day == "1":
        for i in range(25 - next_hour):
            temperatures.append(datum['data'][i]['temp'])
            hours.append(i + next_hour)
    elif day == "2":
        for i in range(24 - next_hour, 49 - next_hour):
            temperatures.append(datum['data'][i]['temp'])
            hours.append(i - 24 + next_hour)
    elif day == "3":
        for i in range(48 - next_hour, 48):
            temperatures.append(datum['data'][i]['temp'])
            hours.append(i - 48 + next_hour)

    plt.yticks(np.arange(0, max(temperatures), 1.0))
    plt.bar(hours, temperatures, color=['orange', 'blue'], width=0.5)
    plt.title("Hourly Forecast")
    plt.ylabel('Temperature (℃)')
    plt.xlabel('Hour (h)')
    plt.show()


root = Tk()
root.geometry("1310x750")
root.title("Weather App")
background_img = ImageTk.PhotoImage(Image.open("C:/Users/polit/Desktop/moon.jpg"))
background = Label(root, image=background_img)
background.place(x=11, y=11)
city_name = StringVar()
city_input_entry = Entry(root, font=("arial", 23), bg='pale green', textvariable=city_name, width=20)
city_input_entry.place(x=748, y=160)

submit_button = Button(root, text="SUBMIT", width=15, font=("comic sans", 13), bg='maroon', fg='white', bd=9, command=lambda: search_weather())
submit_button.place(x=590, y=235)
enter_city_label = Label(root, text="Enter the city name", width=20, font=("comic sans", 23, "bold"), bg='green2', fg='grey2', borderwidth=3, relief="raised")
enter_city_label.place(x=200, y=160)
weather_label = Label(root, text="  WEATHER  ", anchor='e', font=("comic sans", 48, "bold",), bg='lawn green', fg='black', bd=7, relief='raised')
weather_label.place(x=450, y=30)

temperature_today = Label(root, text="", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
temperature_today.place(x=440, y=435)
min_temperature_today = Label(root, text="", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
min_temperature_today.place(x=440, y=485)
pop_today = Label(root, text="", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
pop_today.place(x=440, y=535)

temperature_tomorrow = Label(root, text="", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
temperature_tomorrow.place(x=690, y=435)
min_temperature_tomorrow = Label(root, text="", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
min_temperature_tomorrow.place(x=690, y=485)
pop_tomorrow = Label(root, text="", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
pop_tomorrow.place(x=690, y=535)

temperature_overmorrow = Label(root, text="", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
temperature_overmorrow.place(x=940, y=435)
min_temperature_overmorrow = Label(root, text="", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
min_temperature_overmorrow.place(x=940, y=485)
pop_overmorrow = Label(root, text="", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
pop_overmorrow.place(x=940, y=535)

temperature_label = Label(root, text="Temp", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
temperature_label.place(x=200, y=435)
min_temperature_label = Label(root, text="Min temp", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
min_temperature_label.place(x=200, y=485)
pop_label = Label(root, text="POP", width=15, font=("comic sans", 13), bg='yellow3', fg='black', bd=9)
pop_label.place(x=200, y=535)

icon_today_label = Label(root, bg='black')
icon_today_label.place(x=455, y=585)
icon_tomorrow_label = Label(root, bg='black')
icon_tomorrow_label.place(x=705, y=585)
icon_overmorrow_label = Label(root, bg='black')
icon_overmorrow_label.place(x=955, y=585)

today_button = Button(root, text="TODAY", width=15, height=3, font=("comic sans", 13), bg='yellow3', fg='black', bd=9, command=lambda: make_graph("1"))
today_button.place(x=440, y=340)
tomorrow_button = Button(root, text=tomorrow.strftime('%d.%m'), width=15, height=3, font=("comic sans", 13), bg='yellow3', fg='black', bd=9, command=lambda: make_graph("2"))
tomorrow_button.place(x=690, y=340)
overmorrow_button = Button(root, text=overmorrow.strftime('%d.%m'), width=15, height=3, font=("comic sans", 13), bg='yellow3', fg='black', bd=9, command=lambda: make_graph("3"))
overmorrow_button.place(x=940, y=340)

mainloop()

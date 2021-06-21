from weatherbit.api import Api

from tkinter import Tk, Frame, Label, Button, Entry, E, W, N, BOTH, StringVar

api_key = "b5aa48862f3f4ae3a40280b7b6b4d001"

api = Api(api_key)
api.set_granularity('daily')

class GUI(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getWeather(self):
        try:
            forecast = api.get_forecast(city=self.entryCity.get())
            self.updateDisplays(forecast.get_series(['temp', 'wind_dir', 'wind_spd', 'rh', 'weather']))
        except:
            self.resetDisplays()

    def updateDisplays(self, mapVal):
        self.tempText0.set(mapVal[0]['temp'])
        self.windDirText0.set(mapVal[0]['wind_dir'])
        self.windStrText0.set(mapVal[0]['wind_spd'])
        self.humidityText0.set(mapVal[0]['rh'])
        self.descriptionText0.set(mapVal[0]['weather']['description'])
        self.dateText0.set(mapVal[0]['datetime'].strftime("%m/%d/%Y"))

        self.tempText1.set(mapVal[1]['temp'])
        self.windDirText1.set(mapVal[1]['wind_dir'])
        self.windStrText1.set(mapVal[1]['wind_spd'])
        self.humidityText1.set(mapVal[1]['rh'])
        self.descriptionText1.set(mapVal[1]['weather']['description'])
        self.dateText1.set(mapVal[1]['datetime'].strftime("%m/%d/%Y"))

        self.tempText2.set(mapVal[2]['temp'])
        self.windDirText2.set(mapVal[2]['wind_dir'])
        self.windStrText2.set(mapVal[2]['wind_spd'])
        self.humidityText2.set(mapVal[2]['rh'])
        self.descriptionText2.set(mapVal[2]['weather']['description'])
        self.dateText2.set(mapVal[2]['datetime'].strftime("%m/%d/%Y"))

    def resetDisplays(self):
        self.tempText0.set("_")
        self.tempText1.set("_")
        self.tempText2.set("_")

        self.windDirText0.set("_")
        self.windDirText1.set("_")
        self.windDirText2.set("_")

        self.windStrText0.set("_")
        self.windStrText1.set("_")
        self.windStrText2.set("_")

        self.humidityText0.set("_")
        self.humidityText1.set("_")
        self.humidityText2.set("_")

        self.descriptionText0.set("_")
        self.descriptionText1.set("_")
        self.descriptionText2.set("_")

        self.dateText0.set("_")
        self.dateText1.set("_")
        self.dateText2.set("_")

    def initUI(self):

        self.tempText0=StringVar()
        self.tempText1=StringVar()
        self.tempText2=StringVar()

        self.windDirText0=StringVar()
        self.windDirText1=StringVar()
        self.windDirText2=StringVar()

        self.windStrText0=StringVar()
        self.windStrText1=StringVar()
        self.windStrText2=StringVar()

        self.humidityText0=StringVar()
        self.humidityText1=StringVar()
        self.humidityText2=StringVar()

        self.descriptionText0=StringVar()
        self.descriptionText1=StringVar()
        self.descriptionText2=StringVar()

        self.dateText0=StringVar()
        self.dateText1=StringVar()
        self.dateText2=StringVar()
        self.resetDisplays()

        self.pack(fill=BOTH, expand=True)
        row = 0
        self.entryCity=Entry(self)
        self.entryCity.grid(row=row, column=0, columnspan=2, sticky=E+W+N)

        self.button = Button(self, text="Import weather", command = self.getWeather)
        self.button.grid(row=row, column = 2, sticky = W+E)
        row = row + 1

        self.tempLabel0 = Label(self, textvariable=self.tempText0)
        self.tempLabel0.grid(row=row, column=0, sticky=W+E)
        self.tempLabel1 = Label(self, textvariable=self.tempText1)
        self.tempLabel1.grid(row=row, column=1, sticky=W+E)
        self.tempLabel2 = Label(self, textvariable=self.tempText2)
        self.tempLabel2.grid(row=row, column=2, sticky=W+E)
        self.tempLabelInfo = Label(self, text="Temperature [*C]")
        self.tempLabelInfo.grid(row=row, column=3, sticky=W + E)
        row = row + 1

        self.windDirLabel0 = Label(self, textvariable=self.windDirText0)
        self.windDirLabel0.grid(row=row, column=0, sticky=W+E)
        self.windDirLabel1 = Label(self, textvariable=self.windDirText1)
        self.windDirLabel1.grid(row=row, column=1, sticky=W+E)
        self.windDirLabel2 = Label(self, textvariable=self.windDirText2)
        self.windDirLabel2.grid(row=row, column=2, sticky=W+E)
        self.windDirLabelInfo = Label(self, text="Wind direction [*]")
        self.windDirLabelInfo.grid(row=row, column=3, sticky=W + E)
        row = row + 1

        self.windStrLabel0 = Label(self, textvariable=self.windStrText0)
        self.windStrLabel0.grid(row=row, column=0, sticky=W+E)
        self.windStrLabel1 = Label(self, textvariable=self.windStrText1)
        self.windStrLabel1.grid(row=row, column=1, sticky=W+E)
        self.windStrLabel2 = Label(self, textvariable=self.windStrText2)
        self.windStrLabel2.grid(row=row, column=2, sticky=W+E)
        self.windStrLabelInfo = Label(self, text="Wind speed [m/s]")
        self.windStrLabelInfo.grid(row=row, column=3, sticky=W + E)
        row = row + 1

        self.humidityLabel0 = Label(self, textvariable= self.humidityText0)
        self.humidityLabel0.grid(row=row, column=0, sticky=W+E)
        self.humidityLabel1 = Label(self, textvariable=self.humidityText1)
        self.humidityLabel1.grid(row=row, column=1, sticky=W+E)
        self.humidityLabel2 = Label(self, textvariable=self.humidityText2)
        self.humidityLabel2.grid(row=row, column=2, sticky=W+E)
        self.humidityLabelInfo = Label(self, text="Humidity [%]")
        self.humidityLabelInfo.grid(row=row, column=3, sticky=W + E)
        row = row + 1

        self.generalDescrLabel0 = Label(self, textvariable=self.descriptionText0)
        self.generalDescrLabel0.grid(row=row, column=0, sticky=W+E)
        self.generalDescrLabel1 = Label(self, textvariable=self.descriptionText1)
        self.generalDescrLabel1.grid(row=row, column=1, sticky=W+E)
        self.generalDescrLabel2 = Label(self, textvariable=self.descriptionText2)
        self.generalDescrLabel2.grid(row=row, column=2, sticky=W+E)
        self.generalDescrLabelInfo = Label(self, text="Description")
        self.generalDescrLabelInfo.grid(row=row, column=3, sticky=W + E)
        row = row + 1

        self.dateLabel0 = Label(self, textvariable=self.dateText0)
        self.dateLabel0.grid(row=row, column=0, sticky=W+E)
        self.dateLabel1 = Label(self, textvariable=self.dateText1)
        self.dateLabel1.grid(row=row, column=1, sticky=W+E)
        self.dateLabel2 = Label(self, textvariable=self.dateText2)
        self.dateLabel2.grid(row=row, column=2, sticky=W+E)
        self.dateLabelInfo = Label(self, text="Date")
        self.dateLabelInfo.grid(row=row, column=3, sticky=W + E)

root = Tk()
app = GUI()
root.mainloop()

import tkinter as tk
from tkinter import font
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = tk.Tk()
root.title("Weather Forecast")
root.iconbitmap('icon.ico')

height_of_canvas = 500
width_of_canvas = 810
canvas = tk.Canvas(height=height_of_canvas, width=width_of_canvas).pack()

def delete_text(event):
    """
    This function is used to delete the default text in the entry textbox

    Arguments:
        event {string} -- left click of the mouse
    """
    entry.delete(0, "end")



def get_weather(city):
    """
    This function is used to request the current weather data from the API

    Arguments:
        city {[str]} -- Enter the name of city you wish to check the weather
    """
    weather_key = 'xxxx' ## ENTER YOUR PERSONAL WEATHER KEY
    url_forecast = 'https://api.openweathermap.org/data/2.5/forecast'
    parameters_forecast = {'appid': weather_key, 'q': city, 'units': 'metric'}
    response_forecast = requests.get(url_forecast, params=parameters_forecast)
    weather_forecast = response_forecast.json()
    print(weather_forecast)

    url_current_weather = 'https://api.openweathermap.org/data/2.5/weather'
    parameters = {'appid': weather_key, 'q': city, 'units': 'metric'}
    current_response = requests.get(url_current_weather, params=parameters_forecast)
    current_weather = current_response.json()


    lower_label['text'] = responseWeather(weather_forecast, current_weather)


def responseWeather(weather_forecast, current_weather):
    """
    This function is used to return the different parameters of weather data

    Arguments:
        current_weather {[dict]} -- The json data consists of different weather parameters in a dictionary

    Returns:
        [str] -- Returns the required parameter in a string format
    """

    desc = current_weather['weather'][0]['description']
    temp = current_weather['main']['temp']
    feels_like = current_weather['main']['feels_like']

    list_temp = []
    for i in weather_forecast['list']:
        temp = i['main']['temp']
        list_temp.append(temp)

    list_time = []
    for i in weather_forecast['list']:
        x = i['dt_txt']
        spl_word = " "
        time = x.partition(spl_word)[2]
        list_time.append(time)

    df_time_temp = pd.DataFrame(
        list(zip(list_time[:8], list_temp[:8])), columns=['time', 'temperature'])

    
    
    figure2 = plt.Figure(figsize=(5, 4), dpi=100)
    ax2 = figure2.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure2, lower_frame)
    line2.get_tk_widget().place(relx=0, rely=0.135, relwidth=1, relheight=0.8)
    df_time_temp.plot(kind='line', legend=True, ax=ax2, color='c',
                      marker='s', fontsize=8, grid=True, x = "time")

    return "Temperature: {0}°C\n Feels like: {1}°C\t\tDescription: {2}\n".format(temp, feels_like, desc)

## Following lines of code sets the background image of the GUI

background_image = tk.PhotoImage(file='weather.png')
background_label = tk.Label(root,  image=background_image)
background_label.place(relwidth=1, relheight=1)

## Following lines of code sets the "Enter City" block and the frame

city_frame = tk.Frame(root, bg='sky blue', bd=1)
city_frame.place(relx=0.225, rely=0.173,
                 relwidth=0.2, relheight=0.1, anchor='n')


entry = tk.Entry(city_frame, bg='white', font=('Comic Sans MS', 12))
entry.insert(0, "Enter name of City")
entry.place(relwidth=1, relheight=1)
entry.bind("<Button-1>", delete_text)

## Following lines of code sets the "Weather Update" button and it's corresponding frame

upper_right_frame2 = tk.Frame(root, bg='sky blue', bd=1)
upper_right_frame2.place(
    relx=0.735, rely=0.173, relwidth=0.275, relheight=0.1, anchor='n')


button_main = tk.Button(upper_right_frame2, text="Weather Update", bg='white',
                        fg='black', font=('Calibri Bold', 14), command=lambda: get_weather(entry.get()))
button_main.place(relx=0, relwidth=1, relheight=1)


## Following lines of code sets the display graph block and it's frame

lower_frame = tk.Frame(root, bg='sky blue', bd=2)
lower_frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.6, anchor='n')

lower_background_image = tk.PhotoImage(file='sunny.png')


lower_label = tk.Label(lower_frame, bg='white', fg='black',
                       font=('Calibri Bold', 12), anchor='nw', justify='left')
lower_label.place(relwidth=1, relheight=1)


root.mainloop()

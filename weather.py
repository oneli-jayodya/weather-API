from tkinter import *
import tkinter as TK
from geopy.geocoders import Nominatim
from tkinter import messagebox
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz
from PIL import Image, ImageTk

root = Tk()
root.title("Weather App")
root.geometry("1150x650+100+100")
root.configure(bg="#152238")
root.resizable(False, False)

def getWeather():
    city = search_entry.get()

    geolocator = Nominatim(user_agent="geoapiExcercises")
    location = geolocator.geocode(city)
    obj = TimezoneFinder()

    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    
    #print(result)  # Print the timezone identifier
    
    timezone.config(text=result)
    long_lat.config(text=f"{round(location.latitude,4)}°N  |  {round(location.longitude,4)}°E")
    
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)

    # Weather
    base = "https://api.openweathermap.org/data/2.5/weather?"
    api = '2a6b1678bd08bee7f22296587e7027d3'

    def cel(kelvin):
        celsius= kelvin - 273.15
        return celsius
    
    # Use the user input city
    
    url = base + "appid=" + api + "&q=" + city
    json_data = requests.get(url).json()
    temp = json_data['main']['temp']
    tcel= cel(temp)
    humidity = json_data['main']['humidity']
    pressure = json_data['main']['pressure']
    wind = json_data['wind']['speed']
    description = json_data['weather'][0]['description']
    
    t.config(text=(f"{tcel:.2f}°C"))
    h.config(text=(humidity,"%"))
    p.config(text=(pressure,"hPa"))
    w.config(text=(wind,"m/s"))
    d.config(text=description)

     #1st box

    firstdayimage=json_data['weather'][0]['icon']
   # print(firstdayimage)

    photo1 =ImageTk.PhotoImage(file=f"icons/{firstdayimage}@2x.png")
    firstimage.config(image=photo1)
    firstimage.image=photo1
    
    sunrise_time = datetime.fromtimestamp(json_data['sys']['sunrise'] + json_data['timezone'])
    sunset_time =datetime.fromtimestamp(json_data['sys']['sunset'] + json_data['timezone'])

    # Format the times as strings
    #formatted_sunrise = sunrise_time.strftime('%H:%M')
    #formatted_sunset = sunset_time.strftime('%H:%M')

    # Display the formatted times
    day1temp.config(text=f"Sunrise: {sunrise_time}\nSunset: {sunset_time}")

    # Display the weather and temp
    weathertemp.config(text=description)
    currentemp.config(text=str(round(tcel)) + "°C")

    # Forecast
    forecast_base = "http://api.openweathermap.org/data/2.5/forecast?"
    forecast_url = f"{forecast_base}q={city}&appid='2a6b1678bd08bee7f22296587e7027d3'"
    forecast_data = requests.get(forecast_url).json
    
    first=datetime.now()
    day1.config(text=first.strftime("%A"))
   
# icon
image_icon=PhotoImage(file="images/logo.png")
root.iconphoto(False,image_icon)

# Load the image
Round_box = PhotoImage(file="images/16-163701_dark-blue-rectangle-transparent.png")

# Resize the image to 200x200 pixels
Round_box = Round_box.subsample(2, 3)  # Adjust the subsampling factor as needed

# Display the image on a Label
label = Label(root, image=Round_box, bg="#152238")
label.place(x=50, y=150)

# Label on image
label1=Label(root,text="Temperature",font=('calibri',13),fg="white",bg="#1B5C9D")
label1.place(x=110,y=175)

label2=Label(root,text="Humidity",font=('calibri',13),fg="white",bg="#1B5C9D")
label2.place(x=110,y=200)

label3=Label(root,text="Pressure",font=('calibri',13),fg="white",bg="#1B5C9D")
label3.place(x=110,y=225)

label4=Label(root,text="Wind Speed",font=('calibri',13),fg="white",bg="#1B5C9D")
label4.place(x=110,y=250)

label5=Label(root,text="Description",font=('calibri',13),fg="white",bg="#1B5C9D")
label5.place(x=110,y=275)

# Load and resize the search image
search_image = Image.open("images/rounded.png")
search_image = search_image.resize((search_image.width // 1, search_image.height // 2))
search_photo = ImageTk.PhotoImage(search_image)

# Display the search image
search_label = Label(root, image=search_photo, bg="#152238")
search_label.image = search_photo
search_label.place(x=550, y=100)

# Create an Entry widget for user input
search_entry = Entry(root, bg="#13294B", fg="white", font=('Arial', 18 ,"bold"), border=0, justify='center')
search_entry.place(x=670, y=215)
search_entry.focus()

# Load and resize the weather image
weat_image = Image.open("images/search-image.png")
weat_image = weat_image.resize((weat_image.width // 11, weat_image.height // 11))
weat_photo = ImageTk.PhotoImage(weat_image)

# Display the weather image
weatherimage = Label(root, image=weat_photo, bg="#13294B")
weatherimage.image = weat_photo
weatherimage.place(x=600, y=205)

# search icon
search_icon = Image.open("images/search.png")
search_icon_resized = search_icon.resize((search_icon.width // 48, search_icon.height // 48))
search_icon_tk = ImageTk.PhotoImage(search_icon_resized)

# Create the search icon button
search_image = Button(image=search_icon_tk, borderwidth=0, cursor="hand2", bg="#13294B",command=getWeather)
search_image.image = search_icon_tk  # Keep a reference to the image to prevent garbage collection
search_image.place(x=970, y=210)


#clock place time
clock=Label(root,font=("Helvetica",30,'bold'),fg="white",bg="#152238")
clock.place(x=60,y=40)

#timezone
timezone=Label(root,font=("Helvetica",20,'bold'),fg="white",bg="#152238")
timezone.place(x=870,y=30)

long_lat=Label(root,font=("Helvetica",10),fg="white",bg="#152238")
long_lat.place(x=870,y=70)

#values
t=Label(root,font=("Helvetica",11),fg="white",bg="#184D8E")
t.place(x=300,y=180)
h=Label(root,font=("Helvetica",11),fg="white",bg="#184D8E")
h.place(x=300,y=205)
p=Label(root,font=("Helvetica",11),fg="white",bg="#184D8E")
p.place(x=300,y=230)
w=Label(root,font=("Helvetica",11),fg="white",bg="#184D8E")
w.place(x=300,y=255)
d=Label(root,font=("Helvetica",11),fg="white",bg="#184D8E")
d.place(x=300,y=280)

#current box
firstframe=Frame(root,width=850,height=260,bg="#152238")
firstframe.place(x=200,y=400)

day1=Label(firstframe,font="arial 30 bold", bg="#152238",fg="#04BADE")
day1.place(x=5,y=0)

firstimage=Label(firstframe,bg="#152238")
firstimage.place(x=40,y=55)

day1temp = Label(firstframe,bg="#152238",fg="#FFBCBC",font="arial 16 ")
day1temp.place(x=210,y=50)

weathertemp = Label(firstframe,bg="#152238",fg="#E8E9ED",font="arial 16 bold")
weathertemp.place(x=280,y=130)

currentemp = Label(firstframe,bg="#152238",fg="#E0115F",font="arial 80 bold")
currentemp.place(x=560,y=30)


root.mainloop()

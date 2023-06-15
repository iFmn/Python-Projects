# Test ChatBot @TripWizardBot for travellers by Iana Fomina
import telebot
from telebot import types
import requests
import json
import webbrowser
import time
import os

bot = telebot.TeleBot("6111104498:AAGxSsDYh5H5zPVQJWjeP_igFhK74Wn0vE8")

# reacting to command 'start'
@bot.message_handler(commands=['start'])
def start(message):
    msgHello = f"Hello, <b>{message.from_user.first_name}</b>"
    bot.send_message(message.chat.id, msgHello, parse_mode="html")
    bot.register_next_step_handler(message, weather)
    msgQu = f"What <b>city</b> do you want to go to?"
    bot.send_message(message.chat.id, msgQu, parse_mode="html")

# check the temperature in the city
@bot.message_handler(func=lambda message: True)
def weather(message):
    API_weather = "f47477fc2dfbd00d9ba3c19b9c3dfcc5"
    weather_icons = {
        'Clear': "sunny_By Freepik.png",
        'Clouds': "cloudy_By iconixar.png",
        "Rain": "rain_By Freepik.png",
        "Thunderstorm": "thunderstorm_By Freepik.png",
        "Snow": "snow_By Freepik.png"
    }
    global city
    city = message.text
    city = city.capitalize()

    if city == 'Back':
        msgQu = f"What <b>city</b> do you want to go to?"
        bot.send_message(message.chat.id, msgQu, parse_mode="html")
        city = input().capitalize()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=eng&appid={API_weather}")
    if res.status_code == 200:
        data = json.loads(res.text)
        temperature = round(data['main']['temp'])
        weather_info = data['weather'][0]['main']
        bot.reply_to(message, f"In {city} it's currently {temperature}°C and {weather_info}")

        image = weather_icons[weather_info]
        file = open('/Users/y_fmn/Documents/Python_Programming/myenv/Python_chatBot/' + image, 'rb')
        bot.send_photo(message.chat.id, file)

        if temperature < 10:
            bot.send_message(message.chat.id, "Oh it's so cold.. Don't forget to dress warmly! 🥶")  
            booking_details(message)
        else:
            booking_details(message)
    else:
        bot.send_message(message.chat.id, "Can't find this city. Please try another one.") 

# choose the option of booking
def booking_details(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    hotels = types.KeyboardButton("Hotels")
    transport  = types.KeyboardButton("Transport")
    back = types.KeyboardButton("Back")
    markup.add(hotels, transport, back)
    bot.send_message(message.chat.id, "What are you looking for?", reply_markup=markup)
    markup.row(hotels, transport)
    markup.row(back)
    bot.register_next_step_handler(message, on_click)
    
# buttons click handling
def on_click(message):
        if message.text == "Hotels":
            #webbrowser.open(f"https://www.booking.com/searchresults.ru.html?ss={city}&lang=en-us") // another way of openning sites, may be c too scary for users
            #bot.send_message(message.chat.id, "Website is open")
            bot.send_message(message.chat.id, f"I recommend you to try\nhttps://www.booking.com/searchresults.ru.html?ss={city}&lang=en-us\n")
            bot.register_next_step_handler(message, on_click)
        elif message.text == "Transport":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            buses = types.KeyboardButton("Buses")
            flights = types.KeyboardButton("Flights")
            back = types.KeyboardButton("Back")
            markup.add(buses, flights, back)
            bot.send_message(message.chat.id, "What will we be traveling on?", reply_markup=markup)
            markup.row(buses, flights)
            markup.row(back)
            bot.register_next_step_handler(message, on_click2)
        elif message.text == "Back":
            weather(message)

#buttons v_2 click handling
def on_click2(message):
    if message.text == "Back":
        bot.send_message(message.chat.id, "Ok, let's try again!")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        hotels = types.KeyboardButton("Hotels")
        transport  = types.KeyboardButton("Transport")
        back = types.KeyboardButton("Back")
        markup.add(hotels, transport, back)
        bot.send_message(message.chat.id, "What are you looking for?", reply_markup=markup)
        markup.row(hotels, transport)
        markup.row(back)
        bot.register_next_step_handler(message, on_click)
    elif message.text == "Buses":
        bot.send_message(message.chat.id, f"I recommend you to try\nhttps://global.flixbus.com")
        bot.register_next_step_handler(message, on_click2)
    elif message.text == "Flights":
        bot.send_message(message.chat.id, f"I recommend you to try\nhttps://www.aviasales.ru")
        bot.register_next_step_handler(message, on_click2)


# bot is nonstop working 
bot.polling(non_stop=True)

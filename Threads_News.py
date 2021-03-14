from __future__ import print_function

import glob
import json
import os
import tkinter as tk
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

import mysql.connector
import requests
from tkscrolledframe import ScrolledFrame

# Global_Variables
API_KEY = '70fa13af5be9481994d7f14a06e892da'

url_list = ['http://newsapi.org/v2/top-headlines?q=biden&sortBy=publishedAt'
            '&country=us&apiKey=' + API_KEY,
            'http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=' + API_KEY,
            'http://newsapi.org/v2/top-headlines?q=corona&'
            'sortBy=popularity&sources=cbs-news,cnn,reuters,the-verge,vice-news&apiKey=' + API_KEY]

window = tk.Tk()
window.geometry('1350x690+0+0')
window.title('News with Threading')


def db_conn():
    db = mysql.connector.Connect(host="localhost", user="root", db="newsapidb")
    cursor = db.cursor()
    return db, cursor


def get_news(url, file_name):
    try:
        html = requests.get(url, stream=True)
        open(f'{file_name}.json', 'wb').write(html.content)
        return html.status_code
    except requests.exceptions.RequestException as e:
        return e


def runner():
    threads = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for url in url_list:
            file_name = uuid.uuid1()
            threads.append(executor.submit(get_news, url, file_name))

        for task in as_completed(threads):
            print(task.result())
            if task.result() == 401:
                print('Error: Api Key Missing')


def reset_results():
    files = glob.glob("*.json")
    for file in files:
        os.remove(file)


def store_data(data):
    val = []
    db, cursor = db_conn()
    insert_query = """ INSERT INTO newsdata (title, description) VALUES (%s,%s)"""
    for news in data['articles']:
        val.append((news['title'].title(), news['description']))
    cursor.executemany(insert_query, val)
    db.commit()
    cursor.close()
    db.close()
    return


def insert_db():
    news_data = []
    reset_db()
    files = glob.glob("*.json")
    for data_file in files:
        f = open(data_file)
        try:
            data = json.load(f)
            # data1= json.dump(data)
            if data["status"] == "ok" and data["totalResults"] > 0:
                news_data.append(data)
        except:
            print('Error insert_db', f)
    for data in news_data:
        try:
            store_data(data)
        except Exception as e:
            print(e)


def reset_db():
    db, cursor = db_conn()
    cursor.execute(" TRUNCATE TABLE newsdata")


def print_news():
    db, cursor = db_conn()
    cursor.execute("SELECT title, description FROM newsdata")
    db_result = cursor.fetchall()

    # GUI
    data_frame = tk.Frame(window)
    data_frame.pack(side="left", expand=0, fill="y")
    sf = ScrolledFrame(data_frame, width=1128, bg='#ffffff')
    sf.pack(side="left", expand=1, fill="y")

    # Bind the arrow keys and scroll wheel
    sf.bind_arrow_keys(window)
    sf.bind_scroll_wheel(window)

    frame = sf.display_widget(tk.Frame)
    frame['bg'] = '#E8E7F7'
    frame['bd'] = 15
    frame['relief'] = 'sunken'

    for news in db_result:
        # Title Label
        l = tk.Label(text=news[0],
                     bg='#E8E7F7',
                     fg='#3f0052',
                     wraplength=1070,
                     master=frame,
                     font="-size 18 -weight bold",
                     justify='left',
                     pady='10')
        l.pack()

        # Description Label
        l = tk.Label(text=news[1],
                     bg='#DEDEDE',
                     fg='#3f0052',
                     wraplength=1070,
                     master=frame,
                     font="-size 14",
                     justify='left',
                     padx='15')
        l.pack()

        # Separator
        l = tk.Label(
            text='--------------------------------------------------------------------------------------------------',
            bg='#E8E7F7',
            fg='#3f0052',
            wraplength=1070,
            master=frame,
            font="-size 14",
            justify='left',
            pady='25')
        l.pack()

    window.mainloop()


# reset_results()

# Creating The Buttons
button1 = tk.Button(window, bd=5, relief='raised', font='-size 10 -weight bold', text="Get Data From Api",
                    command=runner)
button2 = tk.Button(window, bd=5, relief='raised', font='-size 10 -weight bold', text="Insert Data To DataBase",
                    command=insert_db)
button3 = tk.Button(window, bd=5, relief='raised', font='-size 10 -weight bold', text="Get Data from DataBase",
                    command=print_news)
button4 = tk.Button(window, bd=5, padx=10, relief='raised', font='-size 10 -weight bold', text="Exit", command=quit)

button1.place(x=1175, y=250)
button2.place(x=1160, y=300)
button3.place(x=1160, y=350)
button4.place(x=1215, y=420)
window.mainloop()

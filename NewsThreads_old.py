import ast
from tkscrolledframe import ScrolledFrame
import requests
import uuid
import json, glob, os, inspect
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = '8495809e3537476fb9ca75ebec9b1386'

url_list = ['http://newsapi.org/v2/top-headlines?q=biden&sortBy=publishedAt'
            '&country=us&sources=cbs-news,cnn,reuters,the-verge,vice-news&apiKey=' + API_KEY,
            'http://newsapi.org/v2/top-headlines?country=uk&category=business&apiKey=' + API_KEY,
            'http://newsapi.org/v2/top-headlines?q=apple&'
            'sortBy=popularity&sources=cbs-news,cnn,reuters,the-verge,vice-news&apiKey=' + API_KEY]


def get_news(url, file_name):
    try:
        html = requests.get(url, stream=True)
        # open(f'{file_name}.json', 'wb').write(html.content)
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


# def on_configure(event):
# update scrollregion after starting 'mainloop'
# when all widgets are in canvas
# canvas.configure(scrollregion=canvas.bbox('all'))


window = tk.Tk()
window.geometry('1350x690+0+0')
window.title('News')


# canvas = tk.Canvas(window, borderwidth=15, background="#ffffff", width='1200')


def print_news():
    news_data = []
    files = glob.glob("*.json")
    for data_file in files:
        f = open(data_file)
        try:
            data = json.load(f)
            news_data.append(data)
        except:
            print('Error')
    # GUI

    # canvas.pack(side='left', fill='y')

    # vsb = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    # vsb.pack(side='right', fill='y')

    # canvas.configure(yscrollcommand=vsb.set)
    # canvas.bind('<Configure>', on_configure)

    # data_frame = tk.Frame(window, bg='#d7d5f7', height='800', width='1200', bd=0)
    # canvas.create_window((0, 0), window=data_frame, anchor='nw')

    data_frame = tk.Frame(window)
    data_frame.pack(side="left", expand=0, fill="y")

    sf = ScrolledFrame(data_frame, width=1150, height=250, bg='#ffffff')
    sf.pack(side="left", expand=1, fill="y")

    # Bind the arrow keys and scroll wheel
    sf.bind_arrow_keys(data_frame)
    sf.bind_scroll_wheel(data_frame)

    frame = sf.display_widget(tk.Frame)
    frame['bg'] = '#d7d5f7'
    frame['bd'] = 15
    frame['relief'] = 'sunken'

    for news_list in news_data:
        for news in news_list['articles']:
            print(news['description'])
            l = tk.Label(text=news['title'].title(),
                         fg='#3f0052',
                         bg='#d7d5f7',
                         wraplength=1120,
                         master=frame,
                         font="-size 18 -weight bold",
                         justify='left',
                         pady='10')

            l.pack()

            l = tk.Label(text=news['description'],
                         bg='#d7d5f7',
                         fg='#3f0052',
                         wraplength=1120,
                         master=frame,
                         font="-size 14",
                         justify='left',
                         padx='15')

            l.pack()

            l = tk.Label(text='--------------------------------------------------------------------------------------------------',
                         bg='#d7d5f7',
                         fg='#3f0052',
                         wraplength=1120,
                         master=frame,
                         font="-size 14",
                         justify='left',
                         pady='25')

            l.pack()

    window.mainloop()


# resultsContents = tk.StringVar()
# label['textvariable'] = resultsContents
# resultsContents.set('New value to display')


# reset_results()
runner()
print_news()

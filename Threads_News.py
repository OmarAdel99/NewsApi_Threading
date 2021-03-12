import ast
from tkscrolledframe import ScrolledFrame
import requests
import uuid
import json, glob, os, inspect
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global_Variables
API_KEY = '8495809e3537476fb9ca75ebec9b13860'

url_list = ['http://newsapi.org/v2/top-headlines?q=biden&sortBy=publishedAt'
            '&country=us&apiKey=' + API_KEY,
            'http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=' + API_KEY,
            'http://newsapi.org/v2/top-headlines?q=corona&'
            'sortBy=popularity&sources=cbs-news,cnn,reuters,the-verge,vice-news&apiKey=' + API_KEY]

window = tk.Tk()
window.geometry('1350x690+0+0')
window.title('News')


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


def print_news():
    news_data = []
    files = glob.glob("*.json")
    for data_file in files:
        f = open(data_file)
        try:
            data = json.load(f)
            if data["status"] == "ok" and data["totalResults"] > 0:
                news_data.append(data)
        except:
            print('Error')

    # GUI
    data_frame = tk.Frame(window)
    data_frame.pack(side="left", expand=0, fill="y")

    sf = ScrolledFrame(data_frame, width=1178, bg='#ffffff')
    sf.pack(side="left", expand=1, fill="y")

    # Bind the arrow keys and scroll wheel
    sf.bind_arrow_keys(window)
    sf.bind_scroll_wheel(window)

    frame = sf.display_widget(tk.Frame)
    frame['bg'] = '#E8E7F7'
    frame['bd'] = 15
    frame['relief'] = 'sunken'

    for news_list in news_data:
        for news in news_list['articles']:
            # Title Label
            l = tk.Label(text=news['title'].title(),
                         fg='#3f0052',
                         wraplength=1120,
                         master=frame,
                         font="-size 18 -weight bold",
                         justify='left',
                         pady='10')
            l.pack()

            # Description Label
            l = tk.Label(text=news['description'],
                         bg='#DEDEDE',
                         fg='#3f0052',
                         wraplength=1120,
                         master=frame,
                         font="-size 14",
                         justify='left',
                         padx='15')
            l.pack()

            # Separator
            l = tk.Label(
                text='--------------------------------------------------------------------------------------------------',
                fg='#3f0052',
                wraplength=1120,
                master=frame,
                font="-size 14",
                justify='left',
                pady='25')
            l.pack()

    window.mainloop()


# reset_results()

# Run Fetch from API
# runner()

# Load GUI with Data
print_news()

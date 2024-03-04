from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime





finviz_url='https://finviz.com/quote.ashx?t='
tickers = ['DELL','AMZN','GOOG']
news_tables = {}
for ticker in tickers:
    url = finviz_url + ticker

    req= Request(url=url,headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response,'html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

parsed_data = []
for ticker,news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        title = row.a.text
        date_data = row.td.text.strip().split(' ')
        print(date_data)
        if len(date_data) == 1:
            time = date_data[0]
        else:
            if date_data[0] == 'Today':
                date = datetime.now().strftime('%d-%m-%y')
            else:
                date = date_data[0]
            time = date_data[1]
        parsed_data.append([ticker,date,time,title])

df = pd.DataFrame(parsed_data,columns=['ticker','date','time','title'])
vader=SentimentIntensityAnalyzer()
f = lambda title: vader.polarity_scores((title))['compound']
df['compound'] = df['title'].apply(f)
df['date'] = pd.to_datetime(df.date).dt.date
plt.figure(figsize=(10,8))
mean_df = df.groupby(['ticker', 'date']).mean('compound')
mean_df=mean_df.unstack()
mean_df=mean_df.xs('compound',axis="columns").transpose()
mean_df.plot(kind='bar')
plt.show()

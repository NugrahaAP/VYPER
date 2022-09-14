import os
import sqlite3
import datetime
import pandas as pd


def get_chrome_hist():


    path = os.getenv('LOCALAPPDATA')

    fullpath = f'{path}\\Google\\Chrome\\User Data\\Default\\History'
    con = sqlite3.connect(fullpath)
    cursor = con.cursor()
    cursor.execute("SELECT url FROM urls")
    urls = cursor.fetchall()
    return(urls)

def get_firefox_hist():

    hist = []

    path = os.getenv('APPDATA')

    fullpath = f'{path}\\Mozilla\\Firefox\\Profiles\\'
    listdir = os.listdir(fullpath)
    for data in listdir:
        detail = []
        datemod = os.stat(f'{fullpath}\\{data}').st_mtime
        timestring = datetime.datetime.fromtimestamp(datemod).strftime('%Y-%m-%d-%H:%M')
        detail.append(f'{fullpath}{data}')
        detail.append(timestring)
        hist.append(detail)
    

    df = pd.DataFrame(hist, columns=['dir','last modified'])
    lastmod = df.loc[:,'last modified'].max()
    for index, row in df.iterrows():
        if row['last modified'] == lastmod:
            targetdir = row['dir']
    
    con = sqlite3.connect(f'{targetdir}\\places.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT url FROM moz_places ")
    urls = cursor.fetchall()
    
    return(urls)

def main():
    
    localappdata = os.getenv('LOCALAPPDATA')
    appdata = os.getenv('APPDATA')



    if (os.path.exists(f'{localappdata}\\Google\\Chrome\\User Data\\Default\\')):
        chrome = get_chrome_hist()
    else:
        chrome = ''

    if (os.path.exists(f'{appdata}\\Mozilla\\Firefox\\Profiles\\')):

        firefox = get_firefox_hist()
    else:
        firefox= ''

  
  

if __name__=="__main__":
    main()




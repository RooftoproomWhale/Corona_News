from flask import Flask,render_template
#from wsgiref.simple_server import make_server
import json as js
import time
import datetime
from datetime import timedelta
from flask_cors import CORS

now = time.strftime('%Y.%m.%d.%I.%M',time.localtime(time.time()))
at =(datetime.datetime.strptime(now,'%Y.%m.%d.%I.%M') - timedelta(hours=6))

app = Flask(__name__)
CORS(app)
@app.route('/covid/')
def get():
    import requests
    from bs4 import BeautifulSoup
    headers = {'User-Agent': 'Mozilla/5.0'}
    res=requests.get("https://search.naver.com/search.naver?where=news&query=코로나%20속보%20확진&sm=tab_srt&sort=1&photo=0&field=0&reporter_article=&pd=12&ds="+str(at)+"&de="+now+"&docid=&nso=so%3Add%2Cp%3Aall%2Ca%3Aall&mynews=0&refresh_start=0&related=0",
                     headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')                                                                                             #pd=n 시간 7=1시간
    result=[]
    for i in range(1,20):
        # title = soup.find_all(class_='_sp_each_title', limit=5)
        title=soup.select('#sp_nws'+str(i)+' > dl > dt > a')
        content=soup.select('#sp_nws'+str(i)+' > dl > dd:nth-child(3)')
        if title :
            if '속보' in str(title):
                if '코로나' in str(content):
                    for tit in title:
                        newstitle=tit.get_text()
                        href=tit.attrs['href']
                        result.append({'title':newstitle,'href':href})
                jsonresult=js.dumps(result,indent=1,ensure_ascii=False)
    print('요청')
    return jsonresult;

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9997 , debug=True)


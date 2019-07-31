from flask import Flask, escape, request, render_template
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# @app.route('/')
# def hello():
#     name = request.args.get("name", "World")
#     # "name" 이라는 key 값에 해당되는 value값을 가져오기
#     # none(값이 없으면) 이면 World. default값?!
#     return f'Hello, {escape(name)}!'

@app.route('/')
#  홈페이지 주소의 root
def hello():
    return render_template("index.html")

@app.route('/lotto')
def lotto():
    numbers = random.sample(range(1,46), 6)
    return render_template("lotto.html", numbers=numbers)

@app.route('/lunch')
def lunch():
    menus=["파스타","순두부찌개","소불고기","다슬기해장국"]
    menu = random.choice(menus)
    return render_template("lunch.html", menu=menu)

# 나중에 시간되면 이미지도 가져오는 거


@app.route('/opgg')
def opgg():
    # 사용자에게 보여주는 폼
    return render_template("opgg.html")

@app.route('/search')
def search():
    opgg_url = "https://www.op.gg/summoner/userName="
    summoner = request.args.get('summoner')
    url = opgg_url + summoner
    
    res = requests.get(url).text
    
    soup = BeautifulSoup(res, 'html.parser')
    # bss는 res의 정보를 탐색하기 편하게 바꿔준다.
    # 값을 넣어줄 때 어떤 문서인지 같이 알려준다.

    tier = soup.select_one("#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierRank")
    #  괄호안의 조건에 맞는 것만 골라 보여준다.
    user_tier = tier.text.strip()
    # print(tier.text.strip())
    return render_template("search.html", user_tier=user_tier, summoner=summoner)

if __name__ == "__main__":
    app.run(debug=True)
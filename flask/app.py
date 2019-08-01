from flask import Flask, escape, request, render_template
import random
import requests
import csv
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

@app.route("/nono")
def nono():

    with open("data.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        products = list(reader)

    return render_template("nono.html", products=products)
    # nono.html은 안에 html 언어가 아닌 다른 언어도 씌여있는 불완전한 html
    # 크롬이 인식할 수 있도록 완전한 html 로 바꿔주는 것이 render_template

@app.route("/new")
# 데이터 입력할 수 있는 페이지
def new():
    return render_template("new.html")

@app.route("/create")
def create():
    product = request.args.get('product')
    category = request.args.get('category')
    replace = request.args.get('replace')
   
    
    with open("data.csv", "a+", encoding="utf-8", newline="") as f:
    # a+ 는 사용자가 계속 데이터를 입력할 것이기 떄문에 한줄 한줄 계속 추가하라는 것.
        writer = csv.writer(f)
        #["해피해킹","키보드","대체상품"]
        product_info = [product, category, replace]
        writer.writerow(product_info)
        # list를 넘겨주면 하나의 row로 판단하여 값을 입력
        # crud logic
        # create , read, update, delete
        # 

    return render_template("create.html")
    # html 이 없다면 template not found - 404 not found

@app.route("/card")
def card():
    with open("data.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        products = list(reader)

    return render_template("card.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
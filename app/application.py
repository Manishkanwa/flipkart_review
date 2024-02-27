from flask import Flask, request, render_template,jsonify
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen as uReq
from flask_cors import CORS, cross_origin

application = Flask(__name__)

app = application
@app.route("/",methods = ["GET"])

def home():
    return render_template("index.html")
    

@app.route("/review",methods = ["POST","GET"]) 
def index():
    if(request.method == "POST"): 
        try: 
            searchstring = request.form["content"].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchstring
            uclient = uReq(flipkart_url)
            flipkart_page = uclient.read()
            flipkart_html = bs(flipkart_page, "html.parser")
            bigboxes = flipkart_html.find_all("div",{"class" :"_1AtVbE col-12-12" })
            box = bigboxes[2]
            product_url = "https://www.flipkart.com"+box.div.div.div.a["href"]
            product_req = requests.get(product_url)
            product_req =bs(product_req.text,"html.parser")
            review_box= product_req.find_all("div",{"class":"_16PBlm"})
            reviews =[]
            for comment in review_box:
                
                try:
                    text = comment.div.div.find_all("div" ,{"class" : ""})[0].div.text
                except Exception as e:
                    print("unable to fetch text")
                try:
                    name = comment.div.find_all("div",{"class" : "row _3n8db9"})[0].div.p.text
                except:
                    print("no name")
                mydict = {"name" : name,"text" : text}
                reviews.append(mydict)
            print(reviews)
            return render_template("result.html",reviews = reviews[0:(len(reviews)-1)])
            
        except Exception as e:
            print("The exception message is ",e)
            return "something went wrong.."
    else:
        print("condition not met")



if __name__ == "__main__":
    app.debug =True
    app.run(host="0.0.0.0", port = 5000, debug = True)

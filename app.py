from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging
import pymongo
logging.basicConfig(filename = "scrapper.log",level = logging.INFO)
import os

app = Flask(__name__)

@app.route("/",methods = ['GET'])
def homepage():
        return render_template("index.html")

@app.route("/review",methods = ['POST','GET'])
def index():
        if request.method == 'POST':
                try:
                        query = request.form['content'].replace(" ","")
                        save_dir = "images/"
                        if not os.path.exists(save_dir):
                                os.makedirs(save_dir)
                        headers = {"User-Agent":
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
                        response = requests.get(f"https://www.google.com/search?q={query}&sca_esv=555916648&rlz=1C1VDKB_enIN1052IN1052&tbm=isch&sxsrf=AB5stBiYo5rOi3Q04tDBEu8zXsu5FCJ_EQ:1691762202472&source=lnms&sa=X&ved=2ahUKEwjkqv2o4dSAAxXX-DgGHd_ABWQQ_AUoAnoECAQQBA&biw=1536&bih=747&dpr=1.25")
                        print(response)
                        soup = BeautifulSoup(response.content,'html.parser')
                        image_tags = soup.find_all("img")
                        # print(image_tags)
                        print(len(image_tags))  
                        del image_tags[0]
                        img_data_mongo = []
                        for index,image_tag in enumerate(image_tags):
                                image_url = image_tag['src']
                                image_data = requests.get(image_url).content
                                mydict = {"index":index,"image":image_data}
                                img_data_mongo.append(mydict)
                                with open(os.path.join(save_dir,f"{query}_{index}.jpg"),"wb") as f:
                                        f.write(image_data) 
                                                       
                        client = pymongo.MongoClient("mongodb+srv://richa:iNeuron1@cluster0.kfsuwrj.mongodb.net/?retryWrites=true&w=majority")
                        db = client['image_scrapper']
                        review_col = db['image_scrap_data']
                        review_col.insert_many(img_data_mongo)
                        return "image loaded"
                except Exception as e:
                        logging.info(e)
                        return 'something is wrong'

        else:
                return render_template("index.html")

if __name__ == '__main__':
        app.run(host="0.0.0.0",port = 8000)

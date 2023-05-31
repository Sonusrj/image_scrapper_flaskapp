from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import os
import base64

app = Flask(__name__)

# Custom filter for base64 encoding
@app.template_filter('b64encode')
def base64_encode(s):
    return base64.b64encode(s).decode('utf-8')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    query = request.form.get('query')
    save_dir = "image/"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(
        f"https://www.google.com/search?q={query}&rlz=1C1VDKB_enIN969IN969&sxsrf=APwXEdcH6gWFD01Dm2JliAzV1t22Ns6zrg:1685071899481&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjj8vT_hZL_AhWybGwGHUVXCI4Q_AUoAnoECAEQBA&biw=614&bih=736&dpr=1.25",
        headers=headers
    )

    soup = BeautifulSoup(response.content, 'html.parser')
    image_tags = soup.find_all("img")
    del image_tags[0]
    img_data_mongo = []

    for i in image_tags:
        image_url = i["src"]
        image_data = requests.get(image_url).content
        my_dict = {"index": image_url, "image": image_data}
        img_data_mongo.append(my_dict)
        with open(os.path.join(save_dir, f"{query}_{image_tags.index(i)}.jpg"), "wb") as f:
            f.write(image_data)

    return render_template('result.html', query=query, img_data=img_data_mongo)


if __name__ == '__main__':
    app.run(debug=True,port=8000 )

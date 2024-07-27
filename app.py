# BEGIN CODE HERE
import numpy
from selenium.webdriver.common.by import By
from ssl import Options
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get("name")
    print(name)
    doc = mongo.db.test.find({"$text": {"$search": f"\"{name}\""}},{"_id":0}).sort("name",-1)
    alist=list(doc)
    if (len(alist)==0):
        return alist
    return alist
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    new_product = {}
    new_product["name"] = request.args.get('name')
    new_product["production_year"] = float(request.args.get('production_year'))
    new_product["price"] = float(request.args.get('price'))
    new_product["color"] = float(request.args.get('color'))
    new_product["size"] = float(request.args.get('size'))
    print(new_product)
    if ((new_product["size"]<1) or (new_product["size"]>4) or (new_product["color"]<1) or (new_product["color"]>3)):
        return "Invalid information"
    exists = mongo.db.test.find_one({"name": new_product["name"]})
    if (exists is not None):
        mongo.db.test.update_one({"name": new_product["name"]},{"$set": {"price": new_product["price"], "size":new_product["size"], "color":new_product["color"],"production_year":new_product["production_year"]}})
        return "Updated"
    else:
        mongo.db.test.insert_one(new_product)
        return "Added"
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    product = {}
    product["name"] = request.args.get('name')
    product["production_year"] = float(request.args.get('production_year'))
    product["price"] = float(request.args.get('price'))
    product["color"] = float(request.args.get('color'))
    product["size"] = float(request.args.get('size'))
    print(product)
    product_array=numpy.array([(product["production_year"]),(product["price"]),(product["color"]),(product["size"])])
    
    doc = mongo.db.test.find({},{"_id":0})
    alist=list(doc)
    blist=list()
    for x in range(0,len(alist)):
        blist.append([(alist[x]["production_year"]),(alist[x]["price"]),(alist[x]["color"]),(alist[x]["size"])])
    arr=numpy.array(blist)
    
    list70=list()
    similarity=numpy.zeros(arr.shape)
    for i in range(arr.shape[0]):
        x = product_array
        y = arr[i,:]
        mult = numpy.nansum([x[i]*y[i] for i in range(len(x))])
        norm1=numpy.sqrt(numpy.nansum([x[i]*x[i] for i in range(len(x))]))
        norm2=numpy.sqrt(numpy.nansum([y[i]*y[i] for i in range(len(y))]))
        similarity = mult/(norm1*norm2)
        if (similarity>0.7):
            list70.append([similarity,i])
    list70.sort(reverse=True)
    
    names=list()
    for x in range(0,len(list70)):
        names.append(alist[list70[x][1]]["name"])
    
    return names

    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    try:
        semester = request.args.get("semester")
        print(semester)
        if ((int(semester)<1) or (int(semester)>8)):
            return "Invalid input"
        url = "https://qa.auth.gr/el/x/studyguide/600000438/current"
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        sem="exam"+semester
        print(sem)
        elements = driver.find_elements(By.XPATH, f"//table[@id='{sem}']/tbody/tr/td/span/a")
        res = []
        for element in elements:
            res.append(element.text)
        return jsonify(res), 200
    except Exception as e:
        return "BAD REQUEST", 400
    # END CODE HERE

from flask import Flask
from flask import render_template
from flask import url_for
import pymongo
from flask import request
from flask import abort
import os

app = Flask(__name__)




conn = pymongo.MongoClient('mongodb://rahultalreja:rahulrahul@ds155132.mlab.com:55132/mydatabase')
db = conn.mydatabase



@app.route('/')
def mainpage():
    allinfo = db.foodname.find()
    return render_template("mainpage.html", allinfo=allinfo)
   


@app.route('/order/<name>')
def order(name):
    a = db.foodname.find({'name':name})
    return render_template("order.html",info=a)


@app.route('/order/<name>/fetchcustomar', methods=['POST'])
def postdetails(name):
    cname = request.form['cname']
    add = request.form['add']
    mob = request.form['mob']
    db.order.insert({"name":name,'cname':cname,'address':add,'mob':mob})
    info = db.order.find({"name":name,'cname':cname,'address':add,'mob':mob})
    sandwich = db.foodname.find({"name":name})
    return render_template('orderconfirm.html',info=info,sandwich=sandwich)

@app.route('/addmyproductsecretly')
def addproduct():
    return render_template('addproduct.html')


@app.route('/addedyourproductsecretly', methods=['POST'])
def productadded():
    name = request.form['name']
    description = request.form['description']
    img = request.form['img']
    price = request.form['price']
    db.foodname.insert({'name': name , 'description': description , 'price': price, 'img': img})
    new = db.foodname.find({'name': name})
    return render_template("added.html", new = new) 


@app.route('/deletemyproductsecretly')
def deleteproduct():
    info=db.foodname.find()
    return render_template('deleteproduct.html',info=info)


@app.route('/deletedyourproductsecretly/<name>' , methods=['DELETE'] )
def productdeleted(name):
    db.foodname.deletemany({"name":name})
    return render_template("deleted.html")




@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
   app.run(debug=True)
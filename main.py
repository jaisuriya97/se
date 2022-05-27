from flask import Flask,render_template,redirect, render_template_string,url_for,request,session,flash
import sqlite3
app=Flask(__name__)
app.secret_key="iuwbdcishdb"
con=sqlite3.connect("databas.db")
con.execute("create table if not exists map(name text,mail text,password text,phone text,address text,whereto text, pop text,arrivals text,leaving text)")
con.close()
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/singup',methods=["POST","GET"])
def signup():
    if request.method=="POST":
        name=request.form['name']
        mail=request.form['mail']
        password=request.form['password']
        con=sqlite3.connect("databas.db")
        cur=con.cursor()
        cur.execute("insert into map(name,mail,password)values(?,?,?)",(name,mail,password))
        con.commit()
        session["name"]=name
        session["logged_in"]=True
        return redirect(url_for("booking"))
        con.close()   
    return render_template("signup.html")
@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=="POST":
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("databas.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from map where password=? and name=?",(password,name))
        data=cur.fetchone()
        if data:
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            session["logged_in"]=True
            return redirect(url_for("booking"))
        else:
            flash("Login Error")
            return render_template("LOGIN.html")
    return render_template("LOGIN.html")
@app.route('/booking',methods=["GET","POST"])
def booking():
    if request.method=="POST":
        name=request.form['name']
        mail=request.form['mail']
        phone=request.form['phone']
        address=request.form['address']
        where=request.form['where']
        print(name,mail,phone,address)
        con=sqlite3.connect("databas.db")
        cur=con.cursor()
        cur.execute("insert into map(name,mail,phone,address,whereto)values(?,?,?,?,?)",(name,mail,phone,address,where))
        con.commit()
        return redirect(url_for("final"))
        con.close()
    else:      
     return render_template("booking.html")
@app.route('/logout')
def logout():
    session.pop("name",None)
    session.clear()
    return redirect(url_for("Home"))
@app.route('/romepage')
def rome():
    return render_template("rome.html")
@app.route('/france') 
def france():
    return render_template("france.html")   
@app.route('/final')
def final():
    return ("<h1>!</h1>")
if __name__=="__main__":
    app.run(debug=True)
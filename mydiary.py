from flask import Flask,render_template,request,flash,redirect,session,url_for,Response
import sqlite3 as sql
app = Flask(__name__)
app.secret_key="randomstring"
@app.route("/")
def home():
 if 'email' in session:
    return redirect("/view")
 else:
    return render_template("mydiaryhome.html")
@app.route("/signup",methods=['POST','GET'])
def signup():
 if request.method=='POST':
  try:
   name=request.form['nm']
   email=request.form['email']
   password=request.form['pass']
   session['name']= name
   session['email']= email
   with sql.connect("mydiary.db") as con:
    cur=con.cursor()
    cur.execute("INSERT INTO AUTHOR(name,email,password) VALUES(?,?,?)",(name,email,password))
    con.commit()
    flash("NOW YOU CAN SHARE YOUR THOUGHTS AND SECRETS WITH DEAR DIARY:)")
    return render_template("mydiaryview.html",name=name,email=email,result={})
  except:
   con.rollback()
   flash("SORRY SOMETHING WENT WRONG:( PLEASE TRY AGAIN!!")
   return render_template("mydiarysignup.html")
  finally:
   con.close()
 return render_template("mydiarysignup.html")
@app.route("/login",methods=['POST','GET'])
def login():
 if request.method=='POST':
  temail=request.form['email']
  tpassword=request.form['pass']
  session['email']=temail;
  con=sql.connect("mydiary.db")
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM AUTHOR WHERE email = ? AND password=?", (temail,tpassword))
  x=cur.fetchall()
  for y in x:
      session['name']=y["name"]
  if int(len(x)) == 1:
    return redirect("/view")
  else :
      flash("Invalid username or password")
 return render_template("mydiarylogin.html")
@app.route("/addnew/<email>",methods=['POST','GET'])
def addnew(email):
 print "entered addnew"
 result={}
 if request.method=='POST':
  #try:

    cdate=request.form["date"]
    content=request.form['content']
    with sql.connect("mydiary.db") as con:
     con.row_factory = sql.Row
     cur=con.cursor()
     cur.execute("INSERT INTO DIARY(cemail,cdate,content) VALUES(?,?,?)",(session['email'],cdate,content))
     print "entered content in database"
     con.commit()
     return redirect("/view")

 return render_template("mydiaryview.html",name=session['name'],email=session['email'],result=result)

@app.route("/view", methods=['POST','GET'])
def view():
     print "entered view"
     con=sql.connect("mydiary.db")
     con.row_factory = sql.Row
     cur = con.cursor()
     cur.execute("SELECT cdate,content FROM DIARY WHERE cemail = ?",(session['email'],))
     result=cur.fetchall()

     return render_template("mydiaryview.html",name=session['name'],email=session['email'],result=result)

@app.route("/logout",methods=['POST','GET'])
def logout():
    session.pop('email',None)
    return redirect("/");        


if __name__=="__main__":
 app.run(debug=True)

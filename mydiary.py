from flask import Flask,render_template,request,flash,redirect
import sqlite3 as sql
app = Flask(__name__)
app.secret_key="randomstring"
@app.route("/")
def home():
 return render_template("mydiaryhome.html")
@app.route("/signup",methods=['POST','GET'])
def signup():
 if request.method=='POST':
  #try:
   name=request.form['nm']
   email=request.form['email']
   password=request.form['pass']
   with sql.connect("mydiary.db") as con:
    cur=con.cursor()
    cur.execute("INSERT INTO AUTHOR(name,email,password) VALUES(?,?,?)",(name,email,password))
    con.commit()
    flash("NOW YOU CAN SHARE YOUR THOUGHTS AND SECRETS WITH DEAR DIARY:)")
    return render_template("mydiaryview.html",content="")
  #except:
   con.rollback()
   flash("SORRY SOMETHING WENT WRONG:( PLEASE TRY AGAIN!!")
   return render_template("mydiarysignup.html")
  #finally:
   con.close()
 return render_template("mydiarysignup.html")
@app.route("/login",methods=['POST','GET'])
def login():
 if request.method=='POST':
  temail=request.form['email']
  tpassword=request.form['pass']
  con=sql.connect("mydiary.db")
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT password FROM AUTHOR WHERE email = ?", (temail,))
  x=cur.fetchone()
  if int(len(x)) > 0:
   print x[0]
   if x[0]==tpassword:
    #cur.execute("SELECT content FROM AUTHOR WHERE email=?",(temail,))
    #c=cur.fetchall()
    return redirect("/view/%s"%temail)
   else :
    flash("Invalid username or password")
 return render_template("mydiarylogin.html")
@app.route("/view/<email>",methods=['POST','GET'])
def view(email):
 con=sql.connect("mydiary.db")
 con.row_factory = sql.Row
 cur = con.cursor()
 cur.execute("SELECT content FROM AUTHOR WHERE email=?",(email,))
 content=cur.fetchall()
 if request.method=='POST':
  cnew=request.form['content']
  cur.execute("SELECT content FROM AUTHOR WHERE email = ?", (email,))
  c=cur.fetchone()
  content=c[0]+' '+cnew
  cur.execute("UPDATE AUTHOR SET content=? WHERE email=?",((content,),(email,)))
 return render_template("mydiaryview.html",content=content)
   
if __name__=="__main__":
 app.run(debug=True)
 





from flask import Flask, render_template, request, flash,url_for,redirect
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin,current_user
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import datetime
from datetime import date
import CardinalRoute as cd
import sqlite3
import cybersecurity as cbs
import re
import os
from flask_paginate import Pagination, get_page_args

from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm

import encryption as ep
import userscenter as uc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'We love beer and beach, 777'
app.config['UPLOAD_FOLDER']=''
app.config['MAX_CONTENT_PATH']='1000kb'

login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'





USERS=uc.getuser()



def get_user(user_name):
    for user in USERS:
        if user.get('name')==user_name:
            return user

    return None

class User(UserMixin):
    def __init__(self,user):

        self.username=user.get('name')
        self.password_hash=user.get('password')
        self.id=user.get('id')

    def verify_password(self,password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash,password)

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        for user in USERS:
            if user.get('id')==user_id:
                return User(user)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField("Password", validators=[DataRequired()])


@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    emsg=None
    if form.validate_on_submit():
        user_name=form.username.data
        password=form.password.data
        user_info=get_user(user_name)
        if user_info is None:
            emsg="Username or password is invalid"
        else:
            user=User(user_info)
            if user.verify_password(password):
                login_user(user)
                return redirect(request.args.get('next') or url_for("index"))
            else:
                emsg="Username or password is invalid"
    return render_template('login.html',form=form,emsg=emsg)

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template('index.html',username=current_user.username)

@app.route('/about')
@login_required
def about():
    today_w = cd.today_is()
    today_x = cd.today_cd()
    return render_template('about.html',today_w=today_w,today_x=today_x)

@app.route('/knowledge',methods=['GET','POST'])
@login_required
def knowledge():
    if request.method == "POST":
        result=request.form['message']

        rowid=result


        results=cbs.know(rowid)
        cnt = len(results)
        info = "{} records with same name were found".format(cnt)

        return render_template('knowledge.html', results=results, info=info)
    else:

        return render_template('knowledge.html')



@app.route('/uploader', methods = ['GET', 'POST'])
@login_required
def uploader_file():
   if request.method == 'POST':
      files = request.files.getlist('file')
      for f in files:
        f.save(f.filename)
      cbs.buildfile()
      flash('Wonderful,the data is imported successfully!!!')
      return render_template('index.html')


@app.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
   if request.method == 'POST':
      #get the data post from broswer. this is the search condition
      risk_critical=request.form.getlist('critical')
      risk_high=request.form.getlist('high')
      risk_medium = request.form.getlist('medium')
      risk_low = request.form.getlist('low')
      risk_none = request.form.getlist('none')

      branch_boyn = request.form.getlist('boyn')
      branch_bran = request.form.getlist('bran')
      branch_brsp = request.form.getlist('brsp')
      branch_chas = request.form.getlist('chas')
      branch_clea = request.form.getlist('clea')
      branch_cola = request.form.getlist('cola')
      branch_colu = request.form.getlist('colu')
      branch_dani = request.form.getlist('dani')
      branch_dayt = request.form.getlist('dayt')
      branch_deer = request.form.getlist('deer')
      branch_flor = request.form.getlist('flor')
      branch_ftla = request.form.getlist('ftla')
      branch_ftpi = request.form.getlist('ftpi')
      branch_gain = request.form.getlist('gain')
      branch_jaxd = request.form.getlist('jaxd')
      branch_jaxs = request.form.getlist('jaxs')
      branch_kend = request.form.getlist('kend')
      branch_lake = request.form.getlist('lake')
      branch_ltri = request.form.getlist('ltri')
      branch_melb = request.form.getlist('melb')
      branch_mlks = request.form.getlist('mlks')
      branch_ocal = request.form.getlist('ocal')
      branch_orln = request.form.getlist('orln')
      branch_ptri = request.form.getlist('ptri')
      branch_rock = request.form.getlist('rock')
      branch_sara = request.form.getlist('sara')
      branch_stua = request.form.getlist('stua')
      branch_summ = request.form.getlist('summ')
      branch_tall = request.form.getlist('tall')
      branch_wpbh = request.form.getlist('wpbh')
      branch_all = request.form.getlist('all')




      solved_yes=request.form.getlist('yes')
      solved_no=request.form.getlist('no')
      search_keyword=request.form.getlist('keyword')
      #transform the requested data to condition words using in sql

      risk=()
      if risk_critical:
          risk=risk+('Critical',)
      if risk_high:
          risk=risk+('High',)
      if risk_medium:
          risk=risk+('Medium',)
      if risk_low:
          risk=risk+('Low',)
      if risk_none:
          risk=risk+('None',)
      if len(risk)==1:
          risk=str(risk).replace(',','')
      else:
          risk=str(risk)

      branch = ()
      if branch_all:
          branch=('BOYN','BRAN','BRSP','CHAS','CLEA','COLA','COLU','DANI','DAYT','DEER','FLOR','FTLA','FTPI','GAIN','JAXD','JAXS','KEND','LAKE','LTRI','MELB','MLKS','OCAL','ORLN','PTRI','ROCK','SARA','STUA','SUMM','TALL','WPBH',)
      else:
          if branch_boyn:
              branch=branch+('BOYN',)
          if branch_bran:
              branch = branch + ('BRAN',)
          if branch_brsp:
              branch = branch + ('BRSP',)
          if branch_chas:
              branch = branch + ('CHAS',)
          if branch_clea:
              branch = branch + ('CLEA',)
          if branch_cola:
              branch = branch + ('COLA',)
          if branch_colu:
              branch = branch + ('COLU',)
          if branch_dani:
              branch = branch + ('DANI',)
          if branch_dayt:
              branch = branch + ('DAYT',)
          if branch_deer:
              branch = branch + ('DEER',)
          if branch_flor:
              branch = branch + ('FLOR',)
          if branch_ftla:
              branch = branch + ('FTLA',)
          if branch_ftpi:
              branch = branch + ('FTPI',)
          if branch_gain:
              branch = branch + ('GAIN',)
          if branch_jaxd:
              branch = branch + ('JAXD',)
          if branch_jaxs:
              branch = branch + ('JAXS',)
          if branch_kend:
              branch = branch + ('KEND',)
          if branch_lake:
              branch = branch + ('LAKE',)
          if branch_ltri:
              branch = branch + ('LTRI',)
          if branch_melb:
              branch = branch + ('MELB',)
          if branch_mlks:
              branch = branch + ('MLKS',)
          if branch_ocal:
              branch = branch + ('OCAL',)
          if branch_orln:
              branch = branch + ('ORLN',)
          if branch_ptri:
              branch = branch + ('PTRI',)
          if branch_rock:
              branch = branch + ('ROCK',)
          if branch_sara:
              branch = branch + ('SARA',)
          if branch_stua:
              branch = branch + ('STUA',)
          if branch_summ:
              branch = branch + ('SUMM',)
          if branch_tall:
              branch = branch + ('TALL',)
          if branch_wpbh:
              branch = branch + ('WPBH',)

      if len(branch) == 1:
          branch = str(branch).replace(',', '')
      else:
          branch = str(branch)


      solved=()
      if solved_yes:
          solved=solved+('Yes',)
      if solved_no:
          solved=solved+('No',)

      if len(solved)==1:
          solved=str(solved).replace(',','')
      else:
          solved=str(solved)


      #search_keyword will return a list with one item, need to seperate the key words.change this ['john;jason;tom'] to be '%john%jason%tom%'

      result=search_keyword[0].replace(';','%')
      keyword="%"+result+"%"

      #engine=create_engine('sqlite:///secure_database.db', echo=True)
      #connect to database server
      conn=sqlite3.connect('secure_database.db')
      c=conn.cursor()
      #set search condition

      search_condition='SELECT rowid,* FROM security WHERE risk in {risk} AND substring(filename,1,4) in {branch} AND solved in {solved} AND (name like "{keyword}" OR description like "{keyword}" OR solution like "{keyword}" OR comment like "{keyword}")'.format(risk=risk,branch=branch,solved=solved,keyword=keyword)

      c.execute(search_condition)
      results=c.fetchall()
      cnt=len(results)
      info="{} records were found".format(cnt)
      conn.commit()
      conn.close()
      # page, per_page, offset=get_page_args(page_parameter='page',per_page_parameter='per_page')
      # per_page=50
      # #pagination_results=results[offset:offset+per_page]
      #pagination =  Pagination(page=page, total=cnt,record_name='Records',per_page=per_page,css_framework='bootstrap4')
      #print (pagination.links)
      return render_template('index.html',results=results,info=info,username=current_user.username)
   if request.method=='GET':
       return render_template('index.html')

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
   if request.method == 'POST':
       result=request.form.to_dict()
       id,value=str(result).split(";")
       id=id.replace("{'","")
       id=id.replace("Checkbox","")

       if "true" in value:
           value_t="Yes"
       elif "false" in value:
           value_t="No"
       else:
           value_t="Erroe"

       cbs.update_solved(id,value_t)

   return render_template('index.html')

def repl_last(s, sub, repl):
    pattern = sub + '(?!.*' + sub + ')'
    return re.sub(pattern, repl, s, flags=re.DOTALL)

@app.route('/comment', methods = ['GET', 'POST'])
@login_required
def comment():

   if request.method == 'POST':
       result=request.form.to_dict()
       id, value = str(result).split(";")
       id = id.replace("{'", "")
       value=value.replace(r"\n","").replace("': ''}","")
       value=re.sub("Comment","",value)
       value = repl_last(value,"save","").strip()
       value = repl_last(value, "search", "").strip()


       now= datetime.datetime.now()
       dt_string=now.strftime("%m/%d/%Y %H:%M:%S")

       values=value+"---"+current_user.username+str(dt_string)+"\n"
       cbs.update_comment(id,values)

   return render_template('index.html')

@app.route('/users_center')
@login_required
def users():

    uc.initialize()
    users=uc.getinfo()

    return render_template('users.html',users=users, username=current_user.username)

@app.route('/new_user', methods = ['GET', 'POST'])
@login_required
def newuser():
    if request.method == 'POST':
        userid = ''.join(request.form.getlist('userid'))
        name = ''.join(request.form.getlist('name'))
        email = ''.join(request.form.getlist('email'))
        password = ''.join(request.form.getlist('password'))

        check=uc.checkuser(userid,email,password)
        if check:
            uc.adduser(userid,name,email,password)
            flash("New user is Created in System")
            global USERS
            USERS = uc.getuser()
        else:
            flash("Invalid UserID or Password, Please Try again")
    return render_template('newuser.html',username=current_user.username)

@app.route('/reset_password',methods = ['GET', 'POST'])
@login_required
def resetpassword():

    if request.method=='POST':
        oldpassword = ''.join(request.form.getlist('oldpassword'))
        newpassword = ''.join(request.form.getlist('password'))
        userid=current_user.username
        checkold=uc.checkold(userid,oldpassword)
        if checkold:
            uc.changepassword(userid,newpassword)
            flash("Reset password successfully")
            global USERS
            USERS = uc.getuser()
        else:
            flash("Your old password is not correct")
    password=uc.getpassword(current_user.username)
    return render_template('resetpassword.html',username=current_user.username,password=password)


@app.route('/status', methods = ['GET', 'POST'])
@login_required
def status():
   if request.method == 'POST':
       result=request.form.to_dict()
       id,value=str(result).split(";")
       id=id.replace("{'","")
       id=id.replace("Checkbox","")

       uc.edstatus(id,value)
       global USERS
       USERS = uc.getuser()

   return render_template('users.html')

if __name__=='__main__':
    app.debug=True
    app.run()
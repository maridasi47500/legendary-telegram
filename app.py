from flask import Flask, render_template, request, session, redirect
from myplace import Myplace
from bs4 import BeautifulSoup
import subprocess
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,email,password,country_id,phone) values (:username,:email,:password,:country_id,:phone)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from user')


        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','email','password','country_id','phone']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','email','password','country_id','phone']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','email','password','country_id','phone']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from country')


        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_phonecall", methods=["GET","POST"])
def add_one_phonecall():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into phonecall (user_id,grievous_situation_degree,description,place,lat,lon) values (:user_id,:grievous_situation_degree,:description,:place,:lat,:lon)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from phonecall')


        return render_template("phonecallform.html", phonecalls=user, one_user=one_user, the_title="add new phonecall")


    user = query_db('select * from phonecall')
    one_user = query_db("select * from phonecall limit 1", one=True)
    return render_template("phonecallform.html", phonecalls=user, one_user=one_user, the_title="add new phonecall")



@app.route("/searchjobcity", methods=["POST"])
def trouver_lieu_city():
    leslieu=Myplace(request.form["lieu"]).trouver1()

    return dict({"city":leslieu[0], "code":leslieu[1], "region":leslieu[3], "departement":leslieu[2], "pays":leslieu[2], "latitude":leslieu[4], "longitude":leslieu[5]})
@app.route("/add_one_real_time_posting", methods=["GET","POST"])
def add_one_real_time_posting():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesroleplayer= query_db("select * from roleplayer")

        one_user = query_db("insert into real_time_posting (user_id,title,content,social_media_reputation_risk,personal_relation_risk,lat,lon,roleplayer_id) values (:user_id,:title,:content,:social_media_reputation_risk,:personal_relation_risk,:lat,:lon,:roleplayer_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from real_time_posting')


        return render_template("real_time_postingform.html", real_time_postings=user, one_user=one_user, the_title="add new real_time_posting", touslesroleplayer=touslesroleplayer)


    touslesroleplayer= query_db("select * from roleplayer")

    user = query_db('select * from real_time_posting')
    one_user = query_db("select * from real_time_posting limit 1", one=True)
    return render_template("real_time_postingform.html", real_time_postings=user, one_user=one_user, the_title="add new real_time_posting", touslesroleplayer=touslesroleplayer)



@app.route("/searchjobcity", methods=["POST"])
def trouver_lieu_city():
    leslieu=Myplace(request.form["lieu"]).trouver1()

    return dict({"city":leslieu[0], "code":leslieu[1], "region":leslieu[3], "departement":leslieu[2], "pays":leslieu[2], "latitude":leslieu[4], "longitude":leslieu[5]})
@app.route("/add_one_roleplayer", methods=["GET","POST"])
def add_one_roleplayer():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        one_user = query_db("insert into roleplayer (name,pic,description) values (:name,:pic,:description)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from roleplayer')


        return render_template("roleplayerform.html", roleplayers=user, one_user=one_user, the_title="add new roleplayer")


    user = query_db('select * from roleplayer')
    one_user = query_db("select * from roleplayer limit 1", one=True)
    return render_template("roleplayerform.html", roleplayers=user, one_user=one_user, the_title="add new roleplayer")

@app.route("/add_one_plan_day_outdoor_activities", methods=["GET","POST"])
def add_one_plan_day_outdoor_activities():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into plan_day_outdoor_activities (user_id,lat,lon,title,description,at_datetime) values (:user_id,:lat,:lon,:title,:description,:at_datetime)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from plan_day_outdoor_activities')


        return render_template("plan_day_outdoor_activitiesform.html", plan_day_outdoor_activitiess=user, one_user=one_user, the_title="add new plan_day_outdoor_activities")


    user = query_db('select * from plan_day_outdoor_activities')
    one_user = query_db("select * from plan_day_outdoor_activities limit 1", one=True)
    return render_template("plan_day_outdoor_activitiesform.html", plan_day_outdoor_activitiess=user, one_user=one_user, the_title="add new plan_day_outdoor_activities")



@app.route("/searchjobcity", methods=["POST"])
def trouver_lieu_city():
    leslieu=Myplace(request.form["lieu"]).trouver1()

    return dict({"city":leslieu[0], "code":leslieu[1], "region":leslieu[3], "departement":leslieu[2], "pays":leslieu[2], "latitude":leslieu[4], "longitude":leslieu[5]})

from flask import Flask, render_template, request, flash, redirect,session
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from constants import UPLOAD_FOLDER as cnst
from processing import resume_matcher
from utils import file_utils
import uuid
import contact_details as cd
app = Flask(__name__)
app.secret_key = '2956'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///results.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = cnst.UPLOAD_FOLDER
db = SQLAlchemy(app)
#session_id = str(uuid.uuid4()) 
#db = SQLAlchemy(app)


class Ratings(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    Job_desc = db.Column(db.String(), nullable=False)
    Resume_list = db.Column(db.String(), nullable=False)
    session_id = db.Column(db.String(),nullable=False)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} - {self.Job_desc} - {self.Resume_list}"
class Result(db.Model):
    sno = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(),nullable=False)
    score = db.Column(db.Integer(),nullable=False)
    phone = db.Column(db.String(),nullable=True)
    email =db.Column(db.String(),nullable=True)
    session_id = db.Column(db.String(), nullable=False)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.name} - {self.score} - {self.phone} - {self.email} - {self.session_id}"
class users(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    email_id = db.Column(db.String(100),nullable=False)
    name = db.Column(db.String(50),nullable=False)
    password =db.Column(db.String(256),nullable=False)

    def __repr__(self) -> str:
        return f"{self.user_id} - {self.email_id} - {self.name} - {self.password}"

@app.route('/', methods=['GET', 'POST'])
def home():
    session_id = str(uuid.uuid4())
    #session_id=str(uuid.uuid4())
    #session_id = str(uuid.uuid4())
    if request.method == 'POST':
        file = request.files['Job_desc']
        Resume_list = request.files.getlist("Resume_list")
        Result.query.filter_by(session_id=session_id).delete()
       # if 'Job_desc' not in request.files:
       #     flash('Requirements document cannot be empty')
       #     return redirect(request.url)
#
       # if 'Resume_list' not in request.files:
       #     flash('Select at least one resume file to proceed further')
       #     return redirect(request.url)
#
       # if file.filename == '':
       #     flash('Requirements document has not been selected')
       #     return redirect(request.url)
#
       # if len(Resume_list) == 0:
       #     flash('Select at least one resume file to proceed further')
       #     return redirect(request.url)
        #session_id = int(uuid.uuid4())
        abs_paths = []
        title = request.form['title']
        Job_desc = secure_filename(file.filename)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], Job_desc))

        resume_list = ""
        for resume_file in Resume_list:
            resume_filename = secure_filename(resume_file.filename)
            resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))
            abs_paths.append(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))
            resume_list += resume_filename + ","

        rating_test = Ratings(title=title, Job_desc=Job_desc, Resume_list=resume_list,session_id=session_id)
        db.session.add(rating_test)
        db.session.commit()
        result,resume_txt = resume_matcher.process_files(os.path.join(app.config['UPLOAD_FOLDER'], Job_desc), abs_paths)
        #input_contact = cd.get_resume_text(resume_list)
        phone=[]
        email=[]
        for resume in resume_txt:
          phone_numbers, email_addresses = cd.extract_contact_info(resume)
          phone.append(phone_numbers)
          email.append(email_addresses)
 
        final = []
        for temp,p,e in zip(result,phone,email):
            name=temp[0]
            tmp=os.path.splitext(name)[0]
            tmp=tmp.split('_')
            vmp=" "
            val_1=vmp.join(tmp)
            val_2=temp[1]
            if len(p) == 0 or len(e) ==0:
                ph="Not Found"
                em="Not Found"
            else:
                p=p[0]
                ph=str(p)
                e=e[0]
                em=str(e)
            #p=str(p)
            #e=str(e)
            final.append(Result(name=val_1,score=val_2,session_id=session_id,phone=ph,email=em))
            #final = Result(name=val_1,score=val_2)
            #db.session.add(final)

        #print(result)
        #print(Job_desc)
        #print(resume_list)
        #print(abs_paths)
        #db.session.add(rating_test)
        db.session.add_all(final) 
        db.session.commit()


        for file_path in abs_paths:
             file_utils.delete_file(file_path)

        #ratings = Ratings.query.all()
       # return render_template('index.html', Ratings=ratings)


        
    results = Result.query.filter_by(session_id=session_id).all()
    ratings = Ratings.query.all()
    return render_template('index.html', Ratings=ratings, Result=results)



@app.route('/display/<string:session_id>')
def display(session_id):
    #all_todo = Ratings.query.all()
    #print(all_todo)
    results = Result.query.filter_by(session_id=session_id).all()
    ratings = Ratings.query.all()
    db.session.add_all(results)
    db.session.commit()
    return render_template('index.html',Ratings=ratings,Result=results)
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Ratings.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
@app.route('/login',methods=['GET', 'POST'])
def login_validation():
   if request.method == "POST":
       # if 'error_message' in session:
       #     flash(session['error_message'])
       #     session.pop('error_message', None)
        email=request.form.get('email')
        password=request.form.get('password')
        try:
            user = users.query.filter_by(email_id=email).first()
            if (user and user.password == password) and (user and user.email_id == email):
                return redirect('/home')
            else:
                session['error_message'] = 'Wrong Email Id or Password'
                return redirect('/')
        except Exception as e:
            print("an Exception occured: ",e)
   return render_template('Login.html')
@app.route('/sign_up',methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        user_id = request.form.get('user_id') 
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        data = users(user_id=user_id,email_id=email,name=name,password=password)
        db.session.add(data)
        db.session.commit()
        return redirect('/')
    return render_template("sign_up.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the  tables
    app.run(debug=True)

from flask import Blueprint, request, Flask, render_template, redirect, flash, session, jsonify, url_for
from models import Fcuser, db

login_register = Blueprint('login_register',__name__, template_folder='templates')

@login_register.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        id = request.form.get('userid')
        pwd = request.form.get('password')
        data = Fcuser.query.filter_by(userid=id, password=pwd).first()
        print(id)
        if data is not None:
            session['login']=True

            # 이름 조회
            fcuser = Fcuser.query.filter_by(userid=id).values('username')
            print(fcuser)
            return render_template("dashboard.html")
        else:
            flash('아이디와 비밀번호를 확인해주세요')
            return render_template('login.html')

# 모든 웹화면에서 로그인 했을 경우 웹 상단에 '로그아웃' 버튼이 활성화됨. 이때 '로그아웃' 버튼 클릭시 아래 함수 실행
@login_register.route('/logout')
def logout():
    session['login']=False # session을 클리어 해버림. 즉 session이 유지된다는 말은 로그아웃을 누르기전까진 로그인이 되어 있는 상태를 뜻함.

    if session['login']==False:
        return redirect(url_for('login_register.home'))

    return render_template('login.html')

#GET = 페이지가 나오도록 요청. POST = 버튼을 눌렀을때 데이터를 가지고오는 요청/ 요청정보확인하려면 request 임포트 필요
@login_register.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        #회원정보 생성
        userid = request.form.get('userid')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        username = request.form.get('username')
        birth_year = request.form.get('birth_year')
        sex = request.form.get('sex')
        email = request.form.get('email')
        print(password) # 들어오나 확인해볼 수 있다.


        if not (userid and username and password and re_password and username and birth_year and sex and email) :
            flash("모두 입력해라")
            return render_template('register.html')
        elif password != re_password:
            flash("비밀번호 확인해라")
            return render_template('register.html')
        else: #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
            fcuser = Fcuser()
            fcuser.userid = userid
            fcuser.password = password           #models의 FCuser 클래스를 이용해 db에 입력한다.
            fcuser.username = username
            fcuser.birth_year = birth_year
            fcuser.sex = sex
            fcuser.email = email

            db.session.add(fcuser)
            db.session.commit()
            flash('회원가입 완료')
            return render_template('login.html')

        return redirect('/')

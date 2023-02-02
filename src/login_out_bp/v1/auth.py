# @Author  : kane.zhu
# @Time    : 2023/2/2 15:13
# @Software: PyCharm
# @Description:
from flask import Blueprint, jsonify,render_template,request,flash,redirect,url_for
from settings.conf import PrdConfig

login_out_bp = Blueprint('login_out_bp', __name__, template_folder=PrdConfig.TEMPLATE_PATH)



@login_out_bp.route('/')
def index():
    return render_template('index.html')


@login_out_bp.route('/profile')
def profile():
    return render_template('profile.html')


@login_out_bp.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        print(request.form)
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        print('email is {}, password is {}'.format(email,password))
        if email != "kane.zhu@example.com" or password != '123':
            flash('Please check your login details and try again.')
            return redirect(url_for('login_out_bp.login'))

        return  redirect(url_for('login_out_bp.profile'))
    else:
        return render_template('login.html')



@login_out_bp.route('/signup', methods=['POST'])
def signup():

    return render_template('signup.html')








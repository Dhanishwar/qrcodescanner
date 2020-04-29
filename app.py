from qr import qrgen
from flask import  Flask,render_template
from flask import *
from sqlalchemy.sql import select
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
app = Flask(__name__)
engine = create_engine('sqlite:///qrs.db', echo = True)
meta = MetaData()
emp = Table(
   'login', meta, 
   Column('uid', String, primary_key = True), 
   Column('name', String), 
   Column('passw', String),
)
store = Table(
   'history', meta, 
   Column('uid', String), 
   Column('qrname', String),
)
meta.create_all(engine)
connection = engine.connect()


@app.route('/',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		result = request.form.to_dict()

		return render_template('login.html')
	else:
		return render_template('login.html')

@app.route('/signin',methods=['GET','POST'])
def signin():
	if request.method == 'POST':
		return render_template('signin.html')
	return render_template('signin.html')

@app.route('/generateQR',methods=['GET','POST'])
def home():
	if request.method == 'POST':
		result = request.form.to_dict()
		print(result)
		global cur_user
		cur_user = str(result['user'])
		print(cur_user)
		if len(result)>2:
			print('From signin')
			query = emp.insert()
			query = emp.insert().values(uid=str(result['user']), name=str(result['name']), passw=str(result['pass'])) 
			#query = emp.insert().values(uid='dhanish',name='Dhanishwar',passw='dhanish')
			connection = engine.connect()
			ResultProxy = connection.execute(query)
			return render_template('index.html')
		else:
			print('From login')
			s = select([text("* from login")])
			# .where(text("login.uid = "+result['user']+" and login.passw = "+result['pass']))
			conn = engine.connect()
			res = conn.execute(s, x = 'A', y = 'L')
			pw = res.fetchall()
			print(pw)
			if pw != []:
				for u, n, p in pw:
					if u == str(result['user']) and p == str(result['pass']):
						return render_template('index.html')
					else:
						print(u,result['user'],'dunno')
				return render_template('invalid.html')				
			else:
				return render_template('invalid.html')
    
@app.route('/converted',methods = ['POST'])
def convert():
    global tex
    tex = request.form['test']
    qrgen(tex)
    query = store.insert()
    query = store.insert().values(uid=str(cur_user), qrname=str(tex)) 
    connection = engine.connect()
    ResultProxy = connection.execute(query)
    print('successfully inserted')
    filename = tex+'.png'
    print(filename)
    return send_file(filename,as_attachment = True)

@app.route('/download')
def download():
    s = select([text("* from history")])
    ans = {}
    conn = engine.connect()
    res = conn.execute(s, x = 'A', y = 'L')
    pw = res.fetchall()
    print(pw)
    for u, n in pw:
    	if u == cur_user:
    		ans[n] = 1
    if len(ans) == 0:
    	ans['Nothing yet'] = 1
    return render_template('download.html',result = ans)

if __name__ == "__main__":
     app.run(debug=True)

from datetime import timedelta, datetime


from flask import Flask, render_template, request, jsonify

app: Flask = Flask(__name__)

from pymongo import MongoClient
client = MongoClient()
db = client.izren
import hashlib
import jwt
import os


@app.route('/')
def home():
    print('home')
    token = request.cookies.get('token')
    try:
        tokenDecode = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        print(tokenDecode)

        return render_template('index.html', name = tokenDecode['name'])
    except jwt.ExpiredSignatureError:
        return render_template("index.html")
    except jwt.exceptions.DecodeError:
        return render_template("index.html")


@app.route('/join')
def join_redirect():
    return render_template('join.html')

@app.route("/join", methods=["POST"])
def join():
    ID = request.form['ID']
    PW = request.form['PW']
    name = request.form['name']
    print(PW)
    hash_object = hashlib.sha256()
    hash_object.update(PW.encode())
    PWencode = hash_object.hexdigest()
    print(PWencode)
    doc = {
        'ID':ID,
        'PW':PWencode,
        'name':name
    }
    db.users.insert_one(doc)
    return jsonify({'msg':"가입 완료"})

@app.route('/login')
def login_redirect():
    return render_template('login.html')


SECRET_KEY = 'secret_key'
@app.route('/login', methods=['POST'])
def login():
    ID = request.form['ID']
    PW = request.form['PW']
    hash_object = hashlib.sha256()
    hash_object.update(PW.encode())
    PWencode = hash_object.hexdigest()

    user = db.users.find_one({'ID':ID,'PW':PWencode}, {'_id': False})
    print(user)

    if user == None:
        return jsonify({'msg': "아이디,비밀번호를 확인해주세요"})
    else:
        name = (user['name'])
        payload = {
            "ID": ID,
            "name": name,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
    if os.environ.get('HOME') == None:
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    else:
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256").decode('utf-8')
    print(os.environ.get)
    return jsonify({'response': 'success', 'token': token})


@app.route("/ID_CHECK", methods=["POST"])
def ID_CHECK():
    ID = request.form['ID']
    print(ID)
    user = db.users.find_one({'ID': ID})
    print(user)
    if user != None:
        return jsonify({'msg': "이미 있는 아이디 입니다."})
    else :
        return jsonify({'msg': "가능한 아이디 입니다."})

@app.route("/list", methods=["POST"])
def moods_post():
    emt_receive = request.form['emt_give']
    comment_receive = request.form['comment_give']
    music_receive = request.form['music_give']

    doc = {
        'emt':emt_receive,
        'comment':comment_receive,
        'music':music_receive
    }

    db.mood.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


@app.route("/rank", methods=["POST"])
def rank_post():
    emoji_receive = request.form['emoji_give']

    doc = {
        'emoji' : emoji_receive
    }
    db.ranks.insert_one(doc)
    return jsonify({'msg': '태그 완료'})

@app.route("/rank", methods=["GET"])
def rank_get():
    emoji_list = list(db.ranks.find({}, {'_id': False}))
    return jsonify({'emojis': emoji_list})


@app.route("/list", methods=["POST"])
def mood_post():
    emt_receive = request.form['emt_give']
    comment_receive = request.form['comment_give']
    music_receive = request.form['music_give']
    comment_list = list(db.mood.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'emt':emt_receive,
        'comment':comment_receive,
        'music':music_receive,
        'num': count
    }

    db.mood.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/list", methods=["GET"])
def comment_get():
    comment_list = list(db.mood.find({}, {'_id': False}))
    print(comment_list)
    return jsonify({'comments':comment_list})

@app.route("/list/comment", methods=["POST"])
def homework2_post():
    text_receive = request.form['text_give']
    num_receive = request.form['num_give']

    print(num_receive,text_receive)

    doc = {
        'postComment': text_receive,
        'num': num_receive
    }
    db.mood_post.insert_one(doc)
    return jsonify({'msg':'댓글 완료!'})

@app.route("/list/comment", methods=["GET"])
def text_get():
    text_list = list(db.mood_post.find({}, {'_id': False}))
    return jsonify({'texts':text_list})




if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
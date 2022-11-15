from flask import Blueprint, render_template, request, jsonify

from db import db

import routes.common_function as common_function

mypage = Blueprint("mypage", __name__, url_prefix="/mypage")


# 마이 페이지 기본 정보 get
@mypage.route('/')
def mypage_home():
    user_id = "qwer"
    user = db.testUsers.find_one({'user_id': user_id}, {'_id': False})

    return render_template('mypage.html', user_name=user['user_name'], til_count=user['til_count'])

# 내가 작성했던 리스트 get
@mypage.route('/data')
def mypage_data():
    user_id = "qwer"
    question_list = list(db.testQuestions.find({'user_id': user_id}, {'_id': False}))
    print(question_list)

    return jsonify({'question_list': question_list})


# til 카운터 +1
@mypage.route('/til/keeping', methods=['POST'])
def mypage_til_save():
    user_id = "mina"

    til_url = request.form['til_url']
    print(til_url)
    til_count = request.form['til_count']
    print(til_count)
    date = common_function.now_time('sametime')

    db.users.update_one({'user_id': user_id}, {'$set': {'til_count': int(til_count) + 10}})
    doc = {
        'user_id': user_id,
        'til_url': til_url,
        'til_date': date
    }
    db.til.insert_one(doc)

    return jsonify({"message": "축하드려요 🎉 + 10 점을 획득하셨습니다! "})



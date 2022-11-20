import datetime

from flask import Blueprint, render_template, request, jsonify
from datetime import date, timedelta
import calendar

from db import db

import routes.common_function as common_function
import routes.login as jwt_check

mypage = Blueprint("mypage", __name__, url_prefix="/mypage")


# 마이 페이지 기본 정보 get
@mypage.route('/')
def mypage_home():


    user_check = jwt_check.user_check()

    if user_check['result'] != "fail":
        user_id = user_check['user_id']

        user = db.users.find_one({'user_id': user_id}, {'_id': False})
        user_name = user['user_name']
        til_count = user['til_count']

        # 자신의 til_count보다 높은 유저들의 list 길이
        til_rank = len(list(db.users.find({'til_count': {'$gt': til_count}})))
        til_rank = til_rank + 1

        return render_template('mypage.html', user_name=user['user_name'], til_count=til_count, til_rank=til_rank)

    else:
        return render_template('login.html')

# 내가 작성했던 리스트 및 til 데이터 get
@mypage.route('/data')
def mypage_data():

    user_check = jwt_check.user_check()

    if user_check['result'] != "fail":

        user_id = user_check['user_id']

        today = date.today()
        year = today.year
        month = today.month

        last_day = calendar.monthrange(year, month)[1]

        month_first_day = datetime.datetime(year, month, 1)
        month_last_day = datetime.datetime(year, month, last_day)

        question_list = list(db.question.find({'user_id': user_id}, {'_id': False}))
        til_list = list(db.til.find({'user_id': user_id, 'til_date': {'$gte': month_first_day, '$lte': month_last_day}}, {'_id': False}).sort('til_date', 1))

        til_date_list = []

        for i in til_list:
            til_date_list.append(i['til_date'].day)

        return jsonify({'question_list': question_list, 'til_date_list': til_date_list}), 200

    else:
        return render_template("login.html")


# til 카운터 +1
@mypage.route('/til/keeping', methods=['POST'])
def mypage_til_save():

    user_check = jwt_check.user_check()

    if user_check['result'] != "fail":
        user_id = user_check['user_id']

        til_url = request.form['til_url']
        til_count = request.form['til_count']

        date = common_function.now_time('sametime')
        today_til = db.til.find_one({'user_id': user_id, 'til_date': date})

        if today_til is None:

            db.users.update_one({'user_id': user_id}, {'$set': {'til_count': int(til_count) + 10}})

            doc = {
                'user_id': user_id,
                'til_url': til_url,
                'til_date': date
            }

            db.til.insert_one(doc)
            return jsonify({"message": "축하드려요 🎉 + 10 점을 획득하셨습니다! "}), 200

        else:
            return jsonify({"message": "하루에 한번만 가능합니다."}), 200

    else:
        return render_template('login.html')

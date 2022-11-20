from flask import Blueprint, render_template ,request, jsonify
import routes.common_function as common_function
from db import db
import routes.login as jwt_check

post = Blueprint("post", __name__, url_prefix="/post")

# 답변 저장 APi
@post.route('/answer', methods=['POST'])
def answer_insert():
    try:

        user_check = jwt_check.user_check()

        if user_check['result'] != "fail":
            user_id = user_check['user_id']


            question_id = int(request.form['question_id'])
            answer_detail = request.form['answer_detail']

            user = db.users.find_one({'user_id': user_id}, {'_id': False})
            user_name = user['user_name']

            answer_date = common_function.now_time('othertime')

            # question_id일 때의 데이터 중 answer_list의 값 중 가장 최신일 때의 데이터
            question = db.question.find_one({'question_id': question_id}, {'answer_list': {'$slice': -1}})

            if len(question['answer_list']) != 0:
                # 가장 최신의 answer_id를 가져옴
                answer_id = question['answer_list'][0]['answer_id']
                answer_id = answer_id + 1
            else:
                answer_id = 1
        
            doc = {
                'user_id': user_id,
                'user_name': user_name,
                'answer_date': answer_date,
                'answer_id': answer_id,
                'answer_detail': answer_detail,
                'a_heart_count': 0
            }

            # question_id일 때의 answer_list 필드에  답변 추가
            db.question.update_one({'question_id': question_id}, {'$push': {'answer_list': doc}})

            return jsonify({"message": "댓글 등록 완료!"})
           

        else:
            return render_template('login.html')

    except: return jsonify({"message": "다시 시도해주세요."})



# 게시글 수정
@post.route('/modification', methods=['POST'])
def post_update():

    user_check = jwt_check.user_check()

    if user_check['result'] != "fail":
        user_id = user_check['user_id']

        question_id = int(request.form['question_id'])
        question_detail = request.form['question_detail']

        # user_id와 question_id에 저장된 user_id가 맞는지 확인 하기 위한 find
        post = db.question.find_one({'question_id': question_id}, {'_id': False})

        # 같다면 update
        if post['user_id'] == user_id:
            db.question.update_one({'question_id': question_id}, {'$set': {'question_detail': question_detail}})
            return jsonify({"message": "success"}), 200

        else:
            # 같지 않다면 fail
            return jsonify({"message": "fail"}), 203

    else:
        return render_template('login.html')


# 게시글 삭제
@post.route('/deletion', methods=['POST'])
def post_delete():

    user_check = jwt_check.user_check()

    if user_check['result'] != "fail":
        user_id = user_check['user_id']

        question_id = int(request.form['question_id'])

        # user_id와 question_id에 저장된 user_id가 맞는지 확인 하기 위한 find
        post = db.question.find_one({'question_id': question_id}, {'_id': False})

        # 같다면 delete
        if post['user_id'] == user_id:
            db.question.delete_one({'question_id': question_id})
            # question의 answer들도 삭제하는 로직 추가 구현 필요
            return jsonify({"message": "success"}), 200

        else:
            # 같지 않다면 fail
            return jsonify({"message": "fail"}), 203

    else:
        return render_template('login.html')
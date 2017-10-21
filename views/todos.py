# coding: utf-8
import datetime

from leancloud import Object
from leancloud import Query
from leancloud import LeanCloudError
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from model import action_parser

class Todo(Object):
    pass

todos_view = Blueprint('todos', __name__)


@todos_view.route('')
def show():
    try:
        todos = Query(Todo).descending('createdAt').find()
    except LeanCloudError as e:
        if e.code == 101:  # 服务端对应的 Class 还没创建
            todos = []
        else:
            raise e
    return render_template('todos.html', todos=todos)


@todos_view.route('', methods=['POST'])
def add():
    content = request.form['content']
    todo = Todo(content=content)
    try:
        todo.save()
    except LeanCloudError as e:
        return e.error, 502
    return redirect(url_for('todos.show'))

@todos_view.route('/schedule', methods=['GET'])
def show_schedule():
    # todos = Query(Todo).descending('createdAt').find()
    #
    # action_list = []
    # for a_todo in todos:
    #     action_list.append(eval(a_todo.get('content')))
    #
    #
    #
    # print(action_list)
    # action_list = sorted(action_list, key=lambda k: list(k.keys())[0])
    #
    # task_list = []
    #
    # for _action in action_list:
    #     for _time, _text in _action.items():
    #         if 'add_task' in _text:
    #             _freq = int(_text[10])
    #             _task_name = str(_text[12:])
    #
    #             task_list.append(
    #                 {
    #                     'task_name': _task_name,
    #                     'freq': _freq,
    #                     'last': _time
    #                 }
    #             )
    #
    #         elif 'exec_task' in _text:
    #             _task_name = str(_text[11:])
    #             _task_id = [_id for _id, _dict in enumerate(task_list) if _dict['task_name'] == _task_name][0]
    #             task_list[_task_id]['last'] = _time
    #
    task_list = []

    actions = Query(Todo).descending('createdAt').find()
    for _action in actions:
        _args = action_parser(_action.get('content'))
        print(_action.get('createdAt'))
        print(type(_action.get('createdAt')))
        _time = int(filter(str.isdigit, str(_action.get('createdAt')))[:14])

        if _args.is_new:
            task_list.append(
                {
                    'task_name': _args.task,
                    'freq': _args.freq,
                    'last': _time
                }
            )

        elif _args.is_exec:
            _task_name = _args.task
            _task_id = [_id for _id, _dict in enumerate(task_list) if _dict['task_name'] == _task_name][0]
            task_list[_task_id]['last'] = _time

        elif _args.is_update:
            _task_name = _args.task
            _task_id = [_id for _id, _dict in enumerate(task_list) if _dict['task_name'] == _task_name][0]
            old_task = task_list[_task_id]
            task_list[_task_id] ={
                'task_name': _args.task,
                'freq': _args.freq,
                'last': old_task['last']
            }



    todo_list = []
    for _task in task_list:
        # now
        _now = datetime.datetime.now()

        # num2datetime
        _str_date = str(_task['last'])
        _py_date = datetime.datetime.strptime(_str_date,'%Y%m%d%H%M%S')

        # diff_time
        _diff = (_now - _py_date).total_seconds()

        # heat
        _task_freq = int(_task['freq'])
        if _task_freq == 0:
            _heat = round(_diff * 0.5, 2)

        elif _task_freq == 1:
            _heat = round(_diff/60 - 1, 2)
        elif _task_freq == 2:
            _heat = round(_diff/60/60 - 1, 2)
        elif _task_freq == 3:
            _heat = round(_diff/60/60/24 - 1, 2)
        elif _task_freq == 4:
            _heat = round(_diff/60/60/24/7 - 1, 2)
        elif _task_freq == 5:
            _heat = round(_diff/60/60/24/30 - 1, 2)
        elif _task_freq == 6:
            _heat = round(_diff/60/60/24/365 - 1, 2)
        else:
            _heat = -9

        # update todo_list
        todo_list.append([_heat, _task['freq'], _task['task_name']])

    # print todo list
    todo_list.sort(key=lambda x:x[0],reverse=True)  #逆序
    todo_list[0:0] = [['heat', 'freq', 'task_name']]

    return render_template('schedule.html', schedule=todo_list)
    # return str(todo_list)



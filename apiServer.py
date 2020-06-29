import flask, json
from flask import request, make_response
from flask_cors import CORS
import time
import main

server = flask.Flask(__name__)
CORS(server, resources=r'/*')

def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

server.after_request(after_request);

@server.route('/addPic', methods=['get', 'post'])

def addPic():
    # 获取通过url请求传参的数据

    params = request.json
    if params == None:
        params = request.values
    allParams = {}
    for item in ['startPage']:
        try:
            allParams[item] = int(params.get(item))
        except BaseException:
            return {
                'code': 400,
                'message': item + '错误',
                'data': []
            }
    startPage = allParams['startPage']
    result = main.manyWebsite(startPage)
    uploadResult = True
    msg = []
    for indexs, items in enumerate(result):
        for index, item in enumerate(items):
            if item != 'success':
                uploadResult = False
                errorInfo = ('第', (startPage + indexs), '页,', '第', index, '个图片有问题')
                msg.append(errorInfo)
    return json.dumps({
        'startPage': startPage,
        'result': result[0],
        'msg': msg,
        'uploadResult': uploadResult,
        'length': len(result)
    }, ensure_ascii=False)  # 将字典转换为json串, json是字符串

@server.route('/getPicInfo', methods=['get', 'post'])

def getPicInfo():
    params = request.json
    if params == None:
        params = request.values
    allParams = {}
    for item in ['page', 'pageSize', 'kind']:
        try:
            allParams[item] = int(params.get(item))
        except BaseException:
            return {
                'code': 400,
                'message': item+'错误',
                'data': []
            }
    page = allParams['page']
    pageSize = allParams['pageSize']
    kind = allParams['kind']
    data = main.getTableMainInfo(page, pageSize, kind)
    result = {
        'code': 200,
        'message': '成功',
        'data': data
    }
    return result

@server.route('/ChangePicStatus', methods=['get', 'post'])

def ChangePicStatus():
    params = request.json
    if params == None:
        params = request.values
    allParams = {}
    for item in ['picId', 'kind']:
        try:
            allParams[item] = int(params.get(item))
        except BaseException:
            return {
                'code': 400,
                'message': item + '错误',
                'data': []
            }
    picId = allParams['picId']
    kind = allParams['kind']
    main.changePicStatus(picId, kind)
    return {
        'code': 200,
        'message': '修改成功'
    }

@server.route('/loginVerify', methods=['get', 'post'])

def loginVerify():
    params = request.json
    if params == None:
        params = request.values
    allParams = {}
    for item in ['username', 'password']:
        try:
            allParams[item] = params.get(item)
        except BaseException:
            return {
                'code': 400,
                'message': item + '错误',
                'data': []
            }
    username = allParams['username']
    password = allParams['password']
    result = main.loginVerify(username, password)
    if result == 200:
        return {
            'code': result,
            'message': '登录成功'
        }
    else:
        return {
            'code': result,
            'message': '登录失败'
        }


@server.route('/insertLoginInfo', methods=['get', 'post'])

def insertLoginInfo():
    params = request.json
    if params == None:
        params = request.values
    allParams = {}
    for item in ['username', 'password']:
        try:
            allParams[item] = params.get(item)
        except BaseException:
            return {
                'code': 400,
                'message': item + '错误',
                'data': []
            }
    username = allParams['username']
    password = allParams['password']
    data = main.insertLoginInfo(username, password)
    print(data)
    return {
        'code': 200,
        'data': data
    }

@server.route('/updateFieldNum', methods=['get', 'post'])

def updateFieldNum():
    params = request.json
    if params == None:
        params = request.values
    allParams = {}
    for item in ['id', 'field']:
        try:
            allParams[item] = params.get(item)
        except BaseException:
            return {
                'code': 400,
                'message': item + '错误',
                'data': []
            }
    id = allParams['id']
    field = allParams['field']
    data = main.updateFieldNum(id, field)
    return {
        'code': data['code'],
        'message': data['message']
    }

@server.route('/getChartSource', methods=['get', 'post'])

def getChartSource():
    data = main.getChartSource()
    for i in data['result']:
        print(i)
        i['percent'] = round(i['count'] / data['sum'], 2)
    print(data)
    return {
        'code': 200,
        'data': data['result']
    }

@server.route('/getManageInfo', methods=['get', 'post'])

def getManageInfo():
    data = main.getManageInfo()
    print(data)
    return {
        'code': 200,
        'data': data
    }


if __name__ == '__main__':
    server.run(debug=True, port=8888, host='0.0.0.0')

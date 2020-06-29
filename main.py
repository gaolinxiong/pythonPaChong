import useSelenium
import requests
from io import BytesIO  # python 3
from PIL import Image
import nude
import random
import string
import connectMysql
import hashlib

def getChartSource():
    sql = connectMysql.getChartSourceSQL()
    getResult = connectMysql.getTableInfoResult(sql)
    result = []
    sum = 0
    for item in list(getResult):
        result.append({
            'item': list(item)[1],
            'count': list(item)[0]
        })
        sum += list(item)[0]

    return {
        'result': result,
        'sum': sum
    }

def getManageInfo():
    sql = connectMysql.getManageInfo()
    getResult = connectMysql.getTableInfoResult(sql)
    result = []
    for item in list(getResult):
        result.append({
            'username': list(item)[1],
            'password': list(item)[3]
        })
    return result


def main(url):
    allResult = []
    for imgUrl in useSelenium.findPic(url):
        response = requests.get(imgUrl)
        content = BytesIO(response.content)  # 图片io流转入
        picInfo = UploadFun(content)
        picUrl = picInfo['data']
        picMsg = picInfo['msg']

        img = Image.open(content)
        width = img.size[0]
        height = img.size[1]
        n = nude.Nude(img)
        n.resize(maxheight=800, maxwidth=600)
        n.parse()

        greyPic = n.showSkinRegions()
        imgByteArr = BytesIO()
        # greyPic.save(imgByteArr, format='JPEG')
        greyPic.save(imgByteArr, format='PNG')

        greyContent = BytesIO(imgByteArr.getvalue())
        judgeInfo = n.inspect()
        judgeResult = judgeInfo['result']
        judgeMessage = judgeInfo['message']
        greyWidth = judgeInfo['width']
        greyHeight = judgeInfo['height']

        greyPicInfo = UploadFun(greyContent)
        greyPicUrl = greyPicInfo['data']
        greyPicMsg = greyPicInfo['msg']

        uploadParams = {
            'pic_url': picUrl,
            'pic_width': width,
            'pic_height': height,
            'pic_message': picMsg,
            'greypic_url': greyPicUrl,
            'greypic_width': greyWidth,
            'greypic_height': greyHeight,
            'greypic_message': greyPicMsg,
            'judge_result': judgeResult,
            'judge_message': judgeMessage,
        }
        sql = connectMysql.addPicData(uploadParams)
        mysqlResult = connectMysql.connectFun(sql)
        allResult.append(mysqlResult)
    return allResult

def UploadFun(img_url):
    url = 'http://rd-cdn-services-server.qutoutiao.net/upload'
    data = {
        'name': '高林雄',
        'userid': 'gaolinxiong@qutoutiao.net',
        'position': '前端开发工程师',
        'rootdir': 'wlx/lp/interImgs',
        'token': '2457iU-P5Hq2RS1phgoxbY2MmQ2OWGgQGDGufG4k8ZoE2BLVdUHEDQdqCxDvux9I70kJGsAiIKQ16zkQj-mn4os'
    }
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    name = 'glx_' + salt + '.jpg'
    files = {
        'file': (name, img_url)
    }
    r = requests.post(url, data=data, files=files)
    return eval(r.content.decode('utf-8'))

def manyWebsite(startPage):
    mysqlResults = []
    website = 'https://reeoo.com//page/' + str(startPage)
    mysqlResults.append(main(website))
    return mysqlResults

def changePicStatus(picId, kind):
    sql = connectMysql.changePicStatus(picId, kind)
    connectMysql.getTableInfoResult(sql)

def insertLoginInfo(username, password):
    hl = hashlib.md5()
    hl.update(password.encode(encoding='utf-8'))
    sql = connectMysql.insertLoginInfo(username, hl.hexdigest(), password)
    connectMysql.getTableInfoResult(sql)
    return '增加成功'

def loginVerify(username, password):
    hl = hashlib.md5()
    hl.update(password.encode(encoding='utf-8'))
    sql = connectMysql.getLoginInfo(username)
    passwordResult = connectMysql.getTableInfoResult(sql)
    try:
        if (list(list(passwordResult)[0])[0] == hl.hexdigest()):
            # 高林雄很帅，200是校验成功
            return 200
        else:
            # 反之
            return 204
    except BaseException:
        return 205


def getTableMainInfo(page, pageSize, kind):
    startNum = (page - 1) * pageSize
    sql = connectMysql.getTableMainInfo(startNum, pageSize, kind)
    sql2 = connectMysql.getTableCountInfo(kind)
    getResult = connectMysql.getTableInfoResult(sql)
    getTotal = connectMysql.getTableInfoResult(sql2)
    tableList = []
    for item in getResult:
        listItem = {
            'id': item[0],
            'pic_url': item[1],
            'pic_width': item[2],
            'pic_height': item[3],
            'pic_message': item[4],
            'greypic_url': item[5],
            'greypic_width': item[6],
            'greypic_height': item[7],
            'greypic_message': item[8],
            'judge_result': item[9],
            'judge_message': item[10],
            'upload_time': item[11],
            'likes': item[12],
            'favorites': item[13],
            'dislikes': item[14],
        }
        tableList.append(listItem)
    return {
        'list': tableList,
        'total': getTotal[0][0]
    }

def updateFieldNum(id, field):
    try:
        sql1 = connectMysql.getFieldNum(id, field)
        getResult = connectMysql.getTableInfoResult(sql1)
        sql2 = connectMysql.addFieldNum(id, field, list(list(getResult)[0])[0]+1)
        connectMysql.getTableInfoResult(sql2)
        return {
            'code': 200,
            'message': '修改成功'
        }
    except BaseException:
        return {
            'code': 205,
            'message': '修改成功'
        }

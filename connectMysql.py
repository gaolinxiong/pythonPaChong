import pymysql
import time

def connectFun(sql):
    db = pymysql.connect("localhost", "root", "root", "picData")
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        # 如果发生错误则回滚
        db.rollback()
        return 'error'
    # 关闭数据库连接
    db.close()
    return 'success'


def getChartSourceSQL():
    sql = f"""
            select count(*), date from picSet group by date
        """
    return sql

def getManageInfo():
    sql = f"""
                select * from manager
            """
    return sql


def addPicData(uploadParams):
    judge_result = int(0)
    if uploadParams['judge_result']:
        judge_result = int(1)
    upload_date = int(time.time())
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    sql = f"""
        INSERT INTO `picSet` (`pic_url`,
                            `pic_width`,
                            `pic_height`,
                            `pic_message`,
                            `greypic_url`,
                            `greypic_width`,
                            `greypic_height`,
                            `greypic_message`,
                            `judge_result`,
                            `judge_message`,
                            `upload_date`,
                            `date`)
        VALUES ('{uploadParams['pic_url']}',
                '{uploadParams['pic_width']}',
                '{uploadParams['pic_height']}',
                '{uploadParams['pic_message']}', 
                '{uploadParams['greypic_url']}', 
                '{uploadParams['greypic_width']}',
                '{uploadParams['greypic_height']}',
                '{uploadParams['greypic_message']}',
                {judge_result},
                '{uploadParams['judge_message']}',
                {upload_date},
                '{date}'
                )"""
    return sql

def getTableMainInfo(startNum, pageSize, kind):
    sql = f"""
        select * from picSet where judge_result = {kind} limit {startNum}, {pageSize}
    """
    return sql

def getFieldNum(id, field):
    sql = f"""
        select {field} from picSet where id = {id}
    """
    return sql

def addFieldNum(id, field, num):
    sql = f"""
        update picSet set {field} = {num} where id = {id}
    """
    return sql

def changePicStatus(picId, kind):
    sql = f"""
            update picSet set judge_result = {kind} where id = {picId} 
        """
    return sql;

def getTableCountInfo(kind):
    sql = f"""
        select count(*) from picSet where judge_result = {kind}
    """
    return sql

def getLoginInfo(username):
    sql = f"""
        select password from manager where username = '{username}'
    """
    return sql

def insertLoginInfo(username, password, real_password):
    sql = f"""
            INSERT INTO manager ( `username`, `password`, `real_password` )
                       VALUES
                       ( '{username}', '{password}', '{real_password}' );
        """
    return sql

def getTableInfoResult(sql):
    db = pymysql.connect("localhost", "root", "root", "picData")
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        selectResultList = cursor.fetchall()
        db.commit()
    except Exception as e:
        print(e)
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()
    # if selectResultList:
    return selectResultList

if __name__ == "__main__":
    connectFun()

# def createPicSet():
#     sql = """
#         CREATE TABLE `picSet` (
#         `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
#           `pic_url` varchar(256) NOT NULL,
#           `pic_width` varchar(40) NOT NULL,
#           `pic_height` varchar(40) NOT NULL,
#           `pic_message` varchar(128) NOT NULL,
#           `greypic_url` varchar(256) NOT NULL,
#           `greypic_width` varchar(40) NOT NULL,
#           `greypic_height` varchar(40) NOT NULL,
#           `greypic_message` varchar(128) NOT NULL,
#           `judge_result` int(11) NOT NULL,
#           `judge_message` varchar(128) NOT NULL DEFAULT '',
#           `upload_date` int(11) NOT NULL,
#           `likes` int(11) DEFAULT '0',
#           `favorites` int(11) DEFAULT '0',
#           PRIMARY KEY (`id`)
#         ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#     """
#     return sql
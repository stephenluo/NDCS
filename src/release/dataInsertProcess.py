import json
import pymssql
import sys
import os


# 执行数据插入功能
def do_data_insert(task_path, parse_time):
    # 读取配置文件
    with open("../parser_conf.json", "r") as cfgFile:
        cfgMsg = json.load(cfgFile)

    # 解析结果文件读取
    parserResultFilePath = task_path + os.sep + parse_time + os.sep + cfgMsg['PARSER_RESULT_DIR']
    # 得到同批次所有文件
    listFile = os.listdir(parserResultFilePath)
    it = iter(listFile)

    # 得到数据库连接对象,游标对象
    conn = DBHelper.get_connection()
    cursor = DBHelper.get_cursor(conn)

    # 遍历解析后数据文件
    for fileName in it:
        filePath = parserResultFilePath + os.sep + fileName
        with open(filePath, "r", encoding='utf-8') as file:
            estateList = json.load(file)

        for item in estateList:
            # 得到增加楼盘的sql
            insertSql = get_insert_sql(item, parse_time)
            try:
                # 插入一条楼盘数据
                cursor.execute(insertSql)
                conn.commit()
            except Exception as err:
                # 发生错误时回滚
                conn.rollback()
                print("插入数据error: {0}".format(err))
    conn.close()
    print("----------------------------【data insert finished】----------------------------------")


# 得到插入sql语句
def get_insert_sql(e_info, time):
    insertSql = "insert into estate_data values('{0:s}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}')" \
        .format(e_info['id'],
                time,
                e_info['items']['estate_name'],
                e_info['items']['estate_address'],
                e_info['items']['unit_price'],
                e_info['items']['area'],
                e_info['items']['total_price'],
                e_info['items']['room_type'],
                e_info['items']['floor'],
                e_info['items']['orientation'],
                e_info['items']['building_age']
                )
    return insertSql

    # print(item["data_name"], item["id"])
    # print(item["items"]["estate_name"], item["items"]["room_type"], item["items"]["building_age"])


class DBHelper:
    @staticmethod
    def get_connection() -> pymssql.Connection:
        conn = pymssql.connect(server='172.28.70.68', user='sa', password='1qaz!QAZ', database='DB_DC_LEJU_DATA')
        return conn

    @staticmethod
    def get_cursor(conn) -> pymssql.Cursor:
        return conn.cursor()


# 接收参数
taskPath = sys.argv[1]
parseTime = sys.argv[2]

# taskPath = 'D:/task'
# parseTime = '20160613111111'

# 执行数据插入
do_data_insert(taskPath, parseTime)

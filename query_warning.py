import pymysql
import datetime


class get():
    def __init__(self):
        pass

    def get_data(self):

        now_time = datetime.datetime.now()

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='ywjk', password='Zcsy_2021', db='kmjk',
                               charset='utf8')
        sql = "select * from send_waring where Remove_time = 'Null'"
        cursor = conn.cursor()
        cursor.execute(sql)
        info = ""
        for i in cursor.fetchall():
            info1 = ''
            delay = round(
                ((now_time - (datetime.datetime.strptime(i[6], "%Y%m%d %H:%M:%S"))).total_seconds()) / 60 / 60, 3)
            delay2 = round(
                ((now_time - (datetime.datetime.strptime(i[2], "%Y%m%d %H:%M:%S"))).total_seconds()) / 60 / 60, 3)
            print("上次告警时长:", delay, '小时')
            if delay >= 5 or i[-1] == i[2]:
                print("==已经发送钉钉告警==")
                info1 = '服务器地址：' + i[1] + '\n首告警时间：' + i[2] + '\n告警时长(天)：' + str(round(delay2 / 24, 3)) + '\n告警内容：\n' + \
                        i[5] + '\n\n'
                sql1 = "update send_waring  set LastSend_Time='%s' where Remove_time = 'Null' and id ='%s' " % (
                    now_time.strftime("%Y%m%d %H:%M:%S"), i[0])
                cursor.execute(sql1)
                conn.commit()
            else:
                print("无最新告警数据")
            info = info + info1
        return info


if __name__ == "__main__":
    get = get()
    get.get_data()

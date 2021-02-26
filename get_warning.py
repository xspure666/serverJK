import datetime
import pymysql

"""
fuction: get data from mysql
author: xspure
date: 2021-02
"""


class warning:
    def __init__(self):
        self.now_time = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")

    def get_info(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='ywjk', password='Zcsy_2021', db='kmjk',
                               charset='utf8')
        sql = "select b.*,a.ip from server_health_info b, machine_info a where a.id= " \
              "b.serverid and b.cjsj=(select cjsj from server_health_info ORDER BY cjsj desc LIMIT 1) ORDER BY a.ip"
        cursor = conn.cursor()
        cursor.execute(sql)
        print("查询数据库调用成功")
        for i in cursor.fetchall():
            info = ""
            level0 = "正常\n"
            level1 = "一般\n"
            level2 = "严重\n"
            level3 = "致命\n"

            ipaddress = i[-1]
            if ipaddress != None:
                info = ''
                # info = info + "服务器地址：" + ipaddress + '\n'
            else:
                info = info + "无此ID：%s  对应服务器\n" % i[17]

            # 系统整机健康状态
            if i[3] != '00':
                if i[3] == '01':
                    info = info + "系统整机健康状态：" + level1
                elif i[3] == '02':
                    info = info + "系统整机健康状态：" + level2
                elif i[3] == '03':
                    info = info + "系统整机健康状态：" + level3

                # 温感子系统健康状态
                if i[4] != '00':
                    if i[4] == '01':
                        info = info + "温感子系统健康状态：" + level1
                    elif i[4] == '02':
                        info = info + "温感子系统健康状态：" + level2
                    elif i[4] == '03':
                        info = info + "温感子系统健康状态：" + level3

                # 　电压子系统健康状态
                if i[5] != '00':
                    if i[5] == '01':
                        info = info + "电压子系统健康状态：" + level1
                    elif i[5] == '02':
                        info = info + "电压子系统健康状态：" + level2
                    elif i[5] == '03':
                        info = info + "电压子系统健康状态：" + level3

                # 电源子系统健康状态
                if i[6] != '00':
                    if i[6] == '01':
                        info = info + "电源子系统健康状态：" + level1
                    elif i[6] == '02':
                        info = info + "电源子系统健康状态：" + level2
                    elif i[6] == '03':
                        info = info + "电源子系统健康状态：" + level3

                # 风扇子系统健康状态
                if i[7] != '00':
                    if i[7] == '01':
                        info = info + "风扇子系统健康状态：" + level1
                    elif i[7] == '02':
                        info = info + "风扇子系统健康状态：" + level2
                    elif i[7] == '03':
                        info = info + "风扇子系统健康状态：" + level3

                # 　硬盘系统健康状态
                if i[8] != '00':
                    if i[8] == '01':
                        info = info + "硬盘系统健康状态：" + level1
                    elif i[8] == '02':
                        info = info + "硬盘系统健康状态：" + level2
                    elif i[8] == '03':
                        info = info + "硬盘系统健康状态：" + level3

                # TPM系统健康状态
                if i[9] != '00':
                    if i[9] == '01':
                        info = info + "TPM系统健康状态：" + level1
                    elif i[9] == '02':
                        info = info + "TPM系统健康状态：" + level2
                    elif i[9] == '03':
                        info = info + "TPM系统健康状态：" + level3

                # 系统上电状态
                if i[10] != '00':
                    if i[10] == '01':
                        info = info + "系统上电状态：" + level1
                    elif i[10] == '02':
                        info = info + "系统上电状态：" + level2
                    elif i[10] == '03':
                        info = info + "系统上电状态：" + level3

                # 内存健康状态
                if i[11] != '00':
                    if i[11] == '01':
                        info = info + "内存健康状态：" + level1
                    elif i[11] == '02':
                        info = info + "内存健康状态：" + level2
                    elif i[11] == '03':
                        info = info + "内存健康状态：" + level3

                # CPU健康状态
                if i[12] != '00':
                    if i[12] == '01':
                        info = info + "CPU健康状态：" + level1
                    elif i[12] == '02':
                        info = info + "CPU健康状态：" + level2
                    elif i[12] == '03':
                        info = info + "CPU健康状态：" + level3

                # PCI健康状态
                if i[13] != '00':
                    if i[13] == '01':
                        info = info + "PCI健康状态：" + level1
                    elif i[13] == '02':
                        info = info + "PCI健康状态：" + level2
                    elif i[13] == '03':
                        info = info + "PCI健康状态：" + level3

                # update DingDing

                try:
                    sql = "insert into send_waring(id, ip, ReciveTime,AlarmTime,Remove_time,content,LastSend_Time) values('%s', '%s','%s','%s','Null','%s', '%s')" % (
                        i[17], i[-1], self.now_time, i[16], info, self.now_time)
                    sql1 = "select * from send_waring where id = '%s' and Remove_time='Null'" % i[17]
                    print(sql1)
                    cursor.execute(sql1)
                    if cursor.fetchone() == None:
                        print("插入告警数据")
                        print(sql)
                        cursor.execute(sql)
                    else:
                        sql2 = "update send_waring set AlarmTime='%s' where id = '%s'" % (self.now_time, i[17])
                        cursor.execute(sql2)
                    print("更新告警数据")
                except Exception as e:
                    print("更新告警信息error", e)
                conn.commit()

            else:
                sql3 = "select * from send_waring where id = '%s' and Remove_time='Null'" % i[17]
                sql4 = "update send_waring set Remove_time='%s' where id = '%s'" % (self.now_time, i[17])
                cursor.execute(sql3)
                if cursor.fetchone() == None:
                    print("服务器: %s 无告警取消 " % i[-1])
                else:
                    cursor.execute(sql4)
                    print("服务器: %s  告警取消完成" % i[-1])
                conn.commit()
                info = info + "服务器状态：" + level0

            info = info + '当前时间：%s\n告警时间：%s\n' % (self.now_time, i[16])
            print(info)


if __name__ == "__main__":
    warning = warning()
    warning.get_info()

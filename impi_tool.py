import paramiko
import sqlite3
import time
import os
import datetime
import pymysql


# 华三服务器获取健康状态
# 通过impitool工具来获取服务器的状态，并写入到mysql数据中
# 只针对华三服务器
# author: xspure
# fuction：get hardware infomation by impitool


class Ipmi_tool:
    def __init__(self):
        self.now_time = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
        print("============================================")
        print("======== 当前时间：" + self.now_time + '  =======')
        print("============================================")
        # self.conn = sqlite3.connect('impi.db')
        # self.cursor = self.conn.cursor()

    def insert_to_db(self, sql):
        try:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='ywjk', password='Zcsy_2021', db='kmjk',
                                   charset='utf8')
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            print("插入数据库调用成功")
        except Exception as e:
            print("插入数据库调用失败！,失败原因 %s" % e)
        cursor.close()
        conn.close()

    def query_db(self, sql):
        try:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='ywjk', password='Zcsy_2021', db='kmjk',
                                   charset='utf8')
            cursor = conn.cursor()
            cursor.execute(sql)
            print("查询数据库调用成功")
            return cursor
        except Exception as e:
            print("查询数据库调用失败！,失败原因 %s" % e)
        cursor.close()
        conn.close()

    # 远程执行命令
    def excute_command_ssh(self, hostname, passwd, command):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname, port=22, username='root', password=passwd)
        stdin, stdout, stderr = client.exec_command(command)  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值
        # 打印执行结果
        info = stdout.read().decode('utf-8')
        return info

    # 获取服务器的电源信息
    def power_info(self, hostname, passwd):
        command = 'ipmitool sdr elist | grep PMBPower'
        info = self.excute_command_ssh(hostname, passwd, command)
        info = info.strip().split('\n')
        sql = "select id from  machine_info where ip = '%s'" % hostname
        machine_id = self.query_db(sql).fetchone()[0]
        for i in info:
            cpu_name = i.split('|')[0].strip()
            up_time = i.split('|')[1].strip().replace('h', '')
            cpu_status = i.split('|')[2].strip()
            if cpu_status == 'ok':
                cpu_status = '1'
            else:
                cpu_status = '0'
            cpu_power = i.split('|')[4].replace('Watts', '').strip()
            sql = "insert into  power_info(id,cpu_name,up_time,cpu_status,cpu_power,uptime) values('%s','%s','%s','%s','%s','%s')" % (
                machine_id, cpu_name, up_time, cpu_status, cpu_power, self.now_time)
            print(sql)

            try:
                self.insert_to_db(sql)
                print("提交电源信息成功！")
            except Exception as e:
                print("提交电源信息失败！", e)

    # 获取硬件的状态
    def harward_info(self, hostname, passwd):
        now_time = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
        command = "ipmitool raw 0x36 0x05 0xa2 0x63 0x00 0x0a"
        info = self.excute_command_ssh(hostname, passwd, command)
        info_len = len(info.strip().split(' '))
        mach_info = info.strip().split(' ')
        sql = "select id from  machine_info where ip = '%s'" % hostname
        machine_id = self.query_db(sql).fetchone()[0]
        # 追加填空
        if info_len > 16:
            mach_info = mach_info[0:16]
        for i in range(0, 16 - info_len):
            mach_info.append('Null')
        mach_info.append(self.now_time)
        mach_info.append(machine_id)
        sql1 = str(mach_info).replace('[', '').replace(']', '')
        sql = "insert into server_health_info(D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,D11,D12,D13,D14,D15,D16,cjsj,serverid) values(%s)" % sql1
        print(sql)
        self.insert_to_db(sql)
        print("更新服务器硬件信息成功")

    def abc(self):
        sql = "select ip,passwd from machine_info where  mfrs='H3C' "
        print(sql)
        results = self.query_db(sql).fetchall()
        for i in results:
            print('当前服务器地址：', i[0])
            self.harward_info(i[0], i[1])
            self.power_info(i[0], i[1])
            print("\n")


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    impi = Ipmi_tool()
    impi.abc()
    end_time = datetime.datetime.now()
    cost_time = end_time - start_time
    print("本次查询时长：", str(cost_time) + '秒\n')

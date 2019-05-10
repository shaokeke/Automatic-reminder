#!/usr/bin/python
# -*- coding: UTF-8 -*-
import psutil, time
import datetime
# from wechatpy import WeChatClient


class Monitor():
	cpu_data = []

	@classmethod
	def mem(cls, max=90):
		val = psutil.virtual_memory().percent
		if val > max:
			cls.send_msg('内存使用率为{:.1f}%，超过了{}%，请关注'.format(val, max))

	@classmethod
	def disk(cls, max=90):
		disk_part = psutil.disk_partitions() # 磁盘分区信息
		val = psutil.disk_usage('/').percent
		if val > max:
			cls.send_msg('磁盘使用率为{:.1f}%，超过了{}%，请关注'.format(val, max))

	@classmethod
	def cpu(cls, max=90):
		val = psutil.cpu_percent(1)
		cls.cpu_data.append(val)
		if len(cls.cpu_data) >= 3:
			avg = sum(cls.cpu_data) / len(cls.cpu_data)
			if avg > max:
				cls.send_msg('CPU使用率为{:.1f}%，超过了{}%，请关注'.format(avg, max))
				cls.cpu_data.pop(0)

	@classmethod
	def send_msg(cls, content):
		cls.mail(content)
		# cls.wechat(content)

	@classmethod
	def mail(cls, content):
		import smtplib
		from email.mime.text import MIMEText
		from email.utils import formataddr

		nickname = '监控程序'
		# 发送者的信息
		sender = 'XXXX@163.com'
		password = 'xxxx'
		# 接收方的邮箱
		receiver = '499646194@qq.com'
		msg = MIMEText(content, 'html', 'utf-8')
		msg['From'] = formataddr([nickname, sender])
		msg['Subject'] = '自动报警'
		server = smtplib.SMTP_SSL('smtp.163.com', 465)

		try:
			server.login(sender, password)
			server.sendmail(sender, [receiver], msg.as_string())
		except Exception as ex:
			print(ex)
		finally:
			server.quit()

	@classmethod
	def wechat(cls, content):
		client = WeChatClient('xxxx', 'xxxx')
		template_id = 'xxxxx'
		openid = 'xxxx'
		data = {
		'msg': {"value": content, "color": "#173177"},
		'time': {"value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "color": "#173177"},
		}

		try:
			client.message.send_template(openid, template_id, data)
		except Exception as ex:
			print(ex)

while True:
 Monitor.mem(40)
 Monitor.disk(30)
 Monitor.cpu(90)
 time.sleep(20)

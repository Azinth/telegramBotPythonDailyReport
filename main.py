import telebot
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

bot = telebot.TeleBot("paste your token here")
messages = []

@bot.message_handler(commands=['report'])
def send_daily_report(message):
	if not messages:
		bot.reply_to(message, "No messages found.")
	else:
		report = "Relatório Diário - {}\n\n".format(datetime.now().strftime("%d/%m/%Y"))
		for msg in messages:
			enum = messages.index(msg) + 1
			report += "{} - {}\n".format(enum, msg['text'])
		bot.reply_to(message, report)

@bot.message_handler(commands=['reset'])
def reset_messages(message):
	messages.clear()
	bot.reply_to(message, "All messages deleted.")

@bot.message_handler(commands=['send_email'])
def send_email(message):
	if not messages:
		bot.reply_to(message, "No messages found.")
	else:
		report = "Relatório Compra e Frota - {}\n\n".format(datetime.now().strftime("%d/%m/%Y"))
	for msg in messages:
		enum = messages.index(msg) + 1
		report += "{} - {}\n".format(enum, msg['text'])
	try:
		from_address = "paste you e-mail here"
		from_password = "paste your password here"
		to_address = "paste the e-mail you want to send the report to here"
		msg = MIMEText(report)
		msg['From'] = from_address
		msg['To'] = to_address
		msg['Subject'] = "subject"
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.login(from_address, from_password)
		server.sendmail(from_address, to_address, msg.as_string())
		server.quit()
		bot.reply_to(message, "Report sent successfully.")
	except Exception as e:
		bot.reply_to(message, "Error sending email: {}".format(e))

@bot.message_handler(func=lambda message: True)
def store_messages(message):
	messages.append({"text": message.text})
	bot.reply_to(message, "Message registered.")

bot.polling()

#encoding:utf-8

import serial
import time
import smtplib
import email

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders

USUARIO_GMAIL = 'manalfman@gmail.com'
CONTRASENA_GMAIL = '1123581321Se'

DESTINATARIO = 'zacariasaguasdelpozo@yahoo.es'
REMITENTE = 'manalfman@gmail.com'

ASUNTO = 'Alarma de su coche'
MENSAJE = '¡Su sistema de seguridad instalado en su coche ha detectado un posible intruso. Pinche aqui para conectar en directo con la camara:  http://192.168.1.9:8080/stream.html '

def enviar_correo():
	print("Enviando e-mail")
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.login(USUARIO_GMAIL, CONTRASENA_GMAIL)
	header = 'To:   ' + DESTINATARIO + '\n'
	header += 'From:  ' + REMITENTE + '\n'
	header += 'Subject:  ' + ASUNTO + '\n'
	print header
	msg = MIMEMultipart()
	msg.attach(header + MENSAJE)
	##msg = header + '\n' + MENSAJE + '\n\n'
	##adjuntamos archivo adjunto
	fp = open('/tmp/stream/' 'pic.jpg', 'rb')
	msg2 = MIMEBase('multipart', 'encrypted')
	msg2.set_payload(fp.read())
	fp.close()
	encoders.encode_base64(msg2)
	msg2.add_header('Content-Disposition', 'attachment', filename='pic.jpg')
	msg.attach(msg2)
	smtpserver.sendmail(REMITENTE,DESTINATARIO, msg.as_string())
	smtpserver.close()

enviar_correo()

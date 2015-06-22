#encoding:utf-8

import serial
import time
import smtplib

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
	msg = header + '\n' + MENSAJE + '\n\n'
	smtpserver.sendmail(REMITENTE,DESTINATARIO, msg)
	smtpserver.close()

enviar_correo()

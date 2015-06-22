#encoding: utf-8
import smtplib
import mimetypes

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64

REMITENTE = "manalfman@gmail.com"
PASS = "1123581321Se"
DESTINATARIO = "zacariasaguasdelpozo@yahoo.es"
ASUNTO = "Alarma de su coche"

msg = MIMEMultipart()
msg['From']=REMITENTE
msg['To']=DESTINATARIO
msg['Subject']=ASUNTO

body = "¡El sistema de seguridad instalado en su coche ha detectado un posible instruso. Pinche aqui para conectar en directo con la camara: http://192.168.1.9:8080/stream.html"
msg.attach(MIMEText(body))

file = open("/tmp/stream/pic.jpg","rb")
#file = open("/home/pi/Desktop/detect.jpg","rb")

attach_image = MIMEImage(file.read())
attach_image.add_header('Content-Disposition','attachment; filename = "foto.jpg"')
msg.attach(attach_image)

mailServer = smtplib.SMTP('smtp.gmail.com', 587)
mailServer.ehlo()
mailServer.starttls()
mailServer.ehlo()
mailServer.login(REMITENTE,PASS)
print "Enviando e-mail..."
mailServer.sendmail(REMITENTE, DESTINATARIO, msg.as_string())
print "e-mail enviado OK"
mailServer.close()

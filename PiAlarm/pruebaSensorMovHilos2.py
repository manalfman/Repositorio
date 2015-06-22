import RPi.GPIO as GPIO
import time
import picamera
import os
import threading 

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO_TRIGGER = 10
GPIO_ECHO = 12

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

def lanzarGrabacion():
	os.system("raspistill --nopreview -w 640 -h 480 -q 15 -o /tmp/stream/pic.jpg -tl 10 -t 100000 -th 0:0:0 &" )
def lanzarMjpg():
	os.system("./activamjpg.sh")	
def enviarEmail():
	os.system("python pruebaCorreo3.py")
def crearDirectorio():
	os.system("mkdir /tmp/stream")
def reconocimientoFacial():
	os.system("python pruebaFaceDetection.py")

try:
	crearDirectorio()
	while True:
		print "+++Sensor de movimiento activado+++"
		GPIO.output(GPIO_TRIGGER,False)
		time.sleep(0.5)

		GPIO.output(GPIO_TRIGGER,True)
		time.sleep(0.00001)
		GPIO.output(GPIO_TRIGGER,False)
		start = time.time()
		while GPIO.input(GPIO_ECHO)==0:
			start = time.time()
			print "+++Todo OK+++"
		while GPIO.input(GPIO_ECHO)==1:
			stop = time.time()
			
		elapsed = stop - start
		distance = (elapsed*34300)/2

		print "Distancia obstaculo: %0.2f cm" %(distance)
		if(distance<30):
			print "++++ALERTA. POSIBLE INTRUSO DETECTADO++++"
			print "Distancia: %0.2f cm " %(distance)
			#print distance
			##os.system("python pruebaCorreo3.py")
			break
		time.sleep(1)

	with picamera.PiCamera() as picam:
		print "Grabando video del sospechoso...."
		graba = threading.Thread(target=lanzarGrabacion)
		graba.start()
	
		reconocimiento = threading.Thread(target=reconocimientoFacial)
		reconocimiento.start()

		mjpg = threading.Thread(target=lanzarMjpg)
		mjpg.start()

		email = threading.Thread(target=enviarEmail)
		email.start()

		##picam.resolution = (640, 480)
		##picam.start_recording('video.h264')
		##picam.wait_recording(10)
		##picam.stop_recording()
	print "Proceso finalizado"

	

except KeyboardInterrupt:
	print "quit"
	GPIO.cleanup()
	

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

hilo_terminado = False
hilo_terminado2 = False

def lanzarGrabacion():
	global hilo_terminado
	os.system("raspistill --nopreview -w 640 -h 480 -q 15 -o /tmp/stream/pic.jpg -tl 10 -t 100000 -th 0:0:0 &" )
	hilo_terminado = True

def lanzarMjpg():
	global hilo_terminado2
	os.system("./activamjpg.sh")
	hilo_terminado2 = True
	
def enviarEmail():
	os.system("python pruebaCorreo3.py")

def lanzarReconocimiento():
	os.system("python pruebaFaceDetection.py")

def crearDirectorio():
	os.system("mkdir /tmp/stream")

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
		while(not hilo_terminado):	
			graba = threading.Thread(target=lanzarGrabacion)
			graba.start()		
			if(hilo_terminado):
				email = threading.Thread(target=enviarEmail)
				email.start()
				mjpg = threading.Thread(target=lanzarMjpg)
				mjpg.start()	
				while(not hilo_terminado2):
					reconocimiento = threading.Thread(target=lanzarReconocimiento)
					reconocimiento.start()

		##picam.resolution = (640, 480)
		##picam.start_recording('video.h264')
		##picam.wait_recording(10)
		##picam.stop_recording()
	print "Proceso finalizado"

	

except KeyboardInterrupt:
	print "quit"
	GPIO.cleanup()
	

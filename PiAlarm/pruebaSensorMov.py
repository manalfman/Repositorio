import RPi.GPIO as GPIO
import time
import picamera
import os
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO_TRIGGER = 10
GPIO_ECHO = 12

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

try:
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

		print distance
		if(distance<30):
			print "++++ALERTA. POSIBLE INTRUSO DETECTADO++++"
			print "Distancia: "
			print distance
			os.system("python pruebaCorreo3.py")
			break
		time.sleep(1)

	with picamera.PiCamera() as picam:
		print "Grabando video del sospechoso...."
		os.system("raspistill --nopreview -w 640 -h 480 -q 15 -o /tmp/stream/pic%04d.jpg -tl 10 -t 10000 -th 0:0:0 &" )
		##picam.resolution = (640, 480)
		##picam.start_recording('videoLadron.h264')
		##picam.wait_recording(10)
		##picam.stop_recording()
	print "Proceso finalizado"

except KeyboardInterrupt:
	print "quit"
	GPIO.cleanup()

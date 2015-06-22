import cv2
import picamera


def detect_faces(image):
	haar_faces = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
	detected = haar_faces.detectMultiScale(image, scaleFactor=1.3, minNeighbors=4,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
	return detected


image = cv2.imread('/tmp/stream/pic.jpg')
faces = detect_faces(image)
if len(faces) != 0:
	for(x,y,w,h) in faces:
		cv2.rectangle(image, (x,y), (x+w, y+h), 255)
	cv2.imwrite('/tmp/stream/pic.jpg', image)
	print 'Se ha detectado un rostro'
else:
	print ("No se ha detectado ningun rostro")

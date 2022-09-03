# carro-robot-con-opencv-y-mediapipe

1) code complete.
 ```python
 # container generic detect hands in the mediapipe
import time

import mediapipe as mp
import cv2
import serial

serial = serial.Serial('COM17',9600,timeout=1)
time.sleep(1)



# inicializamos la clase Hands y almacenarla en una variable
handsMp = mp.solutions.hands
# cargamos componente con las herramientas que nos permitira dibujar mas adelante
drawingMp = mp.solutions.drawing_utils
# cargamos los estilos en la variable mp_drawing_styles
mp_drawing_styles = mp.solutions.drawing_styles
# iniciamos una captura de video en la camara 1
cap = cv2.VideoCapture(1)
# save height and width image
height, width = [0, 0]

global saveSeparatorPoints

saveSeparatorPoints = False

arrayPoints = []


# ejecutamos del bloque de deteccion
def findCuadrantes(arrayPoints, point, eje):
    cuadrante = 0
    for i in range(0, len(arrayPoints)):
        if arrayPoints[i][eje] > point:
            if i > 0:
                if point > arrayPoints[(i - 1)][eje]:
                    cuadrante = i
                    break
            else:
                cuadrante = 0
                break

    if eje == 1:
        return int(cuadrante/3)
    else:
        return cuadrante

def sendBluetoothCar(character):
    serial.write(character.encode())

def arrDer():
    sendBluetoothCar('e')
    print("arriba derecha")
def arr():
    sendBluetoothCar("w")
    print("arriba")
def arrIzq():
    sendBluetoothCar('q')
    print("arriba izquierda")

def der():
    sendBluetoothCar('a')
    print("derecha")
def centro():
    sendBluetoothCar('s')
    print("centro")
def izq():
    sendBluetoothCar('d')
    print("izquierda")

def abaDer():
    sendBluetoothCar('z')
    print("abajo derecha")
def abajo():
    sendBluetoothCar('x')
    print("abajo")
def abaizq():
    sendBluetoothCar('c')
    print("abajo izquierda")

def error():
    print("error")

def findArrayPoints(image, arrayPoints, pointX, pointY):
    cuadranteX = findCuadrantes(arrayPoints, pointX, 0)
    cuadranteY = findCuadrantes(arrayPoints,pointY,1)
    return [cuadranteX, cuadranteY]


def drawSeparator(image, pointX, pointY):
    global saveSeparatorPoints
    separatorHeight = int(height / 3)
    separatorWidth = int(width / 3)

    for i in range(1, 3):
        # line horizontal
        cv2.line(image, (0, int(separatorHeight * i)), (width, int(separatorHeight * i)), (255, 0, 0), 2)
        # line vertical
        cv2.line(image, (int(separatorWidth * i), 0), (int(separatorWidth * i), height), (255, 0, 0), 2)

    if saveSeparatorPoints is False:
        for j in range(1, 4):
            for k in range(1, 4):
                arrayPoints.append([separatorWidth * k, separatorHeight * j])
        saveSeparatorPoints = True
        print(arrayPoints)
    radio = 0
    # print(arrayPoints)
    # print("---------------------------")
    if separatorWidth > separatorHeight:
        radio = separatorHeight
    else:
        radio = separatorWidth

    if saveSeparatorPoints is True:
        cuadrantes = findArrayPoints(image, arrayPoints, pointX, pointY)

        if cuadrantes == [0,0]:
            arrDer()
        elif cuadrantes == [1,0]:
            arr()
        elif cuadrantes == [2,0]:
            arrIzq()

        elif cuadrantes == [0,1]:
            der()
        elif cuadrantes == [1,1]:
            centro()
        elif cuadrantes == [2,1]:
            izq()

        elif cuadrantes == [0,2]:
            abaDer()
        elif cuadrantes == [1,2]:
            abajo()
        elif cuadrantes == [2,2]:
            abaizq()


def joystick(image, hand_landmarks):
    # getPosition point 9
    pointX = int(hand_landmarks.landmark[handsMp.HandLandmark.MIDDLE_FINGER_MCP].x * width)
    pointY = int(hand_landmarks.landmark[handsMp.HandLandmark.MIDDLE_FINGER_MCP].y * height)
    drawSeparator(image, pointX, pointY)


with handsMp.Hands(static_image_mode=False,
                   max_num_hands=1,
                   min_detection_confidence=0.5,
                   min_tracking_confidence=0.5) as hands:
    # mientras la camara este en ejecucion
    while cap.isOpened():
        # guardamos en la variable succes el estado de la captura y en image la captura
        success, image = cap.read()
        if not success:
            print("camara vacia")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        # get shape image
        if height == 0:
            # return height, width and channels
            height, width, _ = image.shape
            print(width, height)

        # convertimos la imagen de bgr a rgb debido a que la funcion hands process acepta rgb
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Procesa una imagen RGB y devuelve los puntos de referencia de la mano y la destreza de cada mano detectada
        results = hands.process(image)
        # convertimos la imagen rgb a bgr
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # si obtenemos puntos de referencia multiples
        if results.multi_hand_landmarks is not None:
            # recorremos esos puntos multiples de referencia
            for hand_landmarks in results.multi_hand_landmarks:
                # dibujamos los puntos de referencia (imagen,puntos referencia de la mano,describe las conexiones
                # de los puntos de referencia,
                drawingMp.draw_landmarks(
                    image,
                    hand_landmarks,
                    handsMp.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                # *************************************
                joystick(image, hand_landmarks)
                # *************************************
        # Voltee la imagen horizontalmente para obtener una vista de selfie.
        cv2.imshow('MediaPipeJHR', cv2.flip(image, 1))
        # en caso de teclear la letra q suspendemos la operacion
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
# Cierra el archivo de video o el dispositivo de captura.
cap.release()
serial.close()

```

2) en videos anteriores explicamos el codigo ejemplo o base, por ende partiremos desde la creación de la clase joystick(image,hand_landmarks), cuyos atributos son image y hand_landmarks en donde image sera la imagen que usaremos para dibujar todo lo que realizaremos de aqui en adelante, hand_landmarks(puntos de referencia de la mano) son los puntos de referencia que tendremos en cuenta mas adelante.

```python
joystick(image, hand_landmarks)
```

3) en este proyecto utilizare el punto de referencia que aparacen en la sigiente imagen.
![hands](https://user-images.githubusercontent.com/66834393/188290312-ec85a116-0a5a-45ea-9b2f-d21461026e40.png)
para ello el paso a seguir es capturar la posicion de este punto en X y Y.

```python
# getPosition point 9
    pointX = int(hand_landmarks.landmark[handsMp.HandLandmark.MIDDLE_FINGER_MCP].x * width)
    pointY = int(hand_landmarks.landmark[handsMp.HandLandmark.MIDDLE_FINGER_MCP].y * height)
```

4) una vez ya tenemos los puntos de referencia que usaremos, crearemos una nueva función que nos permitira inicialmente separar en divisiones iguales la pantalla
 ```python
 drawSeparator(image, pointX, pointY)
 ```
 esta función nos acepta como parametros la imagen y los puntos de referencia tanto en X como en Y de la mano.
 ```python
 global saveSeparatorPoints
    separatorHeight = int(height / 3)
    separatorWidth = int(width / 3)
 ```
 en este caso decidi tomar 3 divisiones de ancho y 3 divisiones de alto, para un total de 9 puntos o cuadrantes, como se ve en la imagen.
 
 
 

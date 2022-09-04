# carro-robot-con-opencv-y-mediapipe

1) codigo completo al final de las instrucciones.
 

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
 
![image](https://user-images.githubusercontent.com/66834393/188290766-fafdaa46-30bd-4014-b920-af0e2a8ebf5e.png)
 
para dibujarlas hago uso de un for que me permite recorrer la pantalla y dibujar estas lineas separadoras.

 ```python
     for i in range(1, 3):
        # line horizontal
        cv2.line(image, (0, int(separatorHeight * i)), (width, int(separatorHeight * i)), (255, 0, 0), 2)
        # line vertical
        cv2.line(image, (int(separatorWidth * i), 0), (int(separatorWidth * i), height), (255, 0, 0), 2)
  ```
  
  la funcion cv2.line me toma como parametros, la imagen, la coordenada de inicio y la coordenada final adicionalmente el color de la linea, ya que en este caso escogi azul esta acepta bgr, por ende el (255,0,0), por ultimo el ancho de la linea en este caso 2.
![image](https://user-images.githubusercontent.com/66834393/188292718-e3804fb1-afaf-4dc2-ad06-3d044473690e.png)

5) en cuanto los puntos esten trazados en nuestra pantalla procedemos a guardar un array de valores en donde se encontraran los puntos de nuestro cuadrantes y los guardamos en la variable arrayPoints
asi se almacenan en nuestro array los puntos que separan nuestro cuadrantes.
![image](https://user-images.githubusercontent.com/66834393/188292783-88694577-63d3-414c-ba53-9d83d5aa80a0.png)
para este ejemplo el tamaño de pantalla es de 640,480

a continuación el codigo que almacena estas coordenadas en mi array, antes de proceder puse una variable booleana saveSeparatorPoints con el fin de no guardar cada vez que pase por esta seccion las coordenadas de estos puntos sino que solo una unica vez, reduciendo tiempo en procesamiento de información.

 ```python
    if saveSeparatorPoints is False:
        for j in range(1, 4):
            for k in range(1, 4):
                arrayPoints.append([separatorWidth * k, separatorHeight * j])
        saveSeparatorPoints = True
        print(arrayPoints)
  ```
  
  6) luego, el siguiente proceso es capturar el cuadrante en donde se detecto la mano, o el punto que en este proyecto se definio con el siguiente llamado a la funcion findArrayPoints, que retorna el cuadrante en donde se detecto la mano en las coordenadas especificas, para ello le enviamos como atributo, el arrayPoints y los puntos que anteriormente capturamos de la mano en especifico, pointX, pointY.
 
 cabe resaltar que primero pregunto si el array fue cargado con la informacion para proceder como se ve a continuación.
  
  ```python
     if saveSeparatorPoints is True:
        cuadrantes = findArrayPoints(arrayPoints, pointX, pointY)
   ```
 
 7) la funcion findArrayPoints depende de otra función para completar su tarea, por ende hace uso de findCuadrantes que le permite conocer el cuadrante especificamente de cada elemento, es decir de la posición de la mano en X y Y, como se muestra en las siguientes lineas de codigo.
 
  ```python
def findArrayPoints(arrayPoints, pointX, pointY):
    cuadranteX = findCuadrantes(arrayPoints, pointX, 0)
    cuadranteY = findCuadrantes(arrayPoints,pointY,1)
    return [cuadranteX, cuadranteY]
   ```
8) metodo findCuadrantes, nos pide como parametros arrayPoints y la posicion si es en X o Y de la cual quieres conocer el cuadrante, por ende en el anterior codigo enviamos primero pointX y luego pointY, para especificar el eje decimos que si es 0, entonces es por que deseamos conocer la ubicación del ejeX de lo contrario si enviamos un 1 es por que deseamos la ubicacion en el cuadrante de pointY.

```python

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

 ```
 ----------codigo completo---------------------
 
 tal cual como vemos en el codigo, este nos retorna en que cuadrante esta la posición que deseamos, haciendo un recorrido en donde se busca inicialmente encontrar que el valor del punto sea inferior al del cuadrante, si es asi, entonces se le pide al cuadrante anterior que revise si el punto es mayor que es, si esto se cumple es por que esta en medio de los dos puntos, con ello sabremos entonces el cuadrante en donde se encuentra el punto, en el caso del eje y que mencionamos anteriormente que se enviaba a la función un 1 es por que en la busqueda del array nos retornada valores como [0,3,6] y no valores como [0,1,2] que nos definan el cuadrante, por ende una solución sencilla fue dividirlo entre 3 y ya normalizamos los valores a un rango entre [0 y 2].
 
9)volviendo al paso 7 vemos que una vez tenemos los cuadrantes este nos retornara un arreglo como el siguiente [0,1] en donde se especifica realmente el cuadran en el que esta la mano detectada.

10) una vez tenemos los cuadrantes no queda mas que saber que direccion le asignaremos a cada cuadrante, para ello las siguientes condiciones.

```python
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
```
11) cada una de estas condiciones llama a una funcion definida.
```python
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
 ```
 12) cada función ademas de ello, envia un caracter correspondiente a Arduino llamando a la siguiente función.

 ```python
 def sendBluetoothCar(character):
    serial.write(character.encode())
 ```
 este se codifica y se envia a arduino.
 
 
 con ello damos por terminado este proyecto de aqui en adelante solo es implementar el codigo arduino que pegare en esta seccion y buscar mas opciones de uso, si te gusto suscribete, y gracias por el tiempo que te tomes en leer esto, gracias.
 
 https://www.youtube.com/c/INGENIER%C3%8DAJHR
 
 
CODIGO ARDUINO.

```C++
#include<Servo.h>
Servo Serv;
char rxDato;

String conChar,Grados;

int velocidad=200,gServo;
int diferencia=50;

#define PwmI 8
#define PwmD 9
#define LlantaIT 10
#define LlantaID 11
#define LlantaDT 12
#define LlantaDD 13

void setup() {
Serial3.begin(9600);
pinMode(LlantaIT,OUTPUT);
pinMode(LlantaID,OUTPUT);
pinMode(LlantaDT,OUTPUT);
pinMode(LlantaDD,OUTPUT);
Serv.attach(3);
Serv.write(90);

}

void loop() {
  if(Serial3.available()>0){
    rxDato=Serial3.read();
    //Serial3.print(rxDato);
    if(rxDato=='v'){
      delay(10);
      while(Serial3.available()){
        rxDato=Serial3.read();
        conChar=conChar+rxDato;
      }
      velocidad=conChar.toInt();//0,100,130,240
      velocidad=map(velocidad,0,100,100,255);
      //Serial3.println(conChar);
      conChar="";//v200
    }
    if(rxDato=='g'){        
      rxDato=Serial3.read();
      delay(10);
      while(Serial3.available()){
        rxDato=Serial3.read();
        Grados=Grados+rxDato;
      }
      gServo=Grados.toInt();
      Serv.write(gServo);
      Grados="";
    }
  }
  //HACIA ADELANTA
  if(rxDato=='w'){
   digitalWrite(LlantaIT,LOW);
   digitalWrite(LlantaDT,LOW);
   digitalWrite(LlantaID,HIGH);
   digitalWrite(LlantaDD,HIGH);
   analogWrite(PwmI,velocidad);
   analogWrite(PwmD,velocidad);
  }
  //HACIA ATRAS
  if(rxDato=='x'){
   digitalWrite(LlantaIT,HIGH);
   digitalWrite(LlantaDT,HIGH);
   digitalWrite(LlantaID,LOW);
   digitalWrite(LlantaDD,LOW);
   analogWrite(PwmI,velocidad);
   analogWrite(PwmD,velocidad);
  }
  //HACIA LA DERECHA
  if(rxDato=='a'){
   digitalWrite(LlantaIT,HIGH);
   digitalWrite(LlantaDT,LOW);
   digitalWrite(LlantaID,LOW);
   digitalWrite(LlantaDD,HIGH);
   analogWrite(PwmI,velocidad);
   analogWrite(PwmD,velocidad); 
  }

  //HACIA LA IZQUIERDA
  if(rxDato=='d'){
   digitalWrite(LlantaIT,LOW);
   digitalWrite(LlantaDT,HIGH);
   digitalWrite(LlantaID,HIGH);
   digitalWrite(LlantaDD,LOW);
   analogWrite(PwmI,velocidad);
   analogWrite(PwmD,velocidad);
  }
  //DETIENE
  if(rxDato=='s'){
   digitalWrite(LlantaIT,LOW);
   digitalWrite(LlantaDT,LOW);
   digitalWrite(LlantaID,LOW);
   digitalWrite(LlantaDD,LOW);
   analogWrite(PwmI,0);
   analogWrite(PwmD,0);
  }
  //HACIA LA DERECHA ARRIBA
   if(rxDato=='e'){
   digitalWrite(LlantaIT,LOW);
   digitalWrite(LlantaDT,LOW);
   digitalWrite(LlantaID,HIGH);
   digitalWrite(LlantaDD,HIGH);
   analogWrite(PwmI,velocidad-diferencia);
   analogWrite(PwmD,velocidad);
  }
  //HACIA LA IZQUIERDA ADELANTE
  if(rxDato=='q'){
   digitalWrite(LlantaIT,LOW);
   digitalWrite(LlantaDT,LOW);
   digitalWrite(LlantaID,HIGH);
   digitalWrite(LlantaDD,HIGH);
   analogWrite(PwmI,velocidad);
   analogWrite(PwmD,velocidad-diferencia);
  }
  //HACIA LA IZQUIERDA ATRAS
  if(rxDato=='z'){
   digitalWrite(LlantaIT,HIGH);
   digitalWrite(LlantaDT,HIGH);
   digitalWrite(LlantaID,LOW);
   digitalWrite(LlantaDD,LOW);
   analogWrite(PwmI,velocidad);
   analogWrite(PwmD,velocidad-diferencia);
  }
  //HACIA LA DERECHA ATRAS
  if(rxDato=='c'){
   digitalWrite(LlantaIT,HIGH);
   digitalWrite(LlantaDT,HIGH);
   digitalWrite(LlantaID,LOW);
   digitalWrite(LlantaDD,LOW);
   analogWrite(PwmI,velocidad-diferencia);
   analogWrite(PwmD,velocidad);
  }
}

```
 

```python
 # container generic detect hands in the mediapipe
import time

import mediapipe as mp
import cv2
import serial

serial = serial.Serial('COM17',9600)
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

 

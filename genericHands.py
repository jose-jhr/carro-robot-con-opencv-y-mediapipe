#container generic detect hands in the mediapipe
import mediapipe as mp
import cv2

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
            print(height, width)

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
                #*************************************

                #*************************************
        # Voltee la imagen horizontalmente para obtener una vista de selfie.
        cv2.imshow('MediaPipeJHR', cv2.flip(image, 1))
        # en caso de teclear la letra q suspendemos la operacion
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
# Cierra el archivo de video o el dispositivo de captura.
cap.release()
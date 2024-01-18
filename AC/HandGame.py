import cv2
import mediapipe as mp

# Configuración de Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Configuración de la cámara
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Configuración del modelo de manos de Mediapipe
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:

    while True:
        # Captura de un fotograma desde la cámara
        ret, frame = cap.read()

        # Verifica si la captura fue exitosa
        if ret == False:
            break

        # Ajusta la orientación del fotograma
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesa la imagen para detectar manos
        results = hands.process(frame_rgb)

        # Dibuja los landmarks si se detectan manos
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=3, circle_radius=5),
                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=4, circle_radius=5))

        # Muestra el fotograma con landmarks
        cv2.imshow('Frame', frame)

        # Sale del bucle si se presiona la tecla Esc
        if cv2.waitKey(1) & 0xFF == 27:
            break

# Libera los recursos y cierra las ventanas
cap.release()
cv2.destroyAllWindows()

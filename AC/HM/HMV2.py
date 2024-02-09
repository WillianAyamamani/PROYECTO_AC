
import cv2
import numpy as np
import SMV2 as sm
import autopy
import time

def main():
    anchocam, altocam = 640, 480
    cuadro = 100
    anchopanta, altopanta = autopy.screen.size()
    sua = 5
    pubix, pubiy = 0,0
    cubix, cubiy = 0,0
    ultimo_clic = time.time()

    cap = cv2.VideoCapture(0)
    cap.set(3,anchocam)
    cap.set(4,altocam)

    detector = sm.detectormanos(maxManos=1)

    while True:
        ret, frame = cap.read()
        frame = detector.encontrarmanos(frame)
        lista, bbox = detector.encontrarposicion(frame)

        if len(lista) != 0:
            x1, y1 = lista[8][1:]
            x2, y2 = lista[12][1:]

            dedos = detector.dedosarriba()
            cv2.rectangle(frame, (cuadro, cuadro), (anchocam - cuadro, altocam - cuadro), (0, 0, 0), 2)

            if dedos[1] == 1 and dedos[2] == 0:
                x3 = np.interp(x1, (cuadro, anchocam - cuadro), (0, anchopanta))
                y3 = np.interp(y1, (cuadro, altocam - cuadro), (0, altopanta))

                cubix = pubix + (x3 - pubix) / sua
                cubiy = pubiy + (y3 - pubiy) / sua

                autopy.mouse.move(anchopanta - cubix, cubiy)
                pubix, pubiy = cubix, cubiy

            if dedos[1] == 1 and dedos[2] == 1:
                longitud, frame, linea = detector.distancia(8, 12, frame)
                if longitud < 30:
                    cv2.circle(frame, (linea[4], linea[5]), 10, (0, 255, 0), cv2.FILLED)
                    tiempo_actual = time.time()
                    if tiempo_actual - ultimo_clic >= 0.5:
                        autopy.mouse.click()
                        ultimo_clic = tiempo_actual

        cv2.imshow("Mouse", frame)
        k = cv2.waitKey(1)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


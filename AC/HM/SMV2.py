import math
import cv2
import mediapipe as mp
import time

class detectormanos():
    def __init__(self, node=False, maxManos = 2, Confdeteccion = 1, Confsequi = 0.5):
        self.mode = node
        self.maxManos = maxManos
        self.Confdeteccion = Confdeteccion
        self.Confsequi = Confsequi

        self.mpmanos = mp.solutions.hands
        self.manos = self.mpmanos.Hands(self.mode, self.maxManos, self.Confdeteccion, self.Confsequi)
        self.dibujo = mp.solutions.drawing_utils
        self.tip = [4,8,12,16,20]

    def encontrarmanos (self, frame, dibujar = True):
        imgcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultados = self.manos.process(imgcolor)

        if self.resultados.multi_hand_landmarks:
            for mano in self.resultados.multi_hand_landmarks:
                if dibujar:
                    self.dibujo.draw_landmarks(frame, mano, self.mpmanos.HAND_CONNECTIONS)
        return frame
    def encontrarposicion(self, frame, ManoNum = 0, dibujar = True):
        xlist = []
        ylist = []
        bbox = []
        self.list = []
        if self.resultados.multi_hand_landmarks:
            miMano = self.resultados.multi_hand_landmarks[ManoNum]
            for id, lm in enumerate(miMano.landmark):
                alto, ancho, c  = frame.shape
                cx, cy = int(lm.x*ancho), int(lm.y * alto)
                xlist.append(cx)
                ylist.append(cy)
                self.list.append([id,cx,cy])
                if dibujar:
                    cv2.circle(frame, (cx,cy), 5, (0,0,0), cv2.FILLED)

            xmin, xmax = min(xlist), max(xlist)
            ymin, ymax = min(ylist), max(ylist)
            bbox = xmin, ymin, xmax, xmax
            if dibujar:
                cv2.rectangle(frame,(xmin - 20,ymin - 20), (xmax + 20, ymax + 20), (0,255,0), 2)
        return self.list, bbox
    def dedosarriba (self):
        dedos = []
        if self.list[self.tip[0]][1] > self.list[self.tip[0]-1][1]:
            dedos.append(1)
        else:
            dedos.append(0)

        for id in range (1,5):
            if self.list[self.tip[id]][2] < self.list[self.tip[id]-2][2]:
                dedos.append(1)
            else:
                dedos.append(0)

        return dedos
    
    def distancia(self, p1, p2, frame, dibujar = True, r = 15, t = 3):
        x1, y1 = self.list[p1][1:]
        x2, y2 = self.list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if dibujar:
            cv2.line(frame, (x1, y1), (x2, y2), (0,0,255), t)
            cv2.circle(frame, (x1, y1), r, (0,0,255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), r, (0,0,255), cv2.FILLED)
            cv2.circle(frame, (cx, cy), r, (0,0,255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, frame, [x1,y1,x2,y2,cx,cy]

    def main():
        ptiempo = 0
        ctiempo = 0

        cap = cv2.VideoCapture(0)

        detector = detectormanos()

        while True:
            ret, frame = cap.read()
            frame = detector.encontrarmanos(frame)
            list, bbox = detector.encontrarposicion(frame)
            if len(list) != 0:
                print (list[4])
            ctiempo = time.time()
            fps = 1 / (ctiempo - ptiempo)
            ptiempo = ctiempo

            cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            cv2.imshow("Manos", frame)
            k = cv2.waitkey(1)

            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()


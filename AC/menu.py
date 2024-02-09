from sopa import main as sopa
import os
import platform
import pygame as game
import subprocess
import sys

game.init()

Screen_Width = 1000
Screen_Eigth = 500

screen = game.display.set_mode((Screen_Width, Screen_Eigth))
game.display.set_caption("MENU MESSI")

font = game.font.SysFont("arialblack", 18)
color = (246, 239, 232)
background_image = game.image.load(r"C:\Users\ADDUSER\Pictures\WPP\LINUXC_wallpaper.jpg").convert()

# Ruta completa a HMV2.py
HMV2_path = r"C:\Users\ADDUSER\Downloads\PROYECTO_AC\AC\HM\HMV2.py"
# Rutas completas a los otros archivos
ProjectAC_path = r"C:\Users\ADDUSER\Downloads\PROYECTO_AC\AC\ProjectAC.py"
Test_path = r"C:\Users\ADDUSER\Downloads\PROYECTO_AC\AC\Test.py"

# Función para iniciar HMV2.py como un subproceso
def start_HMV2():
    subprocess.Popen([sys.executable, HMV2_path])

def draw_T(text, font, color, x, y):
    img = font.render(text, True, color)
    text_rect = img.get_rect(center=(x, y))
    screen.blit(img, text_rect)
    return text_rect

def UpText(mouse, text):
    return text.collidepoint(mouse)

print("KDA")

# Inicia HMV2.py como un subproceso
start_HMV2()

run = True
while run:
    screen.blit(background_image, (0, 0))

    option1 = draw_T("VIRTUAL ASISTENT", font, color, Screen_Width // 2, Screen_Eigth // 2 + 50)
    option2 = draw_T("GAMES", font, color, Screen_Width // 2, Screen_Eigth // 2)
    option3 = draw_T("TEST", font, color, Screen_Width // 2, Screen_Eigth // 2 - 50)

    mouseP = game.mouse.get_pos()

    for event in game.event.get():
        if event.type == game.QUIT:
            run = False
        elif event.type == game.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (UpText(mouseP,option1)):
                    print("1")
                    if platform.system() == 'Linux':
                        os.system("python ./ProjectAC.py")
                    elif platform.system() == 'Windows':
                        os.system("python .\ProjectAC.py")
                    else:
                        print("Sistema operativo no compatible")
                if (UpText(mouseP,option2)):
                    print("2") 
                    sopa()                   
                if (UpText(mouseP,option3)): 
                    print("3")
                    if platform.system() == 'Linux':
                        os.system("python ./Test.py")
                    elif platform.system() == 'Windows':
                        os.system("python .\Test.py")
                    else:
                        print("Sistema operativo no compatible")

    game.display.update()

game.quit()


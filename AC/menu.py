import pygame as game
import os
import platform
import sys
from sopa import main as sopa

game.init()

Screen_Width = 1000
Screen_Eigth = 500

screen = game.display.set_mode((Screen_Width,Screen_Eigth))
game.display.set_caption("MENU MESSI")
#--------------------FONT'S DEFINITION------------------
font = game.font.SysFont("arialblack", 18)
#--------------------COLOR DEFINITION------------------
color = (246, 239, 232)

def ProcessPy(archivo):
    #copia
    activate_command = ".\\HM\\ENV\\Scripts\\activate"
    script_command = ["python", archivo]
    combined_command = f"{activate_command} & {' '.join(script_command)}"
    subprocess.run(combined_command, shell=True)
    #fin

def draw_T (text, font, color, x, y):
    img = font.render(text, True, color)
    text_rect = img.get_rect(center=(x, y))
    screen.blit(img, (x,y))
    return text_rect

def UpText (mouse, text):
    return text.collidepoint(mouse)

run = True
while run:
    screen.fill((17, 21, 13))


    option1 = draw_T("VIRTUAL ASISTENT", font,color, Screen_Width//2, Screen_Eigth//2+50)
    option2 = draw_T("GAMES", font,color, Screen_Width//2, Screen_Eigth//2)
    option3 = draw_T("TEST", font,color, Screen_Width//2, Screen_Eigth//2-50)

    mouseP = game.mouse.get_pos()



    for event  in game.event.get():
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
                    if platform.system() == 'Linux':
                        os.system("python ./HM/HMV2.py")
                    elif platform.system() == 'Windows':
                        os.system("python .\HM\HMV2.py")
                    else:
                        print("Sistema operativo no compatible")
                if (UpText(mouseP,option3)): 
                    print("3")
                    sopa()

    game.display.update()
game.quit()


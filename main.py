import pygame
import random
import io
import math
from pygame import mixer

# Inicializar Pygame
pygame.init()

#music settings
mixer.music.load('backGroundMusic.wav')
mixer.music.set_volume(0.4)
mixer.music.play(-1)

# Configurar la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mi Juego")

#Title Icon
pygame.display.set_caption("METEOR SHOWER")
icono = pygame.image.load("nave.png")
pygame.display.set_icon(icono)
background = pygame.image.load("fondo2.jpg")
#Convert font to bytes
def font_bytes(fontbt):

    with open(fontbt,'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)

font_as_bytes = font_bytes("Monster-Bites.ttf")
font = pygame.font.Font(font_as_bytes,64)

#points
points = 0
font_as_bytes = font_bytes("Monster-Bites.ttf")
font = pygame.font.Font(font_as_bytes,32)
font_gameover = pygame.font.Font(font_as_bytes,62)
text_x = 10
text_y = 10
startGame_text = pygame.font.Font(font_as_bytes,80)
endGame_text = pygame.font.Font(font_as_bytes,80)
instructions_text = pygame.font.Font(font_as_bytes,15)
press_spacebar_text = pygame.font.Font(font_as_bytes,40)

# Definir colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Cargar imagen de nave, del disparo y del enemigo
nave_img = pygame.image.load("nave.png")
bullet_img = pygame.image.load("bullet.png")



# Definir la posición inicial de nave
nave_x = screen_width // 2
nave_y = screen_height - 100

# Definir la posición y velocidad inicial del disparo
bullet_x = -100
bullet_y = -100
bullet_speed = 2

# Definir el estado del disparo (disparando o no)
bullet_state = "ready"

# Definir la posición del enemigo
enemy_img = []
enemy_x = []
enemy_y = []
enemysQuantity = 10

for e in range (enemysQuantity):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(-500, 100))
    enemy_width = enemy_img[e].get_rect().size
    enemy_height = enemy_img[e].get_rect().size

#menu boolean
main_menu = True

# Definir velocidad de movimiento del auto
nave_speed = 0.8

# Definir la lista de enemigos
enemies = []

#check collision bullet/enemy
def isCollision (x_1, y_1 ,x_2 ,y_2):
    distance = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distance < 30:
        return True
    else:
        return False
#show points function
def show_points(x,y):
    text = font.render(f"Points: {points}",True,(255,255,255))
    screen.blit(text,(x,y))


# Definir la función para mover nave, el disparo y el enemigo
def move_objects(keys_pressed):
    global nave_x, nave_y, bullet_x, bullet_y, bullet_state, enemy_x, enemy_y,points
    if keys_pressed[pygame.K_LEFT]:
        nave_x -= nave_speed
    elif keys_pressed[pygame.K_RIGHT]:
        nave_x += nave_speed
    if nave_x < 0:
        nave_x = 0
    elif nave_x > screen_width - nave_img.get_width():
        nave_x = screen_width - nave_img.get_width()

    if keys_pressed[pygame.K_UP]:
        nave_y -= nave_speed
    elif keys_pressed[pygame.K_DOWN]:
        nave_y += nave_speed
    if nave_y < 0:
        nave_y = 0
    elif nave_y > screen_height - nave_img.get_height():
        nave_y = screen_height - nave_img.get_height()

    if keys_pressed[pygame.K_SPACE] and bullet_state == "ready":
        bullet_x = nave_x + nave_img.get_width() // 2 - bullet_img.get_width() // 2
        bullet_y = nave_y
        bullet_state = "fire"

    if bullet_state == "fire":
        bullet_y -= bullet_speed
        if bullet_y < 0:
            bullet_state = "ready"

    for e in range(enemysQuantity):
        # Mover el enemigo
        if enemy_y[e] < screen_height:
            enemy_y[e] += 0.5

        else:
            enemy_y[e] = 1
            enemy_x[e] = random.randint(0,  screen_width - enemy_img[e].get_width())

         # Collision
    for e in range(enemysQuantity):
        collision = isCollision(enemy_x[e], enemy_y[e], bullet_x, bullet_y)
        if collision:
            bullet_hit = mixer.Sound('golpe.mp3')
            bullet_hit.play()
            bullet_y = 500
            bullet_state = "ready"
            points += 10
            enemy_x[e] = random.randint(0, 736)
            enemy_y[e] = random.randint(50, 200)

#start menu
def start_game():
    showStartGameText = startGame_text.render("METEOR SHOWER!",True,(white))
    showInstructionsText = instructions_text.render("Shoot to the asteroids with spacebar or avoid them before they crush you!", True, (white))
    showPressSpacebarText = press_spacebar_text.render("Press Spacebar to Start!", True, (white))
    screen.blit(showStartGameText,(80,200))
    screen.blit(showInstructionsText, (100, 300))
    screen.blit(showPressSpacebarText, (150, 330))


# Definir la función para dibujar el auto, el disparo y el enemigo
def draw_objects():
    global bullet_state
    screen.blit(nave_img, (nave_x, nave_y))
    if bullet_state == "fire":
        screen.blit(bullet_img, (bullet_x, bullet_y))


    # change enemy ubication
    for e in range(enemysQuantity):
        screen.blit(enemy_img[e], (enemy_x[e], enemy_y[e]))


    # Detectar colisiones entre el auto y el enemigo
    for e in range(enemysQuantity):
        nave_rect = pygame.Rect(nave_x, nave_y, nave_img.get_width(), nave_img.get_height())
        enemy_rect = pygame.Rect(enemy_x[e], enemy_y[e], enemy_img[e].get_width(), enemy_img[e].get_height())
        if nave_rect.colliderect(enemy_rect):
            font
            text = font_gameover.render("Game Over!", True, red)
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text, text_rect)
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            quit()



# Bucle principal del juego
running = True
while running:

    #show main menu screen
    if main_menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_menu = False

        screen.blit(background, (0, 0))
        start_game()
        draw_objects()
        pygame.display.update()

    else:

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obtener teclas presionadas
        keys_pressed = pygame.key.get_pressed()

        # Mover el auto, el disparo y el enemigo
        move_objects(keys_pressed)

        # Dibujar el auto, el disparo y el enemigo
        screen.blit(background,(0,0))
        draw_objects()
        show_points(text_x, text_y)

        # Actualizar la pantalla
        pygame.display.update()

# Salir del juego
pygame.quit()
quit()


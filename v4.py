import pygame 
from pygame import *


#initialize pygame
pygame.init()

#Game window 
WIDTH = 500
HEIGHT = 600 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Soccer Pong')
clock = pygame.time.Clock()

#colors 
grass_green = (40, 135, 58)
white = (255, 255, 255)

#create field background 
background = pygame.Surface((WIDTH, HEIGHT))
background.fill(grass_green)

#Field Markings 
centre_circle_radius = 70 
pygame.draw.circle(background, white, (WIDTH//2, HEIGHT//2), centre_circle_radius, 2)
pygame.draw.circle(background, white, (WIDTH//2, HEIGHT//2), 5)
pygame.draw.line(background, white, (0, HEIGHT//2), (WIDTH, HEIGHT//2), 2)
pygame.draw.rect(background, white, (WIDTH//2 - 110, 0, 220,60), 2)

#Goal net 
GOAL_WIDTH = 250 
GOAL_HEIGHT = 40 
net_color = (200, 200, 200, 150)
net_surface = pygame.Surface((GOAL_WIDTH, GOAL_HEIGHT), pygame.SRCALPHA)
for i in range(0, GOAL_WIDTH, 15):
    pygame.draw.line(net_surface, net_color, (i,0), (i, GOAL_HEIGHT), 1)
for i in range(0, GOAL_HEIGHT, 15):
    pygame.draw.line(net_surface, net_color, (0,i), (GOAL_HEIGHT, i), 1)
    
goal_rect = net_surface.get_rect(center=(WIDTH//2, 20))

#paddle x'tics 
keeper_width = 100 
keeper_height = 15 
player_width = 80 
player_height = 15 
paddle_speed = 8 

#Place the paddles  
keeper_pos = [WIDTH//2 -keeper_width // 2, 60] 
player_pos = [WIDTH//2 - player_width//2, HEIGHT - player_height - 10]

def draw_paddle(pos, width, height):
    pygame.draw.rect(screen, white, (pos[0], pos[1], width, height))

#Game Loop 
run = True     
while run: 
    for e in pygame.event.get():
        if e.type == QUIT:
            run = False 
        
        
    screen.blit(background, (0,0))
    screen.blit(net_surface, goal_rect)
    draw_paddle(keeper_pos, keeper_width, keeper_height)
    draw_paddle(player_pos, player_width, player_height)
    
    pygame.display.update()
    clock.tick(60)
        
pygame.quit()
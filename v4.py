import pygame 
from pygame import *

#initialize pygame
pygame.init()

#scoring init 
player_score = 0
keeper_score = 0 
wining_score = 10 
game_over = False 
font = pygame.font.Font(None, 36)

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

def reset_ball():
    return [WIDTH//2, HEIGHT//2], [5, 5 if pygame.time.get_ticks() % 2 == 0 else -5]

#Add the ball and ball movement 
ball_pos = [WIDTH // 2, HEIGHT//2]
ball_radius = 10 
ball_speed = [5, 5]

def draw_ball(pos):
    pygame.draw.circle(screen, white, (int(pos[0]), int(pos[1])), ball_radius)

# keeper AI 
keeper_direction = 1 

def show_game_over(winner):
    screen.blit(background, (0,0))
    text = font.render(f"{winner} Wins! Press R to restart", True , white)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    waiting = True     
    while waiting: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False 
            if event.type == KEYDOWN:
                if event.key == K_r:
                    return True
            clock.tick(60)
    
#Game Loop 
run = True     
while run: 
    for e in pygame.event.get():
        if e.type == QUIT:
            run = False 
    #Player controls 
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= paddle_speed 
    if keys[K_RIGHT] and player_pos[0] < WIDTH - player_width:
        player_pos[0] += paddle_speed
        
    # keeper 
    keeper_pos[0] += paddle_speed * 0.7 * keeper_direction
    if keeper_pos[0] <= 0 or keeper_pos[0] >= WIDTH - keeper_width:
        keeper_direction *= -1 
    
    #ball movement 
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]
    
    #collision with our walls 
    if ball_pos[0] <= ball_radius or ball_pos[0] >= WIDTH - ball_radius:
        ball_speed[0] *= -1
    
    #collision with our paddles 
    if (keeper_pos[0] < ball_pos[0] < keeper_pos[0] + keeper_width and keeper_pos[1] < ball_pos[1] < keeper_pos[1] + keeper_height):
        ball_speed[1] = abs(ball_speed[1])
        ball_speed[0] += (ball_pos[0] - (keeper_pos[0] + keeper_width/2)) / 20
        
    if (player_pos[0] < ball_pos[0] < player_pos[0] + player_width and player_pos[1] < ball_pos[1] < player_pos[1] + player_height):
        ball_speed[1] = -abs(ball_speed[1])
        ball_speed[0] += (ball_pos[0] - (player_pos[0] + player_width/2)) / 20
   
    #Goal logic 
    if ball_pos[1] <= ball_radius:
        if goal_rect.left < ball_pos[0] < goal_rect.right:
            player_score += 1 
            ball_pos, ball_speed = reset_ball()
        else: 
            ball_speed[1] *= -1 
    elif ball_pos[1] >= HEIGHT - ball_radius:
        keeper_score += 1
        ball_pos, ball_speed = reset_ball()
           
    #displaying score 
    player_text = font.render(f"Player: {player_score}", True, white)
    keeper_text = font.render(f"Keeper: {keeper_score}", True, white)
    
    if player_score >= wining_score or keeper_score >= wining_score:
        winner = "Player" if player_score >= wining_score else "Keeper"
        game_over = True
        
    if game_over:
        run = show_game_over(winner)
        if run:
            player_score = 0
            keeper_score = 0 
            ball_pos, ball_speed = reset_ball()
            game_over = False 
        
    screen.blit(background, (0,0))
    screen.blit(net_surface, goal_rect)
    screen.blit(player_text, (20, HEIGHT - 50))
    screen.blit(keeper_text, (20, 20))
   

    draw_paddle(keeper_pos, keeper_width, keeper_height)
    draw_paddle(player_pos, player_width, player_height)
    draw_ball(ball_pos)

    pygame.display.update()
    clock.tick(60)
        
pygame.quit()
import pygame
import sys
import random
import pickle
import os

pygame.init()
os.chdir(r'C:BLOCK_DASH')
class Player:
    
    def __init__(self, color, width):
        self.color = color
        self.size = 50
        self.y = 700
        self.x = width/2-self.size/2
        self.speed = 12       
    # user input to see if we should go left or right
    # make sure we don't go out of the window
    def animation(self, width):
        keys = pygame.key.get_pressed()
        self.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed

        if self.x <= 0:
            self.x = 0
        if self.x >= width-self.size:
            self.x = width-self.size
    # draws player on the screen
    def draw(self, screen):
        self.rect = pygame.Rect(self.x,self.y,self.size,self.size)     
        pygame.draw.rect(screen, self.color, (self.rect))

class Obstacles(pygame.sprite.Sprite):

    def __init__(self, color, width, score):
        self.color = color
        self.size = 50
        self.x = random.randint(0, width - self.size)
        self.y = 0
        self.pos = (self.x, self.y)
        self.speed = score/10+ 5
    # draws obstacles on screen
    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

        
# General Setup
clock = pygame.time.Clock()
    
# window Setup
width = 1000
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Block Dash')

# Color Variables
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0 ,255)
white = (255, 255, 255)
green = (0,255,0)

# Images
restart_img = pygame.image.load('restart.png')
play_button_img = pygame.image.load('play.png')
leaders_button_img = pygame.image.load('leaders.png')
home_img = pygame.image.load('home.png')
block_dash_img = pygame.image.load('block_dash.png')
music_on_img = pygame.image.load('music.png')
music_off_img = pygame.image.load('music_off.png')
play_button_img = pygame.transform.scale(play_button_img, (300,100))
leaders_button_img = pygame.transform.scale(leaders_button_img, (440,100))
home_img = pygame.transform.scale(home_img, (100,100))
restart_img = pygame.transform.scale(restart_img, (300,200))
block_dash_img = pygame.transform.scale(block_dash_img, (1000,330))
music_on_img = pygame.transform.scale(music_on_img, (75,75))
music_off_img = pygame.transform.scale(music_off_img, (75,75))


# Fonts
mono_font = pygame.font.SysFont("monospace", 35)
calibri_font = pygame.font.SysFont('calibri', 100)
leaderborad_calibri = pygame.font.SysFont('calibri', 75)

# Object player
player = Player(green, width)

# list of obstacles
obstacle_list = []

# list of highscores
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
music = True

# score variable
score = 0

main_menu = True
restart = False
leaders = False
running = False

# drops obstacles for player to dodge
def drop_obstacles(obstacle_list, score, difficulty, num_obstacles):
    delay = random.random()
    if len(obstacle_list) < num_obstacles and delay < difficulty:
        new_obstacle = Obstacles(blue, width, score)
        obstacle_list.append(new_obstacle)                
    for new in obstacle_list:
        new.draw(screen)
    for idx, new in enumerate(obstacle_list):
        if new.y >= 0 and new.y <= height:
            new.y += new.speed
        else:
            obstacle_list.pop(idx)
            score += 1

    return score

# check if their is a collision between the player and an obstacle
def collision_check(obstacle_list, running, restart):
    for new in obstacle_list:
        if new.rect.colliderect(player.rect):
            running = False
            restart = True
    return running, restart

# shows user how many obstacles they've dodged
def keeping_score(score, mono_font, white):
    score_text = "Score:" + str(score)
    score_label = mono_font.render(score_text, 1, white)
    screen.blit(score_label, (20, 750))
    

# Progressivley makes game harder
def increase_difficulty(score):
    difficulty = score/1000 + .05
    if difficulty > .5:
        difficulty = .5
    num_obstacle = 10
    num_obstacle += score/10
    return difficulty, num_obstacle



def game_over(screen, score, calibri, white,width, restart_img, home_img, height, block_dash_img, leaderboard):
    score_text = "Score: " + str(score)  
    score_label = calibri.render(score_text, 1, white)
    score_rect = score_label.get_rect(center = (width/2, 600))
    screen.blit(score_label, (score_rect))

    high_score_text = "Highscore: " + str(leaderboard[0])
    high_score_label = calibri.render(high_score_text, 1, white)
    high_score_rect = high_score_label.get_rect(center = (width/2, 450))
    screen.blit(high_score_label,(high_score_rect))

    restart_rect = restart_img.get_rect(center = (width/2, (score_rect.bottom + height)/2))
    screen.blit(restart_img,(restart_rect))

    home_rect = home_img.get_rect(bottomleft = (0, height))
    screen.blit(home_img,(home_rect))

    block_dash_rect = block_dash_img.get_rect(topleft = (0, 25))
    screen.blit(block_dash_img,(block_dash_rect))
    return restart_rect, home_rect

def main_menu_visuals(play_button_img, screen, width, height, leader_button_img, block_dash_img, music_on_img, music_off_img):
    play_button_rect = play_button_img.get_rect(center = (width/2, 475))
    screen.blit(play_button_img, (play_button_rect))

    leader_button_rect = leader_button_img.get_rect(center = (width/2, 585))
    screen.blit(leaders_button_img, (leader_button_rect))

    block_dash_rect = block_dash_img.get_rect(topleft = (0, 25))
    screen.blit(block_dash_img,(block_dash_rect))

    music_on_rect = music_on_img.get_rect(bottomleft = (0, height))

    music_off_rect = music_off_img.get_rect(bottomleft = (0, height))

    return play_button_rect, leader_button_rect, music_off_rect, music_on_rect
    
def leaderboard_organize(leaderboard, score):
    while len(leaderboard) < 10:
        leaderboard.append(0)
    leaderboard.append(score)
    leaderboard.sort(reverse = True)
    while len(leaderboard) > 10:
        leaderboard.pop()
    with open ('leaderboard.pkl', 'wb') as f:
        pickle.dump(leaderboard, f)
def leaderboard_screen(calibri, screen, width, home_img):
    with open('leaderboard.pkl', 'rb') as f:
        leaderboard_list = pickle.load(f)
    for idx, i in enumerate(leaderboard_list):
        text = str(idx+1) + '.' + "    " + str(i)
        label = calibri.render(text, 1, white)
        rect = label.get_rect(center = (width/2, idx * 75 + 50))
        screen.blit(label, (rect))
    
    home_rect = home_img.get_rect(bottomleft = (0, height))
    screen.blit(home_img,(home_rect))
    return home_rect



with open('leaderboard.pkl', 'rb') as f:
        leaderboard = pickle.load(f)

while True:
    while leaders:

        home_rect = leaderboard_screen(leaderborad_calibri, screen, width, home_img)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_rect.x < mouse_x < home_rect.x + home_rect.w and home_rect.y < mouse_y < home_rect.y + home_rect.h:
                    leaders = False
                    main_menu = True

        
        
        pygame.display.update()
        clock.tick(20)
        screen.fill(black)
    while running:

        # exit game if click top right corner
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        difficulty, num_obstacles = increase_difficulty(score)
        player.animation(width)
        player.draw(screen)
        score = drop_obstacles(obstacle_list, score, difficulty, num_obstacles)
        running, restart = collision_check(obstacle_list, running, restart)
        keeping_score(score, mono_font, white)
        
        # updating window
        pygame.display.update()
        clock.tick(20)
        screen.fill(black)
    leaderboard_organize(leaderboard, score)

    while main_menu:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        play_button_rect, leader_button_rect, music_off_rect, music_on_rect = main_menu_visuals(play_button_img, screen, width, height, leaders_button_img, block_dash_img, music_on_img, music_off_img)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.x < mouse_x < play_button_rect.x + play_button_rect.w and play_button_rect.y < mouse_y < play_button_rect.y + play_button_rect.h:
                    running = True
                    main_menu = False
                    score = 0
                    obstacle_list = []
                if leader_button_rect.x < mouse_x < leader_button_rect.x + leader_button_rect.w and leader_button_rect.y < mouse_y < leader_button_rect.y + leader_button_rect.h:
                    leaders = True
                    main_menu = False

                if music_on_rect.x < mouse_x < music_on_rect.x + music_on_rect.w and music_on_rect.y < mouse_y < music_on_rect.y + music_on_rect.h:
                    if music == True:
                        music = False
                    else:
                        music = True
                

        if music == True:
            screen.blit(music_on_img,(music_on_rect))
            pygame.mixer.music.unpause()
        if music == False:
            screen.blit(music_off_img,(music_off_rect))
            pygame.mixer.music.pause()

        

        
        
        pygame.display.update()
        clock.tick(10)
        screen.fill(black)
        
    # game menu after collision
    while restart:
        # mouse x and y
        mouse_x, mouse_y = pygame.mouse.get_pos()


        restart_rect, home_rect = game_over(screen, score, calibri_font, white, width, restart_img, home_img, height, block_dash_img, leaderboard)

        # exit game if click top right corner
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.x < mouse_x < restart_rect.x + restart_rect.w and restart_rect.y < mouse_y < restart_rect.y + restart_rect.h:
                    running = True
                    restart = False
                    score = 0
                    obstacle_list = []
                if home_rect.x < mouse_x < home_rect.x + home_rect.w and home_rect.y < mouse_y < home_rect.y + home_rect.h:
                    main_menu = True
                    restart = False
                    score = 0
                    obstacle_list = []

        # updating window
        pygame.display.update()
        clock.tick(20)
        screen.fill(black)

    # runs game loop until collision is detected




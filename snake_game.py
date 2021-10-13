import pygame
from pygame.locals import *
import time
import random


SIZE = 40
WHITE = (255,255,255)
BACKGROUND_COLOR = (110,100,5)
BACKGROUND_IMAGE = 'resources/background.jpg'
INITIAL_STARTING_SPEED =.2 #this is the starting speed of the snake



class Apple:

     # Size of apple must be a multiple of 4

    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.apple_block = pygame.image.load('resources/apple.jpg').convert()
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw_apple(self):
        self.parent_screen.blit(self.apple_block,(self.x,self.y))
        pygame.display.flip()

    def move_apple(self):
        self.x =random.randint(0,24) * SIZE # 25 is max
        self.y = random.randint(0,14) * SIZE # 15 is max







class Snake:

    ''' This class helps to create a snake object that moves about the screen '''

    def __init__(self, parent_screen,length):
        self.length = length
        self.direction = None
        self.parent_screen = parent_screen
        self.snake_block = pygame.image.load('resources/block.jpg').convert()
        self.x = [SIZE] * length   # Snakes initial x position multiply with length to increase snake size on eating apple
        self.y = [SIZE] * length   # Snakes initial x position

    def draw_snake(self):
        # self.parent_screen.fill(BACKGROUND_COLOR)
        #self.parent_screen.fill(BACKGROUND_COLOR)

        for i in range(self.length):
            self.parent_screen.blit(self.snake_block, (self.x[i], self.y[i]))
            pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def snake_walk(self):

        for  i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw_snake()

    def increase_length(self):
        self.length += 1 # Increase length of snake  on eating apple
        self.x.append(-1) # Increase length of snake by a block on eating apple
        self.y.append(-1) # Increase length of snake by a block on eating apple
        




class Game:
    '''This is the main class of my snake game using OOP'''


    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.game_size = (1000,600) # Set the window size width and height as 500px
        self.surface = pygame.display.set_mode((self.game_size))
        self.render_background()
        #self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface,1)
        self.snake.draw_snake()
        self.apple = Apple(self.surface)
        self.apple.draw_apple()
        self.play_background_music('resources/bg_music_1.mp3')

    def is_collision(self,x1,y1,x2,y2):
        if (x1 >= x2) and (x1 < x2 + SIZE):
            if (y1 >= y2) and (y1 < y2 + SIZE):
                return True
        return False

    def has_hit_wall(self,x1,y1,x2,y2):
        if (x1 < 0) or (x1 > x2) or y1>y2 or y1 < 0:
            return True
        return False

    def play_background_music(self,file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

    def play_sound(self,file):
        ''' play sound file passed into game'''
        sound = pygame.mixer.Sound(file)
        pygame.mixer.Sound.play(sound)



    def play_game(self):
        '''Play game by drawing apple and snake'''
        self.render_background()
        self.snake.snake_walk()
        self.apple.draw_apple()
        self.display_score()

        #  Snake colliding or eating apple
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            # play a ding sound when the snake eats the apple
            self.play_sound(file='resources/ding.mp3')
            self.snake.increase_length() # increase snake length when it eats the apple
            self.apple.move_apple()

        # Check if snake eats itself or collide with itself
        for j in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[j],self.snake.y[j]):
                self.play_sound(file='resources/crash.mp3') # play crash sound when snake collides with itself
                game_over = "Game Over"
                raise game_over

        # check if snake hit the wall and exit game

        if self.has_hit_wall(self.snake.x[0],self.snake.y[0],self.game_size[0],self.game_size[1]):
            self.play_sound(file='resources/crash.mp3')
            game_over = "Game Over"
            raise game_over


    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('Poppins', 30)
        game_over_message = font.render(f"Game Over, Your score is: {self.snake.length}", True, WHITE)
        self.surface.blit(game_over_message,(280,280))
        game_over_message = font.render(f"To play game again press enter key. To stop playing press Escape", True, WHITE)
        self.surface.blit(game_over_message, (160, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()


    def display_score(self):
        font = pygame.font.SysFont('Poppins',30)
        score = font.render(f"Score: { self.snake.length}",True,WHITE)
        self.surface.blit(score,(900,10))
        pygame.display.flip()

    def render_background(self):
        # This is the background image
        background = pygame.image.load(BACKGROUND_IMAGE)
        self.surface.blit(background,(0,0))

    def increase_speed(self):
        # Increase the speed of the snake as the length increases
        if self.snake.length <= 10:
            time.sleep(INITIAL_STARTING_SPEED-0.1)
        elif self.snake.length <= 18:
            time.sleep(INITIAL_STARTING_SPEED-0.1)
        elif self.snake.length > 18:
            time.sleep(INITIAL_STARTING_SPEED-0.2)



    def reset(self):
        # Reset the game to initial values once the player loses
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)


    def run_snake_game(self):
        running = True # keep on playing game until it is false
        pause = False # pause the game if the player fails
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    # Pause the game if the player presses enter
                    if event.key == K_RETURN:
                        if pause == True:
                            pygame.mixer.music.unpause()
                            pause = False
                        else:
                            pause = True
                            pygame.mixer.music.pause()


                    if event.key == K_ESCAPE:
                        exit(0)
                    if not pause:
                        # don't process keys if game is paused
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play_game()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            self.increase_speed()


if __name__ == '__main__':
    game= Game()
    game.run_snake_game()




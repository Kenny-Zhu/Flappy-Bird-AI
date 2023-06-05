import pygame
import random
import neat
import os
clock = pygame.time.Clock()
# Initialising the modules in pygame
pygame.init()

SCREEN = pygame.display.set_mode((500, 750))  # Setting the display

# background
FLOOR = pygame.transform.scale(pygame.image.load('assets/base.png'), (500, 250))
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load('assets/background-day.png'), (500, 750))

# PIPE

#  BIRD
BIRD_IMAGE = pygame.image.load('bird1.png')
bird_x = 50
bird_y = 300
bird_y_change = 0
base = 0 

class Bird:
    """
    Bird class representing the flappy bird
    """
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        """
        Initialize the object
        :param x: starting x pos (int)
        :param y: starting y pos (int)
        :return: None
        """
        self.x = x
        self.y = y
        self.tilt = 0  # degrees to tilt
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img = BIRD_IMAGE

    def jump(self):
        """
        make the bird jump
        :return: None
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
        if self.y >= 635:
            self.y == 635

    def move(self):
        """
        make the bird move
        :return: None
        """
        self.tick_count += 1

        # for downward acceleration
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  # calculate displacement

        # terminal velocity
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement
    
        
    def display_bird(self):
        if self.y >= 575:
            self.y = 575
        if self.y <= 0:
            self.y = 0 
        SCREEN.blit(BIRD_IMAGE, (self.x, self.y))

    def get_mask(self):
        """
        gets the mask for the current image of the bird
        :return: None
        """
        
        return pygame.mask.from_surface(self.img)

class Pipe():
    """
    represents a pipe object
    """
    GAP = 200
    
    VEL = 5

    def __init__(self, x):
        """
        initialize pipe object
        :param x: int
        :param y: int
        :return" None
        """
        PipeImg = pygame.image.load('assets/pipe-green.png')
        FlippedPipe = pygame.transform.flip(PipeImg, False, True)
        FPX = pygame.transform.scale(FlippedPipe, (52, 1000))
        self.x = x
        self.height = 0

        # where the top and bottom of the pipe is
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = FlippedPipe
        self.PIPE_BOTTOM = PipeImg
        #pygame.transform.flip(PipeImg, False, True)
        self.passed = False

        self.set_height()

    def set_height(self):
        """
        set the height of the pipe, from the top of the screen
        :return: None
        """
        self.height = random.randrange(120, 300)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
        move pipe based on vel
        :return: None
        """

        self.x -= self.VEL

    def draw(self, win):
        """
        draw both the top and bottom of the pipe
        :param win: pygame window/surface
        :return: None
        """
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird, win):
        """
        returns if a point is colliding with the pipe
        :param bird: Bird object
        :return: Bool
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False

def moving_floor():
    SCREEN.blit(BACKGROUND_IMAGE, (base, 0))
    SCREEN.blit(BACKGROUND_IMAGE, (base + 500, 0))
    SCREEN.blit(FLOOR, (0, 635))
# OBSTACLES
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = random.randint(-100,0)
OBSTACLE_COLOR = (211, 253, 117)
OBSTACE_X_CHANGE = -4
obstacle_x = 500
obstacle_gap = 150


#move_pipes


pipe_heights = [-100, -50, 0] 
random_pipe_height = random.choice(pipe_heights)
#gap between flippedpipe and pipeimg for y value must be 500
#def display_obstacle(height, xpos):  
   # SCREEN.blit(FlippedPipe, (xpos, height))
    #bottom_obstacle_height = height + 500
    #SCREEN.blit(PipeImg, (xpos, bottom_obstacle_height))

    #pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, 0, OBSTACLE_WIDTH, height))
    #bottom_obstacle_height = 635 - height - obstacle_gap
    #pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, height+obstacle_gap, OBSTACLE_WIDTH, bottom_obstacle_height))

#COLLISION DETECTION
def collision_detection (obstacle_x, obstacle_height, bird_y, bottom_obstacle_height):
    if obstacle_x >= 50 and obstacle_x <= (50 + 64):
       if bird_y <= obstacle_height + 320 or bird_y >= (bottom_obstacle_height - 64):
           return True
    return False

# SCOREbottom_obstacle_height
score = 0
SCORE_FONT = pygame.font.Font('freesansbold.ttf', 32)

def score_display(score):
    display = SCORE_FONT.render(f"Score: {score}", True, (255,255,255))
    SCREEN.blit(display, (10, 10))

# START SCREEN
startFont = pygame.font.Font('freesansbold.ttf', 32)
def start():
    # displays: "press space bar to start)
    display = startFont.render(f"PRESS SPACE BAR TO START", True, (255, 255, 255))
    SCREEN.blit(display, (20, 200))
    pygame.display.update()

# GAME OVER SCREEN
# This list will hold all of the scores
score_list = [0]

game_over_font1 = pygame.font.Font('freesansbold.ttf', 64)
game_over_font2 = pygame.font.Font('freesansbold.ttf', 32)

def game_over():
    # check for the maximum score
    maximum = max(score_list)
    #  "game over"
    display1 = game_over_font1.render(f"GAME OVER", True, (200,35,35))
    SCREEN.blit(display1, (50, 300))
    # shows your current score and your max score
    display2 = game_over_font2.render(f"SCORE: {score} MAX SCORE: {maximum}", True, (255, 255, 255))
    SCREEN.blit(display2, (50, 400))
    #  If your new score is the same as the maximum then u reached a new high score
    if score == maximum:
        display3 = game_over_font2.render(f"NEW HIGH SCORE!!", True, (200,35,35))
        SCREEN.blit(display3, (80, 100))

def draw_window(win, birds, pipes):
    for pipe in pipes:
        pipe.draw(win)

    for bird in birds:
        bird.display_bird()

running = True
# waiting is going to refer to our end or start screen
waiting = True
# set collision to false in the beginning so that we only see the start screen in the beginning
collision = False
PL = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
def main(genomes, config):
    bird_y = 300
    birds = []
    nets = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)  
        birds.append(Bird(50, 350))
        ge.append(genome)
    running = True
    base = 0 
    waiting = True
    collision = False
    Switch = False
    bird_y_change = 0
    OBSTACLE_WIDTH = 70
    OBSTACLE_COLOR = (211, 253, 117)
    OBSTACLE_HEIGHT = random.randint(-100, 0)
    OBSTACE_X_CHANGE = -4
    obstacle_gap = 150
    obstacle_x = 500
    pipes = [Pipe(obstacle_x)]
    score = 0

    while running:
        
        SCREEN.fill((0, 0, 0))
        # display the background image
        base -= 1
        moving_floor()
        if base <= -500:
            base = 0 
        # we will be sent into this while loop at the beginning and ending of each game
        #while waiting:
            #if collision:
                # If collision is True (from the second time onwards) we will see both the end screen and the start screen
                #genome.fitness -= 1
               
                #start()
            #else:
                # This refers to the first time the player is starting the game
                #start()
            

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #  If we press the space bar we will exit out of the waiting while loop and start to play the game
                        # we will also reset some of the variables such as the score and the bird's Y position and the obstacle's starting position
                        score = 0
                         
                        
                        #  to exit out of the while loop
                        waiting = False

                if event.type == pygame.QUIT:
                    # in case we exit out make both running and waiting false
                    waiting = False
                    running = False
                    pygame.quit()
                    quit()
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If you press exit you exit out of the while loop and pygame quits
                running = False
                pygame.quit()
                quit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #  if you press spacebar you will move up
                    bird_y_change = -8
                    bird.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # when u release space bar you will move down automatically            
                    bird_y_change = 0
        
          # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
        pipe_ind = 0 
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
                pipe_ind = 1    
        for x, bird in enumerate(birds):
            bird.move() 

            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()
           
        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # check for collision
            for bird in birds:
                if pipe.collide(bird, SCREEN):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                    if len(birds) < 1:
                        return(genome.fitness)

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # can add this line to give more reward for passing through a pipe (not required)
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(500))

        for r in rem:
            pipes.remove(r)

        
        # moving the bird vertically
        bird_y += bird_y_change
        bird_y_change += .25
        
        # setting boundaries for the birds movement
        if bird_y <= 0:
            bird_y = 0
        if bird_y >= 571:
            bird_y = 571

        # Moving the obstacle
        obstacle_x += OBSTACE_X_CHANGE

        # COLLISION
       
       
        # generating new obstacles
        if obstacle_x <= -10:
            obstacle_x = 500
            pipe_heights = [-100, -50, 0]
            genome.fitness += 5
            if Switch == False:
                OBSTACLE_HEIGHT = random.choice(pipe_heights)
                Switch = True
            if Switch == True:
                OBSTACLE_HEIGHT = random.randint(-100,0)
                Switch = False
        # displaying the obstacle
        
       
        #display_obstacle(OBSTACLE_HEIGHT, obstacle_x)
       
        # displaying the bird
        
        #p = Bird(50, bird_y)
        #p.display_bird()
        #p.move()
        collision = collision_detection(obstacle_x, OBSTACLE_HEIGHT, bird_y, OBSTACLE_HEIGHT + 500)

        if collision:
            # if a collision does occur we are gonna add that score to our list of scores and make waiting True
            score_list.append(score)
            waiting = True

        #p = Pipe(obstacle_x)
        #p.draw(SCREEN)
        #p.move()

        draw_window(SCREEN, birds, pipes)
        # display the score
        score_display(score)
        clock.tick(60)
        # Update the display after each iteration of the while loop
        pygame.display.update()

# Quit the program
    pygame.quit()

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(main, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
    
    

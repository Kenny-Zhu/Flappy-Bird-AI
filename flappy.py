import pygame, sys, random, neat

pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()

#Game Variables
gravity = 0.25
bird_movement = 0
game_active = True

def draw_floor():
	screen.blit(floor_surface, (floor_x ,900))
	screen.blit(floor_surface, (floor_x + 576, 900))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	#get_rect gets a rectangle that covers the entire surface
	bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
	return bottom_pipe, top_pipe

def move_pipes(pipes):
 	for pipe in pipes:
 		pipe.centerx -= 5
 	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe, pipe)

def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			return False

	if bird_rect.top <= -100 or bird_rect.bottom >= 900:
		return False

	return True
def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
	return new_bird
bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())

floor_x = 0

bird_surface = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_rect = bird_surface.get_rect(center = (100, 512))
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0 

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)

pipe_list = []

#timer for pipes
SPAWNPIPE = pygame.USEREVENT
#pygame.time.set_timer sets off spawnpipe every 1200 milliseconds (1.2 seconds)
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 8

			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100,512)
				bird_movement = 0
		#when SPAWNPIPE is triggered, it extends the list to create a pipe
		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

	screen.blit(bg_surface, (0, 0))
	if game_active:
		# Bird

		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird, bird_rect)
		game_active = check_collision(pipe_list)
		# Pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)

	#Floor
	floor_x -= 1
	draw_floor()
	if floor_x <= -576:
		floor_x = 0

	pygame.display.update()
	clock.tick(60) 

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
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
 # Determine path to configuration file. This path manipulation is
 # here so that the script will run successfully regardless of the
    # current working directory.
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config-feedforward.txt')
	run(config_path)
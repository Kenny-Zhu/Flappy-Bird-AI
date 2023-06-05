import pygame, random

clock = pygame.time.Clock()

#initialize the game
pygame.init()

SCREEN = pygame.display.set_mode((500, 750)) #set the display

#Background
BACKGROUND_IMAGE = pygame.image.load('background.jpg')

BIRD_IMAGE = pygame.image.load('bird1.png')
bird_x = 50 
bird_y = 300
bird_y_change = 0
running = True
base = 0 
# OBSTACLES

OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = random.randint(150,450)
OBSTACLE_COLOR = (211, 253, 117)
OBSTACLE_X_CHANGE = -4
obstacle_x = 500
obstacle_gap = 150

def display_obstacle(height):
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, 0, OBSTACLE_WIDTH, height))
    bottom_obstacle_height = 635 - height - obstacle_gap
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, height+obstacle_gap, OBSTACLE_WIDTH, bottom_obstacle_height))


def display_bird(x,y):
	SCREEN.blit(BIRD_IMAGE, (x,y))
 
def collision_detection (obstacle_x, obstacle_height, bird_y, bottom_obstacle_height):
	if obstacle_x >= 50 and obstacle_x <= (50 + 64):
		if bird_y <= obstacle_height or bird_y >= (bottom_obstacle_height - 64):
			return True
	return False
score = 0
SCORE_FONT = pygame.font.Font('freesansbold.ttf', 32)

def score_display(score):
	display = SCORE_FONT.render(f"Score: {score}", True, (255,255,255))
	SCREEN.blit(display, (10,10))


while running:

	SCREEN.fill((0, 0, 0))


	#display background image
	SCREEN.blit(BACKGROUND_IMAGE, (0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			#if you press exit, it exits out of the while loop and pygame quits
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				bird_y_change = -4

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				bird_y_change = 3



	bird_y += bird_y_change

	if bird_y <= 0:
		bird_y = 0
	if bird_y >= 571:
		bird_y  = 571
 
	obstacle_x += OBSTACLE_X_CHANGE
	if obstacle_x <= -10:
		obstacle_x = 500
		OBSTACLE_HEIGHT = random.randint(200, 400)
		score += 1
	collision = collision_detection(obstacle_x, OBSTACLE_HEIGHT, bird_y, OBSTACLE_HEIGHT + 150)

	if collision:   
		pygame.quit() 

	display_obstacle(OBSTACLE_HEIGHT)

	display_bird(bird_x, bird_y)
	score_display(score)
	clock.tick(30)
	# Updates the display after each iteration of while loop
	pygame.display.update()

pygame.quit()
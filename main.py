import pygame
import sys
import asyncio 

# Initialize Pygame
pygame.init()
pygame.font.init()

# Setup Screen and Clock
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Strawberry Collector")
clock = pygame.time.Clock()

# Fonts and Colors
font = pygame.font.SysFont(None, 36)
BG_COLOR = (20, 24, 40)
WHITE = (255, 255, 255)
PLATFORM_COLOR = (100, 180, 100)

# Function to load standard image files safely
def load_game_image(filename, size):
    try:
        image = pygame.image.load(filename).convert_alpha()
        return pygame.transform.scale(image, size), True
    except Exception as e:
        print(f"Error loading image '{filename}': {e}")
        return None, False

# Load Sprites from files (Make sure these files are in your project folder!)
player_image, has_player_image = load_game_image("strawberry_shortcake.png", (50, 50))
strawberry_image, has_strawberry_image = load_game_image("strawberry.png", (30, 30))

# Game Variables
player_x = 50
player_y = 300
player_dx = 0
player_dy = 0
gravity = 0.5
jump_speed = -10
on_ground = False

score = 0

# Platforms
platforms = [
    pygame.Rect(0, 350, 600, 50),   # Floor
    pygame.Rect(100, 270, 150, 20),
    pygame.Rect(350, 220, 150, 20),
    pygame.Rect(200, 140, 150, 20)
]

# Strawberries (Collectibles)
strawberries = [
    pygame.Rect(150, 230, 30, 30),
    pygame.Rect(400, 180, 30, 30),
    pygame.Rect(520, 310, 30, 30),
    pygame.Rect(260, 100, 30, 30)
]

# 2. Wrap the game loop inside an async function
async def main():
    global player_x, player_y, player_dx, player_dy, on_ground, score
    
    running = True

    while running:
        # 1. EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. KEYBOARD INPUT
        keys = pygame.key.get_pressed()
        
        player_dx = 0
        if keys[pygame.K_LEFT]:
            player_dx = -5
        if keys[pygame.K_RIGHT]:
            player_dx = 5
            
        # Jumping
        if keys[pygame.K_UP] and on_ground:
            player_dy = jump_speed
            on_ground = False

        # 3. UPDATE PHYSICS & POSITION
        player_x += player_dx
        if player_x < 0:
            player_x = 0
        elif player_x > WIDTH - 50:
            player_x = WIDTH - 50

        player_dy += gravity
        player_y += player_dy

        player_rect = pygame.Rect(player_x, player_y, 50, 50)

        # Platform Collision Detection
        on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_dy > 0 and player_rect.bottom - player_dy <= platform.top + 10:
                    player_y = platform.top - 50
                    player_dy = 0
                    on_ground = True

        # Strawberry Collision Detection
        for strawberry in strawberries[:]:
            if player_rect.colliderect(strawberry):
                strawberries.remove(strawberry)
                score += 1

        # 4. RENDER GRAPHICS
        screen.fill(BG_COLOR)

        # Draw Platforms
        for platform in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)

        # Draw Strawberries
        for strawberry in strawberries:
            if has_strawberry_image:
                screen.blit(strawberry_image, (strawberry.x, strawberry.y))
            else:
                pygame.draw.circle(screen, (255, 0, 0), (strawberry.x + 15, strawberry.y + 15), 15)

        # Draw Player (Strawberry Shortcake)
        if has_player_image:
            screen.blit(player_image, (player_x, player_y))
        else:
            pygame.draw.rect(screen, (255, 105, 180), player_rect)

        # Draw Score Display
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        pygame.display.flip()
        clock.tick(60)
        
        # 3. VERY IMPORTANT: Yield control back to the browser/async loop
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

# 4. Run the async main function using asyncio.run()
asyncio.run(main())

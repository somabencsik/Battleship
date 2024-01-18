import pygame

from ships.ship import Ship

pygame.font.init()

WIDTH, HEIGHT = 900, 900
COLS, ROWS = 9, 9
BLOCK_SIZE = 50
RUNNING = False
SHIPS = []
ACTIVE_SHIP = None
TOP_BLOCKS: list[tuple[float, float]] = []
BOTTOM_BLOCKS: list[tuple[float, float]] = []
OUTLINE_SHIP = None


def render(window: pygame.Surface) -> None:
    window.fill((127, 127, 127))

    draw_table(window)
    write_text(window)
    for ship in SHIPS:
        ship.render(window)

    if OUTLINE_SHIP is not None:
        pygame.draw.rect(window, (0, 255, 0), OUTLINE_SHIP, 1)

    pygame.display.flip()


def draw_table(window: pygame.Surface) -> None:
    # Draw upper table
    for col in range(COLS):
        for row in range(ROWS):
            pygame.draw.rect(
                window,
                (0, 0, 0),
                (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1,
            )

    # Thicker middle line
    pygame.draw.line(window, (0, 0, 0), (0, 450), (900, 450), 10)

    # Draw bottom table
    for col in range(COLS):
        for row in range(ROWS):
            pygame.draw.rect(
                window,
                (0, 0, 0),
                (col * BLOCK_SIZE, (row * BLOCK_SIZE) + 450, BLOCK_SIZE, BLOCK_SIZE),
                1,
            )


def write_text(window: pygame.Surface) -> None:
    font = pygame.font.SysFont("Arial", 26)

    detected_ship_text = font.render("Detected enemy ships", True, (0, 0, 0))
    detected_ship_text_rect = detected_ship_text.get_rect()
    detected_ship_text_rect.center = ((400 // 2) + 450, 50 // 2)
    window.blit(detected_ship_text, detected_ship_text_rect)

    own_ship_text = font.render("Own ships", True, (0, 0, 0))
    own_ship_text_rect = own_ship_text.get_rect()
    own_ship_text_rect.center = ((400 // 2) + 450, (50 // 2) + 450)
    window.blit(own_ship_text, own_ship_text_rect)

    for y1, y2 in [(50, 75), (950, 525)]:
        for num in range(8):
            num_text = font.render(f"{num+1}", True, (0, 0, 0))
            num_text_rect = num_text.get_rect()
            num_text_rect.center = (75 + (50 * num), y1 // 2)
            window.blit(num_text, num_text_rect)

        for num, char in enumerate(["A", "B", "C", "D", "E", "F", "G", "H"]):
            char_text = font.render(char, True, (0, 0, 0))
            char_text_rect = char_text.get_rect()
            char_text_rect.center = (50 // 2, y2 + (50 * num))
            window.blit(char_text, char_text_rect)


def update() -> None:
    global RUNNING  # pylint: disable=global-statement

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pylint: disable=no-member
            RUNNING = False

        process_input(event)

    for ship in SHIPS:
        ship.update()


def process_input(event: list[pygame.event.Event]) -> None:
    global ACTIVE_SHIP, OUTLINE_SHIP  # pylint: disable=global-statement

    mouse_pos = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
        if ACTIVE_SHIP is None:
            for ship in SHIPS:
                if not ship.rect.collidepoint(*mouse_pos):
                    continue
                ACTIVE_SHIP = ship

    elif event.type == pygame.MOUSEBUTTONUP:  # pylint: disable=no-member
        ACTIVE_SHIP = None

    if ACTIVE_SHIP is not None:
        ACTIVE_SHIP.x = mouse_pos[0]
        ACTIVE_SHIP.y = mouse_pos[1]
        OUTLINE_SHIP = None
        for block in BOTTOM_BLOCKS:
            rect = pygame.Rect(block[0], block[1], block[2], block[3])
            if rect.collidepoint(*mouse_pos):
                x = block[0] + 10
                y = block[1] + 10
                width = ACTIVE_SHIP.rect.width
                height = ACTIVE_SHIP.rect.height

                if width == BLOCK_SIZE - 10:
                    width -= 10
                elif height == BLOCK_SIZE - 10:
                    height -= 10

                OUTLINE_SHIP = pygame.Rect(x, y, width, height)


def run(window: pygame.Surface) -> None:
    global RUNNING  # pylint: disable=global-statement

    for col in range(1, COLS):
        for row in range(1, ROWS):
            TOP_BLOCKS.append((col * BLOCK_SIZE, row * BLOCK_SIZE))
            BOTTOM_BLOCKS.append(
                (col * BLOCK_SIZE, (row * BLOCK_SIZE) + 450, BLOCK_SIZE, BLOCK_SIZE)
            )

    destroyer = Ship(500, 500, 2)
    SHIPS.append(destroyer)

    RUNNING = True
    while RUNNING:
        update()
        render(window)


if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battleship")
    run(screen)

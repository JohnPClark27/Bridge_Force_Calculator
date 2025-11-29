import pygame
import sys


from models.force_input_popup import force_input_popup
from models.grid import Grid
from models.node import Node
from models.toolbar import Toolbar
from models.joint import Joint
from models.arrow import Arrow





def main():
    # Setup display
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    TOOLBAR_HEIGHT = 25
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    grid_surface = pygame.Surface((WIDTH, HEIGHT))
    toolbar_surface = pygame.Surface((WIDTH, TOOLBAR_HEIGHT))
    pygame.display.set_caption("Structural Analysis Tool")
    clock = pygame.time.Clock()
    grid_size = 25

    grid = Grid(WIDTH, HEIGHT, grid_size)

    toolbar = Toolbar(TOOLBAR_HEIGHT, WIDTH)
    toolbar.add_button("Place Node")
    toolbar.add_button("Connect Node")
    toolbar.add_button("Reaction Force")
    toolbar.add_button("Delete Node")
    toolbar.add_button("Generate force")
    toolbar.add_button("Visualize forces")

    


def draw(screen):
    screen.fill((0,0,0))


if __name__ == "__main__":
    main()
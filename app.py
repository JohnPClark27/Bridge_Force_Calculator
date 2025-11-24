import pygame
import sys


from models.force_input_popup import force_input_popup
from models.grid import Grid
from models.node import Node
from models.toolbar import Toolbar
from models.joint import Joint
from models.arrow import Arrow



def draw(screen, screen_items, mouse_pos=None):
    screen.fill((0,0,0))
    for item in screen_items:
        item.draw(screen)

    # Draw mouse coordinates for testing
    if mouse_pos:
        font = pygame.font.SysFont(None, 24)
        coord_text = font.render(f'X: {mouse_pos[0]} Y: {mouse_pos[1]}', True, (255, 255, 255))
        screen.blit(coord_text, (mouse_pos[0] + 10, mouse_pos[1] + 10))
    
    pygame.display.flip()


def main():
    pygame.init()

    # Set up display
    WIDTH, HEIGHT = 800, 600
    TOOLBAR_HEIGHT = 25
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    grid_surface = pygame.Surface((WIDTH, HEIGHT))
    toolbar_surface = pygame.Surface((WIDTH, TOOLBAR_HEIGHT))
    clock = pygame.time.Clock()
    grid_size = 25

    # Create grid
    grid = Grid(WIDTH, HEIGHT, grid_size)

    # Create toolbar
    toolbar = Toolbar(WIDTH, TOOLBAR_HEIGHT)
    toolbar.add_button("Place Node")
    toolbar.add_button("Connect Node")
    toolbar.add_button("Reaction Force")
    toolbar.add_button("Delete Node")
    toolbar.add_button("Generate force")
    toolbar.add_button("Visualize forces")

    mode = "Place Node"
    reaction_type = 1

    nodes = []
    node1 = None
    node2 = None
    joints = []
    reaction_arrows = []
    force_arrows = []

    screen_items = []
    temp_node = Node(0,0,"temp",(255,0,0))
    temp_arrow = None
    temp_force_arrow = None
    clicked_node = None
    clicked_point = None

    temp_screen_items = []

    # Joint unit vectors
    joint_vectors = []

    popup = force_input_popup("Enter force magnitude:", 300, 200, 200, 100)
    response = ""




    running = True
    mouse_pos = None
    while running:
        for event in pygame.event.get():
            response = popup.handle_event(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if response != "" and response is not None:
                    print("Force magnitude entered:", response)
                    if clicked_node is not None and clicked_point is not None:
                        # Force arrow created between node and point
                        for arrow in force_arrows:
                            if arrow.get_node() == clicked_node and arrow.get_end_pos() == clicked_point:
                                arrow.set_force_magnitude(float(response))
                                break
                        temp_force_arrow = None
                        clicked_point = None
                        clicked_node = None
                    response = ""
            elif event.type == pygame.MOUSEMOTION and popup.active == False:
                mouse_pos = event.pos
                x,y = event.pos
                if mode == "Place Node":
                    temp_node.set_location(x,y)
                    if temp_node not in temp_screen_items:
                        temp_screen_items.append(temp_node)
                if mode == "Reaction Force":
                    if temp_arrow is not None:
                        
                        temp_arrow.set_end_pos(round(x / grid_size) * grid_size, round(y / grid_size) * grid_size)

                for button in toolbar.buttons:
                    if button.is_hovered(event.pos):
                        button.button_color = (150, 150, 150)
                    else:
                        if button.text == mode:
                            button.button_color = (150, 150, 150)
                        else:
                            button.button_color = (100, 100, 100)
                for node in nodes:
                    if mode == "Connect Node" and node1 is not None and node == node1:
                        node.color = (0, 0, 255)
                    elif node.is_hovered(event.pos):
                        if mode == "Reaction Force":
                            node.color = (255, 255, 0)
                        else:
                            node.color = (0, 255, 0)
                    else:
                        node.color = (255, 0, 0)

            elif event.type == pygame.MOUSEBUTTONDOWN and popup.active == False:
                x,y = event.pos
                if (y < (toolbar.height+(grid_size//2)+5)):
                    for button in toolbar.buttons:
                        if button.is_clicked(event.pos):
                            temp_screen_items.clear()
                            temp_arrow = None
                            if button.text == "Place Node":
                                button.button_color = (150, 150, 150)
                                mode = "Place Node"
                            elif button.text == "Connect Node":
                                temp_screen_items.clear()
                                button.button_color = (150, 150, 150)
                                mode = "Connect Node"
                                node1 = None
                                node2 = None
                            elif button.text == "Delete Node":
                                button.button_color = (150, 150, 150)
                                mode = "Delete Node"
                            elif button.text == "Reaction Force":
                                clicked_node = None
                                clicked_point = None
                                button.button_color = (150, 150, 150)
                                mode = "Reaction Force"
                            elif button.text == "Generate force":
                                button.button_color = (150, 150, 150)
                                mode = "Generate force"
                            elif button.text == "Visualize forces":
                                button.button_color = (150, 150, 150)
                                mode = "Visualize forces"
                            
                else:
                    if mode == "Place Node":
                        for node in nodes:
                            if node.x == round(x / grid_size) * grid_size and node.y == round(y / grid_size) * grid_size:
                                break
                        else:
                            node = Node(x, y, "default", (255, 0, 0))
                            nodes.append(node)
                            screen_items.append(node)
                            temp_screen_items.clear()
                    elif mode == "Delete Node":
                        for node in nodes:
                            if node.is_hovered(event.pos):
                                nodes.remove(node)
                                screen_items.remove(node)
                                # Also remove any joints connected to this node
                                joints_to_remove = []
                                for joint in joints:
                                    if joint.node_a == node or joint.node_b == node:
                                        joints_to_remove.append(joint)
                                for joint in joints_to_remove:
                                    joints.remove(joint)
                                    screen_items.remove(joint)
                                arrows_to_remove = []
                                for arrow in reaction_arrows:
                                    if arrow.get_node() == node:
                                        arrows_to_remove.append(arrow)
                                for arrow in arrows_to_remove:
                                    reaction_arrows.remove(arrow)
                                for arrow in force_arrows:
                                    if arrow.get_node() == node:
                                        arrows_to_remove.append(arrow)
                                for arrow in arrows_to_remove:
                                    force_arrows.remove(arrow)
                                break
                    elif mode == "Connect Node":
                        if node1 is None:
                            for node in nodes:
                                if node.is_hovered(event.pos):
                                    node1 = node
                                    break
                        elif node1 is not None and node2 is None and node1.is_hovered(event.pos) == True:
                            node1 = None
                            
                        else: 
                            for node in nodes:
                                if node.is_hovered(event.pos) and node != node1:
                                    node2 = node
                                    # Check that this joint doens't already exist
                                    exists = False
                                    for joint in joints:
                                        if (joint.node_a == node1 and joint.node_b == node2) or (joint.node_a == node2 and joint.node_b == node1):
                                            exists = True
                                            break
                                    if not exists:
                                        joint = Joint(node1, node2)
                                        joints.append(joint)
                                        joint_vectors.append((joint, joint.get_unit_vector()))
                                        screen_items.append(joint)
                                    node1 = None
                                    node2 = None
                                    break
                    elif mode == "Reaction Force":
                        node = None
                        for n in nodes:
                            if n.is_hovered((round(x / grid_size) * grid_size, round(y / grid_size) * grid_size)):
                                node = n
                                break
                        
                        if temp_arrow is None:
                            if node is not None:
                                clicked_node = node
                                temp_arrow = Arrow((node.x, node.y), event.pos,color=(255,165,0))
                                temp_arrow.set_node(clicked_node)
                                temp_screen_items.append(temp_arrow)
                            else:
                                clicked_point = (round(x / grid_size) * grid_size, round(y / grid_size) * grid_size)
                                temp_arrow = Arrow(clicked_point, event.pos,color=(255,165,0))
                                temp_screen_items.append(temp_arrow)
                        else:
                            if node is not None: # We have clicked on a node
                                if clicked_node is not None: # We have clicked another node 
                                    pass
                                else: # We had clicked a point
                                    clicked_node = node
                                    temp_arrow.set_end_pos(node.x, node.y)
                                    temp_arrow.set_node(clicked_node)
                                    temp_screen_items.remove(temp_arrow)
                                    reaction_arrows.append(temp_arrow)
                                    temp_arrow = None
                                    clicked_point = None
                                    clicked_node = None
                            else: # We have clicked on a point
                                if clicked_node is not None: # We had clicked a node
                                    clicked_point = (round(x / grid_size) * grid_size, round(y / grid_size) * grid_size)
                                    temp_arrow.set_end_pos(clicked_point[0], clicked_point[1])
                                    temp_screen_items.remove(temp_arrow)
                                    reaction_arrows.append(temp_arrow)
                                    temp_arrow = None
                                    clicked_point = None
                                    clicked_node = None
                                else: # We had clicked a point
                                    pass
                    elif mode == "Generate force":
                        node = None
                        for n in nodes:
                            if n.is_hovered((round(x / grid_size) * grid_size, round(y / grid_size) * grid_size)):
                                node = n
                                break
                        
                        if temp_force_arrow is None:
                            if node is not None:
                                clicked_node = node
                                temp_force_arrow = Arrow((node.x, node.y), event.pos,color=(255,165,0))
                                temp_force_arrow.set_node(clicked_node)
                                temp_screen_items.append(temp_force_arrow)
                            else:
                                clicked_point = (round(x / grid_size) * grid_size, round(y / grid_size) * grid_size)
                                temp_force_arrow = Arrow(clicked_point, event.pos,color=(255,165,0))
                                temp_screen_items.append(temp_force_arrow)
                        else:
                            if node is not None: # We have clicked on a node
                                if clicked_node is not None: # We have clicked another node 
                                    pass
                                else: # We had clicked a point
                                    clicked_node = node
                                    temp_force_arrow.set_end_pos(node.x, node.y)
                                    temp_force_arrow.set_node(clicked_node)
                                    temp_screen_items.remove(temp_force_arrow)
                                    force_arrows.append(temp_force_arrow)
                                    
                                    popup.open()
                            else: # We have clicked on a point
                                if clicked_node is not None: # We had clicked a node
                                    clicked_point = (round(x / grid_size) * grid_size, round(y / grid_size) * grid_size)
                                    temp_force_arrow.set_end_pos(clicked_point[0], clicked_point[1])
                                    temp_screen_items.remove(temp_force_arrow)
                                    force_arrows.append(temp_force_arrow)
                                    
                                    popup.open()
                                else: # We had clicked a point
                                    pass
                    
                        
                                
                                
                            

                
        toolbar_surface.fill((50, 50, 50))
        grid_surface.fill((255, 255, 255))
        grid.draw(grid_surface)
        toolbar.draw(toolbar_surface)
        for temp_item in temp_screen_items:
            temp_item.draw(grid_surface)
        for node in nodes:
            node.draw(grid_surface)
        for joint in joints:
            joint.draw(grid_surface)
        for arrow in reaction_arrows:
            arrow.draw(grid_surface)
        for arrow in force_arrows:
            arrow.draw(grid_surface)

       
        
        screen.blit(grid_surface, (0, 0))
        screen.blit(toolbar_surface, (0, 0))

        popup.draw(screen)

        if mouse_pos:
            font = pygame.font.SysFont(None, 24)
            coord_text = font.render(f'X: {mouse_pos[0]} Y: {mouse_pos[1]}', True, (255, 255, 255))
            screen.blit(coord_text, (mouse_pos[0] + 10, mouse_pos[1] + 10))
    
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

def draw_toolbar(toolbar, surface):
    toolbar.draw(surface)
    surface.blit(surface, (0, 0))

def draw_grid(grid, surface):
    grid.draw(surface)
    surface.blit(surface, (0, 0))

def calculate_forces(nodes, joints, reaction_arrows, force_arrows):
    pass
    
if __name__ == "__main__":
    main()


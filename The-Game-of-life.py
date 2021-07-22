"""Conway's Game of Life. Implemented using pygame library."""

import pygame
# Intializing widnow
pygame.init()
win = pygame.display.set_mode((1200,800))
pygame.display.set_caption("The game of life")
# variables for drawing grid and cells
rows = 120
w = 1200
sizeBtwn = w // rows

ngbhr_cell = ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1))

#Set holding tuples cells to be drawn
life_cells = set() 
# Variables for function appRules()
moor_ngbhr = set()
dead_cells  = set()
dead_check = set()
new_born_cells = set()

dead_dict = dict()
def drawGrid(w, rows, surface):
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(win, (0,128,0), (x,0),(x,w))
        pygame.draw.line(win, (0,128,0), (0,y),(w,y))

# Drawing life cells 
def drawRects(cells):
    for x,y in cells:
        pygame.draw.rect(win, (0,255,0), (x*sizeBtwn,y*sizeBtwn, sizeBtwn, sizeBtwn))

# Initilazing null generation based on user's input
def addDiscardCells(input=life_cells): 
    if pygame.mouse.get_pressed()[0] == 1: #left mouse button 

        x_mous_pos = pygame.mouse.get_pos()[0]
        y_mous_pos = pygame.mouse.get_pos()[1]

        life_cells.add( (x_mous_pos//10,y_mous_pos//10) )

    if pygame.mouse.get_pressed()[2] == 1: #right mouse button 
        x_mous_pos = pygame.mouse.get_pos()[0]
        y_mous_pos = pygame.mouse.get_pos()[1]

        life_cells.discard( (x_mous_pos//10,y_mous_pos//10) )

# Applying rules/ generation cells of next generation
def appRules(life_cells=life_cells):
    """Life cells check"""
    for cell in life_cells:
        # calculating Moore neighbourhood for every life cell. (≈8*life_cells)
        for ngbhr in ngbhr_cell:
            moor_ngbhr.add((cell[0] + ngbhr[0],cell[1] + ngbhr[1]))
        # Applying first three rules
        life_cells_ngbhr = len(moor_ngbhr.intersection(life_cells))

        if life_cells_ngbhr != 2 and life_cells_ngbhr != 3:
            dead_cells.add(cell)
        # Necessary for applying fourth rule
        for cell in moor_ngbhr:
            if cell not in life_cells:
                dead_dict[cell] = dead_dict.get(cell,0) + 1
        # emptying for next cycle
        moor_ngbhr.clear()
        
    for cell, live_cells_around in dead_dict.items():
        if live_cells_around == 3:
            new_born_cells.add(cell)


    dead_dict.clear()
    # Getting rid of died cells
    life_cells.difference_update(dead_cells)
    # Adding new born cells
    life_cells.update(new_born_cells)

    # emptying for next cycle
    dead_cells.clear()
    dead_check.clear()
    new_born_cells.clear()

    return life_cells

def iniNullGen():
    init_null_gen = True
    while init_null_gen: 
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                init_null_gen = False 
                run = False

        win.fill((0,0,0))

        drawGrid(w,rows,win)
        addDiscardCells() #!
        drawRects(life_cells)

        # end the inside loop by pressing a random key
        pressed = pygame.key.get_pressed()
        for key in pressed:
            if key != 0:
                init_null_gen = False 
                run = True
        pygame.display.update()

    return run    

gen = 0
run = True

# Main loop
while run:
    pygame.time.delay(1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.fill((0,0,0))

    if gen ==0:
        run = iniNullGen()

    drawGrid(w,rows,win)

    print("GENERATION {}".format(gen))
    print("SIZE {}".format(len(life_cells)))
    print("LIFE cells", life_cells)

    drawRects(life_cells)
    life_cells = appRules(life_cells)
    gen += 1

    pygame.display.update()

pygame.quit()

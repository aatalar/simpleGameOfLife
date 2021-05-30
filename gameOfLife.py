import pyglet
import pyglet.window.key as key
import pyglet.window.mouse as mouse

window = pyglet.window.Window(500, 500)
gamefieldBatch = pyglet.graphics.Batch()
blocksBatch = pyglet.graphics.Batch()
# on/off state is determined by color
on = [255, 255, 255]
off = [0, 0, 0]

# first list is x-index, second y-index
blocks = []
# create blocks
for i in range(50):
    xRow = []
    for l in range(50):
        xRow.append(pyglet.shapes.Rectangle(i * 10, l * 10, 10, 10, color=off, batch=blocksBatch))
    blocks.append(xRow)

grid = []
# add the grid to the batch
grey = (120, 120, 120)
for i in range(50):
    horizontal = pyglet.shapes.Line(0, 10 * i, 500, 10 * i, batch=gamefieldBatch, color=grey)
    grid.append(horizontal)
    vertical = pyglet.shapes.Line(10 * i, 0 * i, 10 * i, 500, batch=gamefieldBatch, color=grey)
    grid.append(vertical)

# border lines
left = pyglet.shapes.Line(1, 1, 1, 500, batch=gamefieldBatch, color=(255, 255, 255))
right = pyglet.shapes.Line(500, 1, 500, 500, batch=gamefieldBatch, color=(255, 255, 255))
low = pyglet.shapes.Line(1, 1, 500, 1, batch=gamefieldBatch, color=(255, 255, 255))
high = pyglet.shapes.Line(1, 499, 500, 499, batch=gamefieldBatch, color=(255, 255, 255))


# main game flow

# gives number of "live" neighbours
def getNeighboursAlive(gameField: list, pos: tuple) -> int:
    alive = 0
    x, y = pos
    neighbours = []
    try:
        neighbours.append(gameField[x + 1][y])
        neighbours.append(gameField[x - 1][y])
        neighbours.append(gameField[x][y + 1])
        neighbours.append(gameField[x][y - 1])
        neighbours.append(gameField[x + 1][y + 1])
        neighbours.append(gameField[x - 1][y + 1])
        neighbours.append(gameField[x - 1][y - 1])
        neighbours.append(gameField[x + 1][y - 1])
    except Exception:
        pass

    for neighbour in neighbours:
        if neighbour.color == on:
            alive += 1
    return alive


def isAlive(block: pyglet.shapes.Rectangle) -> bool:
    return block.color == on


# gives grid of blocks with new states back
def getNewState(gameField: list) -> list:
    newStates = []
    for x, column in enumerate(gameField):
        xRow = []
        for y, block in enumerate(column):
            numNeighbours = getNeighboursAlive(gameField, (x, y))
            if isAlive(block) and numNeighbours == 2 or numNeighbours == 3:
                xRow.append(on)
            elif not isAlive(block) and numNeighbours == 3:
                xRow.append(on)
            else:
                xRow.append(off)
        newStates.append(xRow)
    return newStates


# update function called every second to run the simulation
def update(dt):
    newStates = getNewState(blocks)
    for x, column in enumerate(blocks):
        for y, block in enumerate(column):
            block.color = newStates[x][y]


@window.event
def on_mouse_release(x, y, button, modifiers):
    if button == mouse.LEFT:
        xPos = int(x/10)
        yPos = int(y/10)
        block = blocks[xPos][yPos]
        if block.color == on:
            block.color = off
        else:
            block.color = on


@window.event
def on_key_release(symbol, modifiers):
    # start simulation
    if symbol == key.F:
        # run update method every second
        pyglet.clock.schedule_interval(update, 0.2)


@window.event
def on_draw():
    window.clear()
    blocksBatch.draw()
    gamefieldBatch.draw()


pyglet.app.run()
print("after Run")

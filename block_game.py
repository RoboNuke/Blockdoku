
import pygame
import random
from copy import deepcopy
from block_data import block_data

class Game(object):
    def __init__(self):
        # define blocks
        #print("Initalize game")
        self.map = [[False for x in range(9)] for y in range(9)]

        #for shape in block_data:
        #    print(shape)
            
        self.blocks = deepcopy(block_data)
        self.originPart = [0 for x in range(3)]
        self.placedCount = 0
        self.playOptions = self.getRandomBlocks()
        self.placeable = [True, True, True]
        self.placed = [False, False, False]
        random.Random(100)
        self.score = 0
        self.gameOver = False

    def setMap(self, mapp):
        self.map = deepcopy(mapp)
    
    def getActions(self):
        actions = []
        for idx in range(len(self.playOptions)):
            for u in range(len(self.map)):
                for v in range(len(self.map[0])):
                    placeData = self.canPlaceObject(u,v,idx)
                    if(placeData[0]):
                        #print(placeData)
                        actions.append([[u,v,idx], placeData[1]]) # action desc., places to place blocks
        return(actions)
                        
    def getNextState(self, state, toAdd=[]):
        tempMap = deepcopy(state)
        remove = []
        for x,y in toAdd:
            tempMap[x][y] = True
        for u in range(len(tempMap)):
            add = []
            for v in range(len(tempMap[0])):
                if tempMap[u][v]:
                    add.append([u,v])
            if(len(add) == 9):
                remove = remove + add

        for v in range(len(tempMap[0])):
            add = []
            for u in range(len(tempMap)):
                if tempMap[u][v]:
                    add.append([u,v])
            if len(add) == 9:
                remove = remove + add
        # check the boxes
        xMin = 0
        xMax = 3
        yMin = 0
        yMax = 3
        for i in range(3):
            for j in range(3):
                add = []
                for x in range(xMin,xMax):
                    for y in range(yMin, yMax):
                        if(tempMap[x][y]):
                            add.append([x,y])
                if len(add) == 9:
                    remove = remove + add
                xMin = xMin + 3
                xMax = xMax + 3
            yMin = yMin + 3
            yMax = yMax + 3
            xMin = 0
            xMax = 3
        reward = len(remove)/9
        for u,v in remove:
            tempMap[u][v] = False
        return([reward, tempMap])
    
    def getScore(self):
        return self.score
    
    def getRandomBlocks(self):
        x = [self.blocks[random.randint(0,len(self.blocks)-1)] for y in range(3)]
        return x
    
    def canPlaceObject(self, u, v, idx):
        if self.placed[idx]:
            #print("Place already")
            return [False,[]]
        placeIdxs = []
        originPart = self.playOptions[idx][self.originPart[idx]]
        for part in self.playOptions[idx]:
            u1 = u + part[0] - originPart[0]
            v1 = v + part[1] - originPart[1]
            placeIdxs.append([u1,v1])
        
            if( u1 < 0 or u1 > 8 or v1 < 0 or v1 > 8 or self.map[u1][v1]):
                return [False, []]
        return [True, placeIdxs]

    def placeObject(self, u, v, idx):
        #print("Placing Object")
        #print(self.playOptions[idx])
        if self.placed[idx] or not self.placeable[idx] or self.gameOver:
            return
        w,x = self.playOptions[idx][self.originPart[idx]]
        u = u - w
        v = v - x
        for part in self.playOptions[idx]:
            self.map[u+part[0]][v+part[1]] = True
        self.placedCount = self.placedCount + 1
        self.placed[idx] = True
        #print(self.placedCount)
        self.updateMap()
        
        #print("Placed Count:",self.placedCount)
        if(self.placedCount == 3):
            self.placedCount = 0
            self.playOptions = self.getRandomBlocks()
            self.placed = [False, False, False]
            #self.updatePlaceableObjects()
            self.originPart = [0 for x in range(3)]
        self.updatePlaceableObjects()
            
    def updateMap(self):
        remove = self.getRemovableBlocks()
        self.updateScore( int(len(remove)/9 ))
        for x,y in remove:
            self.map[x][y] = False
            
    def updateScore(self, removedRows = 0):
        self.score = self.score + removedRows
        #print("Score:",self.score)
        
    def isPlaceable(self, idx):
        return self.placeable[idx] and not self.placed[idx]
    
    def updatePlaceableObjects(self):
        placeable = 0
        for i in range(3):
            if( not self.placed[i]):
                for u in range(9):
                    for v in range(9):
                        self.placeable[i] = self.canPlaceObject(u,v,i)[0]
                        if(self.placeable[i]):
                            placeable = placeable + 1
                            break
                    if(self.placeable[i]):
                        break
        if(placeable == 0):
            #print("game over")
            self.gameOver = True
            

    
    def getRemovableBlocks(self, toAdd = []):
        remove = []
        tempMap = deepcopy(self.map)
        for x,y in toAdd:
            tempMap[x][y] = True
        for u in range(len(tempMap)):
            add = []
            for v in range(len(tempMap[0])):
                if tempMap[u][v]:
                    add.append([u,v])
            if(len(add) == 9):
                remove = remove + add

        for v in range(len(tempMap[0])):
            add = []
            for u in range(len(tempMap)):
                if tempMap[u][v]:
                    add.append([u,v])
            if len(add) == 9:
                remove = remove + add
        # check the boxes
        xMin = 0
        xMax = 3
        yMin = 0
        yMax = 3
        for i in range(3):
            for j in range(3):
                add = []
                for x in range(xMin,xMax):
                    for y in range(yMin, yMax):
                        if(tempMap[x][y]):
                            add.append([x,y])
                if len(add) == 9:
                    remove = remove + add
                xMin = xMin + 3
                xMax = xMax + 3
            yMin = yMin + 3
            yMax = yMax + 3
            xMin = 0
            xMax = 3
        return(remove)
        
    def offsetPlayOption(self, idx, oIdx):
        # part idex and new origin idx
        #origin = self.playOptions[idx][oIdx]
        self.originPart[idx] = oIdx
        
    def getOffsetObject(self, idx):
        x,w = self.playOptions[idx][self.originPart[idx]]
        locs = []
        for part in self.playOptions[idx]:
            locs.append([part[0] - x, part[1] - w])
        return locs


class GUI(object):
    def __init__(self, _game, gridSize=9):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game = _game
        
        self.blockWidth = 30
        self.mapOffset = (2 * self.blockWidth, 2 * self.blockWidth)
        self.borderThickness = 1
        self.scaleFactor = (self.blockWidth - self.borderThickness * 2)/self.blockWidth

        
        
        self.rects = [[[None, None] for x in range(gridSize)] for y in range(gridSize)]
        self.holdingClick = False
        self.heldObject = None
        self.heldIdx = -1
        self.ignoreParts = []

        
        #self.objectOptions = [[],[],[]]
        self.newBlockOffset = ( (gridSize+2) * self.blockWidth + self.mapOffset[0], self.blockWidth)
        self.optionBlockPadding = int(0.25 * self.blockWidth)

        self.optionWidth = self.blockWidth * 3 + 2 * self.optionBlockPadding
        self.playOptions = []
        self.playOptionOutlines = []
        self.playerBlocks = []
        for i in range(3):
            x = self.newBlockOffset[0] - self.optionBlockPadding
            y = self.newBlockOffset[1] - self.optionBlockPadding + i * (4 * self.blockWidth)
            self.playerBlocks.append(pygame.Rect(x, y, self.optionWidth, self.optionWidth))

        self.playParts = [[] for i in range(3)]
        self.removable = []

        self.font = pygame.font.SysFont("comicsans", 50, True, True)
        
    def mainLoop(self):
        self.screen.fill("purple")
        if(not self.running):
            return
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.drawGrid()
        self.drawPlayerOptions()
        self.handleMouse()

        self.updateScore(self.game.getScore())

        
        pygame.display.flip()
        for i in range(3):
            if self.game.isPlaceable(i):
                return
        print("game over")
        print("final score:",self.game.score)
        self.running = False

    def updateScore(self, newScore):
        text = self.font.render("Score : " + str(newScore), 1, "black")
        self.screen.blit(text, (75, 350))
    def drawPlayerOptions(self):
        # draw white boxes first
        for rec in self.playerBlocks:
            outline = pygame.draw.rect(self.screen, "black", rec)
            pygame.draw.rect(self.screen, "white", outline.scale_by( ( self.optionWidth - self.borderThickness * 8)/self.optionWidth))

        for i, option in enumerate(self.game.playOptions):
            x, y, w, h = self.playerBlocks[i]
            x = (x + self.optionBlockPadding)/self.blockWidth
            y = (y + self.optionBlockPadding)/self.blockWidth
            self.playParts[i] = []
            if(self.holdingClick and i == self.heldIdx):
                for block in self.heldObject:
                    x,y,h,w = block[0]
                    #self.playParts[i].append( self.drawOffGrid(x, y, color="blue"))
            elif(i in self.ignoreParts):
                #print("Ignoring:", i)
                pass
            else:
                canPlace = self.game.isPlaceable(i)
                for block in option:
                    a,b = block
                    if(canPlace):
                        self.playParts[i].append(self.drawBlock(x + a, y + b, color = "blue"))
                    else:
                        self.playParts[i].append(self.drawBlock(x + a, y + b, color = "pink"))
                    
    def handleMouse(self):
        pressed = pygame.mouse.get_pressed()[0]
        pos = pygame.mouse.get_pos()
        rel = pygame.mouse.get_rel()
        if( self.holdingClick and pressed):
            # move held object
            u,v = self.getGridIdx(pos[0],pos[1])
            canPlace, gridIdxs = self.game.canPlaceObject(u, v, self.heldIdx)
            
            if( canPlace ):
                #print("can place")
                for u,v in gridIdxs:
                    self.drawBlock(u,v,"red","green")
                self.removable = self.game.getRemovableBlocks(gridIdxs)
            else:
                #print("can't place")
                offsets = self.game.getOffsetObject(self.heldIdx)
                self.playParts[self.heldIdx] = []
                for offset in offsets:
                    newX = offset[0] * self.blockWidth + pos[0]
                    newY = offset[1] * self.blockWidth + pos[1]
                    self.playParts[self.heldIdx].append(self.drawOffGrid(newX, newY, "blue"))
                self.removable = []

        elif( not self.holdingClick and pressed):
            # check for if a play piece was clicked
            for i, part in enumerate(self.playParts):
                for j, block in enumerate(part):
                    if( block[0].collidepoint(pos) or block[1].collidepoint(pos) ):
                        self.heldObject = part
                        self.holdingClick = True
                        self.heldIdx = i
                        self.game.offsetPlayOption(self.heldIdx, j) # update game state
                        print("grabbed object")
                        return
                        

        elif (self.holdingClick and not pressed):
            # released the press
            for row in self.rects:
                for blocks in row:
                    if( blocks[0].collidepoint(pos) or blocks[1].collidepoint(pos) ):
                        # held over the grid
                        #blocks[1] = pygame.draw.rect(self.screen, "blue", blocks[1])
                        x,y,w,h = blocks[1]
                        u,v = self.getGridIdx(x,y)
                        if(self.game.canPlaceObject(u,v,self.heldIdx)[0]):
                            # place object in map
                            self.game.placeObject(u,v,self.heldIdx) # update game
                            self.ignoreParts.append(self.heldIdx)
                            if( len(self.ignoreParts) == 3 ):
                                self.ignoreParts = []
                                self.playParts = [[] for i in range(3)]
                            self.removable = []
                                
                            
                        
            self.holdingClick = False
            print("let go")
        
        elif( not pressed ):
            # check for hover
            for row in self.rects:
                for blocks in row:
                    x,y,w,h = blocks[1]
                    u,v = self.getGridIdx(x,y)
                    #u = int((x-self.mapOffset[0])/self.blockWidth)
                    #v = int((y-self.mapOffset[1])/self.blockWidth)
                    
                    if( not self.game.map[u][v] and (blocks[0].collidepoint(pos) or blocks[1].collidepoint(pos)) ):
                        blocks[0] = pygame.draw.rect(self.screen, "blue", blocks[0])
                        if( ( (u < 3 or u > 5) and (v < 3 or v > 5)) or (u > 2 and u < 6 and v > 2 and v < 6) ):
                            blocks[1] = pygame.draw.rect(self.screen, "grey", blocks[1])
                        else:
                            blocks[1] = pygame.draw.rect(self.screen, "white", blocks[1])
            
    def drawBlock(self, x, y, color = "white", outline="black"):
        rect = pygame.Rect(self.mapOffset[0] + x * self.blockWidth, self.mapOffset[1] + y * self.blockWidth, self.blockWidth, self.blockWidth)
        outline = pygame.draw.rect(self.screen, outline, rect)
        main_block = pygame.draw.rect(self.screen, color, rect.scale_by(self.scaleFactor))
        return([outline, main_block])

    def drawOffGrid(self, x, y, color="white"):
        rect = pygame.Rect(x, y, self.blockWidth, self.blockWidth)
        outline = pygame.draw.rect(self.screen, "black", rect)
        main_block = pygame.draw.rect(self.screen, color, rect.scale_by(self.scaleFactor))
        return([outline, main_block])

    def getGridIdx(self, x, y):
        u = int( (x - self.mapOffset[0])/self.blockWidth)
        v = int( (y - self.mapOffset[1])/self.blockWidth)
        return (u,v)
    
    def isRunning(self):
        return self.running

    def endGame(self):
        pygame.quit()
        
    def drawGrid(self):
        u = 0
        v = 0
        blockMap = self.game.map

        windowSize = self.blockWidth * len(blockMap[0]) + 4 * self.borderThickness
        
        bgRect = pygame.Rect(self.mapOffset[0] - 2*self.borderThickness, self.mapOffset[1] - 2*self.borderThickness, windowSize, windowSize)
                             
        pygame.draw.rect(self.screen, "black", bgRect)
        col = "white"
        oCol = "grey"
        vSwap = False
        for row in blockMap:
            for block in row:
                if(u % 3 == 0):
                    holder = col
                    col = oCol
                    oCol = holder
                if(not blockMap[u][v]):
                    self.rects[u][v] = self.drawBlock(u, v, col)
                else:
                    self.rects[u][v] = self.drawBlock(u,v,"blue")
                u = u + 1
            u = 0
            v = v + 1
            if(v < 3 or v > 5):
                col = "white"
                oCol = "grey"
            else:
                col = "grey"
                oCol = "white"

        # color removable
        for x,y in self.removable:
            self.rects[x][y] = self.drawBlock(x,y, "pink","purple")

    def flip(self):
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()

    display = GUI(game,9)
    while display.isRunning():
        display.mainLoop()

    display.endGame()
    
    

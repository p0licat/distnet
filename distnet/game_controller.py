"""
    Maintainer of pygame objects.
"""
import os
import contextlib
with contextlib.redirect_stdout(None):
    import pygame


class GameController:
    def __init__(self, imageLocation):
        self._image = None
        self._gameObj = None
        self._clock = None

        pygame.init()
        pygame.mixer.quit()
        self._gameObj = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Visualizer')
        self._clock = pygame.time.Clock()

        if os.path.isfile(imageLocation):
            self._image = imageLocation
        else:
            raise Exception()

    def world(self):
        x = 0
        y = 0
        try:
            self._gameObj.blit(pygame.image.load(self._image), (x, y))
        except pygame.error as pe:
            print('Image draw error.')

        pygame.display.update()
        self._clock.tick(24)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
###

#
# gameDisplay = None
# if args.visual == True:
#     pygame.init()
#     pygame.mixer.quit()
#     gameDisplay = pygame.display.set_mode((800, 600))
#     pygame.display.set_caption('Visualizer')
#
# if args.visual == True:
#     clock = pygame.time.Clock()
#



# world(0, 0, gameDisplay, ftcp.tempfile_name)
# pygame.display.update()
# clock.tick(24)
# for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#         running = False

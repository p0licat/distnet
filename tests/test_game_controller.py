import os
import re
import sys

import tempfile
import pygal
import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../distnet"))

from game_controller import GameController

def test_game_controller_withfile():
    if "TRAVIS" in os.environ and os.environ["TRAVIS"] == "str_true":
        pytest.skip("TravisCI does not support.")

    game_controller = None
    tempfile_name = None
    visual = True
    continuous = True

    try:

        worldmap_chart = pygal.maps.world.World()
        worldmap_chart.title = 'Some countries'

        if tempfile_name == None:
            new_file, filename = tempfile.mkstemp(suffix='.png')
            tempfile_name = str(filename)
            last_write_name = tempfile_name

            os.close(new_file)
            worldmap_chart.render_to_png(tempfile_name)
            if not continuous:
                tempfile_name = None


        if visual == True:
            if game_controller == None:
                game_controller = GameController(tempfile_name)

            running = game_controller.world()

    except Exception as ex:
        if tempfile_name is not None:
            os.remove(tempfile_name)


        print(ex)
        assert False


def test_game_controller_nofile_exception():
    if "TRAVIS" in os.environ and os.environ["TRAVIS"] == "str_true":
        pytest.skip("TravisCI does not support.")
        
    game_controller = None
    tempfile_name = None
    visual = True
    continuous = True

    try:

        worldmap_chart = pygal.maps.world.World()
        worldmap_chart.title = 'Some countries'


        tempfile_name = 'notexist'
        # if tempfile_name == None:
        #     new_file, filename = tempfile.mkstemp(suffix='.png')
        #     tempfile_name = str(filename)
        #     last_write_name = tempfile_name
        #
        #     os.close(new_file)
        #     worldmap_chart.render_to_png(tempfile_name)
        #     if not continuous:
        #         tempfile_name = None


        if visual == True:
            if game_controller == None:
                game_controller = GameController(tempfile_name)
                assert False

            running = game_controller.world()

    #TODO: exception type
    except Exception as ex:
        print(ex)
        assert True

import cocos

from game.visualizer.graphs import *

class EndLayer(cocos.layer.Layer):
    def __init__(self,display_size,parser):
        self.display = display_size
        super().__init__()
        label = cocos.text.Label(
            "Game Over",
            font_name="Comic Sans",
            font_size=64,
            color=(255, 0, 0, 255),
            anchor_x='center',
            anchor_y='center'

        )
        label.position = self.display[0]/2, self.display[1]/2
        self.add(label)

        #Line graph
        self.add(LineGraph([6,48,367], 200,100, parser))
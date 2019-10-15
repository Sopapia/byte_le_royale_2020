import cocos


class CityLayer(cocos.layer.Layer):
    def __init__(self, display_size, turn_info):
        self.display = display_size
        self.info = turn_info
        super().__init__()
        images = [
            "game/visualizer/assets/city_assets/city_level0.png",
            "game/visualizer/assets/city_assets/city_level1.png",
            "game/visualizer/assets/city_assets/city_level2.png",
            "game/visualizer/assets/city_assets/city_level3.png"
        ]
        structure = 0
        try:
            structure = int(self.info['player'].get('city').get('structure'))
        except:
            print("Structure is NoneType")

        #Depending structure draw_correct sprite
        if structure > 150:
            self.city = cocos.sprite.Sprite(images[3])
        elif structure > 100:
            self.city = cocos.sprite.Sprite(images[2])
        elif structure > 50:
            self.city = cocos.sprite.Sprite(images[1])
        else:
            self.city = cocos.sprite.Sprite(images[0])

        #Anchor Point of the sprite is at the center of the sprite
        #This position the sprite to the right side of the screen
        #and the sprite in the middle of the screen on the y axis
        self.sprite_width = self.city.width
        self.sprite_height = self.city.height

        self.city_x = int(self.display[0]-self.sprite_width/2)
        self.city_y = int(self.display[1]/2)

        self.city.position = (self.city_x, self.city_y)
        self.add(self.city)
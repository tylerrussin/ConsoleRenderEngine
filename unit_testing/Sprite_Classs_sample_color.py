import os
import sys

# Path restructure for imports
script_dir = os.path.dirname( __file__ )
main_dir = os.path.join( script_dir, '..' )
sys.path.append( main_dir )

import unittest

from classes.Sprite_Class import Sprite
from sprites.Wall_Sprite import matrix
from sprites.Wall_Sprite import color_to_glyph

test_sprite = Sprite(matrix, color_to_glyph)
  
class TestSprite_ClassMethods(unittest.TestCase):
  
    # Returns True if the if the correct glyph value was sampled
    def test_sample_color(self):
        self.assertEqual( test_sprite.sample_color(0.5, 0.5), 'W')

    # Returns True if the if the correct glyph value was sampled
    def test_sample_color(self):
        self.assertEqual( test_sprite.sample_color(0.90, 0.35), 'W')

    # Returns True if the if the correct glyph value was sampled
    def test_sample_color(self):
        self.assertEqual( test_sprite.sample_color(0.03245323, 0.74464646), 'R')
  
  
if __name__ == '__main__':
    unittest.main()
from typing import Optional
from game.logic.base import BaseLogic
from game.models import Board,GameObject,Position,Config
from typing import Optional
import random
import time
from game.util import get_direction



##algortima nextmove
class pAdu(BaseLogic):
    def __init__(self):
        #Intialize attribute necessary
            self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            self.block_in = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
            self.goal_position: Optional[Position] = None
    def closestDiamond(self,start_position,diamond_objects,Board:Board):
        minlength=10000
        for i in range(Board.width):
             for j in range(Board.height):
                for diamond in diamond_objects:
                        if minlength>((abs(abs(diamond.position.x - start_position.x) + abs(diamond.position.y - start_position.y)))):
                             minlength=((abs(abs(diamond.position.x - start_position.x) + abs(diamond.position.y - start_position.y))))
                             self.goal_position=diamond.position
        return self.goal_position


    def next_move(self, board_bot: GameObject, board: Board):
            props = board_bot.properties
            # Analyze new state
            base = board_bot.properties.base
            current_position = board_bot.position
            if props.diamonds == 5 or props.diamonds == 4  : #error pas inventory diamond = 4 terus dapet diamond merah
                # Move to base
                
                base = board_bot.properties.base
                self.goal_position = base
            else:
                diamond_objects = board.diamonds
                
                self.goal_position = self.closestDiamond(current_position, diamond_objects,board)
                        
               

            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

            return delta_x,delta_y

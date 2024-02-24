from typing import Optional
from game.logic.base import BaseLogic
from game.models import Board,GameObject,Position
from typing import Optional
from ..util import get_direction
import random



##algortima nextmove
class BotsMove(BaseLogic):
    def __init__(self):
        #Intialize attribute necessary
            self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            self.block_in = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
            self.goal_position: Optional[Position] = None
            self.current_direction = 0
            #sisanya apa
    def next_move(self, board_bot: GameObject, board: Board):
            props = board_bot.properties
            # Analyze new state
            if props.diamonds == 5:
                # Move to base
                base = board_bot.properties.base
                self.goal_position = base
            else:
                # Just roam around
                self.goal_position = None

            current_position = board_bot.position

            if self.goal_position:
            # We are aiming for a specific position, calculate delta
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )
            else:
                #roam arround
                # location 0f diamonds
                diamond_objects = board.diamonds
                ##Finding all diamond object in 25 section
                block_size =5

                whichBlock_x = current_position.x//5
                whichBlock_y=current_position.y//5
                block_start_row = whichBlock_x * 5
                block_end_row = (whichBlock_x + 1) * 5
                block_start_col = whichBlock_y * 5
                block_end_col = (whichBlock_y + 1) * 5
                totalpointblock=0
                listrangediamond=[]
                for i in range(block_start_row,block_end_row):
                    #  print("masuk1\n")
                     for j in range(block_start_col,block_end_col):
                        #   print("masuk2\n")
                          for diamond in diamond_objects:
                            #    print(f"total :\n",diamond.properties.points)
                               if (diamond.position.x==i ) and (diamond.position.y==j):
                                    # print("Masuk3\n")
                                    totalpointblock+=diamond.properties.points
                                    print(f"total :\n",diamond.properties.points)
                                    listrangediamond.append((abs(abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)), diamond.position))

                
                if totalpointblock==0:
                     #pindah block
                    #kode sementara
                    print("Random\n")
                    delta = self.directions[self.current_direction]
                    delta_x = delta[0]
                    delta_y = delta[1]
                    if random.random() > 0.6:
                        self.current_direction = (self.current_direction + 1) % len(
                            self.directions
                        )
                else:
                     #cri terdekat
                    sorted_listrangediamond = sorted(listrangediamond, key=lambda x: x[0])
                    _,self.goal_position=sorted_listrangediamond[0]


                    delta_x, delta_y = get_direction(
                        current_position.x,
                        current_position.y,
                        self.goal_position.x,
                        self.goal_position.y,
                    )
            return delta_x,delta_y

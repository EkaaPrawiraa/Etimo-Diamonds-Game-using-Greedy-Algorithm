from typing import Optional
from game.logic.base import BaseLogic
from game.models import Board,GameObject,Position
from typing import Optional
from ..util import get_direction
import random
import time

# Tubes Stima 1 Point :
# 1. Utamain diamond terdekat dan diamond merah kalo bisa
# 2. Kalo ada base terdekat dan jauh dari diamond dan inventory tidak kosong balik ke base
# 3. menjauh dari pemain lawan atau ambil inventorynya
# 4. optimalin teleport dan red button


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
                     for j in range(block_start_col,block_end_col):
                          for diamond in diamond_objects:
                               if (diamond.position.x==i ) and (diamond.position.y==j):
                                    totalpointblock+=diamond.properties.points
                                    # print(f"total :\n",diamond.properties.points)
                                    listrangediamond.append((abs(abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)), diamond.position))

                
                # print(f"total :\n",totalpointblock)
                if totalpointblock==0:
                    #pindah block
                    #kode sementara
                    start_time = time.time()
                    for diamond in diamond_objects:
                            listrangediamond.append((abs(abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)), diamond.position))
                    
                    sorted_listrangediamond = sorted(listrangediamond, key=lambda x: x[0])
                    _,self.goal_position=sorted_listrangediamond[0]
                    end_time = time.time()
                    print(f"Time : {end_time-start_time} sec\n")

                    
                    delta_x, delta_y = get_direction(
                        current_position.x,
                        current_position.y,
                        self.goal_position.x,
                        self.goal_position.y,
                    )
                else:
                     #cri terdekat
                    sorted_listrangediamond = sorted(listrangediamond, key=lambda x: x[0])
                    _,self.goal_position=sorted_listrangediamond[0]

                    # print(f"Position goals: ({self.goal_position.x}, {self.goal_position.y})")
                    delta_x, delta_y = get_direction(
                        current_position.x,
                        current_position.y,
                        self.goal_position.x,
                        self.goal_position.y,
                    )
            return delta_x,delta_y
    
    # def totalpointblock(self,start_position,diamond_objects):
    #     whichBlock_x = 15//5
    #     whichBlock_y=15//5
    #     totaleveryblock=[]
    #     for i in range(3):
    #          for j in range(3):
    #             if i != start_position.x and j !=start_position.y:
    #                 block_start_row = whichBlock_x * 5
    #                 block_end_row = (whichBlock_x + 1) * 5
    #                 block_start_col = whichBlock_y * 5
    #                 block_end_col = (whichBlock_y + 1) * 5
    #                 totalpointblock=0
    #                 listrangediamond=[]
    #                 for i in range(block_start_row,block_end_row):
    #                         for j in range(block_start_col,block_end_col):
    #                             for diamond in diamond_objects:
    #                                 if (diamond.position.x==i ) and (diamond.position.y==j):
    #                                     totalpointblock+=diamond.properties.points
    #                                     print(f"total :\n",diamond.properties.points)
    #                                     listrangediamond.append((abs(abs(diamond.position.x - start_position.x) + abs(diamond.position.y - start_position.y)), diamond.position))
    #                 sorted_listrangediamond = sorted(listrangediamond, key=lambda x: x[0])
    #                 _,self.goal_position=sorted_listrangediamond[0]
            
         
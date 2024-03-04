from typing import Optional
from game.logic.base import BaseLogic
from game.models import Board,GameObject,Position,Config
from typing import Optional
from ..util import get_direction
import random
import time

# Tubes Stima 1 Point :
# 1. Utamain diamond terdekat dan diamond merah kalo bisa
# 2. Kalo ada base terdekat dan jauh dari diamond dan inventory tidak kosong balik ke base
# 3. menjauh dari pemain lawan atau ambil inventorynya
# 4. optimalin teleport dan red button

# Developing note :
# Cari diamond banyak yang deket sama base aja, rata rata max point yang didapet itu cuman 10
#error pas inevntory == 4 terus dapet red diamond
#fungsi buat calculate jarak ke tiap goal point
#masih banyak keliling gajelas perlu kalkulasi lama jalan sama waktu sisa biar optimal
#buat metode untuk atur prioritas untuk balik ke base dulu atau tetep jalan ngambilin diamond
#tiap satu langkah kira kira makan 1 detik
#ukuran table masih fix 15*15 padahal ganentu
#belum optimal fitur red button sama teeport
#buat fungsi menghindari teleport agar tidak looping
#kalo diamond abis, auto ke generate diamond, pilihannya klo sisa 1 diamond, pencet red button atau ambil diamond


##algortima nextmove
class BotsMove(BaseLogic):
    def __init__(self):
        #Intialize attribute necessary
            self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            self.block_in = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
            self.goal_position: Optional[Position] = None
            self.current_direction = 0
            #sisanya apa 
    def current_totalpointblock(self, current_position, diamond_objects):
        whichBlock_x = current_position.x//5
        whichBlock_y=current_position.y//5
        block_start_row = whichBlock_x * 5
        block_end_row = (whichBlock_x + 1) * 5
        block_start_col = whichBlock_y * 5
        block_end_col = (whichBlock_y + 1) * 5
        totalpointblock=0
        listrangediamond=[]
        for k in range(block_start_row,block_end_row):
                for l in range(block_start_col,block_end_col):
                    for diamond in diamond_objects:
                        if (diamond.position.x==k ) and (diamond.position.y==l):
                            totalpointblock+=diamond.properties.points
                            # print(f"total :\n",diamond.properties.points)
                            listrangediamond.append((abs(abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)), diamond.position, diamond.properties.points))


        return totalpointblock, listrangediamond
           
    def totalpointblock(self,start_position,diamond_objects):
        # whichBlock_x = 15//5
        # whichBlock_y=15//5
        totaleveryblock=[]
        for i in range(3):
             for j in range(3):
                    block_start_row = 5 * i
                    block_end_row = (1 + i) * 5
                    block_start_col = j * 5
                    block_end_col = (1 + j) * 5
                    totalpointblock=0
                    listrangediamond=[]
                    for k in range(block_start_row,block_end_row):
                            for l in range(block_start_col,block_end_col):
                                for diamond in diamond_objects:
                                    if (diamond.position.x==k ) and (diamond.position.y==l):
                                        totalpointblock+=diamond.properties.points
                                        # print(f"total :\n",diamond.properties.points)
                                        listrangediamond.append((abs(abs(diamond.position.x - start_position.x) + abs(diamond.position.y - start_position.y)), diamond.position))
                    sorted_listrangediamond = sorted(listrangediamond, key=lambda x: x[0]) #sort berdasar jarak atau jumlah point?
                    if sorted_listrangediamond:
                        distance,locationdiamond=sorted_listrangediamond[0]
                        totaleveryblock.append((totalpointblock,distance,locationdiamond))
        sorted_totaleveryblock=sorted(totaleveryblock,key=lambda x: x[1])

        _,_, self.goal_position=sorted_totaleveryblock[0]
        return self.goal_position

         
    def next_move(self, board_bot: GameObject, board: Board):
            props = board_bot.properties
            print(f"Time left : {props.milliseconds_left/1000} sec\n")
            # Analyze new state
            base = board_bot.properties.base
            current_position = board_bot.position
            distanceToBase = abs(abs(base.x- current_position.x) + abs(base.y - current_position.y))
            if props.diamonds == 5 or props.diamonds == 4  or ( (distanceToBase +1 == (props.milliseconds_left/1000)) and props.diamonds !=0) or (distanceToBase == (props.milliseconds_left/1000)) : #error pas inventory diamond = 4 terus dapet diamond merah
                # Move to base
                print("OTW Base\n")
                base = board_bot.properties.base
                self.goal_position = base
            else:
                # Just roam around
                self.goal_position = None

            

            if self.goal_position:
            # We are aiming for a specific position, calculate delta
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    self.goal_position.x,
                    self.goal_position.y,
                )
            else:
                # print(f"total :\n",totalpointblock)
                diamond_objects = board.diamonds
                item_board = board.game_objects
                totalpointblock, listrangediamond = self.current_totalpointblock(current_position, diamond_objects)
                teleports = []
                for item in item_board:
                    if item.type=='DiamondButtonGameObject':
                        red=item
                    elif item.type=='TeleportGameObject':
                        teleports.append((abs(abs(item.position.x - current_position.x) + abs(item.position.y - current_position.y)), item.position))
                        if(len(teleports) == 2):
                            sorted_teleport = sorted(teleports,key=lambda x: x[0])
                            
                    
                
                redpos = red.position
                _, telpos = sorted_teleport[1]
                if totalpointblock==0: ##bagian red buttoon
                    print(f"Sini\n")
                    if(red) and ((redpos.x//5 == current_position.x//5) and (redpos.y//5 == current_position.y//5)):
                        self.goal_position = redpos
                    
                    if(sorted_teleport) and ((telpos.x//5 == current_position.x//5) and (telpos.y//5 == current_position.y//5)):
                         self.goal_position = telpos
                    else:
                        self.goal_position = self.totalpointblock(board_bot.properties.base, diamond_objects)

                    # self.goal_position=goal_location
                    delta_x, delta_y = get_direction(
                        current_position.x,
                        current_position.y,
                        self.goal_position.x,
                        self.goal_position.y,
                    )
                else:
                     #cri terdekat
                 
                    print(f"Sono\n")
                    
                    sorted_listrangediamond = sorted(listrangediamond, key=lambda x: x[0])
                    # print(sorted_listrangediamond)
                    # if props.diamonds==4 and sorted_listrangediamond[0][2]==2:
                    #      sorted_listrangediamond.pop(0)
                    #      print("MERAH")
                    _,self.goal_position,_=sorted_listrangediamond[0]

                    # print(f"Position goals: ({self.goal_position.x}, {self.goal_position.y})")
                    delta_x, delta_y = get_direction(
                        current_position.x,
                        current_position.y,
                        self.goal_position.x,
                        self.goal_position.y,
                    )
            return delta_x,delta_y
    




















           #kode sementara
                    # start_time = time.time()
                    # for diamond in diamond_objects:
                    #         listrangediamond.append((abs(abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)), diamond.position))
                    
                    # sorted_listrangediamond = sorted(listrangediamond, key=lambda x: x[0])
                    # _,self.goal_position=sorted_listrangediamond[0]
import class_round
import random
def idiot_spins(board):
    this_round = class_round.round()



def explosive_spins(board, spin_type):
    this_round = class_round.round()
    # guaranteed fire in the hole on top row
    reel = random.randint(0, 5)
    for i in range(0, 6):
        if i == reel:
            board.find_block(i, 0).regular_symbol = "fire_in_the_hole"
        else:
            # other symbols on top reel have a 8% chance being water on the hill each
            if random.randint(0, 100) < 8:
                board.find_block(i, 0).regular_symbol = "water_on_the_hill"
            else:
                board.find_block(i, 0).regular_symbol = ""
    if spin_type == 1:
        # guarantees 2 oil barrels on the board
        oil_barrels = 2
        # chance of getting at least 3/4/5: 8%/1%/0.05%
        if random.randint(0, 10000) < 800:
            oil_barrels = 3
        elif random.randint(0, 10000) < 100:
            oil_barrels = 4
        elif random.randint(0, 10000) < 5:
            oil_barrels = 5
        # place oil barrels. NO OVERLAPPING!
        for i in range(0, oil_barrels):
            x = random.randint(0, 5)
            y = random.randint(1, 5)
            while board.find_block(x, y).regular_symbol != "":
                x = random.randint(0, 5)
                y = random.randint(1, 5)
            board.find_block(x, y).regular_symbol = "oil_barrel"
        # TODO HERE
        # We'll talk about the size later on, as well as randomly generated oil (not barrel)
    return this_round
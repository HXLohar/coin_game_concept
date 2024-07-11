
import tkinter
import class_round
import time
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random
import os
import tempfile
from tkinter import messagebox
spin_mode = 1
CONST_SPIN_SPEED = 165
# Create a dictionary containing basic information for all modes.
# Format: ID, Name, TotalCost, Desc
# 0, "Idiot Spins", 1.0, "Each spin have 2 types of outcome: Bonus or no Bonus!"
# 1, "Explosive Spins I", 12.0, "Guaranteed Fire in the Hole!"
# 2, "Explosive Spins II", 30.0, "Guaranteed Fire in the Hole + 2 Oil barrels!"

# 10, "Regular Bonus Buy", 75.0, "Guarantees exactly 3S to trigger a bonus.
# end of dictionary

mode_dictionary = {
    0: [0, "Idiot Spins", 1.0, "Each spin have 2 types of outcome: Bonus or no Bonus!"],
    1: [1, "Explosive Spins I", 12.0, "Guaranteed Fire in the Hole!"],
    2: [2, "Explosive Spins II", 30.0, "Guaranteed Fire in the Hole + 2 Oil barrels!"],
    10: [10, "Regular Bonus Buy", 75.0, "Guarantees exactly 3S to trigger a bonus."]
}

# Some information
# Water on the Hill and Fire on the Hole only appear on the 1st row.
class frame_block:
    def __init__(self, frame, block):
        self.frame = frame
        self.block = block
        self.image_label = tkinter.Label(self.frame)  # Create the image label here
        self.image_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place the label using place method

    def update_frame_img(self):
        frame_size = 50
        img_path = self.block.get_image()

        image = Image.open(img_path)

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial", 15)  # You may need to adjust the font and size

        # Draw the text onto the image
        top_left_text = ""
        bottom_right_text = ""
        if self.block.coinflip_symbol == "dynamite":
            top_left_text = f"x{self.block.coinflip_symbol_extra_info}"
        elif self.block.coinflip_symbol != "":
            top_left_text = f"{self.block.coinflip_symbol_extra_info}x"
        if self.block.regular_symbol_extra_info > 1:
            bottom_right_text = f"(x{self.block.regular_symbol_extra_info})"
        draw.text((0, 0), top_left_text, fill="black", font=font)

        # Calculate the width of the bottom right text
        text_width = len(bottom_right_text) * 7
        draw.text((frame_size - text_width, frame_size - 20), bottom_right_text, fill="black", font=font)

        # Save the image to a temporary file
        temp_file = tempfile.mktemp(suffix=".png")
        image.save(temp_file)

        # Load the temporary image into the label
        photo = ImageTk.PhotoImage(file=temp_file)
        self.image_label.config(image=photo)
        self.image_label.image = photo

        # Delete the temporary file
        os.remove(temp_file)

class profile:
    def __init__(self):
        self.balance = 10000
        self.biggest_win = []
        self.highest_multi = []
class interface:
    def __init__(self):
        # task_list的格式是: [task, sleep_before_execution, param1, param2, ...]
        # 其中param为可选
        self.task_list = []

        self.profile = profile
        self.round = class_round.round()

        self.root = tkinter.Tk()
        self.root.geometry("1000x600")  # Set the size of the main window

        self.frameblock = []
        # Create image frames
        frame_size = 50
        spacing = 10
        for col in range(6):  # 6 rows
            for row in range(6):  # 6 columns per row
                x = 10 + col * (frame_size + spacing)
                y = 10 if row == 0 else 80 + (row - 1) * (frame_size + spacing)
                self.img_frame = tkinter.Frame(self.root, width=frame_size, height=frame_size, bg='grey', borderwidth=1, relief='solid')
                self.img_frame.place(x=x, y=y)
                self.frameblock.append(frame_block(self.img_frame, self.round.board.find_block(col, row)))

        # Create labels and buttons
        self.balance_label = tkinter.Label(self.root, text="Balance: 10,000.00")
        self.balance_label.place(x=400, y=10)

        self.base_bet_label = tkinter.Label(self.root, text="Base bet: 1.00")
        self.base_bet_label.place(x=400, y=35)

        self.options_button = tkinter.Button(self.root, text="Click to select", command=lambda: self.popup_mode_menu())
        self.options_button.place(x=400, y=60, width=200, height=30)
        # text is determined by the selected mode's name from dictionary
        self.total_cost_label = tkinter.Label(self.root, text=f"Total Cost: {mode_dictionary[spin_mode][2]:.2f}")
        self.total_cost_label.place(x=400, y=90)

        # Buttons for rounds
        self.rounds_label = tkinter.Label(self.root, text="Manual")
        self.rounds_label.place(x=400, y=120)

        self.one_round_button = tkinter.Button(self.root, text="1 Round", command=lambda: self.init_spin())
        self.one_round_button.place(x=400, y=145, width=100, height=30)

        self.auto_label = tkinter.Label(self.root, text="Auto: not started..")
        self.auto_label.place(x=400, y=200)

        rounds_buttons = ["10 Rounds", "100 Rounds", "1K Rounds", "5K Rounds"]
        for i, text in enumerate(rounds_buttons):
            btn = tkinter.Button(self.root, text=text)
            btn.place(x=400, y=225 + i * 35, width=80, height=30)

        # Config buttons
        self.printer_button = tkinter.Label(self.root, text="Printer Mode")
        self.printer_button.place(x=400, y=400)

        self.config_button = tkinter.Button(self.root, text="Config")
        self.config_button.place(x=400, y=450)
        # include other mentioned functions in the dictionary
        self.task_dictionary = {
            'spin_reel': self.spin_and_update_img,
            '2_scatter_transform': self.round.convert_scatters,
            'test': self.test_print,
            'spread_oil': self.spread_oil,
            'water_on_the_hill': self.water_on_the_hill,
            'fire_in_the_hole': self.fire_in_the_hole

        }
        self.update_symbol_images()

        self.root.mainloop()

    def spread_oil(self):
        print("SPREAD OIL")
        # spread oil
        # do a for loop to go through each oil barrel on the board ("oil_barrel" in its regular_symbol)
        # for each oil barrel:
        # first there's a list of oil area, begin with only the oil barrel's coordinate in the list
        # oil_quantity: how many blocks to spread. it's randomly decided but have something to do with the oil barrel size.

        # then do the following thing X times, X = oil_quantity. calculate a list of blocks that can be spread onto,
        # with the following requirements: must be adjacent to existing list of oil area (left/right/top/down,
        # no diagonal). must not be on 1st row. must not be already included in the oil area list. must be either an
        # oil area block (NOT oil barrel) or empty block then randomly select one of the eligible blocks,
        # add it to the list of oil. Set that block to oil block with a regular_symbol_extra_info of 1 (being the
        # multiplier) if it's an empty block. if it's an oil area block, increase its multiplier by 1.
        for col in range(0, 6):
            for row in range(0, 6):
                # if it's oil barrel (("oil_barrel" in its regular_symbol))
                if "oil_barrel" in self.round.board.find_block(col, row).regular_symbol:
                    print("oil barrel found at", col, row)
                    oil_area = [(col, row)]
                    oil_quantity = 0
                    # decide the oil quantity
                    # # oil_barrel_small: 60/30/10 weighted chance being 1/2/3
                    # # oil_barrel_medium: 60/30/9/1 weighted chance being 2/3/4/5
                    # # oil_barrel_large: 40/25/20/10/4/1 weighted chance being 3/4/5/6/7/8
                    if "small" in self.round.board.find_block(col, row).regular_symbol:
                        oil_quantity = random.choices([1, 2, 3], [60, 30, 10])[0]
                    elif "medium" in self.round.board.find_block(col, row).regular_symbol:
                        oil_quantity = random.choices([2, 3, 4, 5], [60, 30, 9, 1])[0]
                    elif "large" in self.round.board.find_block(col, row).regular_symbol:
                        oil_quantity = random.choices([3, 4, 5, 6, 7, 8], [40, 25, 20, 10, 4, 1])[0]
                    for i in range(0, oil_quantity):
                        print("adding oil, step", i     + 1, "of", oil_quantity, "steps")
                        eligible_blocks = []
                        # for each block in the oil area list
                        # find adjacent blocks that are not on the 1st row, not already in the oil area list, and either
                        # being empty (symbol is "") or an oil area block (symbol is "Oil")
                        for oil_block in oil_area:
                            for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                                new_block = (oil_block[0] + direction[0], oil_block[1] + direction[1])
                                if new_block[1] > 0 and new_block not in oil_area:
                                    if self.round.board.find_block(new_block[0], new_block[1]).regular_symbol == "" or \
                                            self.round.board.find_block(new_block[0], new_block[1]).regular_symbol == "oil":
                                        eligible_blocks.append(new_block)
                        # pick one of the eligible blocks
                        new_oil_block = random.choice(eligible_blocks)
                        # add it to the oil area list
                        oil_area.append(new_oil_block)
                        # if it's an empty block, set it to oil block with multiplier 1
                        if self.round.board.find_block(new_oil_block[0], new_oil_block[1]).regular_symbol == "":
                            self.round.board.find_block(new_oil_block[0], new_oil_block[1]).regular_symbol = "oil"
                            self.round.board.find_block(new_oil_block[0], new_oil_block[1]).regular_symbol_extra_info = 1
                            self.frameblock[new_oil_block[0] * 6 + new_oil_block[1]].update_frame_img()
                        # if it's an oil block, increase its multiplier by 1
                        else:
                            self.round.board.find_block(new_oil_block[0], new_oil_block[1]).regular_symbol_extra_info += 1
                            self.frameblock[new_oil_block[0] * 6 + new_oil_block[1]].update_frame_img()
                        # print("symbol name: ", self.round.board.find_block(new_oil_block[0], new_oil_block[1]).regular_symbol)
                        # update the block's appearance

    def water_on_the_hill(self):

        # Water on the hill
        # For each block on the top, if it's water on the hill and it's not activated yet, do the followings:
        # Affects block below it. Oil blocks gets their multiplier halved and rounded down.
        # Oil w/o multiplier are treated as 1, halving those will get them zeroed out and removed.
        # Oil barrels are unaffected.
        # If the block below is a water on the hill, it will be activated as well. Well actually no, they can only
        # appear on the 1st row.
        print("WATER ON THE HILL")
        list_affected_reels = []
        for col in range(0, 6):
            if self.round.board.find_block(col, 0).regular_symbol == "water_on_the_hill":
                list_affected_reels.append(col + 1)
                # search for the block below it
                for row in range(1, 6):
                    # if it's an oil block
                    if self.round.board.find_block(col, row).regular_symbol == "oil":
                        self.round.board.find_block(col, row).regular_symbol_extra_info = int(
                            float(self.round.board.find_block(col, row).regular_symbol_extra_info) / 2)
                        if self.round.board.find_block(col, row).regular_symbol_extra_info < 1:
                            self.round.board.find_block(col, row).regular_symbol = ""
                            self.round.board.find_block(col, row).regular_symbol_extra_info = 0
                    # update the block's appearance
                    self.frameblock[col * 6 + row].update_frame_img()
                # change it to activated water on the hill
                self.round.board.find_block(col, 0).regular_symbol = "activated_water_on_the_hill"
                # update the block's appearance
                self.frameblock[col * 6].update_frame_img()

        if len(list_affected_reels) > 0:
            print(f"Water on the hill caused MASSIVE DAMAGE on oil fields on reel: {list_affected_reels} (if any)")
        else:
            print("No water today.")
    def fire_in_the_hole(self):
        print("fire not ready yet. come back later.")

    def popup_mode_menu(self):
        popupmodemenu = tkinter.Menu(self.root, tearoff=0)
        for mode_id in mode_dictionary:
            mode_data = mode_dictionary[mode_id]
            mode_name = mode_data[1]
            mode_cost = mode_data[2]
            mode_desc = mode_data[3]
            popupmodemenu.add_command(label=f"{mode_name}: {mode_cost:.1f} per spin: {mode_desc}",
                                      command=lambda mode_id=mode_id: self.update_mode(mode_id))
        popupmodemenu.post(self.options_button.winfo_rootx(),
                           self.options_button.winfo_rooty() + self.options_button.winfo_height())
    def update_mode(self, new_mode_id):
        spin_mode = new_mode_id
        # update total cost label
        mode_data = mode_dictionary[new_mode_id]
        mode_cost = mode_data[2]
        self.total_cost_label.config(text=f"Total Cost: {mode_cost:.2f}")
        # update options button to selected mode's title
        self.options_button.config(text=mode_data[1])
    def update_symbol_images(self):
        pass

    def do_next_task(self):
        if len(self.task_list) == 0:
            print("all task complete")
            return 0
        new_task = self.task_list.pop(0)

        if not self.task_check(new_task):
            self.do_next_task()

        task_name = new_task[0]
        sleep_before_execution = new_task[1] / 1000.0
        task_params = new_task[2:]

        if task_name in self.task_dictionary:
            time.sleep(sleep_before_execution)
            task_function = self.task_dictionary[task_name]
            task_function(*task_params)

            self.root.update_idletasks()  # Force the GUI to update
            self.root.update()

            self.do_next_task()  # Call the next task after the GUI has updated
        else:
            print(f"Task '{task_name}' is not recognized.")
    def test_print(self, msg):
        print(msg)
    def task_check(self, task):
        return True

    def add_task(self, new_task):
        self.task_list.append(new_task)
    def add_emergency_task(self, new_task):
        self.task_list.insert(0, new_task)

    def init_spin(self):
        if spin_mode != 1:
            print("Other mode(s) not ready yet.")
            return -1
        print("SPIN BUTTON PRESSED")
        self.round.reset_board()
        self.generate_board(spin_mode)
        for i in range(0, 6):
            self.add_task(["spin_reel", CONST_SPIN_SPEED, i])
        # self.add_task(["2_scatter_transform", 225])
        self.add_task(["spread_oil", 800])
        self.add_task(["spread_oil", 800])
        self.add_task(["spread_oil", 800])
        self.add_task(["spread_oil", 800])
        self.add_task(["spread_oil", 800])
        self.add_task(["water_on_the_hill", 1000])
        self.add_task(["fire_in_the_hole", 225])
        # set the block on [2, 2] to medium oil barrel for testing
        self.round.board.find_block(2, 3).regular_symbol = "oil_barrel_medium"
        # set the first 3 blocks on first row being water on the hill for testing
        self.round.board.find_block(0, 0).regular_symbol = "water_on_the_hill"
        self.round.board.find_block(1, 0).regular_symbol = "water_on_the_hill"
        self.round.board.find_block(2, 0).regular_symbol = "water_on_the_hill"
        # print(f"DEBUG: task list is{self.task_list}")
        self.do_next_task()
    def spin_and_update_img(self, reel_id):
        # set all symbols's appeared to False
        # and update the image for each block on the reel
        if reel_id == 0:
            for col in range(0, 6):
                for row in range(0, 6):
                    self.round.board.find_block(col, row).appeared = False
                    self.frameblock[col * 6 + row].update_frame_img()

        self.round.spin(reel_id)
        col = reel_id
        for row in range(0, 6):
            self.frameblock[col * 6 + row].update_frame_img()
        self.root.update_idletasks()
        self.root.update()
    def generate_board(self, mode):
        pass
this_interface = interface()


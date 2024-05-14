
import tkinter
import class_round
import time
from PIL import Image, ImageTk

from tkinter import messagebox

class frame_block:
    def __init__(self, frame, block):
        self.frame = frame
        self.block = block
    def update_frame_img(self):
        frame_size = 50
        img_path = self.block.get_image()
        image = Image.open(img_path)

        # 使用Tkinter兼容的方式转换图片
        photo = ImageTk.PhotoImage(image)

        # 使用Label显示图片
        label = tkinter.Label(self.frame, image=photo)
        label.image = photo  # 保持对图片的引用
        label.pack(fill='both', expand=True)
        print("IMG FRAME UPDATED")

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

        self.options_button = tkinter.Button(self.root, text="Click to select")
        self.options_button.place(x=400, y=60)

        self.total_cost_label = tkinter.Label(self.root, text="Total Cost: 100.00")
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
        # TODO
        # 调整元素的位置和大小, 使得看起来更恰当.
        self.task_dictionary = {
            'spin_reel': self.spin_and_update_img,
            '2_scatter_transform': self.round.convert_scatters,
            'test': self.test_print
        }
        self.update_symbol_images()

        self.root.mainloop()


    def update_symbol_images(self):
        pass
    def do_next_task(self):
        if len(self.task_list) == 0:
            print("all task complete")
            return 0
        new_task = self.task_list.pop(0)

        # 检查是否可以进行任务
        # 若某任务的必要条件缺失, 则执行下一个任务
        if not self.task_check(new_task):
            self.do_next_task()
        # 停顿若干时间
        task_name = new_task[0]
        sleep_before_execution = new_task[1] / 1000.0  # 将毫秒转换为秒
        task_params = new_task[2:]  # 剩余的列表元素是任务参数

        if task_name in self.task_dictionary:
            time.sleep(sleep_before_execution)  # 等待指定的时间
            task_function = self.task_dictionary[task_name]
            task_function(*task_params)  # 调用函数，并传入参数

        else:
            print(f"Task '{task_name}' is not recognized.")
        self.do_next_task()
    def test_print(self, msg):
        print(msg)
    def task_check(self, task):
        return True

    def add_task(self, new_task):
        self.task_list.append(new_task)
    def add_emergency_task(self, new_task):
        self.task_list.insert(0, new_task)

    def init_spin(self):
        print("SPIN BUTTON PRESSED")
        self.round.reset_board()
        for i in range(0, 4):
            self.add_task(["spin_reel", 650, i])
        self.add_task(["2_scatter_transform", 225])
        self.add_task(["spread_oil", 225])
        self.add_task(["water_on_the_hill", 225])
        self.add_task(["fire_in_the_hole", 225])
        # print(f"DEBUG: task list is{self.task_list}")
        self.do_next_task()
    def spin_and_update_img(self, reel_id):
        self.round.spin(reel_id)
        col = reel_id
        for row in range(0, 6):
            self.frameblock[col * 6 + row].update_frame_img()
        self.root.update_idletasks()
        self.root.update()

this_interface = interface()


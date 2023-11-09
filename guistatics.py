import tkinter as tk
import zlib


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 80
        y += self.widget.winfo_rooty() + 40

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1,
                         font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class GUIStatics:
    """
    Define constants and static methods
    """

    # FONTS
    # STANDARD_FONT_1_BOLD = tkFont.Font(family="Arial", size=12, weight='bold')
    # Main Window
    MAIN_WINDOW_SIZE_X = 1200
    MAIN_WINDOW_SIZE_Y = 800

    # Geometry Window
    GEOM_WINDOW_SIZE_X = 1200
    GEOM_WINDOW_SIZE_Y = 800

    # Standard Canvas Size
    CANVAS_SIZE_X = 920  # Needs to be even!
    CANVAS_SIZE_Y = 720  # Needs to be even!
    GRID_SPACE = 10  # Needs to be divisor of GUIStatics.CANVAS_SIZE_X and GUIStatics.CANVAS_SIZE_Y
    CANVAS_SCALE_FACTOR = 100

    # colors
    CANVAS_BORDER_COLOR = '#5F1010'  # Rosewood
    CANVAS_BG = '#D2D2D2'  # Light gray
    CANVAS_COORD_COLOR = '#262626'  # Dark gray
    WINDOWS_SMALL_BG_COLOR = '#D2D2D2'  # Light gray
    CANVAS_HIGHLIGHT_ELEMENT = '#5F1010'
    # Fonts
    STANDARD_FONT_BUTTON_SMALLER = ('Consolas', 8)
    STANDARD_FONT_BUTTON_SMALL = ('Consolas', 9)
    STANDARD_FONT_BUTTON_MID = ('Consolas', 10)
    STANDARD_FONT_BUTTON_BIG = ('Consolas', 11)
    STANDARD_FONT_BUTTON_BIG_BOLD = ('Arial Black', 11)
    STANDARD_FONT_BUTTON_MID_BOLD = ('Arial Black', 10)
    STANDARD_FONT_MID = ('Arial', 10)
    STANDARD_FONT_BIG = ('Arial', 12)
    STANDARD_FONT_BIGGER = ('Arial', 14)
    STANDARD_FONT_MID_BOLD = ('Arial Black', 10)
    STANDARD_FONT_BIG_BOLD = ('Arial Black', 12)
    STANDARD_FONT_BIGGER_BOLD = ('Arial Black', 14)
    STANDARD_FONT_SMALL = ('Arial', 9)
    STANDARD_FONT_SMALLER = ('Arial', 8)
    STANDARD_FONT_SMALLEST = ('Arial', 7)
    STANDARD_FONT_SMALL_BOLD = ('Arial Black', 9)
    SAVELOAD_FONT = ('Verdana', 10)

    # ICON as bytestring

    @staticmethod
    def create_divider(window, x_pos: float, y_pos: float, length: int):
        div = tk.Frame(window, height=2, width=length, bg=GUIStatics.CANVAS_BORDER_COLOR) \
            .place(relx=x_pos, rely=y_pos)
        return div

    @staticmethod
    def resort_keys(some_dict: dict) -> dict:
        """
        resort the dict (keys: str), if key is missing, assign following keys to it
        e.g {'1': 1, '3': 3, '4': 4, '5': 5} -> {'1': 1, '2': 3, '3': 4, '4': 5}

        :param some_dict: {'1': 1, '3': 3, '4': 4, '5': 5}
        :return:
        """

        # get missing key
        keys = some_dict.keys()
        mi_ma = set(range(int(min(keys)), int(max(keys)) + 1))
        missing_key = list(mi_ma - mi_ma.intersection(set([int(key) for key in keys])))
        # sort again
        if not missing_key and min(keys) != '1':
            return dict(sorted(some_dict.items()))
        else:
            missing_key = '0' if min(keys) == '1' else missing_key[0]
            next_key, last_key = int(missing_key) + 1, max([int(key) for key in keys])
            for key in range(next_key, last_key + 1):
                some_dict[str(key - 1)] = some_dict[str(key)]
            del some_dict[str(key)]

            return dict(sorted(some_dict.items()))

    @staticmethod
    def transform_node_to_canvas(node: list):
        """
        Transforms the coordinates of node from natural coord system to canvas coord system
        e.g. [1.0, 2.0] -> [300, 200]
        :param node: [x, y] in natural coordinates
        :return:
        """

        scale_factor = GUIStatics.CANVAS_SCALE_FACTOR
        node_x = node[0]
        node_y = node[1]
        node_new_x = node_x * scale_factor + GUIStatics.CANVAS_SIZE_X / 2
        node_new_y = -node_y * scale_factor + GUIStatics.CANVAS_SIZE_Y / 2

        return node_new_x, node_new_y

    @staticmethod
    def update_text_field(widget: tk.Text, new_text):
        widget.config(state='normal')
        widget.delete('0.0', 'end')
        widget.insert(tk.END, new_text)
        widget.config(state='disabled')

    @staticmethod
    def add_canvas_border(canvas: tk.Canvas):
        """
        Creates just the red border for the canvas
        :param canvas:
        :return:
        """
        width = GUIStatics.CANVAS_SIZE_X
        height = GUIStatics.CANVAS_SIZE_Y

        canvas.create_line(1, 1, width, 1, fill=GUIStatics.CANVAS_BORDER_COLOR, width=4)
        canvas.create_line(1, 0, 1, height, fill=GUIStatics.CANVAS_BORDER_COLOR, width=6)
        canvas.create_line(0, height + 1, width, height + 1,
                           fill=GUIStatics.CANVAS_BORDER_COLOR, width=2)
        canvas.create_line(width + 1, 0, width + 1, height,
                           fill=GUIStatics.CANVAS_BORDER_COLOR, width=2)

    # shared method
    @staticmethod
    def add_canvas_static_elements(canvas: tk.Canvas):
        """
        Adds coordsystem and grid to a canvas
        :param canvas:
        :return:
        """

        width = GUIStatics.CANVAS_SIZE_X
        height = GUIStatics.CANVAS_SIZE_Y

        # grid
        for x in range(GUIStatics.GRID_SPACE, width + GUIStatics.GRID_SPACE, GUIStatics.GRID_SPACE):
            canvas.create_line(x, 0, x, height, fill="dark gray", width=1)
        for y in range(GUIStatics.GRID_SPACE, height, GUIStatics.GRID_SPACE):
            canvas.create_line(0, y, width, y, fill="dark gray", width=1)
        canvas.create_line(1, 1, width, 1, fill=GUIStatics.CANVAS_BORDER_COLOR, width=4)
        canvas.create_line(1, 0, 1, height, fill=GUIStatics.CANVAS_BORDER_COLOR, width=6)
        canvas.create_line(0, height + 1, width, height + 1,
                           fill=GUIStatics.CANVAS_BORDER_COLOR, width=2)
        canvas.create_line(width + 1, 0, width + 1, height,
                           fill=GUIStatics.CANVAS_BORDER_COLOR, width=2)

        # coordinatesystem
        canvas.create_line(width / 2, 0, width / 2, height,
                           fill=GUIStatics.CANVAS_COORD_COLOR, width=1)
        canvas.create_line(0, height / 2, width, height / 2,
                           fill=GUIStatics.CANVAS_COORD_COLOR, width=1)

        # text_values
        text_color = '#575757'
        div_color = '#404040'
        x_it = 0
        for x in range(int(width / 2), width, GUIStatics.GRID_SPACE * 2):
            x_text = x_it / GUIStatics.CANVAS_SCALE_FACTOR
            x_it += GUIStatics.GRID_SPACE * 2
            if x_text == 0:
                x_text = 0
            canvas.create_text(x + 4, height / 2 + 10, text=x_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(x, height / 2 + 3, x, height / 2 - 3, fill=div_color, width=1)

        x_it = 0
        for x in range(int(width / 2), 0, -GUIStatics.GRID_SPACE * 2):
            x_text = x_it / GUIStatics.CANVAS_SCALE_FACTOR
            x_it += GUIStatics.GRID_SPACE * 2
            x_text = '-' + str(x_text)
            if x_text == '-0.0':
                x_text = ''
            canvas.create_text(x + 4, height / 2 + 10, text=x_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(x, height / 2 + 3, x, height / 2 - 3, fill=div_color, width=1)

        y_it = 0
        for y in range(int(height / 2), height, GUIStatics.GRID_SPACE * 2):
            y_text = y_it / GUIStatics.CANVAS_SCALE_FACTOR
            y_it += GUIStatics.GRID_SPACE * 2
            y_text = '-' + str(y_text)
            if y_text == '-0.0':
                y_text = ''
            canvas.create_text(width / 2 + 10, y, text=y_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(width / 2 - 3, y, width / 2 + 3, y, fill=div_color, width=1)

        y_it = 0
        for y in range(int(height / 2), 0, -GUIStatics.GRID_SPACE * 2):
            y_text = y_it / GUIStatics.CANVAS_SCALE_FACTOR
            y_it += GUIStatics.GRID_SPACE * 2
            y_text = str(y_text)
            if y_text == '0.0':
                y_text = ''
            canvas.create_text(width / 2 + 10, y, text=y_text, fill=text_color, font=("Helvetica", 6))
            canvas.create_line(width / 2 - 3, y, width / 2 + 3, y, fill=div_color, width=1)

    @staticmethod
    def get_polygon_center(nodes: list):
        """
        get the center of the polygon (approximately)
        :param nodes:
        :return:
        """
        num_vertices = len(nodes)
        if num_vertices == 0:
            return 0, 0  # Default center if there are no vertices

        # Calculate the average x and y coordinates
        avg_x = sum(x for x, y in nodes) / num_vertices
        avg_y = sum(y for x, y in nodes) / num_vertices

        return avg_x, avg_y

    @staticmethod
    def window_error(root, error_message: str):
        """
        Custom Error Window
        :param root: tkinter root or toplevel
        :return:
        """

        window_error = tk.Toplevel(root)
        window_error.title('ERROR')
        window_error.geometry(f"{300}x{300}")
        window_error.resizable(False, False)
        GUIStatics.create_divider(window_error, 0.025, 0.05, 275)

        # error message
        tk.Label(window_error, text=error_message, font=GUIStatics.STANDARD_FONT_BUTTON_MID) \
            .place(relx=0.05, rely=0.2)

        GUIStatics.create_divider(window_error, 0.025, 0.95, 275)

    @staticmethod
    def check_line_intersection(line1: list, line2: list) -> bool:
        """

        :param line1: [[x_start, y_start],[x_end, y_end]]
        :param line2: [[x_start, y_start],[x_end, y_end]]
        :return:
        """
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        def calculate_slope(point1, point2):
            if point1[0] == point2[0]:
                return 10e3  # stupid workaround for not defined slope TODO
            return (point2[1] - point1[1]) / (point2[0] - point1[0])

        m1 = calculate_slope(line1[0], line1[1])
        m2 = calculate_slope(line2[0], line2[1])
        if m1 == m2:
            return False

        x_intersection = ((y3 - y1) + (m1 * x1 - m2 * x3)) / (m1 - m2)
        y_intersection = m1 * (x_intersection - x1) + y1
        if (x1 <= x_intersection <= x2 or x2 <= x_intersection <= x1) and \
                (y1 <= y_intersection <= y2 or y2 <= y_intersection <= y1) and \
                (x3 <= x_intersection <= x4 or x4 <= x_intersection <= x3) and \
                (y3 <= y_intersection <= y4 or y4 <= y_intersection <= y3):
            if (x_intersection, y_intersection) == (x1, y1) or \
                    (x_intersection, y_intersection) == (x2, y2) or \
                    (x_intersection, y_intersection) == (x3, y3) or \
                    (x_intersection, y_intersection) == (x4, y4):
                return False
            else:
                return True
        else:
            return False


    @staticmethod
    def return_icon_bytestring():
        """
        return deocompressed icon data for icon creation
        :return:
        """
        compressed_icon_data = (b'x\x9c\xedX\x87WT\xd7\xd6\'\xd1\xe4\x99D\xa3\xd1g}jb\x07\xa4Ig\x06f\x98\xde+L\x05\x06d'
                                b'\x98\x0eH\x1b\x90\xde\x06\x98z\xe7\xde\x99\xa1\x08R,Q1\x96$\x9an\x8aQC\x99\xa1\xcc'
                                b'\x0ch\x14\x93\xe8K\xf9\xea\xff\xf0}\xe7:<\xe2S\x8cyk\xbd\x95o\xado\xbd\xcd\x9d\xcb9'
                                b'\xfb\xees\xef\xef\xee\xfd;\xfb\xecs\xc3\xc2^\x00\x7fq\ta\xe0\xbc%\xaclgX\xd8\xa6\xb0'
                                b'\xb0\xb0p\xf0\x8b\x03?uXH\xff/\xf9\xff!]\x99|+\x85m&\xd1\xcd4\x86\x99\xce\xb40Y\x9dT'
                                b'\x9a\x99\xce\xb20X\x16\x1a\xd3Jc\xd9\xe8l\x0b\xd03\x98@\x0f\x0e+\x9d\xe1\x140m""$%C2'
                                b'\x8a]JrH\xc9v\t\xc9)\xa7B2\xb2]LDr\xd0\x86CB\xb4K\x08\x0e)\xd1)\x07f$\xbb8\x13\x96'
                                b'\x91!\xa0\x91\x10B\x1a\x87\x8c\x04\xe5P\x9cR`I@\r\xa4\x99\xa7\x1d\xed\xc1@\xa0\x19'
                                b'\x9b\xdb\x92&\xe8\xc4\x8b\x10^~\x07\x91=\xa0P\xd99B\x1b\x93\xe3\x16\x89\xc1y /\xdfLc'
                                b'\xf6\xc8r\xac\x1c\x9e\x9d\xc3\x1b\xc8/\xb42\x98\xfdJ\xb1+\x8f\x8e\xe4\xd1{\x8a\xf8'
                                b'\x90\x9cz\xbcD\n\xe5P=\x87\xb9.\x05\x0b\xc9\xa1\r\xeaE\x0e)i\xa8D\xee\xceg@rJ\x9f\x8a'
                                b'\x0f\xe7P\x8e\xeb\xb3\xec9\x84\xc1b\xc11=\xd7\x9eG\x1c)\x17;\xf2I}\x06.\\@\xee\xd52'
                                b'\xfb\r<\xd0\xb8\xd4k\x06x\xcac\xa5\x05\xbb\x08K\xee\xb2P\xc5\x1ddn\'\x99ie\xb1m\x0c&"'
                                b'\xcc\xb62XV\x06\xbb\x83\xca\xb00\xd9\xb5$\xca\xef\xf1y3/\xa3[\xc9\xae`\'\x85\xba\x9c'
                                b'\xc4\x9d.\r\xc1Q\x94\x06\xa93\x96lj\xc5\xf1.C&P\xaa\xe8\xe1!M\xb5.\x17\xe0\xd1Ed\x17'
                                b'\xec\xa2.\x99\xb5c\xf8\x8d\x89\x0c\x13\x8ec\xa3\t\xba(\x0c\x1b\x9d\xd9E\xa6@\x1c\xae'
                                b'\x95\xcdi#\x92+\xb0\x19a\xbfC\xda\xc4\xa9nUz\x05\xef`\xa8\xcbM\xd9\x0e\xeb3`\x1d\xb6'
                                b'\x82\x1f\xb9d\xa3\xa4\xef\xeb\xad z\x8e`\x0bio\x854\x95Zi\xd0\x1fp(\x9brw\xfe\xfa\xd6'
                                b'.za[\n\xd7B\x96 \x02\xa5\t\xc7\xee\x97(,4\xc6@\x9e\x02\x11\x89A\xe0Z8\xfc\xdf\x85\'7i'
                                b'\xc8\xc84fE\x87\xba\xbc\xd4\x1d\xa7\xda\xb2\\\xe5\xa9\xf9\xac=K6\x94\x94M\'\xcd\xdc'
                                b'\xde\xa3\x19*\xde\xa2\xb2\xb6,\x07\xe09\x03\x8fd\xaf\xc7\xfd\xea\xc6C\xfc\xd6dAk\n'
                                b'\xb75\x95\xdb\x9e\xc6\xed\xcc\xe4\xd9\x19\\\x10\xb2N:\x03\xe0)\x7f\xcc?v)\x11B9L\x05'
                                b'Lv\xe4\x10a%\xc1\xa5\xc6!\xeatD\x8b\x83\xb5\x19NmzE\xf6\xa2\x7f\x04\xf8\xed\xce\xca'
                                b'\x04\xc4\x98\x90p`\xf5\xd2\xf0\xd7_}\xd1y4\xc5U\x9b\xa0\xccz3\xa4\xa9*\x11\x83xy\xbf'
                                b'\x1c\x93\xef\xa3/\x99At]c|V+6\xcbL\x95\xb5\xa4r\xfb\xc4j3\x85\x8f\x08%V6\xcf\xc6'
                                b'\xe4619\xbfZ\xe6\xd1\x8e\xe9Dv)\xf9\x98>\xdb\x9e\x8f\x1f>\xca\xef\xaf`\xb84\xb8\xa1'
                                b'\x1a\x01\xa4\xc1\x9el\xe2\xd7(b\x17\xe3\x85\xdb\xeai\xc1w\x96\xc7<\xe1FK]\x9a\xab\xf5'
                                b'\x90&go\xa8[]\x0e\xf0\xf8\xfd\xd3\xb3*\xb2l\xc9\xa6.6\xbb&\x92W\x17\xc7jNa\xb7\xa5p'
                                b'\xda\xd28\x1d8\xae\x99\xc2\xee \xd3A\x12(\xc3\xa4/YZ\xc5\x99\x00\x8cCFv\xe6\x93\x9dJ'
                                b'\x9c\xcb@p\xa8\xb0.\x1d\xce}$\x13)OB*\x93\xcb\xe5\x07\x16\xe3E\xdc\x8c4\xc5U\xa9\x16'
                                b'\xe3\x12\x15\xbe*\xd4\xd0+\xf78L\x11Ey\xdb\x17\xfdS.\x02\xfe\t\x06\x83\xf6\xfa\xae'
                                b'\xa5\xa74\xc6K\xcbv3\x9b\x12\xb3\xac\x94\xbc\xd6$\x96\x19\x97\xdd\x92\xc2r\x0b\xe5'
                                b'\x10_h"\x93\xeb)\xbf2\x1fLg0\x97\xed2\xe2\xb1R\xaeKKp\x1b\x88=G(NMjo\r\t\xaaJ<\xd6D'
                                b'\xae*\x88\nY\xf2)\x9b\x8fY\xf0y\xd9\x8b\xcf-\xd1-68\xcc-\xdd\xf0\xa1\xc2\xfc\xad'
                                b'\xa1nM\xb5\x18\xf0\x07\xe097|&\xec\xd9\x12\xb9z\xa3[\xa8p\nEf\n\xa5\x96D\xfe\r\xcb'
                                b'\x90t\x18\xb0\xce\xaa\x84\xe1\x0ej\xadfq6\xf1\xe8\x1b\x87\xbb\xf1\x98\x14\x94<\xabV'
                                b'\xbd`\xb1\xee\xc3`\xde\x00\xed-[V\xb8\xfb\xa2\x0b5\x8bxjk\xc5!\xff\\\xb9|\xe57\xee'
                                b'\x7fp\xcd\xa6\xf6\x0c\x96\x99J\xb7\xd2\xe9\x15\xd8\xf4\xdf\xb0\x0cI\x93:\x1e\xaeNp5DW'
                                b'\xa9v\x874|\xf6zK\xe7b\xb0\x08\xd4\xd5\xf0@DN\xe1\xe6P\xb7\xae\xebM\x85~q\xb1\xaf\xac'
                                b'\xce\x9a{\x84\xe7\xea\xd5\xab\xbf\x8d\xc7\xc6\x9088\x02+\x8b\xd5\x91\x95\xfd\\<p-'
                                b'\ri84\x04e\x1a\xb5\xfbB\x1a.w]s\xdb"\xb75\x95oA\'\xf779\x0f\x85\xba\xea\xba7\x0b'
                                b'\x8d;C\xed\xea&\xf1\\\xc0\xff\x04\x1e\xd5\x0eNe\xb8\xb0l/\xd7x\x80\xdb\x18/hK\xe5'
                                b'\x990\xdcV,\xd3La\x82t]\xf9\x98\x7f\x1c\x12\x12\\@E4xD\x83\x835X\xa4,\xddY\x91\x0c'
                                b'\x1b\x93]\xf5i\x9e\xb6D\xb85\xc6\xa8\xff\x9b\x7f\xb2\xd7\xe7\xaa6\x86\xdaG\xe1\xdd'
                                b'\x96\xb3\xe1\xa6\x91\x88P\x97\x91\xb3!\xcf\xf8\x97P\xbb\xac1{\xce\xff$\x1ec\x92R\xbf'
                                b'\x97_\x97\x9cg"\xa8jb\xf96Z^K\x1a\x07\xe6\xe5\xbb\xb2d`U\xad\xa3\xff\x9a\x19z\n\xb9`'
                                b'\x01r\xeb\x08\xa7\xea\x84\xae\xe2\x8cc\xf5\x94c\x8d4\xb8\n3df!\xadI\xc3.Z]\xd5b\xfe'
                                b'\xe1\x897\x12Y\xdb@c\xdd\xe6\x15\x96\xcb\xe9\x96+\xe9\xceO\xe9\t\xb4\xf5@\xb3u\xdf'
                                b'\x9fdG\x17\xddX\xda*\x0b\xf1\xf9q<G\xc2%\x9a\xad\xf4\xa3\xd1\xa2\xfad\xb91\x9c\xd3'
                                b'\x89\xc9jMbZ\xc9b\x1b+\xab\x9dL\xab\xc2e.Y\x82|\xe8VSA\xf6\xeb;B\x85t\xa9}u\x99\x881'
                                b'\xd5U\x9f2`&9[\x0ey\xec\x87\xca\xcb\x16\x13\x1d\x91\xbdn\xe5K/\x80\x06A\xb1\xcdt\x8d'
                                b'\xd8\xf4\t\xbe\xe5s\x1a\xbfv\x91\xed\xe9\xb2m\xa1F\x89i\x19<\xea\x9d\\\xedvn\xe9'
                                b'\x1evE\x04\xd7\x18)0a$\xedi\xbc\xb64\xae\x89\xc0239Ux\xe2\x92%\xa2\xa0z\x0c4\x87:'
                                b'\x1d,\x8bp\x19\x16\xaeJu\xd7\xa4\xc3\xb5\t\xee\xd6d\xa4=\xbe\x07N4\x1a\x17\x13\xdd'
                                b'\x9a\xf5/\x84\x1a\x12(\xb5\xe2kq\xc5-\xc9\xd1or\xf3G\x16\xa7\xea\xab\x9bV\x86\x1a'
                                b'\xba\x8e\xdc\xb9\xa7\xf0,+\xabW\xbcdg\x88\x1c\\a\x87\xf0\xf9|\xc6&l\xf4t\xc5\x9f\x1e'
                                b'\xa4\xd5\xd5G>q\xa9\xe8c\x952\xd8z8\xd0X{\xbbUsS\xf9\xc4U\xadY\xf9\xb4\x7f\x96\x95W^'
                                b'\\\xd1\x91\xc9\x01\xe5Y\x05\xe6\xf9\xf3=1f\x8d\xcb\x1c\x878"\x8d\xb5;\x1f\xd7\xaf;'
                                b'\xb0\x861\xdf\x9d\xf6\xdd\x07\xf8\x85\xb3\xfc\xdb\x8e\x9c`\xc3~Y\xec\xdf\xa1\xb5\x14'
                                b'\xfdN<\xaf\xadX\xe9\xe4\xe5\x98\x19\xac\x06&\xfb\xb9x2\xd2v]z\xbb\xf6\xbd\x8bm6{\xe1'
                                b'\xe3zN\xa5\xb4\xee\x87i\xdc/?\xc6\xfe0\xc6\xfe\xe12\xfb\xee1\xa2\xa7\xe8\xef\xf0@'
                                b'\xfa\xe0\xa3\xf9\xbe$\xb3\xbe\xd9\xfa\xac\n\xe5V^\xdezz\xf9>~e\x04\xffh\x8c\xa0=U'
                                b'\xd8\x9c\xc2\xec"qM$\nX\xe2\xed\x02\xba\'\x97\t\xc9iv\x05\xdee AE\xe9Hi\x86\xa3"\xd9S'
                                b'\x83\xf54\xa48\x1b\xa3\xbb\xcd\xe4\x89\xeb\xe7n\xcf\x81;\xfb\x03s\xb3\xfe\xe0\xac'
                                b'\x1f=\x07f\x83\xc1/\xe7\xee\xa6\xfd\xf8K\xf8C\x7f\xf2\xfd\x8f3\x16\xde\xe6\xdc\x1d'
                                b'\x14\xcd[\x85\xc1v\xf9\\\x974\xd8\xd15\xd6\xf7\x04\x9e` x\xceuB\xb1\x81\xae}+\xab.>'
                                b'\xb7\xfc\x00\xa7&.\xbb!\x89c&KZ\xf1,\x1b\x8b\xeb\x12I\xac\x02\x1a\x92\xc7\xb4\x89\t'
                                b'\x1e\x1d\x1d\xacY`~\x1d\xab\xa3#\xc64w\r\xd6\xdd\x90\xeanK\xee\xee\xca\xe8\xb6R|'
                                b'\x13Wn\x07f\xe7\x02\xc1\xf9\xbf\x1d@n\xce\x7fK\xfe\xe9\xbf"\x1f|\x9b\xf8\xd7q\xec'
                                b'\xc2{\xf4\x85s\xf4{\xc3Yw\xba\xf3\xe6m\x92\xf9.\xcb\xc4\xe0\x93x\xc0\x90k7\nv\xb1'
                                b'\r\xfbDM\x18Ue\xb8\xa0\x05\x93\xd7\x92\xc2s\xb2\xf3;)B\x07[\xd0\xab(pd3zT\x02P\x8d'
                                b'\xf7\x18\x98}\xe5L\x97\x1e?\xd2.tU\xa7{\xea\t=\xad\x19\xdd\xa6\x94A\'\xc3i\x8e\xeev'
                                b'\x91n}}\x0e]\x8f\x02\xc1\xb9G\x07z\xf3\xdb\xf7\x18?\xffw\xdc_\x1f\xe2\x7f\x9aI\xfe'
                                b'\xfe:\xfb\xbbK\xcc{g\xd9\x0b\xa3\xb9\xf7O\xf3\xef@]\x13#O\xe3\tL\xfb\x8d\x02\xed\xe1'
                                b'\xcdl\xcdvnU\xb8\xb02\x9c\xdb\x9e,hKaw\xe2y\xa0\xa8F\xe3\x95E\x87\xe54\x87\x8c\x08)q'
                                b'\x88>\xd3\xa9\x033\x1d\x03U&#\xb5)\xdd-\xc9pS\x9c\xb3#\x11q\xc4\xba\xe08w7n|\xf2B08'
                                b'\x9d\x9b\x9b\x1b\x15\x15UZZ\xfa\xeeW\xd7\xd3~\xfa\xf7\xfd?\xff[\xc4\xc3\xa9\x88\x87'
                                b'\x13\xe9\xf7? ,\x9c\xcb\xb8w&\xfd\xfe\xdb |\xf5\x93\xef<\x8d\x07\xc8\xf9\x9e\x13\xaa7'
                                b'\x85uI\x85U\x07\x04V\x92\xae5I\xe0f\xe7;\xd9 ?\xb3\xfa\x15\nHD\x1b)\x95!\nro\t}\xb8.'
                                b'\x0b6`\x87L\\\xb8:u\xa0\x93\xdc\xd7\x95\x89\xb4\'\x8d\xf42aG\xf4\xc8\x10\xc9}<\xde9'
                                b'\x8c\xbd>q\x1a\x87[\xac*c\xe2\x13\x08\xf3w\x0f\xfc\xf2\x1f)?\x07\x0f>\xf4R\x7f\xbcIY'
                                b'\x18%\x7f7\xca\xfc\xfe"\xe1\xde\xd9\x96\xa9\xf7\xe7\x9e\xc6\x13\x98\xfb\xf2\xa3\xcf'
                                b'\x0bwrt\xdby\x95\xfb\x04\xe5\xfb8M\xf1<S\x1a\xa7+\x93\xd5E\xa1\x83]\x18,\xa1\xdb\xc1'
                                b'\xf6J\x96\xd1\xad\xc9\x04\x8b\x05R\x8cq\x1b1\xee\xea\x14\xb8!\tj\x8eG\xda\x0fu;\x12'
                                b'`(\xca\xe9\x89\x80\x06\xc2\xed\xc3\x11\xdd\x97h\x9f\xdc:=335\xd0\xdf\x0f m\xad0\xee'
                                b'\xff\xe9?\xf7<\x9c=\xf0\xc0\x17\xf7\xc3\r\xdc\xbd\xd1\xcc\xfbg\xf0\x0bg2\xef\x9f\xad'
                                b'\xf7^\xf2?\x1d\xaf@\xd0?\x15\xe8,\xa8-;(\xab\xd8\xc7\xef\xcaT7\'\n\xcdDq\x17\x99ger='
                                b'\xf2\x1cHL\x1d,\x96\xba\x0b\xa9n\x1d\xdeSFu\x97aFLt\xb8*a\xd0J\xea\xb5\xe0\x9c\xa6'
                                b'\x98\xe3\x1e<\xec\x8c\x1c<\x8d\xb7\x0cD\xc0\xa3\xb1\xf0e\x9c\xfd\n\xe5\xf3\x99\xd1@p'
                                b'\xc6PU\r \xed\xb9v\x1d\xf3\xd3|\xc4\x03/\xee\xe1\x18\xe3\xfe\x05\xd2\xc2\x19\xce\xf7'
                                b'\x17\x89\x0b\xa3\xcd\xbew\x03\xcb\xc5k.\x18<\x01\x0f\x95\xec\x93\x94\xbc\xc5i\x88'
                                b'\x93\xb4$\nMX~\'\x91ma\xb0aq6$\xa6\xb8\x14LW!\x11Q\xe3<z\xa2\xa7\x1c\xd3[\x9f\x89'
                                b'\x16\x84`Zu\xa6B]\x07=\xced\x08\x89\xe8\x19I\x82N\xc6X\xcf\x1cp^\xc5\xb5}\x82\xb7'
                                b'\xdc<\xfc\xd1\xdc\xc7\xef~}\x03\xe0y%//\xe1\xc1t\xd4\x03/\xe6\x87/Iw\xcf\x81\x90'
                                b'\xd1\x16FI\x0b\xe7\x1b}\x97\x97\xe5OSS\x13\x18E\xfcs\xe2\x91= \x05\xf1\x1a\xe3Y\xed'
                                b'\xe9\\\x0b\x8d\xd7N\xa4\xd4\x93\xd0\x9d#~\xffv[^\xbaKG0\xab\xd0\x8dI\xcc\xde\xd7'
                                b'\xe1\xa3\xa9Ps\x82\xad9\xcem\x8fq;\x93\xf3\n\xd0\x92O\xdf\xf0\x17\xdb\xf9\xa8\x8e+'
                                b'\x89\r_P\xca\xc7\x0br\x82\x1e\xe7\xdd\xd9\x15\xbb\xd0"d\xcf\xd5SQ\x0f\'\xf0\xdf]%'
                                b'\xdf\x1b\xc5\xdf=K\xbd?\x9a\xb1p\xb6n\xf2\xe2\xb2x\x06\x07\x07\xc1\x10j\x0c\xae\xeaP'
                                b'\x96\x85Z\xd4\x8a\xe59\xf9\x8a.6\x1f\xecO\xbb\x15\xb2WW\xbe\xb8\xfe\xd5\x97\xed\x87q'
                                b'\xbde\xf4\x91:\xe1\xae-\x7f\x02\xc6\x96\xf2\xc4\x01\x1b\xb9\xdbB@\xacq\x83\xbd\xd4r#'
                                b'\xfaP\xa9f\xa7\xedB"\xf4\x19\xe7\xe8\x17\xec\x9a\x99\x1a\xce\x9d\x13\x84\xf9\x89\x10'
                                b'\xb1\xd7g3\xd3\xee}$}\xf0\x1e\x7f\xe1<\xf5\xde(\xff\xbb\x0b\x94{g\x9a\xa7\x96\x8f'
                                b'\xd7\x87\x1f~\x08\x86\xecX\xbb\xa91\x91\xe7\xe1i\xacD\x91++\xcf\xc1\xcf\xee S\xecB'
                                b'\x1av\x0f\xfa\xee\xad9i\xb0\x06l9qL\x0cZ-\xd4\xab#\x91\xd6xG[\x9c\xcb\x1e\x05;bM6tg'
                                b'\x91B|\xcd\xf2Nt\xc7\xd5\xa4\xda/h\xc5cE\xdc;\x9e\xc8/\xd07]\xb9\x7f\x078G\x9fo!'
                                b'\xdc?C\x00L^8C@)}\xf6\xe8\xe4\xc5e\xf1\xf8|\xbe\xd0[\xd4%0<\xfc"\x0bI\xd0\'\xcfGDR'
                                b'\x07\x8fw\xea\x88R\x96\x82\xae\xdaU\xd9I`7\xd1k\xa4+yh5\xa5\x95\xec\x1d\xb0\xe1<'
                                b'\x96\xd4n8\xf6\xd4\t*\xd4\xb7\x7f\xe3\x96\x15+^\n\xb3\x8c\xc6A\x9f\x91\x1b?\xa74M'
                                b'\xe9\x15\xfe\xc6\x8cs\x15h|\x87\x8d+6\xaf]K\x8dg/\xbc\xcdZ\x18\xceZ\x18V\xdc\x1f\xe6'
                                b'\xdfv\xb5O\x9eX6^@\xf8<\x1eJ\x80\xa8\x8c\x0e<\x07l\xbe:\xe9,3\x8b\xdbF#CrF19'
                                b'\x11\\R1\x13\xc0\x86\xcbY\x96iT\xa0E \x1b\xb7\x19dfG{\xb4\x1b\x8a\xf6\xb8\x12]\xc7'
                                b'\x0e\x12\x18kP\xd8\xf0.\xcb\xd54P\x80\x19\xaf\x0bt\x93\x1a\xacM\x08\x94\xb4\xcf\x8c'
                                b'\tVt\xc7\x87\x1f\xd1d\x05\xbb$\xf3f\xf9\xbcE\x14\xec0\x8d\xf5\x83\xc5nY<\xcd\x8d'
                                b'\x8d\xc0>\xf7`\xbc\x13\xd4<T\x06,\x14w2XV!\xb3\xa7H\xd8\xc8\xc5\xa3\xec\x8a\xddq'
                                b'\xdc\xc8?\xd9\x92k-As\xdd\xfe\x9d\xaf\xb8\xdbS\xbami\x88-\xba\x1bIE\xfa\x0e\x1e\xd6'
                                b'\xa3AQ5\xbei\xbb\x9a\xda\xf6QF\xcb\rQ\xc5D~\x82\x01\xfd\xe2!\x1ao\x90\xf9L\xabv\xbd'
                                b'\xb1\x01\xb3[4\xd3.\x9a\xeb\x94\xcd\x9b%s\x1d\xe6\x89\xfe\xd9\xc0\xf2x\x86\x87\x86'
                                b'\xd0\x17\xd9\xbd\xafW\x9acep ~\x96\x85\xcd\x84\xa5\xcc\x1e\xad\xc8,"\x81K\xdb\xd6'
                                b'\xbe\xdcSJ\xee7r\x1cz\xec\xd6\r(\xa5{L\x8ca\x17\xa3\x0fN\xee\xefMw\rD\xd5\xb6\xa3a'
                                b'\x15\x16nr\xbe\x8f5}\x90\xd2uSRs\x9d\xff\x16a\xfb\xaa-\xab\x94\xber\xed=[\x9aS\x8a'
                                b'\x16\'\xfd\n\xf9\x1ds\xfe\x1d\xabx\xde\xd49y\xfcY\xfe\xf9\xe8\x83\x0f\x80\xf1\xae5'
                                b'\xaf\x9b\xe9l\x0b\x8dac\xb2m<\xa6]D\x82\xe4dDN\x89\xdf\xb1\x01\\\xedP$"\xda\x0cWI:)'
                                b'\x11\xddL\x95\xe4F\xf5td\x0e@\xd8\xb3#\xd9pwL\xbb\r\x9db1\xc9/\xdb\xceGv\\\x89o\xf8'
                                b'\x14W\xf9\t\xfa\x15e?\x7f\x8fz\xa2P=\xa5\xcf\x19;\xb2:r\xd3\xeb\xb1[\x05SM\x92\xf9N'
                                b'\x80\xa7c\x0c\xf8g\x19\xfe\x04\x02\x01\xdf\xe4\xe4\xca\x17_\x04\xc3!\xb1\xcc\xccd'
                                b'\x1d+(\xecQH\x1d2\xfapy.$\xa7\xe4\xe1\xd0\x0f\xb7\xf5\xb2\xe4\x81J\xb6\xe7\x08\xce C'
                                b'\xa3\x90\x1a\xbd\xb1\xdfL\xf6t`F\xba9\xbd\x1e\xcc\xc9S\xf4\xb5o\xa0w\xe8y\x87d\xbd'
                                b'\x82\xb1~%,9\x8f\x16\xcc\x84\n\x8caR]\xe5/7xu\x02w\x16\xd0P`\xc1\x91om\x8a@\x8b}bh'
                                b'\xf6\xd1~p\x19H33\xc9{\xd1\x89S\x96\x9a\xdeIeXY\x1cg6\x03\xfd\x1e(\'9d\x14M&Zg\x16Q'
                                b'\x0e\xc0j\x9c\xab4\xbd<g\xf1;O\xa1x\x17\xdc\x1a\xef\xeaJE\xa0\x18\x18\t\x8f\x8e{\x19'
                                b'\xc5s\x9e\x00\xbd\x9ff\xfe\x84U\xd4\x8f\x05]V\'N;^\xa4\xf7\xaa\xf5\x93\x1a\xed\xad'
                                b'\xa2?\xc7nX\xbd\xfb\xb5\xa2\xebE\xeaI\xad\xe3\xa6\xc3\x1f\\~~\x81\xcaNLF\xdd\xab'
                                b'\xa11Lb\x99\xfd\xf0agQ\x0e\xa4\x91\xf4V*mE\xd9\xedJ\xb4\xaa\x17dD\x1do8\x0cW\xf1\xec'
                                b'\xd5\xe8k\xc6Gn]\xfd\xeaJ\xb9 \n\xe9\xcar9\x18]\x9d\xcc\x95+_\xd8\xb6}\xd5\xf1\x0b'
                                b'\xa2\x9e\xf3\x82\x13\x9fi5\x9d\xa8\x7fd}\xb4R\x9f\xae~\xceX\xe2\xd3V\xf8K\xd8\x1e'
                                b'\x06P\xd2\xad4\xc3\x94\xd6=\x86,\x1b\xaf\x90\x8c<\xca\xd2\xa5\xc5%\xb3>\x9f\x7fz'
                                b'\xda?\xe5\x9d\xf1M\x06f\xa6\xa6}\x13\xdf\xdc\xbc\x0e.a\xb1\x98\xd9i\xef\xf4\xd4'
                                b'\xf8\x94w|\xed\xda\xd7ssd\x97.\x8eFGG=^\x12CN\x8b?89\xe3\x1f\x9f\rx\xeb\x9bjQ\xaf'
                                b'\x9e\x97\x96\xf8TU\xb3G\x80\x7fJ\xa6t\xea[\x85[\xd3\xb6\xbe\xb2uU\xe1\xe7\x05\xd0'
                                b'\r\xc7\xb3\xe6\x17\x90O?\xfd\x14\x0c?t\xe8P`\xb9\x98\xe2p\xe8\xca5>>\x1e\xeaJ\xa5'
                                b'\xd2m\xdb\xb6\xf9\xfd\xfe[\xb7n\x99L&p5!!\xc1l6\xcf\xcc\xcc,\r\x01U\x19\x18R\x0c'
                                b'\x1c5\xa1\xd4yU\xba\xc9\xa2\x12\x9fA\xefS3{\xd0o8\x84f\xfc#<\xcf\xf4\x0f\xb8\xd5'
                                b'\xbau\xeb\x80\xe5\x8d\x1b7\x9ee\xf3\x8f\x8aw\xde\xd78Ug\x98\xd0\x1ag\xcbK\xbd\xda'
                                b'\xda`u\xd9TI\xf1\x94\xa6b\xb6\x14\xd0\xdb5\xe6z\x16\x9fC"\x97\xcb\x01\x9e\x0b\x17.'
                                b'\xfc\xb3\xf0L\x06\'\xaa\xc6\xcbt\x93*\x83W\x0b(\xad\xf3\xa9\xc0\xa1\xf5*\xf5\xbe"'
                                b'\x83O\xed\xf8\xda\xf68\x1e\xe0\x90U\xabV-\xb3\xa1\xfa{\x01\xb1\x00\xc6\xd7\xae]C\xd9'
                                b'\xae\xd1\xfcCx\xa6n\xfbj\xbd\x80\xc9\x80\xcf\xf5\x06\xaf\xba\xcc_\x0c\x80\x95N\xeb'
                                b'\x8d\xc1\xaab\xaf\x1a\xb9\xe5|\xc2?\x12\x89\xe4\xb9xB\xb4\x01T\x01%:\xe0\xcc\xe3'
                                b'\x0cy\xaex\xe7&+\xc7K\x80gJ}\x86b\xaf\n`\xd0O\x14\x15O\xa9K\xa7\x8a\x8b\'\xd5\xb6'
                                b'\xeb\xd0\xeco\x85\xeb\x9f/\xde\xb9\xf1\xea\xa92\x95\xb7@?\r\xf2\x8f\xb2b\xa6\x18'
                                b'\xf0Y\xe3-\xd4O\x81x\x159o"\x7f4\x9e\xf9\xc9\xda)\xa3\xcaw\xd8\xe0\xd7\xea|\xca'
                                b'\xea@\xb9aZ\xad\xf2\x15\x18f\xd5j\xdfa\xe4\x1b\xd7\xcc\x1f\x8bg"8V9Q\xaa\xf7j\x0c'
                                b'\x8f\x8eb\xafF7\xa9\xd4{\x95\x064]\xab\xa0\xaf\xe0\x19\x7fp\xe2\x0f\x94[\x937N\xde'
                                b'\x18\x1e\xfaz\xe8\xe4\xd8\xc9\x91\x1b\xc3\'n\x8d\x0c\xdf\x18:qk\xf8\xd4\xd8\xc9'
                                b'\xe1\x9b\xc7/\xdf\xbc\xe8\x0f\x04\xff\xe7\x91\x84\x85=\xf9\xff_\xf2\x7f+\xff\x0b'
                                b'\xf9!\xa0w')

        return zlib.decompress(compressed_icon_data)


if __name__ == '__main__':
    line1 = [[0, 0], [1, 0]]
    line2 = [[1.0, 0], [1.0, 1]]
    print(GUIStatics.check_line_intersection(line1, line2))
import tkinter as tk
from typing import Any, Union


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
    def window_error(root: Union[Any, tk], error_message: str):
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
        tk.Label(window_error, text=error_message, font=GUIStatics.STANDARD_FONT_MID_BOLD) \
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


if __name__ == '__main__':
    line1 = [[0, 0], [1, 0]]
    line2 = [[1.0, 0], [1.0, 1]]
    print(GUIStatics.check_line_intersection(line1, line2))
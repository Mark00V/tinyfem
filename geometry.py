import tkinter as tk
import math
from typing import Callable, Any
from tkinter import filedialog
import json
from guistatics import GUIStatics
import copy

class Geometry(tk.Toplevel):
    """
    Define Geometry Window
    """

    def __init__(self, callback_geometry: Callable[[dict], Any]):
        """
        Constructor, inherits from tk toplevel
        :param callback_geometry: callback method from class GUI
        """

        # Callback geometry to return geometry values to guimain
        self.callback_geometry = callback_geometry
        self.geometry_input = None  # for callback
        self.polygons = {'0': {'coordinates': [], 'area_neg_pos': 'Positive'}}  # init value
        # self.polygons = {'0': {'coordinates': [[0, 0], [1, 0.5], [1.5, 1.5], [0.75, 2.0]], 'area_neg_pos': 'Positive'},
        #                  '1': {'coordinates': [[-1, -1], [-2, -1], [-3, -3], [-2, -3]], 'area_neg_pos': 'Positive'},
        #                  '2': {'coordinates': [[1, -0.5], [3, -1], [3, -3.5], [2, -2.5], [0.5, -4]],
        #                        'area_neg_pos': 'Negative'}}  # TEST TODO
        self.polygon_nodes = [0]  # needed for update for select polygon dropdown (numbers for polygons in list)
        self.points = {}  # init value
        # self.points = {'0': [0, 1], '1': [2, 3], '2': [-2, 3]}  # testing todo
        self.units = 'm'
        self.other = 'None'  # json dump does not support None
        self.highlight_element = None  # highlighting nodes and points
        super().__init__()
        self.main_window()



    def main_window(self):
        """
        Creates main window for class Geometry
        :return:
        """
        self.resizable(False, False)
        self.title('TinyFEM - DEFINE GEOMETRY')
        self.geometry(f"{GUIStatics.GEOM_WINDOW_SIZE_X}x{GUIStatics.GEOM_WINDOW_SIZE_Y}")
        ##################################################
        # Position of elements
        # canvas
        border = 0.025
        canvas_x = 1 - GUIStatics.CANVAS_SIZE_X / GUIStatics.GEOM_WINDOW_SIZE_X - border
        canvas_y = 1 - GUIStatics.CANVAS_SIZE_Y / GUIStatics.GEOM_WINDOW_SIZE_Y - border

        # buttons and text on left side
        widgets_x_start = 0.01
        ##################################################

        ##################################################
        # save and load buttons
        # save geometry button
        def load_geometry():
            """
            load geometry from json file
            :return:
            """

            file_path = filedialog.askopenfilename(
                filetypes=[("json Files", "*.json")],
                title="Open Input File",
            )
            if file_path:
                with open(file_path, "r") as file:
                    content = file.read()
                geo_dict = json.loads(content)
                if geo_dict['points'] == {'None': 'None'}:  # workaround for json dump
                    geo_dict['points'] = {'None'}
                self.polygons = geo_dict['polygons']
                self.points = geo_dict['points']
                self.units = geo_dict['units']
                self.other = geo_dict['other']
                self.geometry_input = {'polygons': self.polygons, 'points': self.points, 'units': self.units,
                                       'other': self.other}

                # point input
                update_point_select_dropdown()
                single_point_var.set('None')
                if not self.points:
                    dropdown_single_point_select["state"] = "disabled"

                # polygon input
                polygon_select_var.set('0')
                polygon_node_var.set('None')
                dropdown_polygon_node_select["state"] = "disabled"
                update_dropdown_polygon_node_select_poly_info()
                if not self.polygons:
                    dropdown_polygon_select["state"] = "disabled"

                # reset canvas
                all_canvas_elements = self.canvas.find_all()
                for elem in all_canvas_elements:
                    self.canvas.delete(elem)
                GUIStatics.add_canvas_static_elements(self.canvas)
                self.update_graphics()

                # set geometry window to foreground
                self.lift()

        def save_geometry():
            """
            save geometry data to json file
            :return:
            """
            if self.points == {'None'}:
                self.points = {'None': 'None'}  # workaround for json dumping
            self.geometry_input = {'polygons': self.polygons, 'points': self.points, 'units': self.units,
                                   'other': self.other}
            #print(self.geometry_input)
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("json Files", "*.json")],
                title="Save Input As",
            )
            if file_path:
                with open(file_path, "w") as file:
                    file.write(json.dumps(self.geometry_input))

            if not self.points:
                self.points = {'None'}  # workaround for json dumping

            # set geometry window to foreground
            self.lift()

        button_save_geo = tk.Button(self, text="SAVE", command=save_geometry,
                                    font=GUIStatics.SAVELOAD_FONT, width=10, height=1)
        button_save_geo.place(relx=widgets_x_start, rely=0.02)

        # load geometry button
        button_load_geo = tk.Button(self, text="LOAD", command=load_geometry,
                                    font=GUIStatics.SAVELOAD_FONT, width=10, height=1)
        button_load_geo.place(relx=0.1, rely=0.02)
        ##################################################

        def show_help():
            window_help = tk.Toplevel(self)
            window_help.title('HELP - GEOMETRY')
            window_help.geometry(f"{800}x{600}")
            window_help.resizable(False, False)

        # Help Button
        tk.Button(self, text="HELP", command=show_help, width=8,
                  font=GUIStatics.STANDARD_FONT_BUTTON_SMALL, height=1).place(relx=0.9, rely=0.025)

        ##################################################
        # unit selector
        def update_unit_text(*args):
            """
            Updates label text when unit is selected from dropdown menu
            :param args:
            :return:
            """
            unit_selected = unit_var.get()
            units_dict = {'m': 'meter', 'mm': 'milimeter', 'km': 'kilometer', 'hm': 'hektometer', 'dam': 'dekameter',
                          'dm': 'dezimeter', 'cm': 'centimeter'}
            self.unit_selected.config(text=units_dict[unit_selected])
            self.units = unit_selected

        unit_select_label = tk.Label(self, text="Unit:", font=GUIStatics.STANDARD_FONT_SMALL_BOLD)
        unit_select_label.place(relx=0.835-0.075, rely=0.04)
        units = ['m', 'mm', 'km', 'hm', 'dam', 'dm', 'cm']
        unit_var = tk.StringVar()
        unit_var.set(units[0])  # default value m
        dropdown_unit_select = tk.OptionMenu(self, unit_var, *units)
        dropdown_unit_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=2, height=1)
        dropdown_unit_select.place(relx=0.865-0.075, rely=0.034)
        self.unit_selected = tk.Label(self, text='meter', font=GUIStatics.STANDARD_FONT_SMALL)
        self.unit_selected.place(relx=0.92-0.075, rely=0.04)
        unit_var.trace('w', update_unit_text)

        ##################################################

        ##################################################
        # Polygon definition

        def update_dropdown_polygon_node_select_poly_info(*args):
            """
            updates the dropdown_polygon_node_select optionMenu for the nodes set in the polygon set
            in dropdown_polygon_select  optionMenu
            Also updates the instance variable self.polygon_nodes
            :param args:
            :return:
            """
            # updates the polygon selection menu
            polygons_numbered = range(0, len(self.polygons)) if self.polygons else ['None']
            dropdown_polygon_select["menu"].delete(0, "end")
            for option in polygons_numbered:
                dropdown_polygon_select["menu"].add_command(label=option,
                                                                 command=tk._setit(polygon_select_var, option))
            # updates the polygon nodes dropdown menu and the info field for nodes
            active_polygon = self.polygons.get(polygon_select_var.get(), None)
            self.polygon_select_var = active_polygon
            if active_polygon == 'None':
                dropdown_polygon_node_select["state"] = "disabled"
            else:
                dropdown_polygon_node_select["state"] = "normal"
            if self.polygons:
                polygon_node_var.set('None')
                self.polygon_nodes = range(0, len(active_polygon['coordinates']))
                dropdown_polygon_node_select["menu"].delete(0, "end")
                for option in self.polygon_nodes:
                    dropdown_polygon_node_select["menu"].add_command(label=option,
                                                                     command=tk._setit(polygon_node_var, option))
                area_neg_pos_var.set(active_polygon['area_neg_pos'])
                update_polygon_nodes_info()
            else:
                polygon_nodes_text.config(state='normal')
                polygon_nodes_text.delete('0.0', 'end')
                polygon_nodes_text.insert('end', 'None')
                polygon_nodes_text.config(state='disabled')

        def update_polygon_nodes_info():
            """
            updates the info field for polygon nodes
            :return:
            """
            active_polygon = self.polygons.get(polygon_select_var.get(), None)
            polygon_nodes_text.config(state='normal')
            polygon_nodes_text.delete('0.0', 'end')
            polygon_nodes_text.insert('end', str(active_polygon['coordinates']))
            polygon_nodes_text.config(state='disabled')

        def update_x_y_entry_polygon_node(*args):
            """
            Updates the x and y values for the selected polygon and node
            :param args:
            :return:
            """
            active_polygon = self.polygons.get(polygon_select_var.get(), None)
            self.polygon_selected = polygon_select_var.get()
            if active_polygon == 'None':
                return None
            polygon_nodes = active_polygon['coordinates']
            if polygon_node_var.get() == 'None':
                add_node_x_entry.delete(0, 'end')
                add_node_x_entry.insert('end', '0')
                add_node_y_entry.delete(0, 'end')
                add_node_y_entry.insert('end', '0')
            else:
                active_polygon_node = int(polygon_node_var.get())
                node_coords = polygon_nodes[active_polygon_node]
                add_node_x_entry.delete(0, 'end')
                add_node_x_entry.insert('end', str(node_coords[0]))
                add_node_y_entry.delete(0, 'end')
                add_node_y_entry.insert('end', str(node_coords[1]))
                last_highlight_element = self.canvas.find_withtag('highlight_element')
                if last_highlight_element:
                    self.canvas.delete(last_highlight_element)
                node = GUIStatics.transform_node_to_canvas(node_coords)
                self.highlight_element = self.canvas.create_oval(node[0] - 10, node[1] - 10, node[0] + 10, node[1] + 10,
                                                                 width=3, outline=GUIStatics.CANVAS_HIGHLIGHT_ELEMENT,
                                                                 dash=(2, 1), fill='', tags='highlight_element')

            self.update_graphics()




        def new_polygon():
            """
            create new polygon on click button NEW
            :return:
            """
            if not self.polygons:
                self.polygons = {'0': {'coordinates': [], 'area_neg_pos': 'Positive'}}
                dropdown_polygon_select["state"] = "normal"
                polygon_select_var.set('0')
                update_polygon_nodes_info()
                update_dropdown_polygon_node_select_poly_info()
            else:
                new_index = str(1 + int(max(self.polygons.keys())))
                self.polygons[new_index] = {'coordinates': [], 'area_neg_pos': 'Positive'}
                update_dropdown_polygon_node_select_poly_info()
                polygon_select_var.set(new_index)

        def delete_poly_node():
            active_polygon = polygon_select_var.get()
            if active_polygon == 'None':
                return None
            selected_node = polygon_node_var.get()
            if selected_node == 'None':
                return None
            else:
                selected_node = int(polygon_node_var.get())
            del self.polygons[active_polygon]['coordinates'][selected_node]
            update_polygon_nodes_info()
            update_dropdown_polygon_node_select_poly_info()
            self.update_graphics()

        def add_poly_node():
            """
            When button ADD for polygon is pressed
            :return:
            """

            this_polygon = polygon_select_var.get()
            if this_polygon == 'None':
                return None
            dropdown_polygon_node_select["state"] = "normal"
            polygon_nodes = self.polygons[this_polygon]['coordinates']
            try:
                x_entry = float(add_node_x_entry_val.get().replace(',', '.'))
                y_entry = float(add_node_x_entry_val.get().replace(',', '.'))
            except ValueError:
                # todo: warning window oder so falls text eingegben..
                x_entry = 0.0
                y_entry = 0.0
            polygon_nodes.append([x_entry, y_entry])
            self.polygons[this_polygon]['coordinates'] = polygon_nodes
            update_dropdown_polygon_node_select_poly_info()
            update_polygon_nodes_info()
            self.update_graphics()

        def update_poly_node():
            """
            When button UPDATE for polygon is pressed
            :return:
            """
            this_polygon = polygon_select_var.get()
            if this_polygon == 'None':
                return None
            selected_node = polygon_node_var.get()
            area_value = area_neg_pos_var.get()
            self.polygons[this_polygon]['area_neg_pos'] = area_value
            self.update_graphics()
            if selected_node == 'None':
                return None
            else:
                selected_node = int(polygon_node_var.get())
            try:
                x_value = float(add_node_x_entry.get())
                y_value = float(add_node_y_entry.get())
            except ValueError:
                x_value = 0.0
                y_value = 0.0
                GUIStatics.window_error(self, "Enter Coordinates as float!")
            self.polygons[this_polygon]['coordinates'][selected_node] = [x_value, y_value]
            update_polygon_nodes_info()

            last_highlight_element = self.canvas.find_withtag('highlight_element')
            if last_highlight_element:  # todo...copypasted a lot -> method
                self.canvas.delete(last_highlight_element)
            node_coords = self.polygons[this_polygon]['coordinates'][selected_node]
            node = GUIStatics.transform_node_to_canvas(node_coords)
            self.highlight_element = self.canvas.create_oval(node[0] - 10, node[1] - 10, node[0] + 10, node[1] + 10,
                                                             width=3, outline=GUIStatics.CANVAS_HIGHLIGHT_ELEMENT,
                                                             dash=(2, 1), fill='', tags='highlight_element')
            self.update_graphics()

        def delete_polygon():
            """
            When button DELETE POLYGON for polygons is pressed
            :return:
            """
            active_polygon = polygon_select_var.get()
            if active_polygon != 'None':
                if len(self.polygons) > 1:
                    del self.polygons[active_polygon]
                    self.polygons = GUIStatics.resort_keys(self.polygons)
                    polygon_select_var.set('0')
                    update_dropdown_polygon_node_select_poly_info()
                    self.update_graphics()
                else:
                    del self.polygons[active_polygon]
                    polygon_select_var.set('None')
                    dropdown_polygon_node_select["state"] = "disabled"
                    dropdown_polygon_select["state"] = "disabled"
                    self.update_graphics()

        GUIStatics.create_divider(self, widgets_x_start, 0.085, 230)

        polygon_def_label = tk.Label(self, text="Define Polygon", font=GUIStatics.STANDARD_FONT_MID_BOLD)
        polygon_def_label.place(relx=widgets_x_start, rely=0.1)

        polygon_select_label = tk.Label(self, text="Select Polygon:", font=GUIStatics.STANDARD_FONT_SMALL)
        polygon_select_label.place(relx=widgets_x_start, rely=0.135)
        self.polygon_selection = [elem for elem in self.polygons.keys()]
        polygon_select_var = tk.StringVar()
        polygon_select_var.set('0')
        dropdown_polygon_select = tk.OptionMenu(self, polygon_select_var, *self.polygon_selection)
        dropdown_polygon_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_polygon_select.place(relx=widgets_x_start + 0.075, rely=0.13)
        polygon_select_var.trace('w', update_dropdown_polygon_node_select_poly_info)
        self.polygon_selected = polygon_select_var.get()

        new_poly_button = tk.Button(self, text="NEW", command=new_polygon,
                                    width=7, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        new_poly_button.place(relx=widgets_x_start + 0.145, rely=0.133)

        polygon_node_select_label = tk.Label(self, text="Select Node:", font=GUIStatics.STANDARD_FONT_SMALL)
        polygon_node_select_label.place(relx=widgets_x_start, rely=0.185)
        polygon_node_var = tk.StringVar()
        polygon_node_var.set('None')
        dropdown_polygon_node_select = tk.OptionMenu(self, polygon_node_var, *self.polygon_nodes)
        dropdown_polygon_node_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_polygon_node_select.place(relx=widgets_x_start + 0.075, rely=0.18)
        dropdown_polygon_node_select["state"] = "disabled"
        polygon_node_var.trace('w', update_x_y_entry_polygon_node)

        add_poly_select_label = tk.Label(self, text="Add/Update Node:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_poly_select_label.place(relx=widgets_x_start, rely=0.225)

        add_node_x_label = tk.Label(self, text="X:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_node_x_label.place(relx=widgets_x_start, rely=0.26)
        add_node_x_entry_val = tk.StringVar()
        add_node_x_entry_val.set('0')
        add_node_x_entry = tk.Entry(self, textvariable=add_node_x_entry_val,
                                    font=GUIStatics.STANDARD_FONT_SMALL, width=6)
        add_node_x_entry.place(relx=widgets_x_start + 0.02, rely=0.262)

        add_node_y_label = tk.Label(self, text="Y:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_node_y_label.place(relx=widgets_x_start + 0.06, rely=0.26)
        add_node_y_entry_val = tk.StringVar()
        add_node_y_entry_val.set('0')
        add_node_y_entry = tk.Entry(self, textvariable=add_node_y_entry_val,
                                    font=GUIStatics.STANDARD_FONT_SMALL, width=6)
        add_node_y_entry.place(relx=widgets_x_start + 0.08, rely=0.262)

        add_poly_node_button = tk.Button(self, text="ADD", command=add_poly_node,
                                         width=11, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        add_poly_node_button.place(relx=widgets_x_start + 0.125, rely=0.258)
        update_poly_node_button = tk.Button(self, text="UPDATE", command=update_poly_node,
                                            width=11, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        update_poly_node_button.place(relx=widgets_x_start + 0.125, rely=0.289)
        delete_polygon_node_button = tk.Button(self, text="DELETE", command=delete_poly_node,
                                     width=11, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        delete_polygon_node_button.place(relx=widgets_x_start + 0.125, rely=0.228)

        polygon_nodes_label = tk.Label(self, text="Polygon Nodes:", font=GUIStatics.STANDARD_FONT_SMALL)
        polygon_nodes_label.place(relx=widgets_x_start, rely=0.30)
        polygon_nodes_text = tk.Text(self, height=4, width=35, wrap=tk.WORD,
                                     font=GUIStatics.STANDARD_FONT_SMALLER, bg='light gray', fg='black')
        polygon_nodes_text.place(relx=widgets_x_start + 0.005, rely=0.33)
        polygon_nodes_text.insert(tk.END, 'None')
        polygon_nodes_text.config(state='disabled')

        area_neg_pos_label = tk.Label(self, text="Area:", font=GUIStatics.STANDARD_FONT_SMALL)
        area_neg_pos_label.place(relx=widgets_x_start, rely=0.42)
        area_neg_pos = ['Positive', 'Negative']
        area_neg_pos_var = tk.StringVar()
        area_neg_pos_var.set(area_neg_pos[0])
        area_neg_pos_select = tk.OptionMenu(self, area_neg_pos_var, *area_neg_pos)
        area_neg_pos_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=6, height=1)
        area_neg_pos_select.place(relx=widgets_x_start + 0.04, rely=0.415)

        delete_polygon_button = tk.Button(self, text="DELETE POLYGON", command=delete_polygon,
                                          width=16, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        delete_polygon_button.place(relx=widgets_x_start, rely=0.465)

        ##################################################

        ##################################################
        # Single Point definition
        def new_point():
            """
            When button NEW for single point definition is pressed
            :return:
            """
            dropdown_single_point_select["state"] = "normal"
            # check if points already in self.points
            if not self.points or self.points == {'None'}:
                self.points = {'0': [0, 0]}
                selected_point = '0'
            else:
                selected_point = str(int(max(list(self.points.keys()))) + 1)
                self.points[selected_point] = [0, 0]
            update_point_select_dropdown()
            single_point_var.set(selected_point)
            self.update_graphics()

        def update_point_select_dropdown():
            """
            updates the select point dropdown menu
            :return:
            """
            points_numbered = range(0, len(self.points)) if self.points else ['None']
            dropdown_single_point_select["menu"].delete(0, "end")
            for option in points_numbered:
                dropdown_single_point_select["menu"].add_command(label=option,
                                                                 command=tk._setit(single_point_var, option))

        def update_x_y_select_point(*args):
            """
            Updates the x and y values for the selected polygon and node
            :param args:
            :return:
            """
            selected_point = single_point_var.get()
            if selected_point == 'None' or not self.points:
                node_coords = [0, 0]
            else:
                node_coords = self.points[selected_point]
            add_point_x_entry.delete(0, 'end')
            add_point_x_entry.insert('end', str(node_coords[0]))
            add_point_y_entry.delete(0, 'end')
            add_point_y_entry.insert('end', str(node_coords[1]))

            last_highlight_element = self.canvas.find_withtag('highlight_element')
            if last_highlight_element:
                self.canvas.delete(last_highlight_element)
            node = GUIStatics.transform_node_to_canvas(node_coords)
            self.highlight_element = self.canvas.create_oval(node[0] - 10, node[1] - 10, node[0] + 10, node[1] + 10,
                                                             width=3, outline=GUIStatics.CANVAS_HIGHLIGHT_ELEMENT,
                                                             dash=(2, 1), fill='', tags='highlight_element')

            self.update_graphics()

        def update_point():
            """
            gets the selected point from dropdown and values from x and y field
            and updates the values for selected point
            :return:
            """
            if not self.points:
                return None
            selected_point = single_point_var.get()
            if selected_point == 'None':
                return None
            try:
                new_x = float(add_point_x_entry_val.get().replace(',', '.'))
                new_y = float(add_point_y_entry_val.get().replace(',', '.'))
            except ValueError:
                new_x = 0.0
                new_y = 0.0
                GUIStatics.window_error(self, "Enter Coordinates as float!")
            self.points[selected_point] = [new_x, new_y]

            last_highlight_element = self.canvas.find_withtag('highlight_element')
            if last_highlight_element:
                self.canvas.delete(last_highlight_element)
            node = GUIStatics.transform_node_to_canvas(self.points[selected_point])
            self.highlight_element = self.canvas.create_oval(node[0] - 10, node[1] - 10, node[0] + 10, node[1] + 10,
                                                             width=3, outline=GUIStatics.CANVAS_HIGHLIGHT_ELEMENT,
                                                             dash=(2, 1), fill='', tags='highlight_element')

            self.update_graphics()

        def delete_point():
            """
            deletes specified point in dropdown menu and resorts dict
            :return:
            """
            selected_point = single_point_var.get()

            if selected_point == 'None':
                return None
            del self.points[selected_point]
            if not self.points:
                single_point_var.set('None')
                dropdown_single_point_select["state"] = "disabled"
                self.update_graphics()
                return None
            self.points = GUIStatics.resort_keys(self.points)
            update_point_select_dropdown()
            single_point_var.set('0')
            self.update_graphics()

        GUIStatics.create_divider(self, widgets_x_start, 0.535, 230)
        single_point_def_label = tk.Label(self, text="Define Point", font=GUIStatics.STANDARD_FONT_MID_BOLD)
        single_point_def_label.place(relx=widgets_x_start, rely=0.55)
        single_point_select_label = tk.Label(self, text="Select Point:", font=GUIStatics.STANDARD_FONT_SMALL)
        single_point_select_label.place(relx=widgets_x_start, rely=0.585)
        single_point_var = tk.StringVar()
        single_point_var.set('None')
        if not self.points:
            self.points = {'None'}
        dropdown_single_point_select = tk.OptionMenu(self, single_point_var, *self.points)
        dropdown_single_point_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_single_point_select.place(relx=widgets_x_start + 0.075, rely=0.58)
        if not self.points:
            dropdown_single_point_select["state"] = "disabled"
        single_point_var.trace('w', update_x_y_select_point)

        new_point_button = tk.Button(self, text="NEW", command=new_point,
                                     width=7, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        new_point_button.place(relx=widgets_x_start + 0.145, rely=0.583)

        add_point_select_label = tk.Label(self, text="Update Point:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_point_select_label.place(relx=widgets_x_start, rely=0.63)

        add_point_x_label = tk.Label(self, text="X:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_point_x_label.place(relx=widgets_x_start, rely=0.665)
        add_point_x_entry_val = tk.StringVar()
        add_point_x_entry_val.set('0')
        add_point_x_entry = tk.Entry(self, textvariable=add_point_x_entry_val,
                                     font=GUIStatics.STANDARD_FONT_SMALL, width=6)
        add_point_x_entry.place(relx=widgets_x_start + 0.02, rely=0.667)

        add_point_y_label = tk.Label(self, text="Y:", font=GUIStatics.STANDARD_FONT_SMALL)
        add_point_y_label.place(relx=widgets_x_start + 0.06, rely=0.665)
        add_point_y_entry_val = tk.StringVar()
        add_point_y_entry_val.set('0')
        add_point_y_entry = tk.Entry(self, textvariable=add_point_y_entry_val,
                                     font=GUIStatics.STANDARD_FONT_SMALL, width=6)
        add_point_y_entry.place(relx=widgets_x_start + 0.08, rely=0.667)

        add_point_button = tk.Button(self, text="UPDATE", command=update_point,
                                     width=11, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        add_point_button.place(relx=widgets_x_start + 0.125, rely=0.663)

        delete_point_button = tk.Button(self, text="DELETE POINT", command=delete_point,
                                        width=14, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        delete_point_button.place(relx=widgets_x_start, rely=0.71)

        ##################################################
        # clear all button
        ##################################################
        def clear_all():
            # reset to init values
            self.geometry_input = None
            self.polygons = {'0': {'coordinates': [], 'area_neg_pos': 'Positive'}}
            self.polygon_nodes = [0]
            self.points = {}

            # reset point input
            update_point_select_dropdown()
            single_point_var.set('None')
            dropdown_single_point_select["state"] = "disabled"

            # reset polygon input
            polygon_select_var.set('0')
            polygon_node_var.set('None')
            dropdown_polygon_node_select["state"] = "disabled"
            update_dropdown_polygon_node_select_poly_info()

            # reset canvas
            all_canvas_elements = self.canvas.find_all()
            for elem in all_canvas_elements:
                self.canvas.delete(elem)
            GUIStatics.add_canvas_static_elements(self.canvas)

        button_clear_all = tk.Button(self, text="CLEAR ALL", command=clear_all,
                                    font=GUIStatics.STANDARD_FONT_BUTTON_MID, width=10, height=1)
        button_clear_all.place(relx=widgets_x_start + 0.25, rely=0.02)

        ##################################################
        # Add canvas for system visualization - DYNAMIC
        self.canvas = tk.Canvas(self, width=GUIStatics.CANVAS_SIZE_X, height=GUIStatics.CANVAS_SIZE_Y,
                                bg=GUIStatics.CANVAS_BG)
        self.canvas.place(relx=canvas_x + 0.0075, rely=canvas_y)
        GUIStatics.add_canvas_static_elements(self.canvas)
        ##################################################

        ##################################################
        # Update graphics
        GUIStatics.create_divider(self, widgets_x_start, 0.87, 230)
        button_update_graphics = tk.Button(self, text="UPDATE GRAPHICS", command=self.update_graphics,
                                           width=25, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_MID)
        button_update_graphics.place(relx=0.025, rely=0.885)
        ##################################################

        ##################################################
        # Accept button and checks
        def check_geometry():
            """
            Checks compatibility of geometry
            :return:
            """

            comp = True

            # self.polygons = {'0': {'coordinates' : [[0,0], [1,0], [1,1], [0,1]], 'area_neg_pos': 'Positive'}}
            # self.polygons = {'0': {'coordinates': [[0, 0], [1, 0], [1.0, 1], [0.5,-1], [0, 1]], 'area_neg_pos': 'Positive'},
            #                  '1': {'coordinates': [[0, 0], [1, 0], [1.0, 1], [0.5,-1], [0, 1]], 'area_neg_pos': 'Positive'}}
            # check if all polygons have at least 3 nodes
            node_count_error = False
            for nbr, polygonvals in self.polygons.items():
                nodes_len = len(polygonvals['coordinates'])
                if nodes_len < 3:
                    node_count_error = True
                    GUIStatics.window_error(self, f"Polygon {nbr} has less than three nodes!")

            # check if lines in polygons intersect todo: works only if lines are not vertical...(missing slope)
            intersect_error = False
            for nbr, polygonvals in self.polygons.items():
                nodes = copy.deepcopy(polygonvals['coordinates'])
                if not nodes:
                    break
                nodes.append(nodes[0])
                for sn, en in zip(nodes[:-1], nodes[1:]):
                    line1 = [sn, en]
                    for nbr_2, polygonvals_2 in self.polygons.items():
                        nodes_2 = copy.deepcopy(polygonvals_2['coordinates'])
                        if not nodes_2 or nbr == nbr_2:
                            break
                        nodes_2.append(nodes_2[0])
                        for sn_2, en_2 in zip(nodes_2[:-1], nodes_2[1:]):
                            if sn == sn_2 and en == en_2:
                                continue
                            line2 = [sn_2, en_2]
                            if GUIStatics.check_line_intersection(line1, line2):
                                GUIStatics.window_error(self, f"Intersection in Polygon {nbr}!")
                                intersect_error = True
                                break
                        if intersect_error:
                            break
                    if intersect_error:
                        break
                if intersect_error:
                    break

            # check if negative polygon entirely inside one positive polygon
            # TODO

            # check if adjacent polygons share 2 nodes
            # todo

            # check if single point inside positive polygon
            # todo


            if node_count_error or intersect_error:
                comp = False
            return comp

        def check_geometry_error_window():
            """
            error window if geometry is not accepted
            :return:
            """

            info_window = tk.Toplevel(self)
            info_window.title("GEOMETRY ERROR")
            info_window.configure(bg='#FFB5B5')
            info_window.geometry(f"300x180")
            info_window.resizable(False, False)
            info_str = f"Single points must be inside positive polygons\n" \
                       f"Positive Polygons must share at least two nodes\n" \
                       f"All vertices of negative Polygons\n" \
                       f"must be inside positive Polygons\n" \
                       f"Polygons must have at least 3 vertices"
            info_label = tk.Label(info_window, text="GEOMETRY NOT COMPATIBLE:\n", font=("Arial Black", 12), bg='#FFB5B5', fg='#470000')
            info_label.place(relx=0.025, rely=0.1)
            info_label = tk.Label(info_window, text=info_str, font=("Arial", 10), bg='#FFB5B5', fg='#470000')
            info_label.place(relx=0.025, rely=0.3)

        def check_and_accept():
            """
            Checks geometry and if compatible returns value to main gui, else error windo
            :return:
            """

            if check_geometry():
                self.return_geometry()
            else:
                check_geometry_error_window()

        # Accept Geometry button - returns value for geometry input and destroys window
        button_accept = tk.Button(self, text="ACCEPT GEOMETRY", command=check_and_accept,
                                  width=16, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_BIG_BOLD)
        button_accept.place(relx=0.025, rely=0.935)
        ##################################################

        ##################################################
        # For debugging
        def debug():
            """
            when button DEBUG is pressed
            :return:
            """
            check_geometry()
            geometry_input = {'polygons': self.polygons, 'points': self.points, 'units': self.units,
                                   'other': self.other}
            print("\n\n")
            print(f"self.polygons: {self.polygons}")
            print(f"self.polygon_nodes: {self.polygon_nodes}")
            print(f"self.points: {self.points}")
            print(f"self.geometry_input: {geometry_input}")

        button_debug = tk.Button(self, text="DEBUG", command=debug,
                                 width=5, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        button_debug.place(relx=0.96, rely=0.005)
        ##################################################

    def update_graphics(self):
        """
        Updates the canvas, draws static elements (coordsystem, grid) and draws defined polygons and single points
        :return:
        """

        selected_polygon = self.polygon_selected

        # delete all
        all_canvas_elements = self.canvas.find_all()
        for elem in all_canvas_elements:
            if elem == self.highlight_element:
                continue
            self.canvas.delete(elem)

        # add grid etc
        GUIStatics.add_canvas_static_elements(self.canvas)

        # draw polygons
        for polygon_nbr, polygon_data in self.polygons.items():
            if selected_polygon == polygon_nbr:
                color_code_plus = '#9C4747'
                color_code_minus = '#283258'
            else:
                color_code_plus = '#7D4C4C'
                color_code_minus = '#222638'
            color_code_plus_node = '#5F0F0F'
            color_code_minus_node = '#3A4571'

            polygon_nodes = polygon_data['coordinates']
            if len(polygon_nodes) < 3:
                continue
            polygon_nodes_transformed = [GUIStatics.transform_node_to_canvas(node) for node in polygon_nodes]
            polygon_neg_pos = polygon_data['area_neg_pos']  # either 'Positive' or 'Negative'
            color_code = color_code_plus if polygon_neg_pos == 'Positive' else color_code_minus
            color_code_node = color_code_plus_node if polygon_neg_pos == 'Positive' else color_code_minus_node
            self.canvas.create_polygon(polygon_nodes_transformed, fill=color_code, outline='#341010', width=2)

            # add text to polygon, todo: position besser finden
            middle_node = math.floor(len(polygon_nodes_transformed) / 2)
            if middle_node == 0:
                middle_node = 1
            text = f'Polygon {polygon_nbr}'
            color_code_text = '#1F1F1F' if polygon_neg_pos == 'Positive' else '#B1C0C2'
            center_node_approx_x = math.floor(abs((polygon_nodes_transformed[middle_node][0] +
                                                   polygon_nodes_transformed[0][0]) / 2))
            center_node_approx_y = math.floor(abs((polygon_nodes_transformed[middle_node][1] +
                                                   polygon_nodes_transformed[0][1]) / 2))
            self.canvas.create_text(center_node_approx_x, center_node_approx_y, text=text, fill=color_code_text,
                                    font=("Helvetica", 7))

            # add nodes
            for node in polygon_nodes:
                node = GUIStatics.transform_node_to_canvas(node)
                self.canvas.create_oval(node[0] - 3, node[1] - 3, node[0] + 3, node[1] + 3, fill=color_code_node,
                                        outline='#1F1F1F', width=1)

        # draw points
        if self.points != {'None'} and self.points:
            for point_nbr, node in self.points.items():
                node = GUIStatics.transform_node_to_canvas(node)
                text = f'Point {point_nbr}'
                self.canvas.create_oval(node[0] - 4, node[1] - 4, node[0] + 4, node[1] + 4, fill='#2D0F0F',
                                        outline='#1F1F1F', width=1)
                self.canvas.create_text(node[0], node[1] - 10, text=text, fill='#1F1F1F', font=("Helvetica", 7))


    def return_geometry(self):
        """
        Callback method to return defined geometry to main class GUI
        :return:
        """
        # todo: check if geometry is valid e.g. polgones have to be connects,
        #  only one polygon can be subtracted, points have to be in valid area, etc.
        self.geometry_input = {'polygons': self.polygons, 'points': self.points, 'units': self.units, 'other': None}

        self.callback_geometry(self.geometry_input)
        self.destroy()  # closes top window



if __name__ == '__main__':
    geo = Geometry(lambda x: x)  # Todo - Develop: For testing Geometry gui, argument simulates callback
    geo.mainloop()
"""
#######################################################################
LICENSE INFORMATION
This file is part of TinyFEM.

TinyFEM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TinyFEM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with TinyFEM. If not, see <https://www.gnu.org/licenses/>.
#######################################################################

#######################################################################
Description:
Definition for geometry.
#######################################################################
"""

import tkinter as tk
import math
from typing import Callable, Any, Tuple, List
from tkinter import filedialog
import json
from source.guistatics import GUIStatics, Tooltip
import copy
from PIL import ImageTk
from shapely.geometry import Polygon, Point, MultiPolygon
from shapely.ops import unary_union
import numpy as np

class Geometry(tk.Toplevel):
    """
    Define Geometry Window
    """

    def __init__(self, callback_geometry: Callable[[dict], Any], geometry_input):
        """
        Constructor, inherits from tk toplevel
        :param callback_geometry: callback method from class GUI
        """

        # Callback geometry to return geometry values to guimain
        self.callback_geometry = callback_geometry
        if not geometry_input:
            self.geometry_input = None  # for callback
            self.polygons = {'0': {'coordinates': [], 'area_neg_pos': 'Positive'}}  # init value
            self.points = {}  # init value
            self.units = 'm'
        else:
            self.geometry_input = geometry_input
            self.polygons = geometry_input['polygons']
            self.points = geometry_input['points']
            self.units = geometry_input['units']


        self.polygon_nodes = [0]  # needed for update for select polygon dropdown (numbers for polygons in list)
        # self.points = {'0': [0, 1], '1': [2, 3], '2': [-2, 3]}  # testing

        # other and highlight for node/point selection
        self.other = 'None'  # json dump does not support None
        self.highlight_element = None  # highlighting nodes
        self.highlight_element_point = None  # highlighting points
        self.highlight_node_coords = None

        # Graphical input
        self.firstclick_canvas = True
        self.clicks_canvas = []

        super().__init__()
        self.set_icon(self)
        self.main_window()

    def set_icon(self, root):
        """
        Creates Icon from raw byte data to not need external files for creating .exe
        :return:
        """
        icon_image = ImageTk.PhotoImage(data=GUIStatics.return_icon_bytestring())
        root.tk.call('wm', 'iconphoto', root._w, icon_image)

    def main_window(self):
        """
        Creates main window for class Geometry
        :return:
        """
        self.resizable(False, False)
        self.title('TinyFEM - DEFINE GEOMETRY')
        self.geometry(f"{GUIStatics.GEOM_WINDOW_SIZE_X}x{GUIStatics.GEOM_WINDOW_SIZE_Y}")
        try:
            self.iconbitmap('tiny_fem_icon.ico')
        except tk.TclError:
            ...  # todo: Muss für exe mitgepackt werden...???
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
                                       'other'   : self.other}

                # point input
                update_point_select_dropdown()
                single_point_var.set('None')
                if not self.points:
                    dropdown_single_point_select["state"] = "disabled"

                # polygon input
                polygon_select_var.set('0')
                self.polygon_node_var.set('None')
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
                                   'other'   : self.other}
            # print(self.geometry_input)
            file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("json Files", "*.json")],
                    title="Save Input As",
            )
            if file_path:
                with open(file_path, "w") as file:
                    file.write(json.dumps(self.geometry_input))

            if self.points == {'None': 'None'}:
                self.points = {'None'}  # workaround for json dumping

            # set geometry window to foreground
            self.lift()

        button_save_geo = tk.Button(self, text="SAVE", command=save_geometry,
                                    font=GUIStatics.SAVELOAD_FONT, width=10, height=1)
        button_save_geo.place(relx=widgets_x_start, rely=0.02)
        tooltip_text = (f"Save the geometry to file")
        Tooltip(button_save_geo, tooltip_text)

        # load geometry button
        button_load_geo = tk.Button(self, text="LOAD", command=load_geometry,
                                    font=GUIStatics.SAVELOAD_FONT, width=10, height=1)
        button_load_geo.place(relx=0.1, rely=0.02)
        tooltip_text = (f"Load the geometry from file")
        Tooltip(button_load_geo, tooltip_text)

        ##################################################

        def show_help():
            """
            Button action to show help window for GUI
            :return:
            """
            window_help = tk.Toplevel(self)
            window_help.title('HELP - GEOMETRY')
            window_help.geometry(f"{800}x{600}")
            window_help.resizable(False, False)
            self.set_icon(window_help)

            help_txt_t = f"GEOMETRY"
            help_txt_inst = (f"I) How to add polygons and single points via input (Define Polygon / Define Single Points section):\n"
                             f"   Polygons:\n"
                             f"    - Select polygon from selector SELECT POLYGON to add/delete/change nodes\n"
                             f"      - Select node from selector SELECT NODE or add new nodes by pressing NEW (select afterwards)\n"
                             f"      - Input coordinates in input fields and press UPDATE\n"
                             f"      - Current nodes and coordinates are shown in POLYGON NODES \n"
                             f"      - Select positive/negative area from Selector AREA (press UPDATE afterwards)\n\n"
                             f"   Single points:\n"
                             f"    - Select point from selector SELECT POINT or ADD new points\n"
                             f"      - Points are mainly used to define acoustic sources (but edge nodes can also be used instead)\n\n"
                             f"II) How to add polygons and single points via mouse clicks:\n"
                             f"   Polygons:\n"
                             f"    - Click on canvas to add node for polygon. Click at least 3 times for valid polygon\n"
                             f"    - Click on button ADD CANVAS POLYGON\n"
                             f"    - Polygon will be added to polygon list with respective node positions\n"
                             f"   Single points:\n"
                             f"    - Click at least once on canvas\n"
                             f"    - Click on button ADD CANVAS POINT to add latest point to single point list\n"
                             f"   Other:\n"
                             f"    - Click on button CLEAR INPUT to delete mouse clicks on canvas\n\n"
                             f"III) Optional: SAVE / LOAD to save or load geometry input \n\n"
                             f"IV)  Click Button ACCEPT GEOMETRY to finish geometry definition and exit window\n"
                             f"    - The geometry will automatically be checked if it is valid for mesh generation\n"
                             f"    - You can also manually check by clicking button CHECK GEOMETRY ")

            tk.Label(window_help, text=help_txt_t, font=GUIStatics.STANDARD_FONT_BIGGER_BOLD, anchor="center",
                     justify="center") \
                .place(relx=0.1, rely=0.1)
            tk.Label(window_help, text='Instructions', font=GUIStatics.STANDARD_FONT_BIG_BOLD, anchor="w",
                     justify="left") \
                .place(relx=0.1, rely=0.175)
            tk.Label(window_help, text=help_txt_inst, font=GUIStatics.STANDARD_FONT_SMALL, anchor="w", justify="left") \
                .place(relx=0.1, rely=0.225)

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
            units_dict = {'m' : 'meter', 'mm': 'milimeter', 'km': 'kilometer', 'hm': 'hektometer', 'dam': 'dekameter',
                          'dm': 'dezimeter', 'cm': 'centimeter'}
            self.unit_selected.config(text=units_dict[unit_selected])
            self.units = unit_selected

        unit_select_label = tk.Label(self, text="Unit:", font=GUIStatics.STANDARD_FONT_SMALL_BOLD)
        unit_select_label.place(relx=0.835 - 0.075, rely=0.04)
        units = ['m', 'mm', 'km', 'hm', 'dam', 'dm', 'cm']
        unit_var = tk.StringVar()
        unit_var.set(units[0])  # default value m
        dropdown_unit_select = tk.OptionMenu(self, unit_var, *units)
        dropdown_unit_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=2, height=1)
        dropdown_unit_select.place(relx=0.865 - 0.075, rely=0.034)
        self.unit_selected = tk.Label(self, text='meter', font=GUIStatics.STANDARD_FONT_SMALL)
        self.unit_selected.place(relx=0.92 - 0.075, rely=0.04)
        unit_var.trace('w', update_unit_text)
        tooltip_text = (f"Select units for geometry                      \n"
                        f"This only affects axes description for solution\n"
                        f"and has no impact on calculation               ")
        Tooltip(dropdown_unit_select, tooltip_text)
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
                self.polygon_node_var.set('None')
                self.polygon_nodes = range(0, len(active_polygon['coordinates']))
                dropdown_polygon_node_select["menu"].delete(0, "end")
                for option in self.polygon_nodes:
                    dropdown_polygon_node_select["menu"].add_command(label=option,
                                                                     command=tk._setit(self.polygon_node_var, option))
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
            if self.polygon_node_var.get() == 'None':
                add_node_x_entry.delete(0, 'end')
                add_node_x_entry.insert('end', '0')
                add_node_y_entry.delete(0, 'end')
                add_node_y_entry.insert('end', '0')
            else:
                active_polygon_node = int(self.polygon_node_var.get())
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
                self.highlight_node_coords = (node[0], node[1])

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
                new_index = str(1 + max([int(k) for k in self.polygons.keys()]))
                self.polygons[new_index] = {'coordinates': [], 'area_neg_pos': 'Positive'}
                update_dropdown_polygon_node_select_poly_info()
                polygon_select_var.set(new_index)

        def delete_poly_node():
            """
            Button action to delete polygon node
            :return:
            """
            active_polygon = polygon_select_var.get()
            if active_polygon == 'None':
                return None
            selected_node = self.polygon_node_var.get()
            if selected_node == 'None':
                return None
            else:
                selected_node = int(self.polygon_node_var.get())
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
                y_entry = float(add_node_y_entry_val.get().replace(',', '.'))
            except ValueError:
                GUIStatics.window_error(self, "Enter coordinates as integer or float!")
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
            selected_node = self.polygon_node_var.get()
            area_value = area_neg_pos_var.get()
            self.polygons[this_polygon]['area_neg_pos'] = area_value
            self.update_graphics()
            if selected_node == 'None':
                return None
            else:
                selected_node = int(self.polygon_node_var.get())
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
        tooltip_text = (f"Select polygon")
        Tooltip(dropdown_polygon_select, tooltip_text)

        new_poly_button = tk.Button(self, text="NEW", command=new_polygon,
                                    width=7, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        new_poly_button.place(relx=widgets_x_start + 0.145, rely=0.133)
        tooltip_text = (f"Create new polygon without nodes")
        Tooltip(new_poly_button, tooltip_text)

        polygon_node_select_label = tk.Label(self, text="Select Node:", font=GUIStatics.STANDARD_FONT_SMALL)
        polygon_node_select_label.place(relx=widgets_x_start, rely=0.185)
        self.polygon_node_var = tk.StringVar()
        self.polygon_node_var.set('None')
        dropdown_polygon_node_select = tk.OptionMenu(self, self.polygon_node_var, *self.polygon_nodes)
        dropdown_polygon_node_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=4, height=1)
        dropdown_polygon_node_select.place(relx=widgets_x_start + 0.075, rely=0.18)
        dropdown_polygon_node_select["state"] = "disabled"
        self.polygon_node_var.trace('w', update_x_y_entry_polygon_node)
        tooltip_text = (f"Select the node from selected polygon")
        Tooltip(dropdown_polygon_node_select, tooltip_text)

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
        tooltip_text = (f"Add a new node to the selected polygon")
        Tooltip(add_poly_node_button, tooltip_text)
        add_poly_node_button.place(relx=widgets_x_start + 0.125, rely=0.258)
        update_poly_node_button = tk.Button(self, text="UPDATE", command=update_poly_node,
                                            width=11, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        update_poly_node_button.place(relx=widgets_x_start + 0.125, rely=0.289)
        tooltip_text = (f"Update entered X/Y values for selected node for selected polygon  \n"
                        f"(Also click UPDATE after selecting positive/negative polygon area)")
        Tooltip(update_poly_node_button, tooltip_text)
        delete_polygon_node_button = tk.Button(self, text="DELETE", command=delete_poly_node,
                                               width=11, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        delete_polygon_node_button.place(relx=widgets_x_start + 0.125, rely=0.228)
        tooltip_text = (f"Delete the selected node from the selected polygon")
        Tooltip(delete_polygon_node_button, tooltip_text)
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
        tooltip_text = (f"Select area positive/negative for selected polygon\n"
                        f"(Click UPDATE to update selected polygon)         ")
        Tooltip(area_neg_pos_select, tooltip_text)

        delete_polygon_button = tk.Button(self, text="DELETE POLYGON", command=delete_polygon,
                                          width=16, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        delete_polygon_button.place(relx=widgets_x_start, rely=0.465)
        tooltip_text = (f"Delete the selected polygon")
        Tooltip(delete_polygon_button, tooltip_text)

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
                selected_point = str(1 + max([int(k) for k in self.points.keys()]))
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

            last_highlight_element = self.canvas.find_withtag('highlight_element_point')
            self.update_graphics()
            if last_highlight_element:
                self.canvas.delete(last_highlight_element)
            node = GUIStatics.transform_node_to_canvas(node_coords)
            self.highlight_element_point = self.canvas.create_oval(node[0] - 10, node[1] - 10, node[0] + 10, node[1] + 10,
                                                             width=3, outline=GUIStatics.CANVAS_HIGHLIGHT_ELEMENT,
                                                             dash=(2, 1), fill='', tags='highlight_element_point')


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

            last_highlight_element = self.canvas.find_withtag('highlight_element_point')
            if last_highlight_element:
                self.canvas.delete(last_highlight_element)
            node = GUIStatics.transform_node_to_canvas(self.points[selected_point])
            self.highlight_element_point = self.canvas.create_oval(node[0] - 10, node[1] - 10, node[0] + 10, node[1] + 10,
                                                             width=3, outline=GUIStatics.CANVAS_HIGHLIGHT_ELEMENT,
                                                             dash=(2, 1), fill='', tags='highlight_element_point')

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
        single_point_def_label = tk.Label(self, text="Define Single Points", font=GUIStatics.STANDARD_FONT_MID_BOLD)
        single_point_def_label.place(relx=widgets_x_start, rely=0.55)
        single_point_select_label = tk.Label(self, text="Select Point:", font=GUIStatics.STANDARD_FONT_SMALL)
        single_point_select_label.place(relx=widgets_x_start, rely=0.585)
        single_point_var = tk.StringVar()
        single_point_var.set('None')
        if not self.points:
            self.points = {'None'}
        dropdown_single_point_select = tk.OptionMenu(self, single_point_var, *self.points)
        dropdown_single_point_select.config(font=GUIStatics.STANDARD_FONT_SMALL, width=4, height=1)
        tooltip_text = (f"Select a defined single point")
        Tooltip(dropdown_single_point_select, tooltip_text)
        dropdown_single_point_select.place(relx=widgets_x_start + 0.075, rely=0.58)
        if not self.points:
            dropdown_single_point_select["state"] = "disabled"
        single_point_var.trace('w', update_x_y_select_point)

        new_point_button = tk.Button(self, text="NEW", command=new_point,
                                     width=7, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        new_point_button.place(relx=widgets_x_start + 0.145, rely=0.583)
        tooltip_text = (f"Create a new single point     \n"
                        f"(Single points can be used as \n"
                        f"acoustic sound source)        ")
        Tooltip(new_point_button, tooltip_text)

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
        tooltip_text = (f"Update X/Y values for selected single point")
        Tooltip(add_point_button, tooltip_text)

        delete_point_button = tk.Button(self, text="DELETE POINT", command=delete_point,
                                        width=14, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALL)
        delete_point_button.place(relx=widgets_x_start, rely=0.71)
        tooltip_text = (f"Delete the selected single point")
        Tooltip(delete_point_button, tooltip_text)
        ##################################################
        # clear all button
        def clear_all():
            """
            Button action, clears all input
            :return:
            """
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
            self.polygon_node_var.set('None')
            dropdown_polygon_node_select["state"] = "disabled"
            update_dropdown_polygon_node_select_poly_info()

            # reset canvas
            all_canvas_elements = self.canvas.find_all()
            for elem in all_canvas_elements:
                self.canvas.delete(elem)
            GUIStatics.add_canvas_static_elements(self.canvas)

            # reset graphical input
            try:
                del Geometry.on_canvas_click.prevpoint
            except AttributeError:
                ...
            self.firstclick_canvas = True
            self.clicks_canvas = []

        button_clear_all = tk.Button(self, text="CLEAR ALL", command=clear_all,
                                     font=GUIStatics.STANDARD_FONT_BUTTON_MID, width=10, height=1)
        button_clear_all.place(relx=widgets_x_start + 0.22, rely=0.02)
        tooltip_text = (f"Clear all geometry input")
        Tooltip(button_clear_all, tooltip_text)

        # Check geometry button
        def check_geometry_on_button():
            """

            :return:
            """
            geom_okay, self.geometry_errors_list = self.check_geometry_detail()
            if geom_okay:
                GUIStatics.window_error(self, 'No errors in Geometry found!')
            else:
                check_geometry_error_window(quit=False)

        button_check_geometry = tk.Button(self, text="CHECK\nGEOMETRY", command=check_geometry_on_button,
                                     font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER, width=10, height=2)
        button_check_geometry.place(relx=widgets_x_start + 0.35, rely=0.02)
        tooltip_text = (f"Check Geometry for compatibility                       \n"
                        f"(Check will also be performed on click ACCEPT GEOMETRY)")
        Tooltip(button_check_geometry, tooltip_text)
        ##################################################
        def snap_canvas(pos):
            """
            highlights cursor position (snapped to closest grid point, where node will be created on click)
            :param pos:
            :return:
            """
            last_snap1 = self.canvas.find_withtag('highlight_snap1')
            last_snap2 = self.canvas.find_withtag('highlight_snap2')
            if last_snap1:
                self.canvas.delete(last_snap1)
            if last_snap2:
                self.canvas.delete(last_snap2)
            x, y = pos.x, pos.y
            snap_x, snap_y = self.find_grid(x, y)
            offset = 5
            self.canvas.create_line((snap_x - offset, snap_y - offset), (snap_x + offset + 1, snap_y + offset + 1), fill='#6A1616', tags='highlight_snap1')
            self.canvas.create_line((snap_x - offset, snap_y + offset), (snap_x + offset + 1, snap_y - offset - 1), fill='#6A1616',
                                    tags='highlight_snap2')

        # Add canvas for system visualization - DYNAMIC
        self.canvas = tk.Canvas(self, width=GUIStatics.CANVAS_SIZE_X, height=GUIStatics.CANVAS_SIZE_Y,
                                bg=GUIStatics.CANVAS_BG)
        self.canvas.place(relx=canvas_x + 0.0075, rely=canvas_y)
        GUIStatics.add_canvas_static_elements(self.canvas)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind('<Motion>', snap_canvas)
        ##################################################

        ##################################################
        # Update graphics
        GUIStatics.create_divider(self, widgets_x_start, 0.87, 230)
        button_update_graphics = tk.Button(self, text="UPDATE\nGRAPHICS", command=self.update_graphics,
                                           width=10, height=2, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        button_update_graphics.place(relx=widgets_x_start + 0.42, rely=0.02)
        tooltip_text = (f"Updates the graphics in canvas in case update not automatically performed\n"
                        f"(Usually not necessary)                                                  ")
        Tooltip(button_update_graphics, tooltip_text)

        ##################################################
        # Graphical input


        def button_clear_graph():
            clear_gprah()

        def clear_gprah():
            try:
                del Geometry.on_canvas_click.prevpoint
            except AttributeError:
                ...
            self.firstclick_canvas = True
            self.clicks_canvas = []
            self.update_graphics()

        def button_polygon_graph():
            if self.clicks_canvas:
                if len(self.clicks_canvas) < 3:
                    GUIStatics.window_error(self, 'Define at least 3 nodes\n'
                                                              'for valid polygon      ')
                    return
                if self.clicks_canvas[-1] == self.clicks_canvas[0]:
                    del self.clicks_canvas[-1]
                canvas_nodes_transformed = [list(GUIStatics.transform_canvas_to_node([float(node[0]), float(node[1])])) for node in self.clicks_canvas]
                if len(self.polygons) == 1 and not self.polygons['0']['coordinates']:
                    self.polygons['0'] = {'coordinates': canvas_nodes_transformed, 'area_neg_pos': 'Positive'}
                else:
                    self.polygons[str(len(self.polygons))] = {'coordinates': canvas_nodes_transformed, 'area_neg_pos': 'Positive'}
                polygon_select_var.set(str(len(self.polygons) - 1))
                clear_gprah()
            else:
                GUIStatics.window_error(self, 'Click on canvas below to \n'
                                                          'define nodes for polygon')

        def button_point_graph():
            if self.clicks_canvas:
                node = self.clicks_canvas[-1]
                canvas_nodes_transformed = GUIStatics.transform_canvas_to_node([float(node[0]), float(node[1])])
                if self.points == {'None'} or not self.points:
                    self.points = {'0': list(canvas_nodes_transformed)}
                else:
                    self.points[str(len(self.points))] = list(canvas_nodes_transformed)
                update_point_select_dropdown()
                selected_point = str(int(max(list(self.points.keys()))))
                single_point_var.set(selected_point)
                clear_gprah()
            else:
                GUIStatics.window_error(self, 'Click on canvas below to  \n'
                                                          'define nodes for polygon \n'
                                                          'Last node will be entered\n'
                                                          'as new single point      ')



        button_add_poly_graph = tk.Button(self, text="ADD CANVAS\nPOLYGON", command=button_polygon_graph,
                                           width=10, height=2, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        button_add_poly_graph.place(relx=0.54, rely=0.02)
        button_add_point_graph = tk.Button(self, text="ADD CANVAS\nPOINT", command=button_point_graph,
                                           width=10, height=2, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        button_add_point_graph.place(relx=0.61, rely=0.02)
        button_clear_graph = tk.Button(self, text="CLEAR\nINPUT", command=button_clear_graph,
                                           width=10, height=2, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        button_clear_graph.place(relx=0.68, rely=0.02)
        tooltip_text = (f"Add in canvas defined polygon                        \n"
                        f"(Alternative way to define polygons)                 \n"
                        f"1) Click on canvas to add polygon nodes              \n"
                        f"   (Click inside grid -> Node locks to 'NW' position)\n"
                        f"2) Click this button to add polygon to list          ")
        Tooltip(button_add_poly_graph, tooltip_text)

        tooltip_text = (f"Add in canvas defined point             \n"
                        f"(Alternative way to define single points\n"
                        f"First node on canvas will be added      ")
        Tooltip(button_add_point_graph, tooltip_text)

        tooltip_text = (f"Clear all clicks on canvas")
        Tooltip(button_clear_graph, tooltip_text)
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

            # check if lines in polygons intersect !works only if lines are not vertical...(missing slope)!
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
            # WIP

            # check if adjacent polygons share 2 nodes
            # WIP

            # check if single point inside positive polygon
            # WIP

            if node_count_error or intersect_error:
                comp = False
            return comp

        def check_geometry_error_window(quit=True):
            """
            error window if geometry is not accepted
            :return:
            """

            def accept_error_geom():
                self.return_geometry()
                geometry_error_window.destroy()
                self.destroy()
            geometry_error_window = tk.Toplevel(self)
            geometry_error_window.title("GEOMETRY ERROR")
            geometry_error_window.geometry(f"400x600")
            geometry_error_window.resizable(False, False)
            self.set_icon(geometry_error_window)

            lbl_str = ("GEOMETRY NOT COMPATIBLE\n"
                       "It is recommended to fix geometry \n"
                       "before proceeding!")
            info_str = (f"Compatible geometry:\n"
                        f"-Adjacent positive polygons must share at least two nodes\n"
                        f" and all nodes on common boundary must have identical nodes\n"
                        f"-All nodes of negative polygons\n"
                        f" must be inside positive polygons (no node on boundary)\n"
                        f"-Polygons must have at least 3 nodes and nodes must not duplicate\n"
                        f"-Polygons must not overlap or intersect\n"
                        f"-Points must be inside positive polygons and not on any boundary\n"
                        f"--> Check documentation/examples")
            error_str = 'Errors found:\n' + ''.join([f"-{elem}\n" for elem in self.geometry_errors_list])

            tk.Label(geometry_error_window, text=lbl_str, font=GUIStatics.STANDARD_FONT_BIG_BOLD,
                      anchor="sw", justify="left").place(relx=0.025, rely=0.05)
            if quit:
                tk.Button(geometry_error_window, text="ACCEPT GEOMETRY ANYWAY", command=accept_error_geom,
                          width=26, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_BIG).place(relx=0.22, rely=0.21)
            tk.Label(geometry_error_window, text=info_str, font=GUIStatics.STANDARD_FONT_SMALLER,
                     anchor="sw", justify="left").place(relx=0.025, rely=0.3)
            tk.Label(geometry_error_window, text=error_str, font=GUIStatics.STANDARD_FONT_SMALLER,
                     anchor="sw", justify="left").place(relx=0.025, rely=0.55)


        def check_and_accept():
            """
            Checks geometry and if compatible returns value to main gui, else error windo
            :return:
            """
            geom_okay, self.geometry_errors_list = self.check_geometry_detail()
            if geom_okay:
                self.return_geometry()
            else:
                check_geometry_error_window(quit=True)

        # Accept Geometry button - returns value for geometry input and destroys window


        button_accept = tk.Button(self, text="ACCEPT GEOMETRY", command=check_and_accept,
                                  width=16, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_BIG_BOLD)
        button_accept.place(relx=0.025, rely=0.935)
        tooltip_text = (f"Accept defined geometry and return to MAIN WINDOW")
        Tooltip(button_accept, tooltip_text)

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
                              'other'   : self.other}
            print("\n\n")
            print(f"self.polygons: {self.polygons}")
            print(f"self.polygon_nodes: {self.polygon_nodes}")
            print(f"self.points: {self.points}")
            print(f"self.geometry_input: {geometry_input}")

        # For Debug
        # button_debug = tk.Button(self, text="DEBUG", command=debug,
        #                          width=5, height=1, font=GUIStatics.STANDARD_FONT_BUTTON_SMALLER)
        # button_debug.place(relx=0.96, rely=0.005)
        ##################################################

        self.update_graphics()  # if Geometry class is loaded with input self.geometry_input, see init

    def check_geometry_detail(self):
        """
        Detailed check for geometry
        :return:
        """
        check_failed_list = []
        # check single points in positive polygon
        if self.points and self.points != {'None'}:
            for sp, point in enumerate(self.points.values()):
                in_poly = False
                for ip1, poly1 in enumerate(self.polygons.values()):
                    poly1_shapely = Polygon([(node[0], node[1]) for node in poly1['coordinates']])
                    if poly1_shapely.contains(Point(point[0], point[1])):
                        in_poly = True
                if not in_poly:
                    check_fail_str = f"Point {sp} not inside any positive polygon"
                    check_failed_list.append(check_fail_str)

        for ip1, poly1 in enumerate(self.polygons.values()):
            poly1_shapely = Polygon([(node[0], node[1]) for node in poly1['coordinates']])

            # check polygon shape
            # check if > 1 node have same position
            nodes_polygon = np.array(poly1['coordinates'])
            nodes_polygon_complex = [node[0] + 1j * node[1] for node in nodes_polygon]
            if len(set(nodes_polygon_complex)) != len(nodes_polygon):
                check_fail_str = f"At least two nodes of polygon {ip1} are identical"
                check_failed_list.append(check_fail_str)
            # check if polygon is valid (lines not crossing, area > 0)
            if not poly1_shapely.is_valid:
                check_fail_str = f"Polygon {ip1} invalid (Segments crossing/Zero Area)"
                check_failed_list.append(check_fail_str)

            # check single points in polygon
            if self.points and self.points != {'None'}:
                for sp, point in enumerate(self.points.values()):
                    p_in_pos_poly = False
                    if poly1_shapely.touches(Point(point[0], point[1])):
                        check_fail_str = f"Point {sp} on boundary of polygon {ip1}"
                        check_failed_list.append(check_fail_str)
                    if poly1_shapely.contains(Point(point[0], point[1])):
                        p_in_pos_poly = True
                        if poly1['area_neg_pos'] == 'Negative':
                            p_in_pos_poly = False
                            check_fail_str = f"Point {sp} inside of negative polygon {ip1}"
                            check_failed_list.append(check_fail_str)
            # check two polygons
            for ip2, poly2 in enumerate(list(self.polygons.values())[ip1 + 1:], start=ip1+1):
                poly2_shapely = Polygon([(node[0], node[1]) for node in poly2['coordinates']])

                # check if positive polygons overlap
                if poly1['area_neg_pos'] == 'Positive' and poly2['area_neg_pos'] == 'Positive':
                    if poly1_shapely.intersects(poly2_shapely):
                        if poly1_shapely.overlaps(poly2_shapely):
                            check_fail_str = f"Positive polygon {ip1} and positive polygon {ip2} overlap"
                            check_failed_list.append(check_fail_str)
                # check if negative polygons overlap
                if poly1['area_neg_pos'] == 'Negative' and poly2['area_neg_pos'] == 'Negative':
                    if poly1_shapely.intersects(poly2_shapely):
                        if poly1_shapely.overlaps(poly2_shapely):
                            check_fail_str = f"Negative polygon {ip1} and negative polygon {ip2} overlap"
                            check_failed_list.append(check_fail_str)
                        if poly1_shapely.touches(poly2_shapely):
                            check_fail_str = f"Negative polygon {ip1} and negative polygon {ip2} intersect/touch at least once"
                            check_failed_list.append(check_fail_str)
                # check if negative polygon inside positive polygon
                if poly1['area_neg_pos'] == 'Positive' and poly2['area_neg_pos'] == 'Negative':
                    if poly1_shapely.intersects(poly2_shapely):
                        if poly1_shapely.contains(poly2_shapely):
                            for node in poly2['coordinates']:
                                if poly1_shapely.touches(Point(node[0], node[1])):
                                    check_fail_str = f"Positive polygon {ip1} and negative polygon {ip2} overlap (on boundary)"
                                    check_failed_list.append(check_fail_str)
                                    break
                if poly1['area_neg_pos'] == 'Negative' and poly2['area_neg_pos'] == 'Positive':
                    if poly1_shapely.intersects(poly2_shapely):
                        if poly2_shapely.contains(poly1_shapely):
                            for node in poly1['coordinates']:
                                if poly2_shapely.touches(Point(node[0], node[1])):
                                    check_fail_str = f"Negative polygon {ip1} and positive polygon {ip2} overlap (on boundary)"
                                    check_failed_list.append(check_fail_str)
                                    break
                # check if two adjacent positive polygons share the same nodes
                if poly1['area_neg_pos'] == 'Positive' and poly2['area_neg_pos'] == 'Positive':
                    if poly1_shapely.intersects(poly2_shapely):
                        shared_boundary = poly1_shapely.intersection(poly2_shapely)
                        if shared_boundary.geom_type == 'LineString':
                            coords = list(shared_boundary.coords)
                        elif shared_boundary.geom_type == 'MultiLineString':
                            coords = []
                            for line in shared_boundary.geoms:
                                for point in line.coords:
                                    coords.append(point)
                        elif shared_boundary.geom_type == 'Point' and len(self.polygons.values()) == 2:
                            check_fail_str = f"Polygon {ip1} and polygon {ip2} share only one node"
                            check_failed_list.append(check_fail_str)
                        else:
                            coords = []
                        poly1nodes_complex = [node[0] + 1j * node[1] for node in np.array(poly1['coordinates'])]
                        poly2nodes_complex = [node[0] + 1j * node[1] for node in np.array(poly2['coordinates'])]
                        shared_nodes_complex = [node[0] + 1j * node[1] for node in coords]
                        in_poly1 = len(set(poly1nodes_complex).intersection(set(shared_nodes_complex)))
                        in_poly2 = len(set(poly2nodes_complex).intersection(set(shared_nodes_complex)))
                        if in_poly1 != in_poly2 and shared_boundary.geom_type != 'Point':
                            check_fail_str = f"Polygon {ip1} and polygon {ip2} do not share same nodes on common boundary"
                            check_failed_list.append(check_fail_str)

        # check if all positive polygons are connected
        all_pos_polygons = [Polygon(poly['coordinates']) for poly in self.polygons.values() if poly['area_neg_pos'] == 'Positive']
        unioned_polygons = unary_union(all_pos_polygons)
        if isinstance(unioned_polygons, MultiPolygon):
            check_fail_str = f"Positive polygons are not connected properly"
            check_failed_list.append(check_fail_str)
        check_failed_list = list(set(check_failed_list))


        if check_failed_list:
            return False, check_failed_list
        else:
            return True, None

    def update_graphics(self):
        """
        Updates the canvas, draws static elements (coordsystem, grid) and draws defined polygons and single points
        :return:
        """
        try:
            selected_polygon = self.polygon_selected
        except AttributeError:
            selected_polygon = None


        # delete all
        all_canvas_elements = self.canvas.find_all()
        for elem in all_canvas_elements:
            if elem == self.highlight_element or elem == self.highlight_element_point:
                continue
            self.canvas.delete(elem)

        # add grid etc
        GUIStatics.add_canvas_static_elements(self.canvas)

        # draw polygons
        for polygon_nbr, polygon_data in self.polygons.items():
            if selected_polygon == polygon_nbr:
                color_code_plus = '#9C4747'
                color_code_minus = '#4A5A99'
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
            if polygon_neg_pos == 'Negative':
                continue
            color_code = color_code_plus if polygon_neg_pos == 'Positive' else color_code_minus
            color_code_node = color_code_plus_node if polygon_neg_pos == 'Positive' else color_code_minus_node
            self.canvas.create_polygon(polygon_nodes_transformed, fill=color_code, outline='#341010', width=2)

            # add text to polygon, WIP: improve position finding
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

        for polygon_nbr, polygon_data in self.polygons.items():
            if selected_polygon == polygon_nbr:
                color_code_plus = '#9C4747'
                color_code_minus = '#4A5A99'
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
            if polygon_neg_pos == 'Positive':
                continue
            color_code = color_code_plus if polygon_neg_pos == 'Positive' else color_code_minus
            color_code_node = color_code_plus_node if polygon_neg_pos == 'Positive' else color_code_minus_node
            self.canvas.create_polygon(polygon_nodes_transformed, fill=color_code, outline='#341010', width=2)

            # add text to polygon, WIP: improve position finding
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

        for polygon_nbr, polygon_data in self.polygons.items():
            polygon_nodes = copy.deepcopy(polygon_data['coordinates'])
            if polygon_nodes:
                polygon_nodes += [polygon_nodes[0]]
                polygon_nodes_transformed = [GUIStatics.transform_node_to_canvas(node) for node in polygon_nodes]
                for na, ne in zip(polygon_nodes_transformed[:-1], polygon_nodes_transformed[1:]):
                    self.canvas.create_line(na, ne, fill='#341010', dash=(1, 1), width=1)
                    node = na
                    self.canvas.create_oval(node[0] - 3, node[1] - 3, node[0] + 3, node[1] + 3, fill='',
                                            outline='#1F1F1F', dash=(1, 1), width=1)

        # draw points
        if self.points != {'None'} and self.points:
            for point_nbr, node in self.points.items():
                node = GUIStatics.transform_node_to_canvas(node)
                text = f'Point {point_nbr}'
                self.canvas.create_oval(node[0] - 4, node[1] - 4, node[0] + 4, node[1] + 4, fill='#2D0F0F',
                                        outline='#1F1F1F', width=1)
                self.canvas.create_text(node[0], node[1] - 10, text=text, fill='#1F1F1F', font=("Helvetica", 7))

    def find_grid(self, coord_x: int, coord_y: int) -> Tuple[int, int]:
        """
        Locks mouse click on canvas for polygon creation to the closest grid point
        :param coord_x: int
        :param coord_y: int
        :return: Tuple[int, int]
        """

        grid_x = range(0, GUIStatics.CANVAS_SIZE_X + GUIStatics.GRID_SPACE, GUIStatics.GRID_SPACE)
        grid_y = range(0, GUIStatics.CANVAS_SIZE_Y + GUIStatics.GRID_SPACE, GUIStatics.GRID_SPACE)

        div_x = math.floor(coord_x / GUIStatics.GRID_SPACE)
        mod_x = coord_x % GUIStatics.GRID_SPACE
        div_y = math.floor(coord_y / GUIStatics.GRID_SPACE)
        mod_y = coord_y % GUIStatics.GRID_SPACE
        if mod_x <= 12:
            new_x = grid_x[div_x]
        else:
            new_x = grid_x[div_x + 1]
        if mod_y <= 12:
            new_y = grid_y[div_y]
        else:
            new_y = grid_y[div_y + 1]

        return new_x, new_y



    def on_canvas_click(self, event: tk.Canvas.bind):   # todo: correct?
        """
        todo
        """

        # Get coordinates of right click
        x, y = event.x, event.y

        # lock coordinates to grid
        x, y = self.find_grid(x, y)
        self.clicks_canvas.append([x, y])  # todo: Transform

        # create lines between points
        if self.firstclick_canvas == True:
            self.firstclick_canvas = False
        if 'prevpoint' in Geometry.on_canvas_click.__dict__ and not self.firstclick_canvas:
            self.canvas.create_line(Geometry.on_canvas_click.prevpoint[0], Geometry.on_canvas_click.prevpoint[1], x, y,
                                    fill="black", width=1)

        Geometry.on_canvas_click.prevpoint = (x, y)
        # create point at click
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, outline="black", fill="#851d1f")


    def return_geometry(self):
        """
        Callback method to return defined geometry to main class GUI
        :return:
        """
        # WIP: check if geometry is valid e.g. polgones have to be connects,
        #  only one polygon can be subtracted, points have to be in valid area, etc.
        self.geometry_input = {'polygons': self.polygons, 'points': self.points, 'units': self.units, 'other': None}
        if len(self.polygons) == 1 and not self.polygons['0']['coordinates']:
            GUIStatics.window_error(self, 'Create valid Geometry first!')
            return
        self.callback_geometry(self.geometry_input)
        self.destroy()  # closes top window


if __name__ == '__main__':
    geo = Geometry(lambda x: x, None)  # Develop: For testing Geometry gui, argument simulates callback
    geo.mainloop()
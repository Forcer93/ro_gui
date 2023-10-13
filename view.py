from datetime import datetime

import pandas as pd
from ScrollableRadiobuttonFrame import ScrollableRadiobuttonFrame
from ScrollableCheckboxFrame import ScrollableCheckBoxFrame

import tkinter as tk
import customtkinter
from tkintermapview import TkinterMapView

customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "Leitstandsoftware"
    WIDTH = 1024
    HEIGHT = 720
    
    LOG_PATH = "./log.csv"
    FILE_PATH = "./data.csv"
    df = pd.DataFrame()
    TASKS = pd.read_csv("./tasks.csv")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.bind("<Command-q>", self.on_closing)
        # self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []

        # Create file if not 
        open(App.LOG_PATH, 'a').close()

        

        # ============ create three CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_middle = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_middle.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, width=200, corner_radius=0, fg_color=None)
        self.frame_right.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        # now = datetime.now().strftime("%H:%M:%S")

        self.local_time_label = customtkinter.CTkLabel(self.frame_left, text=datetime.now().strftime("%H:%M:%S"), anchor="center", width=150, font=("Courier", 38))
        self.update_local_time()
        self.local_time_label.grid(row=1, column=0, padx=(20, 20), pady=(20, 20))

        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self.frame_left, width=150, command=self.checkbox_frame_event,
                                                                 item_list=[], height=400)
        self.scrollable_checkbox_frame.grid(pady=(0, 0), padx=(20, 20), row=2, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Bestätigen",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=4, column=0)


        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Anzeigemodus:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============


        self.frame_right.grid_rowconfigure(2, weight=1)

        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self.frame_right, width=500, command=self.radiobutton_frame_event,
                                                                    item_list=[],
                                                                    label_text="Inzidenzliste")
        self.scrollable_radiobutton_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=200)

        self.textbox = customtkinter.CTkTextbox(master=self.frame_right, corner_radius=0)
        self.textbox.grid(row=3, column=0, padx=(20, 20), sticky="nsew")

        self.button_1 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Update File",
                                                command=self.update_file)
        self.button_1.grid(pady=(20, 20), padx=(20, 20), row=5, column=0)




        # ============ frame_middle ============

        self.frame_middle.grid_rowconfigure(1, weight=1)
        self.frame_middle.grid_rowconfigure(0, weight=0)
        self.frame_middle.grid_columnconfigure(0, weight=1)
        self.frame_middle.grid_columnconfigure(1, weight=0)
        self.frame_middle.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_middle, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        # self.entry = customtkinter.CTkEntry(master=self.frame_middle,
        #                                     placeholder_text="type address")
        # self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        # self.entry.bind("<Return>", self.search_event)

        # self.button_5 = customtkinter.CTkButton(master=self.frame_middle,
        #                                         text="Search",
        #                                         width=90,
        #                                         command=self.search_event)
        # self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        self.map_widget.set_address("Berlin")
        # self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")


    # Update local time
    def update_local_time(self):
        self.local_time_label.configure(text=datetime.now())
        self.local_time_label.after(1000, self.update_local_time)


    # Call and update map based on input
    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    # Update map with given address
    def update_map(self, address: str):
        self.map_widget.set_address(address)

    # Set marker
    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))

    # Update and load file
    def update_file(self):

        self.scrollable_radiobutton_frame.remove_all()
        self.df = pd.read_csv(App.FILE_PATH, dtype={'tasks': str})
        print(self.df.to_string())
    
        for idx, row in self.df.iterrows():
            self.scrollable_radiobutton_frame.add_item(row['id'])
        # self.scrollable_radiobutton_frame.remove_item("")
            
    def checkbox_frame_event(self):
        print(f"checkbox frame modified: {self.scrollable_checkbox_frame.get_checked_items()}")

    # Import data from the chosen incidence
    def radiobutton_frame_event(self):

        select_item = self.scrollable_radiobutton_frame.get_checked_item()
        self.set_marker_event()

        print(f"ID is {select_item}")
        self.textbox.delete("0.0", tk.END)
        self.textbox.insert("0.0", self.df.loc[self.df['id'] == select_item, 'description'].squeeze())

        # print(self.df.loc[self.df['id'] == select_item, 'address'].squeeze())
        self.update_map(self.df.loc[self.df['id'] == select_item, 'address'].squeeze())
        self.update_tasks(select_item)
    
    # Import tasks for a given incidence
    def update_tasks(self, incidence: str):

        self.scrollable_checkbox_frame.remove_all()
        task_code = self.df.loc[self.df['id'] == incidence, 'tasks'].squeeze()

        for idx, row in App.TASKS.iterrows():
            
            if task_code[idx] == '1':
                self.scrollable_checkbox_frame.add_item(row['task'])
            

    # Clear markers
    def clear_marker_event(self):

        self.scrollable_checkbox_frame.remove_all()
        self.textbox.delete("0.0", tk.END)

        # for marker in self.marker_list:
        #     marker.delete()
        with open(App.LOG_PATH, "a") as f_out:
            f_out.write(f"{datetime.now()} - Incidence {self.scrollable_radiobutton_frame.get_checked_item()} finished")

        self.scrollable_radiobutton_frame.remove_item(self.scrollable_radiobutton_frame.get_checked_item())


    # Change dark / light / default mode
    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Change map on map type change
    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
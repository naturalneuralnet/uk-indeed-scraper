import tkinter as tk
from tkinter import ttk
import os
root = tk.Tk()



def call_command():
    search_param = name_entry.get()
    search_param = str(search_param)
    location_param = location_entry.get()
    if search_param != "Search" or location_param != "Location":
        command_cont =f'scrapy crawl indeedspider -a keywords="{search_param}" -a location="{location_param}"'
    
        os.system(command_cont)

        success_message = tk.Label(widgets_frame, text="Check the data folder for results!")
        success_message.grid(row=5, column=0)
    else:
        no_param_warning = tk.Label(
            widgets_frame, text="Enter search parameters!")
        no_param_warning.grid(row=5, column=0)
    

def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")

style = ttk.Style(root)

root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack()

widgets_frame = ttk.LabelFrame(frame, text="Scraper Inputs")
widgets_frame.grid(row=0, column=0, padx=20, pady=10)

name_entry = ttk.Entry(widgets_frame)
name_entry.insert(0, "Search")
name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
name_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")

location_entry = ttk.Entry(widgets_frame)
location_entry.insert(0, "Location")
location_entry.bind("<FocusIn>", lambda e: location_entry.delete('0', 'end'))
location_entry.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="ew")

button = ttk.Button(widgets_frame, text="Search", command=call_command)
button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")


separator = ttk.Separator(widgets_frame)
separator.grid(row=5, column=0, padx=[20, 10], pady=10, sticky="ew")


mode_switch = ttk.Checkbutton(
    widgets_frame, text="Mode", style="Switch", command=toggle_mode)
mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

root.mainloop()

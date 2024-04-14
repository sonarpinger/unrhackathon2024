import tkinter as tk

from gui import HomePage, Practice, Battle, DanceSelect
from choreography import Choreography

choreography_file_path = "./data/choreographies/chors.csv"

list_of_dances = Choreography.load_many_from_csv(choreography_file_path)


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main Menu")
        self.geometry("1920x1080")

        # expand frame to fill window
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, side="top", anchor="n")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for PageClass in [HomePage, Practice, Battle, DanceSelect]:
            page_name = PageClass.__name__
            self.pages[page_name] = PageClass(self.container, self)
            self.pages[page_name].grid(row=0, column=0, sticky="nsew")
            self.pages[page_name].configure(background="#A020F0")

        #self.dance = {}
        #for dance in list_of_dances:
        #    dance_name = dance.name
        #    self.dance[dance_name] = dance(self.container, self)
        #    self.dance[dance_name].grid(row=0, column=0, sticky="nsew")
        #    self.dance[dance_name].configure(background="#A020F0")

        self.show_page("HomePage")

    def show_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            page.tkraise()

    def show_dance(self, dance_name):
        page = self.pages.get("Practice")
        if page:
            page.tkraise()
            #page.load_dance(dance_name)
            print("Dance selected: ", dance_name)
        #dance = self.pages.get(dance_name)
        #if dance:
        #    dance.tkraise()

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
import cv2
import tkinter as tk
import cv2
import pygame

from gui import HomePage, Practice, Battle, DanceSelect, BattleSelect
from choreography import Choreography

choreography_file_path = "./data/choreographies/chors.csv"

list_of_dances = Choreography.load_many_from_csv(choreography_file_path)

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        # for sound
        pygame.mixer.init()

        self.title("Main Menu")
        self.geometry("1920x1080")

        self.cap = cv2.VideoCapture(0)

        # expand frame to fill window
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, side="top", anchor="n")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.webcam_frame = cv2.VideoCapture(0)
        self.webcam_frame.set(cv2.CAP_PROP_FPS, 25)

        self.pages = {}
        for PageClass in [HomePage, Practice, Battle, DanceSelect, BattleSelect]:
            page_name = PageClass.__name__
            self.pages[page_name] = PageClass(self.container, self)
            self.pages[page_name].grid(row=0, column=0, sticky="nsew")
            self.pages[page_name].configure(background="#A020F0")

        # load and play background music
        self.load_and_play_music("./data/sound/hackathonmenu.mp3")

        self.show_page("HomePage")

    def show_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            page.tkraise()

    def show_dance(self, dance_name):
        self.stop_music()
        page = self.pages.get("Practice")
        if page:
            page.tkraise()
            for dance in list_of_dances:
                if dance.name == dance_name:
                    #print(dance)
                    page.load_dance(dance)
            #page.load_dance(dance_name)
            #print("Dance selected: ", dance_name)
        #dance = self.pages.get(dance_name)
        #if dance:
        #    dance.tkraise()
    
    def pass_dance_selection(self, selection):
        page = self.pages.get("Battle")
        if page:
            page.load_selection(selection, list_of_dances)
            page.tkraise()
    
    def load_and_play_music(self, music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    
    def play_menu_music(self):
        self.load_and_play_music("./data/sound/hackathonmenu.mp3")
    
    def stop_music(self):
        pygame.mixer.music.stop()
    
    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
    app.cleanup()
    
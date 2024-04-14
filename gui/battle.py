import tkinter as tk
import cv2
from ultralytics import YOLO
import time
from PIL import Image, ImageTk

import pose_keypoints as pk
import dance_comparison_helpers as dch
import data_helpers as dh
import battle_mode_helpers as bmh
import error_detection as ed
from choreography import Choreography

class Battle(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.continue_looping = True

        self.selection = {
            "dance-moves": False,
            "floss-new": False,
            "gangnam-style": False,
            "get-griddy": False,
            "orange-justice": False,
            "take-the-l": False,
        }

        self.dances = []

        #side bar to show labels
        self.side_bar = tk.Frame(self)
        self.side_bar.pack(side=tk.LEFT, fill=tk.Y)

        # scores label
        self.scores_bar = tk.Frame(self.side_bar)
        self.scores_bar.pack(side=tk.TOP, pady=(30, 50))
        self.player1ScoreLabel = tk.Label(self.scores_bar, text="Player 1 Score: 0", font=("Terminal", 14))
        self.player1ScoreLabel.pack()
        self.player2ScoreLabel = tk.Label(self.scores_bar, text="Player 2 Score: 0", font=("Terminal", 14))
        self.player2ScoreLabel.pack()

        # selected dances:
        self.selected_dances_bar = tk.Frame(self.side_bar)
        self.selected_dances_bar.pack()
        self.selected_dances_title = tk.Label(self.selected_dances_bar, text = "Selected Dances", font=("Terminal", 14))
        self.selected_dances_title.pack(side=tk.TOP)
        self.selection_labels = []

        # countdown
        self.current_count = 3
        self.countdown_bar = tk.Frame(self.side_bar)
        self.countdown_bar.pack()
        self.countdown_bar_label = tk.Label(self.countdown_bar, text=str(self.current_count), font=("Terminal", 20))
        self.countdown_bar_label.pack()

        # buttons
        self.buttons_bar = tk.Frame(self.side_bar)
        self.buttons_bar.pack(side=tk.BOTTOM, pady=(20, 30))
        self.endbutton = tk.Button(self.side_bar, text="End Battle", bg="#A020F0", font=("Terminal", 14), command=lambda: self.back_to_home())
        self.endbutton.pack(side=tk.BOTTOM, fill=tk.X)
        # self.endbutton = tk.Button(self.side_bar, text="Pause Battle", bg="#A020F0", font=("Terminal", 14), command=lambda: self.loop_pause())
        # self.endbutton.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,20))
        self.startbutton = tk.Button(self.side_bar, text="Start Battle", bg="#A020F0", font=("Terminal", 14), command=lambda: self.begin_battle())
        self.startbutton.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,20))

        # video display labels
        self.video_label = tk.Label(self)
        self.video_label.place(x=320, y=25, width=1440, height=960)
        self.webcam_video_label = tk.Label(self)
        self.webcam_video_label.place(x=320, y=25, width=320, height=240)

        # game loop stuff
        self.flags = {
            "countdown" : True,
            "analytics" : False,
            "limb_view" : False,
            "score_timing" : 3
        }
        self.body = dch.init_body_v2()
        self.model = YOLO("./yolov8n-pose.pt")
        self.players = [
            {
                "name" : "Player 1",
                "score" : 0,
                "cd_message" : "Get ready Player 1!"
            },
            {
                "name" : "Player 2",
                "score" : 0,
                "cd_message" : "Get ready Player 2!"
            }
        ]
        
        # cv2 stuff
        self.camera_stuff = dch.init_camera_v2(self.controller) # init webcam
        self.cap = self.camera_stuff["cap"]
        # self.cap = cv2.VideoCapture(0)
        self.window_caption = "Dance Planet"
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.frame_counter = 0
        
        # countdown 
        self.countdown = 3

        # analytics
        self.error_over_time = []
        self.frames = []
        self.chart = None

    def load_selection(self, selection, dances : list):
        self.selection = selection
        print(f"selection: {self.selection}")
        for key in self.selection.keys():
            if self.selection[key]:
                dance_label = tk.Label(self.selected_dances_bar, text=key, font=("Terminal", 12))
                dance_label.pack()
                self.selection_labels.append(dance_label)
                self.dances.append(Choreography.get_chor_from_chors(key, dances))

    def begin_battle(self):
        self.continue_looping = True
        self.game_loop()

    # def frame_process(self):

    def update_labels(self, web_frame, vid_frame):
        web_frame = cv2.cvtColor(web_frame, cv2.COLOR_BGR2RGB)
        web_frame = Image.fromarray(web_frame)
        web_frame = web_frame.resize((320, 240))
        img_tk = ImageTk.PhotoImage(image=web_frame)
        self.webcam_video_label.img_tk = img_tk  # Keep reference to avoid garbage collection
        self.webcam_video_label.config(image=img_tk)

        vid_frame = cv2.cvtColor(vid_frame, cv2.COLOR_BGR2RGB)
        vid_frame = Image.fromarray(vid_frame)
        vid_frame = vid_frame.resize((1440, 960))
        img_tk = ImageTk.PhotoImage(image=vid_frame)
        self.video_label.img_tk = img_tk  # Keep reference to avoid garbage collection
        self.video_label.config(image=img_tk)

        # update scores
        p1_score = self.players[0]["score"]
        p2_score = self.players[1]["score"]
        self.player1ScoreLabel.config(text=f"Player 1 Score : {p1_score}")
        self.player2ScoreLabel.config(text=f"Player 2 Score : {p2_score}")

        # update countdown if applicable
        self.countdown_bar_label.config(text=str(self.current_count))

    def game_loop(self):
        quit = False
        for dance in self.dances:

            print(f"On dance {dance.name}")

            # get dance data
            threshold = dance.threshold
            above_ratio = dance.above_ratio
            below_ratio = dance.below_ratio
            temporal_size = dance.temporal_size
            sma_window = dance.sma_window
            song_min_error = dance.min_error
            song_max_error = dance.max_error

            keys_df = dance.df
            video_frames = dance.video_frames
            video_frames_right_bound = len(video_frames) - 1

            for i, player in enumerate(self.players):

                print("On " + str(player["name"]))

                # init
                last_score_time = time.time()
                self.frame_counter = 0

                # maybe try to incorporate this loading into the countdown

                if self.flags["countdown"]:
                    start_time = time.time()

                    while self.cap.isOpened():
                        ret, frame = self.cap.read()
                        if not ret:
                            break

                        # calculate the time elapsed
                        elapsed_time = time.time() - start_time
                        
                        # Update the countdown
                        self.current_count = self.countdown - int(elapsed_time)
                        if self.current_count < 0:
                            # end countdown if reaches end time (less than 0)
                            break
                        
                        # Put the countdown text on the frame
                        cv2.putText(frame, str(self.current_count), (50, 50), self.font, 2, (255, 0, 0), 3, cv2.LINE_AA)

                        # Display the resulting frame
                        cv2.putText(frame, player["cd_message"], (50, 100), self.font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Update text on the same frame
                        self.update_labels(frame, video_frames[self.frame_counter])

                        # Break the loop with 'Q' key
                        if cv2.waitKey(100) & 0xFF == ord('q'):
                            break

                print("finished countdown")

                while self.cap.isOpened():
                    ret, frame = self.cap.read()
                    if not ret:
                        break

                    # get keypoints and bounding box from model
                    model_stuff = dch.run_model(frame, self.model)
                    # get normalized body list by using camera frame size, model output, and standard body limb setup
                    norm_body = pk.body_normalize(self.camera_stuff, model_stuff, self.body)
                    # add horizontal flip of keypoints if on webcam
                    norm_body = pk.horizontal_body_flip(self.camera_stuff, norm_body)

                    # temporal stuff for error detecting
                    temporal_left_bound = self.frame_counter - temporal_size if self.frame_counter - temporal_size >= 0 else 0
                    temporal_right_bound = self.frame_counter + temporal_size if self.frame_counter + temporal_size <= video_frames_right_bound else video_frames_right_bound
                    temporal_frame_range = [temporal_left_bound, temporal_right_bound]
                    current_source_body_index = (temporal_right_bound - temporal_left_bound) // 2
                    # get source keypoints for comparison
                    source_bodies_raw = dh.get_keypoints_from_df_range(keys_df, temporal_frame_range)
                    # convert to usable keypoints
                    source_bodies_usable = [dh.usable_keypoints_v2(keys) for keys in source_bodies_raw]
                    # get error
                    error = ed.min_temporal_pose_error(source_bodies_usable, norm_body, threshold, above_ratio, below_ratio)
                    temp = self.error_over_time + [error]
                    error_adjusted = ed.simple_moving_average(temp, sma_window)
                    self.error_over_time.append(error_adjusted)

                    # display on screen
                    caption = f"Error: {error_adjusted}"
                    source_frame = video_frames[self.frame_counter]

                    # check score
                    current_time = time.time()
                    if current_time - last_score_time >= self.flags["score_timing"]:  # Check if one second has passed
                        score = ed.error_to_score(song_min_error, song_max_error, error_adjusted)  # Run the function
                        self.players[i]["score"] += score
                        cv2.putText(source_frame, f"+{int(score)} points!", (250, 50), self.font, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        last_score_time = current_time  # Reset the last run time
                    
                    if self.flags["limb_view"]:
                        dch.add_limbs_to_frame(norm_body, self.camera_stuff["norm_box_0"], frame)
                        dch.add_limbs_to_frame(source_bodies_usable[current_source_body_index], self.camera_stuff["norm_box_0"], source_frame)
                        # vis_caption = f"visibility score: {dch.visibility_score(norm_body)}"
                        # cv2.putText(source_frame, vis_caption, (200, 200), self.font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Update text on the same frame

                    # true display
                    cv2.putText(source_frame, caption, (50, 100), self.font, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Update text on the same frame
                    self.update_labels(frame, source_frame)

                    #increment
                    self.frame_counter += 1
                    # self.frames.append(source_frame)

                    # end if frame_counter reaches end
                    if self.frame_counter == video_frames_right_bound + 1:
                        break

                    # break loop if q
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        quit = True
                        break
                if quit:
                    break
            if quit:
                break

        # go to results page?


    def loop_pause(self):
        self.continue_looping = not self.continue_looping
        # add paused view to this
        pass

    def back_to_home(self):
        self.continue_looping = False
        # reset when leaving menu
        self.cleanup()
        self.controller.show_page("HomePage")
    
    def cleanup(self):
        self.selection = {
            "dance-moves": False,
            "floss-new": False,
            "gangnam-style": False,
            "get-griddy": False,
            "orange-justice": False,
            "take-the-l": False,
        }
        self.dances.clear()
        for label in self.selection_labels:
            label.pack_forget()
        self.selection_labels.clear()
import tkinter as tk
import cv2
import time
from PIL import Image, ImageTk
import threading
from ultralytics import YOLO

import pose_keypoints as pk
import dance_comparison_helpers as dch
import data_helpers as dh
import practice_mode_helpers as bmh
import error_detection as ed
from choreography import Choreography

class Practice(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.continue_looping = True

        self.side_bar = tk.Frame(self)
        self.side_bar.pack(side=tk.LEFT, fill=tk.Y)
        self.scores_bar = tk.Frame(self.side_bar)
        self.scores_bar.pack(side=tk.TOP, pady=(30, 50))
        self.player1ScoreLabel = tk.Label(self.scores_bar, text="Score: 0", font=("Terminal", 14))
        self.player1ScoreLabel.pack()
        #self.highScoreLabel = tk.Label(self.side_bar, text="High Score: 0", font=("Terminal", 14))
        #self.highScoreLabel.pack()
        self.danceLabel = tk.Label(self.side_bar, text="Dance: ", font=("Terminal", 14))
        self.danceLabel.pack()

        self.endbutton = tk.Button(self.side_bar, text="End Game", bg="#A020F0", font=("Terminal", 14), command=lambda: self.back_to_home())
        self.endbutton.pack(side=tk.BOTTOM, fill=tk.X)
        self.endbutton = tk.Button(self.side_bar, text="Restart Game", bg="#A020F0", font=("Terminal", 14), command=lambda: self.loop_reenable())
        self.endbutton.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,20))
        self.startbutton = tk.Button(self.side_bar, text="Start Game", bg="#A020F0", font=("Terminal", 14), command=lambda: self.update_video_streams())
        self.startbutton.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,20))

        self.video_label = tk.Label(self)
        self.video_label.place(x=320, y=25, width=1440, height=960)
        self.webcam_video_label = tk.Label(self)
        self.webcam_video_label.place(x=320, y=25, width=320, height=240)

        self.countdown = 5

        # game loop stuff
        self.flags = {
            "countdown" : True,
            "analytics" : False,
            "limb_view" : True,
            "score_timing" : 3,
            "hf" : False
        }
        self.body = dch.init_body_v2()
        self.model = YOLO("./yolov8n-pose.pt")

    def begin_battle(self):
        self.continue_looping = True
        self.players = [
            {
                "name" : "Player 1",
                "score" : 0,
                "cd_message" : "Get ready Player 1!"
            }
        ]
        threading.Thread(target=self.game_loop, daemon=True).start()

    def gui_update(self, frames):
        self.after(0, self.update_labels, frames)

    def update_labels(self, frames):
        web_frame, vid_frame = frames
        web_frame = cv2.cvtColor(web_frame, cv2.COLOR_BGR2RGB)
        web_frame = cv2.flip(web_frame, 1)
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
        self.player1ScoreLabel.config(text=f"Player 1 Score : {int(p1_score)}")

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
                        # self.update_labels(frame, video_frames[self.frame_counter])
                        self.gui_update((frame, video_frames[self.frame_counter]))

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
                    if self.flags["hf"]:
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
                    # self.update_labels(frame, source_frame)
                    self.gui_update((frame, source_frame))

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

    def update_video_streams(self):
        ret1, web_frame = self.capture_webcam.read()
        ret2, vid_frame = self.capture_video.read()
        if ret1 and ret2:
            web_frame = cv2.cvtColor(web_frame, cv2.COLOR_BGR2RGB)
            web_frame = Image.fromarray(web_frame)
            web_frame = web_frame.resize((320, 240))
            self.web_frame = web_frame
            img_tk = ImageTk.PhotoImage(image=web_frame)
            self.webcam_video_label.img_tk = img_tk  # Keep reference to avoid garbage collection
            self.webcam_video_label.config(image=img_tk)

            vid_frame = cv2.cvtColor(vid_frame, cv2.COLOR_BGR2RGB)
            vid_frame = Image.fromarray(vid_frame)
            #vid_frame = vid_frame.resize((1440, 960))
            img_tk = ImageTk.PhotoImage(image=vid_frame)
            self.video_label.img_tk = img_tk  # Keep reference to avoid garbage collection
            self.video_label.config(image=img_tk)

            self.update_score()
            # cv2.imshow('frame', frame)
            # cv2.waitKey(1)
        else:
            self.capture_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        if self.continue_looping:
            self.webcam_video_label.after(10, self.update_video_streams)
        else:
            self.video_label.after_cancel(self.update_video_streams)

    def loop_reenable(self):
        if not self.continue_looping:
            self.continue_looping = True
            self.capture_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.update_video_streams()
            self.scoreLabel.config(text="Score: 0")

    def update_score(self):
        self.score = int(self.danceerror.get_score(self.web_frame))
        print(self.score)
        self.scoreLabel.config(text="Score: " + str(self.score))
        self.scoreLabel.after(1000, self.update_score)

    def load_dance(self, dance):
        self.danceerror = DanceError(dance)
        dance_name = dance.name
        if dance_name == "dance-moves":
            dance_name = "Default"
        elif dance_name == "floss-new":
            dance_name = "Floss"
        elif dance_name == "gangnam-style":
            dance_name = "Gangnam Style"
        elif dance_name == "get-griddy":
            dance_name = "Griddy"
        elif dance_name == "orange-justice":
            dance_name = "Orange Justice"
        elif dance_name == "take-the-l":
            dance_name = "Take the L"

        danceLabel = "Dance: " + dance_name
        self.danceLabel.config(text=danceLabel)
        self.csv_path = dance.csv_path
        self.mp4_path = dance.mp4_path
        self.icon_path = dance.icon_path
        self.threshold = dance.threshold
        self.above_ratio = dance.above_ratio
        self.below_ratio = dance.below_ratio
        self.temporal_size = dance.temporal_size
        self.sma_window = dance.sma_window
        self.min_error = dance.min_error
        self.max_error = dance.max_error
        self.score_timing = dance.score_timing

        self.score = 0
        self.capture_video = cv2.VideoCapture(self.mp4_path)
        self.capture_video.set(cv2.CAP_PROP_FPS, 25)

        self.capture_webcam = self.controller.webcam_frame
        #self.capture_webcam = cv2.VideoCapture(0)
        #self.capture_webcam.set(cv2.CAP_PROP_FPS, 25)

        #pass

    def back_to_home(self):
        self.continue_looping = False
        self.controller.show_page("HomePage")
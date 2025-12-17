import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import webbrowser
from login import IS_LOGGED_IN
from progress_tracking import ProgressTrackingApp
# --- Global Variables (REQUIRED) ---
LOGGED_IN_USER = None
# -----------------------------------

class Mainpage:
    def __init__(self, root):
        self.root = root
        self.root.title("FitQuest Main Page")
        self.login_handler = None # For external app switching
        
        # --- Profile & Data Initialization ---
        self.user_id = LOGGED_IN_USER # Get status from global
        self.stats_frame = None # This will track the entire stats bar container
        # Define a detailed default profile structure
        self.default_profile = {
            'Username': 'Guest'
        }
        self.user_profile = self.default_profile.copy()
        # -------------------------------------
        
        # Color scheme
        self.colors = {
            'primary': '#FE0161',# Pinkish Red
            'secondary': '#4682B4',# Steel Blue
            'dark': '#2F4F4F', # Dark Slate Gray
            'light': '#F5F5F5',
            'card': '#FFFFFF',
            'text': '#333333',
            'text_light': '#666666',
            'accent': '#FF6B6B', # Coral Red
            'warning': '#FFA500', # Orange
            'success': '#32CD32', # Lime Green
            'danger': '#DC3545'# Red for delete buttons
        }

        # Set window to maximized
        self.root.state("zoomed")
        self.root.configure(bg=self.colors['light']) # Set background color

        # Store workout schedule and log
        self.schedule = {}
        self.exercise_log = []

        #Fitness quotes
        self.quotes = [
            "A one hour workout is 4% of your day. No excuses.",
        ]

        # Fitness programs
        self.programs = [
            { "name": "Push-up Program", "description": "Build chest and arm strength", "youtube": "https://www.youtube.com/watch?v=IODxDxX7oi4", "difficulty": "Beginner", "calories": "80-120 per 15 mins", "focus": "Chest, Arms, Core" },
            { "name": "Sit-up Challenge", "description": "Core strengthening exercises",  "youtube": "https://www.youtube.com/watch?v=1fbU_MkV7NE", "difficulty": "Beginner", "calories": "60-90 per 15 mins", "focus": "Abs, Core" },
            { "name": "Squat Mastery", "description": "Build powerful legs and glutes",  "youtube": "https://www.youtube.com/watch?v=aclHkVaku9U", "difficulty": "Intermediate", "calories": "100-150 per 15 mins", "focus": "Legs, Glutes" },
            { "name": "Plank Progression", "description": "Core stability training",  "youtube": "https://www.youtube.com/watch?v=pSHjTRCQxIw", "difficulty": "Beginner", "calories": "40-70 per 10 mins", "focus": "Core, Shoulders" },
            { "name": "Pull-up Training", "description": "Upper back strength", "youtube": "https://www.youtube.com/watch?v=eGo4IYlbE5g", "difficulty": "Advanced", "calories": "70-110 per 15 mins", "focus": "Back, Arms" },
            { "name": "Lunge Program", "description": "Leg and balance training", "youtube": "https://www.youtube.com/watch?v=QOVaHwm-Q6U", "difficulty": "Intermediate", "calories": "90-130 per 15 mins", "focus": "Legs, Glutes" }
        ]

        self.setup_ui()
    
    # ----------------------------------------------------
    # --- DATA LOADING AND PERSISTENCE METHODS ---
    # ----------------------------------------------------
    
    def _load_user_profile_data(self):
        """Returns profile based on global variable instead of JSON file."""
        current_profile = self.default_profile.copy()
        if LOGGED_IN_USER:
            current_profile['Username'] = LOGGED_IN_USER
        return current_profile
        
    # ----------------------------------------------------
    # --- UTILITY AND SETUP METHODS ---
    # ----------------------------------------------------
    
    def set_login_handler(self, handler_function):
        self.login_handler = handler_function

    def start_login_process(self):
        if self.login_handler:
            self.login_handler()

    def setup_ui(self):
        # Create main container
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill="both", expand=True)
        program_card_container = tk.Frame(main_container, bg=self.colors['light'], width=1200, height=800) 
        # Top banner with taskbar
        self.create_taskbar(main_container)

        # Main content area with scrollbar
        self.create_main_content(main_container)

        # Show home screen by default 
        self.show_home_screen()

    def create_taskbar(self, parent):
        banner = tk.Frame(parent, bg=self.colors['primary'], height=70)
        banner.pack(fill="x", side="top")
        banner.pack_propagate(1)

        # App logo
        self.logo_image_ref = None
        try:
            # NOTE: Assuming 'fitness.png' exists in the script's directory.
            self.logo_image_ref = tk.PhotoImage(file="resource/fitness.png")
            self.logo_image_ref = self.logo_image_ref.subsample(5, 5)
        except Exception:
            self.logo_image_ref = None
            
        logo_frame = tk.Frame(banner, bg=self.colors['primary'])
        logo_frame.pack(side="left", padx=20)

        app_name = tk.Label(logo_frame,
                            image=self.logo_image_ref, 
                            compound=tk.LEFT if self.logo_image_ref else tk.CENTER,
                            text = "FitQuest",
                            font=("Arial", 24, "bold"),
                            bg=self.colors['primary'],
                            fg=self.colors['light']
                            )
        app_name.pack(padx=10) 

        # Taskbar buttons in center
        taskbar_frame = tk.Frame(banner, bg=self.colors['primary'])
        taskbar_frame.pack(side="left", padx=100)

        buttons = [
            ("🏠 Home", self.show_home_screen),
            ("👤 Profile", self.show_profile),
            ("🔥 Calorie Calculator", self.show_calorie_calculator),
            ("📊 Progress Tracker & Exercise Log", self.show_progress_tracker)   
        ]
        
        for (text, command) in buttons:
            btn = tk.Button(taskbar_frame,
                            text=text,
                            command=command,
                            font=("Arial", 12),
                            bg=self.colors['primary'],
                            fg=self.colors['light'],
                            bd=0,
                            activebackground=self.colors['secondary'],
                            activeforeground=self.colors['light'],
                            padx=9,
                            pady=8
                            )
            btn.pack(side="left", padx=0)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors['secondary']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors['primary']))

        data_frame = tk.Frame(banner, bg=self.colors['primary'])
        data_frame.pack(side="right", padx=10)

        current_date = datetime.now().strftime("%A, %d %B %Y")
        date_label = tk.Label(data_frame,
                             text=current_date,
                             font=("Arial", 12),
                             bg=self.colors['primary'],
                             fg=self.colors['light']
                             )
        date_label.pack()

    def create_main_content(self, program_card_container): 
        self.canvas = tk.Canvas(program_card_container, bg=self.colors['light'], highlightthickness=0)
        scrollbar = tk.Scrollbar(program_card_container, orient="vertical", command=self.canvas.yview) 

        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['light'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def clear_content(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def open_video(self, program):
        """Opens the YouTube link for the program using the webbrowser module."""
        video_url = program['youtube']
        try:
            webbrowser.open(video_url)
        except Exception:
            messagebox.showerror("Error", f"Could not open video link:\n{video_url}")

    # ----------------------------------------------------
    # --- VIEW METHODS (SCREENS) ---
    # ----------------------------------------------------

    def show_home_screen(self):
        self.clear_content()
        self.everyrow_frame = tk.Frame(self.scrollable_frame, bg=self.colors['light'], width=1200, height=800)
        display_name = LOGGED_IN_USER#self.user_profile.get('Username', 'Guest')

        # Welcome
        welcome_frame = tk.Frame(self.everyrow_frame, bg=self.colors['light'])
        welcome_frame.pack(fill='x', padx=30,pady=20)

        welcome_label = tk.Label(welcome_frame,
                                 text = f"Welcome back, {display_name}!",
                                 font=("Arial", 28, "bold"),
                                 fg=self.colors['dark'],
                                 bg=self.colors['light']  
                                 )
        welcome_label.pack(anchor="w")

        # Quote
        quote_frame = tk.Frame(self.everyrow_frame, bg=self.colors['card'])
        quote_frame.pack(fill='x', padx=30, pady=(0, 30))
        
        quote_label = tk.Label(quote_frame,
                              text=f'"{self.quotes[0]}"',
                              font=('Arial', 14, 'italic'),
                              fg=self.colors['text'],
                              bg=self.colors['card'],
                              wraplength=1100,
                              justify='center')
        quote_label.pack(padx=20, pady=20)

        # Today's workout reminder
        today = datetime.now().strftime("%Y-%m-%d")
        if today in self.schedule:
            reminder_frame = tk.Frame(self.everyrow_frame, bg=self.colors['warning'])
            reminder_frame.pack(fill='x', padx=30, pady=(0, 30))
            
            reminder = tk.Label(reminder_frame,
                                 text=f"📅 Today's Workout: {self.schedule[today]}",
                                 font=('Arial', 14, 'bold'),
                                 fg='white',
                                 bg=self.colors['warning'])
            reminder.pack(padx=20, pady=15)

        # Fitness programs section
        programs_label = tk.Label(self.everyrow_frame,
                                 text="Fitness Programs",
                                 font=("Arial", 22, "bold"),
                                 bg=self.colors['light'],
                                 fg=self.colors['dark'])
        programs_label.pack(pady=(0, 20))
        
        for i in range(0, len(self.programs), 3):
            row_frame = tk.Frame(self.everyrow_frame, bg=self.colors['light'])
            row_frame.pack(anchor='center', pady=50)
            for j in range(3):
                if i + j < len(self.programs):
                    program = self.programs[i + j]
                    self.create_program_card(row_frame, program).pack(side='left', padx=50)
        self.everyrow_frame.pack(anchor="center", pady=20)
        self.show_quick_stats()
        
    def show_quick_stats(self):
        """Show quick statistics on home screen"""
        self.destroy_quick_stats()
          
        # --- FIXED SECTION START ---
        # Create ONE main container and assign it to self.stats_frame.
        self.stats_frame = tk.Frame(self.root, bg=self.colors['card'], height=50)
        self.stats_frame.pack(fill="x", side="bottom")

        # Create a single frame inside the container to hold the stats content.
        mainstats_frame = tk.Frame(self.stats_frame, bg=self.colors['card'])
        mainstats_frame.pack(fill="x")
        # --- FIXED SECTION END ---

        # Calculate stats
        total_workouts = len(self.exercise_log)
        calories_burned = sum(log.get('calories', 0) for log in self.exercise_log)
        scheduled_workouts = len(self.schedule)
        available_programs = len(self.programs)

        # Individual stat frames
        everystate_frame = tk.Frame(mainstats_frame, bg=self.colors['card'])
        stat1_frame = tk.Frame(everystate_frame, bg=self.colors['card'])
        stat1_frame.pack(side='left', padx=(0,0), pady=20)
        stat1_value = tk.Label(stat1_frame, text=f"{total_workouts}", font=('Arial', 24, 'bold'),
                               fg=self.colors['primary'], bg=self.colors['card'])
        stat1_value.pack(padx=10, pady=(0, 5))
        stat1_label = tk.Label(stat1_frame, text="Total Workouts", font=('Arial', 11),
                               fg=self.colors['text_light'], bg=self.colors['card'])
        stat1_label.pack(padx=10)

        stat2_frame = tk.Frame(everystate_frame, bg=self.colors['card'])
        stat2_frame.pack(side='left', padx=(150,0), pady=20)
        stat2_value = tk.Label(stat2_frame, text=f"{calories_burned}", font=('Arial', 24, 'bold'),
                               fg=self.colors['primary'], bg=self.colors['card'])
        stat2_value.pack(padx=10, pady=(0, 5))
        stat2_label = tk.Label(stat2_frame, text="Calories Burned", font=('Arial', 11),
                               fg=self.colors['text_light'], bg=self.colors['card'])
        stat2_label.pack(padx=10)

        stat3_frame = tk.Frame(everystate_frame, bg=self.colors['card'])
        stat3_frame.pack(side='left', padx=(150,0), pady=20)
        stat3_value = tk.Label(stat3_frame, text=f"{scheduled_workouts}", font=('Arial', 24, 'bold'),
                               fg=self.colors['primary'], bg=self.colors['card'])
        stat3_value.pack(padx=10, pady=(0, 5))
        stat3_label = tk.Label(stat3_frame, text="Scheduled Workouts", font=('Arial', 11),
                               fg=self.colors['text_light'], bg=self.colors['card'])
        stat3_label.pack(padx=10)

        stat4_frame = tk.Frame(everystate_frame, bg=self.colors['card'])
        stat4_frame.pack(side='left', padx=(150,0), pady=20)
        stat4_value = tk.Label(stat4_frame, text=f"{available_programs}", font=('Arial', 24, 'bold'),
                               fg=self.colors['primary'], bg=self.colors['card'])
        stat4_value.pack(padx=10, pady=(0, 5))
        stat4_label = tk.Label(stat4_frame, text="Available Programs", font=('Arial', 11),
                               fg=self.colors['text_light'], bg=self.colors['card'])
        stat4_label.pack(padx=10)
        everystate_frame.pack(anchor="center")

    def destroy_quick_stats(self):
        if self.stats_frame is not None:
            self.stats_frame.destroy()
            self.stats_frame = None

    def create_program_card(self, parent, program):
        """Create a program card with watch button"""
        card_frame = tk.Frame(parent,
                              bg=self.colors['card'],
                              width=350,
                              height=250,
                              relief='solid',
                              borderwidth=1)
        card_frame.pack_propagate(False) 
        
        # Program name
        name_label = tk.Label(card_frame,
                              text=program['name'],
                              font=('Arial', 16, 'bold'),
                              fg=self.colors['primary'],
                              bg=self.colors['card'])
        name_label.pack(pady=(15, 5))
        
        # Difficulty
        diff_color = {
            'Beginner': self.colors['success'],
            'Intermediate': self.colors['warning'],
            'Advanced': self.colors['accent']
        }
        
        diff_frame = tk.Frame(card_frame, bg=self.colors['card'])
        diff_frame.pack(pady=5)
        
        diff_label = tk.Label(diff_frame,
                              text=program['difficulty'],
                              font=('Arial', 10, 'bold'),
                              fg='white',
                              bg=diff_color[program['difficulty']],
                              padx=10,
                              pady=3)
        diff_label.pack()
        
        # Description
        desc_label = tk.Label(card_frame,
                              text=program['description'],
                              font=('Arial', 11),
                              fg=self.colors['text'],
                              bg=self.colors['card'],
                              wraplength=320)
        desc_label.pack(pady=10, padx=15)
        
        # Calories
        calorie_label = tk.Label(card_frame,
                                 text=f"🔥 {program['calories']}",
                                 font=('Arial', 10),
                                 fg=self.colors['text_light'],
                                 bg=self.colors['card'])
        calorie_label.pack()
        
        # Focus
        focus_label = tk.Label(card_frame,
                              text=f"🎯 {program['focus']}",
                              font=('Arial', 10),
                              fg=self.colors['text_light'],
                              bg=self.colors['card'])
        focus_label.pack(pady=5)
        
        # Watch button
        watch_btn = tk.Button(card_frame,
                              text="▶ Watch Tutorial",
                              font=('Arial', 11),
                              bg=self.colors['primary'],
                              fg='white',
                              padx=15,
                              pady=5,
                              command=lambda p=program: self.open_video(p))
        watch_btn.pack(pady=15)
        
        return card_frame

    def show_profile(self):
        self.destroy_quick_stats()
        self.clear_content()

        # Check login status: true if the user_id is NOT the generic 'Guest'
        is_logged_in = self.user_id != 'Guest'
        
        # Header
        header = tk.Label(self.scrollable_frame,
                          text="👤 Your Profile",
                          font=('Arial', 28, 'bold'),
                          fg=self.colors['dark'],
                          bg=self.colors['light'])
        header.pack(pady=(20, 30))
        
        profile_card = tk.Frame(self.scrollable_frame, bg=self.colors['card'], bd=2, relief='groove')
        profile_card.pack(fill='x', padx=100, pady=(0, 30))

        if not IS_LOGGED_IN:
            # --- GUEST MODE: Show Login Prompt Container ---
            info_frame = tk.Frame(profile_card, bg=self.colors['card'])
            info_frame.pack(expand=True, padx=20, pady=30)
            
            tk.Label(info_frame,
                      text="🔒 Access Denied: Please Log In",
                      font=('Arial', 18, 'bold'),
                      fg=self.colors['danger'],
                      bg=self.colors['card']
                      ).pack(pady=(0, 15))
            
            # The button links to the login page via the handler
            tk.Button(info_frame,
                      text="👉 Go to Login / Sign Up Page",
                      font=('Arial', 14, 'bold'),
                      bg=self.colors['primary'],
                      fg='white',
                      padx=20,
                      pady=10,
                      relief='flat',
                      command=self.start_login_process
                      ).pack(pady=10)

        else:
            # --- LOGGED IN MODE: Show actual user profile ---
            
            # Profile picture placeholder
            pic_frame = tk.Frame(profile_card, bg=self.colors['light'], width=150, height=150)
            pic_frame.pack(side='left', pady=30, padx=30)
            pic_frame.pack_propagate(0)

            tk.Label(pic_frame,
                      text="👤",
                      font=('Arial', 48),
                      fg=self.colors['text_light'],
                      bg=self.colors['light'],
                      justify='center').pack(expand=True)
            
            # User info container
            info_frame = tk.Frame(profile_card, bg=self.colors['card'])
            info_frame.pack(side='left', padx=20, pady=20)

            # Use the loaded self.user_profile dictionary keys
            profile_info = [
                ("Username:", self.user_id),
            ]
            
            for label_text, value_text in profile_info:
                info_row = tk.Frame(info_frame, bg=self.colors['card'])
                info_row.pack(pady=5, anchor='w')
                
                tk.Label(info_row, text=label_text, font=('Arial', 12, 'bold'), 
                          fg=self.colors['text'], bg=self.colors['card'], width=15, anchor='w').pack(side='left')
                
                # Check for Goals and display in a multi-line format if needed
                if label_text == "Goals:":
                    display_text = value_text if len(str(value_text)) < 50 else f"{str(value_text)[:47]}..."
                else:
                    display_text = value_text

                tk.Label(info_row, text=display_text, font=('Arial', 12), 
                          fg=self.colors['text_light'], bg=self.colors['card'], anchor='w', wraplength=400).pack(side='left')

    # --- Calorie Calculator Screen ---
    def show_calorie_calculator(self):
        """Show calorie calculator screen"""
        ProgressTrackingApp()
        self.destroy_quick_stats()
        self.clear_content()
        
    # --- Progress Tracker Screen ---
    def show_progress_tracker(self):
        """Show progress tracker screen"""
        ProgressTrackingApp()
        self.root.destroy()
        self.clear_content()

# --- Main Execution Block (Controller Simulation) ---
def start_login_process(root_window):
    # --- PROCEED TO LOGIN ---
        # NOTE: Assuming 'login.py' and Login_function() exist for a full application context.
        try:
            from login import Login_function
            root_window.destroy()
            Login_function()
        except ImportError:
            messagebox.showinfo("Login", "Cannot switch to login.py: Module 'login' not found. Staying on Mainpage.")
            # For demonstration, we'll simulate the main window staying open if login.py is missing.

if __name__ == "__main__":
    root = tk.Tk()   
    app = Mainpage(root)
    
    # Inject the function that manages the switch back to login
    app.set_login_handler(lambda: start_login_process(root))
    
    root.mainloop()
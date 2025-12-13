import tkinter as tk
import webbrowser
from tkinter import ttk, messagebox

class PinkThemedFitnessQuestionn:
    def __init__(self, root):
        self.root = root
        self.root.title("Personalized Fitness ")
        
        # Start at a manageable size and allow resizing
        self.root.geometry("800x600") 
        self.root.resizable(True, True) 
        
        # Bind F11 key to toggle fullscreen mode
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.is_fullscreen = False # State tracker

        # Q/A Data Structure (Unchanged)
        self.qa_data = [
            {"q": "What is your primary fitness goal?", "options": ["Build Muscle 💪", "Lose Weight ⚖️", "Improve Health ❤️", "Increase Endurance 🏃"]},
            {"q": "How often do you exercise currently?", "options": ["Never (just starting)", "1-2 times per week", "3-4 times per week", "5+ times per week"]},
            {"q": "What type of workouts do you prefer?", "options": ["Strength Training 🏋️", "Cardio Exercises 🏃", "Yoga & Flexibility 🧘", "Mixed/Cross Training 🤸"]},
            {"q": "How would you describe your diet?", "options": ["Standard (no restrictions)", "Vegetarian 🌱", "High Protein 🥩", "Low Carb 🥗"]},
            {"q": "What is your typical exercise location?", "options": ["At Home 🏠", "Gym/Fitness Center 🏢", "Outdoors 🌳", "No Preference"]}
        ]
        
        self.current_question_index = 0
        self.answers = {}
        
        self.setup_style()
        self.setup_ui()
        
    def toggle_fullscreen(self, event=None):
        """Toggles the window between normal and fullscreen mode."""
        self.is_fullscreen = not self.is_fullscreen
        # Sets the fullscreen attribute based on the state tracker
        self.root.attributes('-fullscreen', self.is_fullscreen)
        
    def setup_style(self):
        """Configures the look and feel using ttk.Style for a pink modern appearance."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # --- PINK THEME COLOR DEFINITIONS ---
        PINK_MAIN = '#FE0161'      # Hot Pink for buttons
        PINK_DARK_ACTIVE = '#C71585' # Darker pink for active (hover/press) state
        BACKGROUND= '#ffffff' # light background
        
        # 1. TFrame (Main containers)
        style.configure('TFrame', background=BACKGROUND)
        
        # 2. Options LabelFrame Container 
        style.configure('Options.TLabelframe', 
                         background='white', 
                         foreground=PINK_MAIN, 
                         relief='groove')
        style.configure('Options.TLabelframe.Label', 
                         font=('Arial', 12, 'italic'),
                         foreground=PINK_DARK_ACTIVE)
        
        # 3. TProgressbar
        style.configure("TProgressbar",
            troughcolor='#ddd',
            background='#F08080', # Light Coral/Pink
            thickness=15
        )

        # 4. TButton 
        style.configure('TButton',
            font=('Arial', 10, 'bold'),
            background=PINK_MAIN,
            foreground='white',
            padding=10,
            relief='flat'
        )
        style.map('TButton', 
            background=[('active', PINK_DARK_ACTIVE)]
        )
        
        # 5. Skip Button (Neutral Style)
        style.configure('Skip.TButton',
            background='#B0C4DE', 
            foreground='white'
        )
        style.map('Skip.TButton',
            background=[('active', '#90A4C7')]
        )
        
        # 6. Question Label
        style.configure('Question.TLabel',
            font=('Helvetica', 16, 'bold'),
            foreground='#333333',
            background=BACKGROUND
        )
        # New Style for Program Title
        style.configure('Program.TLabel',
            font=('Helvetica', 20, 'bold'),
            foreground=PINK_MAIN,
            background=BACKGROUND
        )
        
        # 7. Radiobuttons 
        style.configure('TRadiobutton',
            font=('Arial', 12),
            background='white', 
            foreground='#555555',
            padding=5
        )


    def setup_ui(self):
        """Sets up the main structure and permanent widgets."""
        # This main_frame will hold all survey elements AND the final program display
        self.main_frame = ttk.Frame(self.root, padding="40", style='TFrame')
        self.main_frame.pack(expand=True, fill='both')

        # Grid configuration
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # --- Progress Bar and Label (Row 0, 1) ---
        self.progress_label = ttk.Label(self.main_frame, text="", font=('Arial', 10), background='#f5f5f5')
        self.progress_label.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky='ew')
        
        self.progress = ttk.Progressbar(self.main_frame, length=500, mode='determinate', style='TProgressbar')
        self.progress.grid(row=1, column=0, columnspan=2, pady=(0, 40), sticky='ew')
        
        # --- Question Label (Row 2) ---
        self.question_label = ttk.Label(
            self.main_frame, text="", style='Question.TLabel', wraplength=1000, justify=tk.CENTER
        )
        self.question_label.grid(row=2, column=0, columnspan=2, pady=(0, 30), sticky='ew')
        
        # --- Options Container (Row 3) ---
        self.options_container = ttk.LabelFrame(
            self.main_frame, text="Select One Option:", style='Options.TLabelframe', padding=(15, 10)
        )
        self.options_container.grid(row=3, column=0, columnspan=2, pady=(0, 50), sticky='ew')
        
        self.options_frame = ttk.Frame(self.options_container, style='TFrame')
        self.options_frame.pack(fill='x', padx=10, pady=5)
        self.options_frame.grid_columnconfigure(0, weight=1) 

        # --- Navigation Buttons (Row 4) ---
        self.button_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.button_frame.grid(row=4, column=0, columnspan=2, sticky='e') 
        
        # Skip Survey button: Placed on the far left (sticky='w') of row 4, column 0
        self.skip_btn = ttk.Button(
            self.main_frame, text="Skip Survey ❌", command=self.skip_survey, style='Skip.TButton'
        )
        # Corrected: .grid() call is essential for display
        self.skip_btn.grid(row=4, column=0, columnspan=1, sticky='w') 
        
        
        self.prev_btn = ttk.Button(
            self.button_frame, text="⬅️ Previous", command=self.previous_question, style='TButton', state='disabled'
        )
        self.prev_btn.pack(side=tk.LEFT, padx=10)
        
        self.next_btn = ttk.Button(
            self.button_frame, text="Next ➡️", command=self.next_question, style='TButton'
        )
        self.next_btn.pack(side=tk.LEFT, padx=10)
        
        self.load_question()

    # --- Core Logic Methods ---

    def load_question(self):
        """Updates the progress, question label, and dynamically loads options."""
        q_data = self.qa_data[self.current_question_index]

        self.update_progress()
        self.question_label.config(text=q_data['q'])

        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        self.selected_option = tk.StringVar()
        
        if self.current_question_index in self.answers:
            self.selected_option.set(self.answers[self.current_question_index])
        
        for i, option in enumerate(q_data['options']):
            rb = ttk.Radiobutton(
                self.options_frame, text=option, value=option, variable=self.selected_option, style='TRadiobutton'
            )
            rb.grid(row=i, column=0, sticky=tk.W, pady=8)

        is_last = self.current_question_index == len(self.qa_data) - 1
        
        prev_state = 'normal' if self.current_question_index > 0 else 'disabled'
        self.prev_btn.config(state=prev_state)

        next_text = "Finish 💪" if is_last else "Next ➡️"
        self.next_btn.config(text=next_text)
    
    def update_progress(self):
        """Calculates and updates the progress bar and label text."""
        total_questions = len(self.qa_data)
        current = self.current_question_index + 1
        progress_value = (current / total_questions) * 100
        
        self.progress['value'] = progress_value
        self.progress_label.config(
            text=f"Progress: Question {current} of {total_questions}"
        )

    def next_question(self):
        """Saves answer and moves forward or finishes."""
        answer = self.selected_option.get()
        
        if not answer and self.current_question_index < len(self.qa_data) - 1:
             messagebox.showwarning("Incomplete", "Please select an option before moving to the next question.")
             return 

        self.answers[self.current_question_index] = answer if answer else "Skipped"
        
        if self.current_question_index < len(self.qa_data) - 1:
            self.current_question_index += 1
            self.load_question()
        else:
            self.finish_questionnaire()
    
    def previous_question(self):
        """Moves back and loads the previous state."""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.load_question()
        
    def skip_survey(self):
        """Allows the user to immediately exit the survey."""
        if messagebox.askyesno("Confirm Skip", "Are you sure you want to skip the rest of the survey? All unanswered questions will be marked as 'Skipped'."):
            answer = self.selected_option.get()
            if answer:
                self.answers[self.current_question_index] = answer
            
            self.finish_questionnaire()


    # --- New Program Display Logic ---

    def hide_survey_widgets(self):
        """Hides all survey-related widgets to make way for the program plan."""
        self.progress_label.grid_forget()
        self.progress.grid_forget()
        self.question_label.grid_forget()
        self.options_container.grid_forget()
        self.button_frame.grid_forget()
        self.skip_btn.grid_forget()
        
        # Reset grid weights for the new display
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0) # Only one column needed now

    def generate_program_text(self):
        """
        Generates a simplified fitness plan based on the collected answers.
        In a real app, this would involve complex logic and database lookups.
        """
        # Determine goal (Q1)
        goal = self.answers.get(0, "Improve Health ❤️") 
        # Determine frequency (Q2)
        frequency = self.answers.get(1, "1-2 times per week")
        # Determine preference (Q3)
        preference = self.answers.get(2, "Mixed/Cross Training 🤸")
        
        # Simple Logic to create a response
        if "Build Muscle" in goal:
            title = f"Muscle Building Plan 💪"
            plan = f"Your primary goal is to {goal.lower()}. Focus 3-4 sessions per week on compound lifts (squats, deadlifts, bench press) at a gym or home setup. Keep rest periods long (90-120s). Supplement with a high-protein diet."
        elif "Lose Weight" in goal:
            title = f"Weight Loss & Cardio Plan 🏃"
            plan = f"Your primary goal is to {goal.lower()}. Combine {frequency} of focused cardio ({preference}) with light resistance training. Since you prefer {self.answers.get(4, 'Outdoors 🌳')}, integrate running or hiking. Maintain a caloric deficit and track your steps daily."
        else:
             title = f"Balanced Wellness Program ❤️"
             plan = f"Focus on consistency with {frequency} sessions. We recommend a mix of {preference} for overall health, mobility, and cardiovascular fitness. Prioritize sleep and hydration."

        return title, plan

    def display_program(self):
        """Displays the personalized fitness program in the main window."""
        self.hide_survey_widgets()
        
        program_title, program_plan = self.generate_program_text()

        # --- Display Widgets ---
        
        # Title
        ttk.Label(
            self.main_frame, 
            text="✅ Assessment Complete!", 
            style='Program.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=(20, 5), sticky='n')
        
        # Personalized Title
        ttk.Label(
            self.main_frame, 
            text=program_title, 
            style='Question.TLabel',
            foreground='#333333' 
        ).grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky='n')

        # Program Details (using Text widget for multiline plan)
        program_text = tk.Text(
            self.main_frame, 
            height=15, 
            width=60, 
            font=('Arial', 12),
            wrap=tk.WORD,
            padx=15, pady=15,
            relief=tk.FLAT
        )
        program_text.insert(tk.END, program_plan + "\n\n--- Your Custom Settings ---\n\n")
        
        # Display all answers below the main plan
        for i, data in enumerate(self.qa_data):
            question = data['q']
            answer = self.answers.get(i, 'Skipped')
            program_text.insert(tk.END, f"{question}:\n  {answer}\n\n")

        program_text.config(state=tk.DISABLED) # Make it read-only
        program_text.grid(row=2, column=0, columnspan=2, padx=40, pady=(10, 30), sticky='nsew')
        
        # Exit Button
        ttk.Button(
            self.main_frame, 
            text="Close Application", 
            command=self.root.destroy, 
            style='TButton'
        ).grid(row=3, column=0, columnspan=2, pady=20)


    def finish_questionnaire(self):
        """Compiles final answers and transitions to the program display."""
        # --- 1. Mark Unanswered Questions as 'Skipped' ---
        total_questions = len(self.qa_data)
        for i in range(total_questions):
            if i not in self.answers:
                self.answers[i] = 'Skipped'
        
        # --- 2. Transition to Program Display ---
        self.display_program()
        
        
def main():
    root = tk.Tk()
    app = PinkThemedFitnessQuestionn(root)
    root.mainloop()

if __name__ == "__main__":
    main()
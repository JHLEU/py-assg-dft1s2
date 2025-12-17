import tkinter as tk
from tkinter import ttk, messagebox

class PinkThemedFitnessQuestionn:
    def __init__(self, root):
        self.root = root
        self.root.title("FitQuest | Personalized Assessment")
        
        self.root.state("zoomed")
        self.root.resizable(True, True) 
        
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.is_fullscreen = False

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
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        PINK_MAIN = '#FE0161'
        PINK_DARK_ACTIVE = '#C71585'
        BACKGROUND = '#ffffff'
        
        style.configure('TFrame', background=BACKGROUND)
        style.configure('Options.TLabelframe', background='white', foreground=PINK_MAIN, relief='groove')
        style.configure('Options.TLabelframe.Label', font=('Arial', 12, 'italic'), foreground=PINK_DARK_ACTIVE)
        
        style.configure("TProgressbar", troughcolor='#ddd', background='#F08080', thickness=15)

        style.configure('TButton', font=('Arial', 10, 'bold'), background=PINK_MAIN, foreground='white', padding=10)
        style.map('TButton', background=[('active', PINK_DARK_ACTIVE)])
        
        style.configure('Skip.TButton', background='#B0C4DE', foreground='white')
        style.map('Skip.TButton', background=[('active', '#90A4C7')])
        
        style.configure('Question.TLabel', font=('Helvetica', 16, 'bold'), foreground='#333333', background=BACKGROUND)
        style.configure('Program.TLabel', font=('Helvetica', 20, 'bold'), foreground=PINK_MAIN, background=BACKGROUND)
        style.configure('TRadiobutton', font=('Arial', 12), background='white', foreground='#555555', padding=5)

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding="40", style='TFrame')
        self.main_frame.pack(expand=True, fill='both')

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.progress_label = ttk.Label(self.main_frame, text="", font=('Arial', 10), background='#ffffff')
        self.progress_label.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky='ew')
        
        self.progress = ttk.Progressbar(self.main_frame, length=500, mode='determinate', style='TProgressbar')
        self.progress.grid(row=1, column=0, columnspan=2, pady=(0, 40), sticky='ew')
        
        self.question_label = ttk.Label(self.main_frame, text="", style='Question.TLabel', wraplength=1000, justify=tk.CENTER)
        self.question_label.grid(row=2, column=0, columnspan=2, pady=(0, 30), sticky='ew')
        
        self.options_container = ttk.LabelFrame(self.main_frame, text="Select One Option:", style='Options.TLabelframe', padding=(15, 10))
        self.options_container.grid(row=3, column=0, columnspan=2, pady=(0, 50), sticky='ew')
        
        self.options_frame = ttk.Frame(self.options_container, style='TFrame')
        self.options_frame.pack(fill='x', padx=10, pady=5)

        self.button_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.button_frame.grid(row=4, column=0, columnspan=2, sticky='e') 
        
        self.skip_btn = ttk.Button(self.main_frame, text="Skip Survey ❌", command=self.skip_survey, style='Skip.TButton')
        self.skip_btn.grid(row=4, column=0, sticky='w') 
        
        self.prev_btn = ttk.Button(self.button_frame, text="⬅️ Previous", command=self.previous_question, style='TButton', state='disabled')
        self.prev_btn.pack(side=tk.LEFT, padx=10)
        
        self.next_btn = ttk.Button(self.button_frame, text="Next ➡️", command=self.next_question, style='TButton')
        self.next_btn.pack(side=tk.LEFT, padx=10)
        
        self.load_question()

    def load_question(self):
        q_data = self.qa_data[self.current_question_index]
        self.update_progress()
        self.question_label.config(text=q_data['q'])

        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        self.selected_option = tk.StringVar()
        if self.current_question_index in self.answers:
            self.selected_option.set(self.answers[self.current_question_index])
        
        for i, option in enumerate(q_data['options']):
            rb = ttk.Radiobutton(self.options_frame, text=option, value=option, variable=self.selected_option, style='TRadiobutton')
            rb.grid(row=i, column=0, sticky=tk.W, pady=8)

        self.prev_btn.config(state='normal' if self.current_question_index > 0 else 'disabled')
        self.next_btn.config(text="Finish 💪" if self.current_question_index == len(self.qa_data) - 1 else "Next ➡️")
    
    def update_progress(self):
        current = self.current_question_index + 1
        val = (current / len(self.qa_data)) * 100
        self.progress['value'] = val
        self.progress_label.config(text=f"Progress: Question {current} of {len(self.qa_data)}")

    def next_question(self):
        answer = self.selected_option.get()
        if not answer:
            messagebox.showwarning("Incomplete", "Please select an option.")
            return 

        self.answers[self.current_question_index] = answer
        if self.current_question_index < len(self.qa_data) - 1:
            self.current_question_index += 1
            self.load_question()
        else:
            self.finish_questionnaire()
    
    def previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.load_question()
        
    def skip_survey(self):
        if messagebox.askyesno("Confirm Skip", "Skip to results? Unanswered questions will be marked 'Skipped'."):
            self.finish_questionnaire()

    def display_program(self):
        # Clear the frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        goal = self.answers.get(0, "Health")
        freq = self.answers.get(1, "Starting")
        
        # Simple Logic
        title = f"Your Custom {goal} Plan"
        plan = f"Based on your preference for exercising {freq}, we have designed a specific routine. Focus on consistency and hydration!"

        ttk.Label(self.main_frame, text="✅ Assessment Complete!", style='Program.TLabel').pack(pady=(20, 10))
        ttk.Label(self.main_frame, text=title, style='Question.TLabel').pack(pady=10)

        program_text = tk.Text(self.main_frame, height=12, width=70, font=('Arial', 11), wrap=tk.WORD, padx=20, pady=20)
        program_text.insert(tk.END, plan + "\n\n--- Summary ---\n\n")
        for i, data in enumerate(self.qa_data):
            program_text.insert(tk.END, f"Q: {data['q']}\nA: {self.answers.get(i, 'Skipped')}\n\n")
        
        program_text.config(state=tk.DISABLED)
        program_text.pack(pady=20, padx=40)

        ttk.Button(self.main_frame, text="Return to Home 🏠", command=self.go_to_mainpage, style='TButton').pack(pady=20)

    def go_to_mainpage(self):
        """Clears current UI and reloads the Mainpage class onto the existing root."""
        self.main_frame.destroy() # Remove the survey UI
        try:
            from mainpage import Mainpage
            Mainpage(self.root) # Initialize Mainpage on the same root window
        except ImportError:
            messagebox.showerror("Error", "mainpage.py not found!")

    def finish_questionnaire(self):
        for i in range(len(self.qa_data)):
            if i not in self.answers:
                self.answers[i] = 'Skipped'
        self.display_program()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = PinkThemedFitnessQuestionn(root)
    root.mainloop()
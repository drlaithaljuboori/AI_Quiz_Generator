import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import json
import random
from datetime import datetime

class AIQuizGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Based Quiz Generator - Pumps and Compressors")
        self.root.geometry("1200x800")
        
        # Database setup
        self.setup_database()
        
        # Create main interface
        self.create_main_interface()
        
        # Load initial data
        self.load_quiz_topics()
    
    def setup_database(self):
        """Initialize SQLite database with course structure"""
        self.conn = sqlite3.connect('pumps_compressors.db')
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY,
                week INTEGER,
                day INTEGER,
                title TEXT,
                description TEXT,
                pcs TEXT,
                content TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY,
                topic_id INTEGER,
                question TEXT,
                options TEXT,
                correct_answer TEXT,
                question_type TEXT,
                FOREIGN KEY (topic_id) REFERENCES topics (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY,
                topic_id INTEGER,
                quiz_score REAL,
                completed BOOLEAN,
                timestamp DATETIME,
                FOREIGN KEY (topic_id) REFERENCES topics (id)
            )
        ''')
        
        # Insert sample data if empty
        self.insert_sample_data()
        self.conn.commit()
    
    def insert_sample_data(self):
        """Insert course topics and quizzes based on the provided materials"""
        
        # Check if data already exists
        self.cursor.execute("SELECT COUNT(*) FROM topics")
        if self.cursor.fetchone()[0] > 0:
            return
        
        # Topics data based on the course structure
        topics_data = [
            (1, 1, "Pump Types and Fundamentals", 
             "Centrifugal and Positive Displacement Pumps",
             "PC1.1, PC2.3, PC2.4",
             "Basic principles, construction, and applications of different pump types."),
            
            (2, 2, "Compressor Types and Components", 
             "Centrifugal and Positive Displacement Compressors",
             "PC1.1, PC2.1, PC2.2",
             "Compressor types, components, and operating principles."),
            
            (3, 3, "Measurement Devices", 
             "Pressure, Flow, and Temperature Measurement",
             "PC4.1, PC1.2",
             "Measurement devices including pressure gauges, transducers, and Venturi tubes."),
            
            (4, 4, "Safety Procedures", 
             "Startup, Shutdown and Safety Protocols",
             "PC1.3, PC3.1",
             "Safe operation procedures and common fault diagnosis."),
            
            (5, 5, "Cavitation and Pump Safety", 
             "Pressure Management and Cavitation Effects",
             "PC3.2, PC3.3",
             "Cavitation causes, effects, and prevention methods."),
            
            (6, 7, "Performance Calculations", 
             "Power, Efficiency and Performance Analysis",
             "PC4.2, PC4.3, PC4.4, PC4.5, PC4.6",
             "Power calculations, efficiency curves, and performance analysis."),
        ]
        
        # Insert topics
        for topic in topics_data:
            self.cursor.execute(
                "INSERT INTO topics (week, day, title, description, pcs, content) VALUES (?, ?, ?, ?, ?, ?)",
                topic
            )
        
        # Insert extensive quiz questions
        quiz_data = [
            # Pump Fundamentals (Topic 1)
            (1, "Which pump type uses an impeller to move fluid?", 
             '["Centrifugal Pump", "Piston Pump", "Gear Pump", "Diaphragm Pump"]', 
             "Centrifugal Pump", "multiple_choice"),
            
            (1, "What is the main function of a pump?", 
             '["Increase fluid pressure", "Generate electricity", "Cool the fluid", "Filter contaminants"]', 
             "Increase fluid pressure", "multiple_choice"),
            
            (1, "Which component in a centrifugal pump converts velocity energy to pressure energy?", 
             '["Impeller", "Volute Casing", "Shaft", "Seal"]', 
             "Volute Casing", "multiple_choice"),
            
            (1, "What type of pump is best for high viscosity fluids?", 
             '["Centrifugal Pump", "Positive Displacement Pump", "Jet Pump", "Turbine Pump"]', 
             "Positive Displacement Pump", "multiple_choice"),
            
            (1, "The efficiency of a centrifugal pump is highest at:", 
             '["Best Efficiency Point (BEP)", "Shut-off head", "Run-out point", "All operating points"]', 
             "Best Efficiency Point (BEP)", "multiple_choice"),
            
            # Compressors (Topic 2)
            (2, "Which compressor type is best for high-pressure applications?", 
             '["Centrifugal Compressor", "Rotary Screw Compressor", "Reciprocating Compressor", "Axial Compressor"]', 
             "Reciprocating Compressor", "multiple_choice"),
            
            (2, "What is the purpose of an intercooler in a multi-stage compressor?", 
             '["Reduce power consumption", "Increase final pressure", "Cool the gas between stages", "Lubricate moving parts"]', 
             "Cool the gas between stages", "multiple_choice"),
            
            (2, "Which compressor type provides continuous, pulsation-free flow?", 
             '["Reciprocating Compressor", "Centrifugal Compressor", "Diaphragm Compressor", "Rotary Vane Compressor"]', 
             "Centrifugal Compressor", "multiple_choice"),
            
            (2, "The clearance volume in a reciprocating compressor affects:", 
             '["Volumetric efficiency", "Motor speed", "Lubrication requirements", "Noise level"]', 
             "Volumetric efficiency", "multiple_choice"),
            
            (2, "What safety device is essential on all air compressor receivers?", 
             '["Pressure relief valve", "Temperature gauge", "Flow meter", "Moisture separator"]', 
             "Pressure relief valve", "multiple_choice"),
            
            # Measurement Devices (Topic 3)
            (3, "What does a Venturi tube measure?", 
             '["Pressure", "Temperature", "Flow rate", "Viscosity"]', 
             "Flow rate", "multiple_choice"),
            
            (3, "Which device converts pressure into an electrical signal?", 
             '["Pressure Gauge", "Pressure Transducer", "Manometer", "Bourdon Tube"]', 
             "Pressure Transducer", "multiple_choice"),
            
            (3, "What principle does a Venturi tube operate on?", 
             '["Bernoulli\'s principle", "Pascal\'s principle", "Archimedes\' principle", "Newton\'s law"]', 
             "Bernoulli\'s principle", "multiple_choice"),
            
            (3, "Which temperature sensor uses resistance change with temperature?", 
             '["Thermocouple", "RTD", "Bimetallic strip", "Infrared sensor"]', 
             "RTD", "multiple_choice"),
            
            (3, "A Bourdon tube is typically used in:", 
             '["Flow meters", "Pressure gauges", "Temperature sensors", "Level indicators"]', 
             "Pressure gauges", "multiple_choice"),
            
            # Safety Procedures (Topic 4)
            (4, "What should you check before starting a pump?", 
             '["Lubrication levels", "Weather conditions", "Operator certification", "Manufacturer name"]', 
             "Lubrication levels", "multiple_choice"),
            
            (4, "The correct sequence for pump startup is:", 
             '["Open discharge, start pump, open suction", "Start pump, open suction, open discharge", "Open suction, start pump, open discharge", "Open suction, open discharge, start pump"]', 
             "Open suction, start pump, open discharge", "multiple_choice"),
            
            (4, "What is the purpose of a safety valve?", 
             '["Control flow rate", "Measure pressure", "Prevent overpressure", "Indicate temperature"]', 
             "Prevent overpressure", "multiple_choice"),
            
            (4, "Lockout-Tagout procedures are used for:", 
             '["Increasing efficiency", "Energy isolation during maintenance", "Speed control", "Performance testing"]', 
             "Energy isolation during maintenance", "multiple_choice"),
            
            (4, "Before working on a pump, you should:", 
             '["Drain the fluid", "Increase pressure", "Run at maximum speed", "Check weather forecast"]', 
             "Drain the fluid", "multiple_choice"),
            
            # Cavitation (Topic 5)
            (5, "What causes cavitation in pumps?", 
             '["High suction pressure", "Low suction pressure", "High discharge pressure", "Low fluid viscosity"]', 
             "Low suction pressure", "multiple_choice"),
            
            (5, "The formation and collapse of vapor bubbles in a pump is called:", 
             '["Aeration", "Cavitation", "Turbulence", "Laminar flow"]', 
             "Cavitation", "multiple_choice"),
            
            (5, "What does NPSH stand for?", 
             '["Net Positive Suction Head", "Negative Pressure System Head", "Normal Pump Suction Height", "National Pump Safety Handbook"]', 
             "Net Positive Suction Head", "multiple_choice"),
            
            (5, "Which symptom indicates cavitation?", 
             '["Smooth operation", "Reduced noise", "Knocking sounds", "Increased flow"]', 
             "Knocking sounds", "multiple_choice"),
            
            (5, "To prevent cavitation, you should:", 
             '["Increase suction lift", "Reduce NPSH available", "Increase fluid temperature", "Reduce suction line restrictions"]', 
             "Reduce suction line restrictions", "multiple_choice"),
            
            # Performance Calculations (Topic 6)
            (6, "What is the formula for pump efficiency?", 
             '["(Output Power / Input Power) × 100%", "(Input Power / Output Power) × 100%", "Output Power - Input Power", "Input Power × Output Power"]', 
             "(Output Power / Input Power) × 100%", "multiple_choice"),
            
            (6, "Hydraulic power is calculated using:", 
             '["Flow rate and pressure", "Speed and torque", "Voltage and current", "Temperature and density"]', 
             "Flow rate and pressure", "multiple_choice"),
            
            (6, "The pressure ratio in compressors is defined as:", 
             '["P1/P2", "P2/P1", "(P1+P2)/2", "P2-P1"]', 
             "P2/P1", "multiple_choice"),
            
            (6, "What does a pump characteristic curve show?", 
             '["Pump performance at different flow rates", "Pump material composition", "Pump manufacturing date", "Pump cost analysis"]', 
             "Pump performance at different flow rates", "multiple_choice"),
            
            (6, "Volumetric efficiency in compressors compares:", 
             '["Actual flow to theoretical flow", "Input power to output power", "Pressure ratio to temperature ratio", "Speed to torque"]', 
             "Actual flow to theoretical flow", "multiple_choice"),
        ]
        
        for quiz in quiz_data:
            self.cursor.execute(
                "INSERT INTO quizzes (topic_id, question, options, correct_answer, question_type) VALUES (?, ?, ?, ?, ?)",
                quiz
            )
    
    def create_main_interface(self):
        """Create the main user interface"""
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create frames for different sections
        self.quiz_frame = ttk.Frame(self.notebook)
        self.ai_assistant_frame = ttk.Frame(self.notebook)
        self.progress_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.quiz_frame, text="MCQ Quizzes")
        self.notebook.add(self.ai_assistant_frame, text="AI Learning Assistant")
        self.notebook.add(self.progress_frame, text="Progress Tracking")
        
        # Setup each frame
        self.setup_quiz_frame()
        self.setup_ai_assistant_frame()
        self.setup_progress_frame()
    
    def setup_quiz_frame(self):
        """Setup the quiz interface"""
        
        main_frame = ttk.Frame(self.quiz_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=10)
        
        ttk.Label(header_frame, text="AI Based Quiz Generator", font=('Arial', 16, 'bold')).pack()
        ttk.Label(header_frame, text="Pumps and Compressors - Multiple Choice Questions", font=('Arial', 12)).pack()
        
        # Topic selection for quiz
        selection_frame = ttk.Frame(main_frame)
        selection_frame.pack(fill='x', pady=10)
        
        ttk.Label(selection_frame, text="Select Topic:", font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        
        self.quiz_topic_var = tk.StringVar()
        self.quiz_topic_combo = ttk.Combobox(selection_frame, textvariable=self.quiz_topic_var, 
                                            state='readonly', width=50, font=('Arial', 10))
        self.quiz_topic_combo.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        self.quiz_topic_combo.bind('<<ComboboxSelected>>', self.load_quiz_questions)
        
        # Quiz info
        self.quiz_info = ttk.Label(selection_frame, text="", font=('Arial', 10))
        self.quiz_info.grid(row=1, column=0, columnspan=2, sticky='w', pady=2)
        
        selection_frame.columnconfigure(1, weight=1)
        
        # Quiz area
        quiz_area_frame = ttk.LabelFrame(main_frame, text="Quiz Questions", padding=10)
        quiz_area_frame.pack(fill='both', expand=True, pady=10)
        
        # Question counter
        self.question_counter = ttk.Label(quiz_area_frame, text="", font=('Arial', 10, 'bold'))
        self.question_counter.pack(anchor='w', pady=5)
        
        # Question display
        question_display_frame = ttk.Frame(quiz_area_frame)
        question_display_frame.pack(fill='x', pady=10)
        
        self.quiz_question = tk.Label(question_display_frame, text="Select a topic to start quiz", 
                                     font=('Arial', 11, 'bold'), wraplength=800, justify='left', bg='white')
        self.quiz_question.pack(fill='x', pady=10, padx=10)
        
        # Options frame
        self.quiz_options_frame = tk.Frame(quiz_area_frame, bg='white')
        self.quiz_options_frame.pack(fill='x', pady=10, padx=10)
        
        self.quiz_answer_var = tk.StringVar()
        
        # Navigation buttons
        nav_frame = ttk.Frame(quiz_area_frame)
        nav_frame.pack(fill='x', pady=20)
        
        ttk.Button(nav_frame, text="← Previous", command=self.previous_question).pack(side='left', padx=5)
        ttk.Button(nav_frame, text="Next →", command=self.next_question).pack(side='left', padx=5)
        ttk.Button(nav_frame, text="Submit Quiz", command=self.submit_quiz).pack(side='right', padx=5)
        
        # Results area
        results_frame = ttk.Frame(quiz_area_frame)
        results_frame.pack(fill='x', pady=10)
        
        self.quiz_results = ttk.Label(results_frame, text="", font=('Arial', 12, 'bold'))
        self.quiz_results.pack()
        
        # Load topic names for quiz selection
        self.load_quiz_topics()
        
        self.current_quiz_questions = []
        self.current_question_index = 0
        self.user_quiz_answers = {}
    
    def setup_ai_assistant_frame(self):
        """Setup the AI assistant interface"""
        
        main_frame = ttk.Frame(self.ai_assistant_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=10)
        
        ttk.Label(header_frame, text="AI Learning Assistant", font=('Arial', 16, 'bold')).pack()
        ttk.Label(header_frame, text="Get detailed explanations and ask questions about pumps and compressors", 
                 font=('Arial', 11)).pack()
        
        # Topic selection and sample questions
        topic_frame = ttk.LabelFrame(main_frame, text="Select Topic for Sample Questions", padding=10)
        topic_frame.pack(fill='x', pady=10)
        
        ttk.Label(topic_frame, text="Topic:").grid(row=0, column=0, sticky='w', pady=5)
        
        self.ai_topic_var = tk.StringVar()
        self.ai_topic_combo = ttk.Combobox(topic_frame, textvariable=self.ai_topic_var, 
                                          state='readonly', width=40)
        self.ai_topic_combo.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        self.ai_topic_combo.bind('<<ComboboxSelected>>', self.load_sample_questions)
        
        # Sample questions area
        self.sample_questions_frame = ttk.LabelFrame(main_frame, text="Sample Questions for Selected Topic", padding=10)
        self.sample_questions_frame.pack(fill='x', pady=10)
        
        self.sample_questions_text = scrolledtext.ScrolledText(self.sample_questions_frame, height=6, wrap='word')
        self.sample_questions_text.pack(fill='both', expand=True)
        self.sample_questions_text.config(state='disabled')
        
        # Chat area
        chat_frame = ttk.LabelFrame(main_frame, text="Ask Your Question", padding=10)
        chat_frame.pack(fill='both', expand=True, pady=10)
        
        self.ai_chat_display = scrolledtext.ScrolledText(chat_frame, height=12, wrap='word')
        self.ai_chat_display.pack(fill='both', expand=True, pady=5)
        self.ai_chat_display.config(state='disabled')
        
        # Input area
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill='x', pady=5)
        
        self.ai_user_input = tk.Text(input_frame, height=3, wrap='word')
        self.ai_user_input.pack(side='left', fill='both', expand=True, padx=5)
        
        ttk.Button(input_frame, text="Send Question", command=self.send_to_ai).pack(side='right', padx=5)
        
        topic_frame.columnconfigure(1, weight=1)
        
        # Load topics for AI assistant
        self.load_ai_topics()
    
    def setup_progress_frame(self):
        """Setup progress tracking interface"""
        
        main_frame = ttk.Frame(self.progress_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(main_frame, text="Learning Progress Tracking", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Progress treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, pady=10)
        
        columns = ('Topic', 'Week', 'Day', 'Status', 'Score', 'Last Attempt')
        self.progress_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        column_widths = {'Topic': 250, 'Week': 60, 'Day': 60, 'Status': 100, 'Score': 80, 'Last Attempt': 120}
        for col in columns:
            self.progress_tree.heading(col, text=col)
            self.progress_tree.column(col, width=column_widths.get(col, 100))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.progress_tree.yview)
        self.progress_tree.configure(yscrollcommand=scrollbar.set)
        
        self.progress_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Progress summary
        summary_frame = ttk.Frame(main_frame)
        summary_frame.pack(fill='x', pady=10)
        
        self.progress_summary = ttk.Label(summary_frame, text="", font=('Arial', 12, 'bold'))
        self.progress_summary.pack(side='left')
        
        ttk.Button(summary_frame, text="Refresh Progress", command=self.load_progress).pack(side='right', padx=5)
        
        self.load_progress()
    
    def load_quiz_topics(self):
        """Load topics for quiz selection"""
        self.cursor.execute("SELECT id, title, description FROM topics")
        topics = self.cursor.fetchall()
        
        self.quiz_topic_data = {}
        topic_names = []
        for topic_id, title, description in topics:
            self.quiz_topic_data[title] = (topic_id, description)
            topic_names.append(title)
        
        self.quiz_topic_combo['values'] = topic_names
        
        if topic_names:
            self.quiz_topic_combo.set(topic_names[0])
            self.load_quiz_questions()
    
    def load_ai_topics(self):
        """Load topics for AI assistant"""
        self.cursor.execute("SELECT id, title FROM topics")
        topics = self.cursor.fetchall()
        
        self.ai_topic_data = {}
        topic_names = []
        for topic_id, title in topics:
            self.ai_topic_data[title] = topic_id
            topic_names.append(title)
        
        self.ai_topic_combo['values'] = topic_names
        
        if topic_names:
            self.ai_topic_combo.set(topic_names[0])
            self.load_sample_questions()
    
    def load_sample_questions(self, event=None):
        """Load sample questions for the selected topic in AI assistant"""
        topic_name = self.ai_topic_var.get()
        if not topic_name or topic_name not in self.ai_topic_data:
            return
        
        topic_id = self.ai_topic_data[topic_name]
        
        # Get questions for this topic
        self.cursor.execute(
            "SELECT question FROM quizzes WHERE topic_id=? LIMIT 8", 
            (topic_id,)
        )
        questions = self.cursor.fetchall()
        
        self.sample_questions_text.config(state='normal')
        self.sample_questions_text.delete(1.0, tk.END)
        
        if questions:
            self.sample_questions_text.insert(tk.END, f"Sample questions about {topic_name}:\n\n")
            for i, (question,) in enumerate(questions, 1):
                self.sample_questions_text.insert(tk.END, f"{i}. {question}\n")
            self.sample_questions_text.insert(tk.END, "\nYou can ask any of these questions or your own!")
        else:
            self.sample_questions_text.insert(tk.END, f"No sample questions available for {topic_name}.")
        
        self.sample_questions_text.config(state='disabled')
    
    def load_quiz_questions(self, event=None):
        """Load quiz questions for selected topic"""
        topic_name = self.quiz_topic_var.get()
        if not topic_name or topic_name not in self.quiz_topic_data:
            return
        
        topic_id, description = self.quiz_topic_data[topic_name]
        
        # Update quiz info
        self.quiz_info.config(text=f"Topic: {description}")
        
        self.cursor.execute(
            "SELECT id, question, options, correct_answer, question_type FROM quizzes WHERE topic_id=?", 
            (topic_id,)
        )
        self.current_quiz_questions = self.cursor.fetchall()
        self.current_question_index = 0
        self.user_quiz_answers = {}
        
        if self.current_quiz_questions:
            self.display_question()
            self.quiz_results.config(text="")
        else:
            self.quiz_question.config(text="No questions available for this topic")
            self.clear_options()
            self.question_counter.config(text="")
    
    def display_question(self):
        """Display current question"""
        if not self.current_quiz_questions:
            return
        
        question_data = self.current_quiz_questions[self.current_question_index]
        question_id, question, options_json, correct_answer, question_type = question_data
        
        # Update question counter
        total_questions = len(self.current_quiz_questions)
        self.question_counter.config(
            text=f"Question {self.current_question_index + 1} of {total_questions}"
        )
        
        self.quiz_question.config(text=question)
        self.clear_options()
        
        # Parse options
        options = json.loads(options_json)
        
        # Create radio buttons for options using tk.Radiobutton (not ttk)
        for i, option in enumerate(options):
            rb = tk.Radiobutton(
                self.quiz_options_frame, 
                text=option, 
                variable=self.quiz_answer_var, 
                value=option,
                wraplength=700,
                justify='left',
                bg='white',
                font=('Arial', 10),
                anchor='w'
            )
            rb.pack(anchor='w', pady=2, padx=20)
        
        # Load previous answer if exists
        if self.current_question_index in self.user_quiz_answers:
            self.quiz_answer_var.set(self.user_quiz_answers[self.current_question_index])
        else:
            self.quiz_answer_var.set("")
    
    def clear_options(self):
        """Clear option widgets"""
        for widget in self.quiz_options_frame.winfo_children():
            widget.destroy()
    
    def previous_question(self):
        """Navigate to previous question"""
        if self.current_question_index > 0:
            self.save_current_answer()
            self.current_question_index -= 1
            self.display_question()
    
    def next_question(self):
        """Navigate to next question"""
        if self.current_question_index < len(self.current_quiz_questions) - 1:
            self.save_current_answer()
            self.current_question_index += 1
            self.display_question()
    
    def save_current_answer(self):
        """Save current answer"""
        if self.quiz_answer_var.get():
            self.user_quiz_answers[self.current_question_index] = self.quiz_answer_var.get()
    
    def submit_quiz(self):
        """Submit and grade the quiz"""
        self.save_current_answer()
        
        if not self.user_quiz_answers:
            messagebox.showwarning("Warning", "Please answer at least one question!")
            return
        
        # Calculate score
        correct_count = 0
        total_questions = len(self.current_quiz_questions)
        
        for i, question_data in enumerate(self.current_quiz_questions):
            question_id, question, options_json, correct_answer, question_type = question_data
            
            if i in self.user_quiz_answers and self.user_quiz_answers[i] == correct_answer:
                correct_count += 1
        
        score = (correct_count / total_questions) * 100
        
        # Determine grade
        if score >= 90:
            grade = "A - Excellent!"
            color = "green"
        elif score >= 80:
            grade = "B - Very Good!"
            color = "green"
        elif score >= 70:
            grade = "C - Good!"
            color = "orange"
        elif score >= 60:
            grade = "D - Pass"
            color = "orange"
        else:
            grade = "F - Needs Improvement"
            color = "red"
        
        # Save progress
        topic_name = self.quiz_topic_var.get()
        if topic_name in self.quiz_topic_data:
            topic_id, description = self.quiz_topic_data[topic_name]
            
            self.cursor.execute(
                "SELECT id FROM user_progress WHERE topic_id=?", 
                (topic_id,)
            )
            existing = self.cursor.fetchone()
            
            if existing:
                self.cursor.execute(
                    "UPDATE user_progress SET quiz_score=?, completed=1, timestamp=? WHERE topic_id=?",
                    (score, datetime.now(), topic_id)
                )
            else:
                self.cursor.execute(
                    "INSERT INTO user_progress (topic_id, quiz_score, completed, timestamp) VALUES (?, ?, ?, ?)",
                    (topic_id, score, 1, datetime.now())
                )
            
            self.conn.commit()
        
        # Display results
        result_text = f"Quiz Completed!\nScore: {score:.1f}% ({correct_count}/{total_questions} correct)\nGrade: {grade}"
        self.quiz_results.config(text=result_text, foreground=color)
        
        messagebox.showinfo("Quiz Results", f"Topic: {topic_name}\n\n{result_text}")
        self.load_progress()
    
    def send_to_ai(self):
        """Send user message to AI assistant"""
        user_message = self.ai_user_input.get(1.0, tk.END).strip()
        if not user_message:
            messagebox.showwarning("Warning", "Please enter a question!")
            return
        
        topic_name = self.ai_topic_var.get()
        
        # Clear input
        self.ai_user_input.delete(1.0, tk.END)
        
        # Display user message
        self.display_ai_message(f"You asked about {topic_name}: {user_message}", "user")
        
        # Get AI response
        ai_response = self.get_ai_response(user_message, topic_name)
        self.display_ai_message(f"AI Assistant: {ai_response}", "ai")
    
    def get_ai_response(self, user_message, topic_name):
        """Get AI response using built-in knowledge base"""
        knowledge_base = {
            "Pump Types and Fundamentals": {
                "keywords": ["pump", "centrifugal", "positive displacement", "impeller", "casing", "volute", "BEP"],
                "response": """Centrifugal pumps use rotational energy from an impeller to move fluid by converting rotational kinetic energy to hydrodynamic energy. 

Key Components:
- Impeller: Rotating component that imparts energy to fluid
- Volute Casing: Converts velocity energy to pressure energy
- Shaft: Transmits power from motor to impeller
- Seals: Prevent leakage

Positive displacement pumps move fluid by trapping a fixed amount and forcing it through the system. Types include piston pumps, gear pumps, and diaphragm pumps.

Best Efficiency Point (BEP) is where the pump operates most efficiently with minimal vibration and cavitation."""
            },
            "Compressor Types and Components": {
                "keywords": ["compressor", "reciprocating", "centrifugal", "rotary", "screw", "surge", "intercooler"],
                "response": """Compressors increase gas pressure by reducing volume. 

Centrifugal Compressors:
- Use high-speed impellers
- Suitable for high flow, low pressure applications
- Provide continuous, pulsation-free flow
- Can experience surge at low flow conditions

Positive Displacement Compressors:
Reciprocating: Use pistons in cylinders, suitable for high pressure
Rotary Screw: Use meshing screws, good for medium pressure
Rotary Vane: Use sliding vanes in rotor

Key Components:
- Intercoolers: Cool gas between stages to reduce power
- Aftercoolers: Cool discharge gas
- Safety valves: Prevent overpressure
- Moisture separators: Remove condensate"""
            },
            "Measurement Devices": {
                "keywords": ["measurement", "pressure", "flow", "temperature", "venturi", "transducer", "gauge"],
                "response": """Common Measurement Devices:

Pressure Measurement:
- Bourdon Tube Gauges: Mechanical, for local indication
- Pressure Transducers: Convert pressure to electrical signal
- Differential Pressure Transmitters: Measure pressure difference

Flow Measurement:
- Venturi Tubes: Use Bernoulli's principle, high accuracy
- Orifice Plates: Simple, cost-effective
- Magnetic Flow Meters: For conductive fluids
- Ultrasonic Flow Meters: Non-intrusive

Temperature Measurement:
- RTDs (Resistance Temperature Detectors): High accuracy
- Thermocouples: Wide temperature range
- Thermistors: High sensitivity

All devices require proper calibration and installation for accurate measurements."""
            },
            "Safety Procedures": {
                "keywords": ["safety", "startup", "shutdown", "lockout", "tagout", "procedure", "maintenance"],
                "response": """Safe Pump/Compressor Operation Procedures:

Startup Sequence:
1. Check lubrication levels and conditions
2. Verify valve positions (suction open, discharge closed)
3. Check coupling alignment and guards
4. Ensure proper ventilation
5. Verify all safety devices are functional
6. Start pump/compressor
7. Gradually open discharge valve

Shutdown Sequence:
1. Gradually reduce load
2. Close discharge valve
3. Stop motor
4. Isolate equipment with valves
5. Lockout/Tagout for maintenance

Safety Protocols:
- Always use Lockout/Tagout during maintenance
- Wear appropriate PPE
- Follow manufacturer's instructions
- Regular inspection and maintenance
- Pressure testing as required"""
            },
            "Cavitation and Pump Safety": {
                "keywords": ["cavitation", "npsh", "bubbles", "noise", "vibration", "suction"],
                "response": """Cavitation occurs when liquid pressure drops below vapor pressure, causing vapor bubbles to form and collapse violently.

Causes:
- Low suction pressure
- High fluid temperature
- Clogged suction lines or filters
- Pump operating too far from BEP
- Excessive suction lift

Effects:
- Loud knocking or cracking noises
- Vibration and reduced performance
- Pitting damage to impeller and casing
- Seal and bearing failure
- Reduced efficiency

Prevention:
- Maintain adequate NPSH Available > NPSH Required
- Reduce suction line restrictions
- Operate pump near BEP
- Keep fluid temperature within limits
- Proper suction pipe design

NPSH (Net Positive Suction Head) Required is provided by manufacturer, NPSH Available is determined by system design."""
            },
            "Performance Calculations": {
                "keywords": ["efficiency", "power", "calculation", "performance", "curve", "hydraulic"],
                "response": """Performance Calculations for Pumps and Compressors:

Pump Efficiency:
- Overall Efficiency: η = (Hydraulic Power / Shaft Power) × 100%
- Hydraulic Power: P_hyd = (Q × H × ρ × g) / 1000 [kW]
  Where: Q = Flow rate (m³/s), H = Total head (m), ρ = Density (kg/m³), g = 9.81 m/s²
- Shaft Power: P_shaft = (2π × N × T) / 60000 [kW]

Compressor Efficiency:
- Isothermal Efficiency: Assumes constant temperature compression
- Volumetric Efficiency: η_vol = (Actual Flow / Theoretical Flow) × 100%
- Pressure Ratio: PR = P_discharge / P_suction

Characteristic Curves:
- Show relationship between flow, head, power, and efficiency
- Help in proper pump selection and operation
- Identify BEP (Best Efficiency Point)

Typical pump efficiencies: 50-85%, compressors: 60-80%"""
            }
        }
        
        # Find the matching category
        user_lower = user_message.lower()
        response = "I'm your Pumps and Compressors learning assistant! "
        
        for category, data in knowledge_base.items():
            if any(keyword in user_lower for keyword in data["keywords"]):
                response = data["response"]
                break
        else:
            response += "I can help with topics like pump operation, compressor types, cavitation, efficiency calculations, and safety procedures. Please ask me specific questions about these topics."
        
        return response
    
    def display_ai_message(self, message, sender):
        """Display message in AI chat"""
        self.ai_chat_display.config(state='normal')
        if sender == "user":
            self.ai_chat_display.insert(tk.END, f"\n👤 {message}\n")
        else:
            self.ai_chat_display.insert(tk.END, f"\n🤖 {message}\n")
        self.ai_chat_display.config(state='disabled')
        self.ai_chat_display.see(tk.END)
    
    def load_progress(self):
        """Load and display user progress"""
        # Clear treeview
        for item in self.progress_tree.get_children():
            self.progress_tree.delete(item)
        
        # Get progress data
        self.cursor.execute('''
            SELECT t.title, t.week, t.day, 
                   COALESCE(up.completed, 0) as completed,
                   COALESCE(up.quiz_score, 0) as quiz_score,
                   COALESCE(up.timestamp, 'Never') as last_attempt
            FROM topics t
            LEFT JOIN user_progress up ON t.id = up.topic_id
            ORDER BY t.week, t.day
        ''')
        
        progress_data = self.cursor.fetchall()
        
        total_topics = len(progress_data)
        completed_topics = 0
        total_score = 0
        scored_topics = 0
        
        for topic in progress_data:
            title, week, day, completed, quiz_score, last_attempt = topic
            
            status = "✅ Completed" if completed else "⏳ Not Started"
            score_display = f"{quiz_score:.1f}%" if quiz_score > 0 else "N/A"
            
            # Format timestamp
            if last_attempt != 'Never':
                try:
                    last_attempt = datetime.strptime(last_attempt, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')
                except:
                    last_attempt = str(last_attempt)[:10]
            
            self.progress_tree.insert('', 'end', values=(title, week, day, status, score_display, last_attempt))
            
            if completed:
                completed_topics += 1
            if quiz_score > 0:
                total_score += quiz_score
                scored_topics += 1
        
        # Calculate averages
        completion_rate = (completed_topics / total_topics * 100) if total_topics > 0 else 0
        average_score = (total_score / scored_topics) if scored_topics > 0 else 0
        
        summary_text = f"Overall Progress: {completed_topics}/{total_topics} topics completed ({completion_rate:.1f}%)"
        if scored_topics > 0:
            summary_text += f" | Average Score: {average_score:.1f}%"
        
        self.progress_summary.config(text=summary_text)

def main():
    root = tk.Tk()
    app = AIQuizGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

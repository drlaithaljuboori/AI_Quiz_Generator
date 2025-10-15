import streamlit as st
import sqlite3
import json
import random
from datetime import datetime
import os

# Initialize session state
def init_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'current_topic_id' not in st.session_state:
        st.session_state.current_topic_id = None
    if 'previous_topic' not in st.session_state:
        st.session_state.previous_topic = None

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('pumps_compressors.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
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
    
    cursor.execute('''
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
    
    cursor.execute('''
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
    insert_sample_data(cursor, conn)
    
    return conn, cursor

def insert_sample_data(cursor, conn):
    """Insert sample data if database is empty"""
    cursor.execute("SELECT COUNT(*) FROM topics")
    if cursor.fetchone()[0] > 0:
        return
    
    # Topics data
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
        cursor.execute(
            "INSERT INTO topics (week, day, title, description, pcs, content) VALUES (?, ?, ?, ?, ?, ?)",
            topic
        )
    
    # Quiz questions - Adding questions for ALL topics
    quiz_data = [
        # Pump Fundamentals (Topic 1)
        (1, "Which pump type uses an impeller to move fluid?", 
         '["Centrifugal Pump", "Piston Pump", "Gear Pump", "Diaphragm Pump"]', 
         "Centrifugal Pump", "multiple_choice"),
        
        (1, "What is the main function of a pump?", 
         '["Increase fluid pressure", "Generate electricity", "Cool the fluid", "Filter contaminants"]', 
         "Increase fluid pressure", "multiple_choice"),
        
        (1, "Which component converts velocity energy to pressure energy in centrifugal pumps?", 
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
        
        (2, "What is the purpose of an intercooler in multi-stage compressors?", 
         '["Reduce power consumption", "Increase final pressure", "Cool gas between stages", "Lubricate parts"]', 
         "Cool gas between stages", "multiple_choice"),
        
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
        
        (3, "Which device converts pressure to electrical signal?", 
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
        cursor.execute(
            "INSERT INTO quizzes (topic_id, question, options, correct_answer, question_type) VALUES (?, ?, ?, ?, ?)",
            quiz
        )
    
    conn.commit()

def main():
    st.set_page_config(
        page_title="AI Quiz Generator - Pumps & Compressors",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state and database
    init_session_state()
    conn, cursor = init_database()
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #2e86ab;
            margin-bottom: 1rem;
        }
        .question-box {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 5px solid #1f77b4;
        }
        .result-box {
            background-color: #e8f4fd;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 5px solid #28a745;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">🎯 AI Based Quiz Generator</div>', unsafe_allow_html=True)
    st.markdown("### Pumps and Compressors Learning Platform")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio(
        "Choose Section:",
        ["📝 MCQ Quizzes", "🤖 AI Learning Assistant", "📊 Progress Tracking"]
    )
    
    if app_mode == "📝 MCQ Quizzes":
        show_quizzes(cursor, conn)
    elif app_mode == "🤖 AI Learning Assistant":
        show_ai_assistant(cursor)
    elif app_mode == "📊 Progress Tracking":
        show_progress_tracking(cursor)
    
    conn.close()

def show_quizzes(cursor, conn):
    st.markdown('<div class="sub-header">📝 Multiple Choice Quizzes</div>', unsafe_allow_html=True)
    
    # Get topics for selection
    cursor.execute("SELECT id, week, day, title, description FROM topics ORDER BY week, day")
    topics_data = cursor.fetchall()
    
    if not topics_data:
        st.warning("No topics available. Please contact administrator.")
        return
    
    # Create topic dictionary with proper formatting
    topic_dict = {}
    for topic_id, week, day, title, description in topics_data:
        display_name = f"Week {week}, Day {day}: {title}"
        topic_dict[display_name] = (topic_id, description)
    
    selected_topic_display = st.selectbox("🎯 Select a Topic:", list(topic_dict.keys()))
    
    if selected_topic_display:
        topic_id, description = topic_dict[selected_topic_display]
        
        # Reset question index if topic changed
        if st.session_state.current_topic_id != topic_id:
            st.session_state.current_question = 0
            st.session_state.user_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.current_topic_id = topic_id
        
        st.info(f"**Topic Description:** {description}")
        
        # Get questions for selected topic
        cursor.execute(
            "SELECT id, question, options, correct_answer FROM quizzes WHERE topic_id=?", 
            (topic_id,)
        )
        questions = cursor.fetchall()
        
        if not questions:
            st.warning("No questions available for this topic yet.")
            st.session_state.current_question = 0
            return
        
        # Display current question
        display_question(questions, cursor, conn)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.session_state.current_question > 0:
                if st.button("⬅️ Previous Question"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col3:
            if st.session_state.current_question < len(questions) - 1:
                if st.button("Next Question ➡️"):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("🎯 Submit Quiz", type="primary"):
                    calculate_score(questions, topic_id, cursor, conn)
                    st.session_state.quiz_submitted = True
                    st.rerun()

def display_question(questions, cursor, conn):
    """Display the current question"""
    # Ensure current_question is within bounds
    if st.session_state.current_question >= len(questions):
        st.session_state.current_question = 0
    
    if not questions:
        st.warning("No questions available for this topic.")
        return
    
    question_id, question, options_json, correct_answer = questions[st.session_state.current_question]
    
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    
    # Question counter
    st.write(f"**Question {st.session_state.current_question + 1} of {len(questions)}**")
    
    # Question text
    st.subheader(question)
    
    # Parse and display options
    options = json.loads(options_json)
    
    # Create a unique key for each question
    answer_key = f"q_{st.session_state.current_topic_id}_{st.session_state.current_question}"
    
    # Display options as radio buttons
    selected_option = st.radio(
        "Select your answer:",
        options,
        key=answer_key,
        index=None
    )
    
    # Save answer to session state
    if selected_option:
        st.session_state.user_answers[st.session_state.current_question] = selected_option
    
    st.markdown('</div>', unsafe_allow_html=True)

def calculate_score(questions, topic_id, cursor, conn):
    """Calculate and display quiz results"""
    correct_count = 0
    total_questions = len(questions)
    
    # Calculate score
    for i, (question_id, question, options_json, correct_answer) in enumerate(questions):
        if i in st.session_state.user_answers and st.session_state.user_answers[i] == correct_answer:
            correct_count += 1
    
    score = (correct_count / total_questions) * 100
    
    # Determine grade and color
    if score >= 90:
        grade = "A - Excellent! 🎉"
        color = "green"
    elif score >= 80:
        grade = "B - Very Good! 👍"
        color = "green"
    elif score >= 70:
        grade = "C - Good! 👏"
        color = "orange"
    elif score >= 60:
        grade = "D - Pass ✅"
        color = "orange"
    else:
        grade = "F - Needs Improvement 📚"
        color = "red"
    
    # Save progress to database
    cursor.execute(
        """INSERT OR REPLACE INTO user_progress 
           (topic_id, quiz_score, completed, timestamp) 
           VALUES (?, ?, ?, ?)""",
        (topic_id, score, 1, datetime.now())
    )
    conn.commit()
    
    # Display results
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.success("### 🎊 Quiz Completed!")
    st.info(f"**📊 Score:** {score:.1f}% ({correct_count}/{total_questions} correct)")
    st.info(f"**🎯 Grade:** {grade}")
    
    # Show correct answers for learning
    with st.expander("📖 Review Correct Answers"):
        for i, (question_id, question, options_json, correct_answer) in enumerate(questions):
            st.write(f"**Q{i+1}: {question}**")
            st.write(f"✅ **Correct Answer:** {correct_answer}")
            user_answer = st.session_state.user_answers.get(i, "Not answered")
            if user_answer == correct_answer:
                st.write(f"🎯 **Your Answer:** {user_answer} ✓")
            else:
                st.write(f"❌ **Your Answer:** {user_answer}")
            st.write("---")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Reset button
    if st.button("🔄 Take Another Quiz"):
        st.session_state.current_question = 0
        st.session_state.user_answers = {}
        st.session_state.quiz_submitted = False
        st.rerun()

def show_ai_assistant(cursor):
    st.markdown('<div class="sub-header">🤖 AI Learning Assistant</div>', unsafe_allow_html=True)
    
    # Get topics for context
    cursor.execute("SELECT id, week, day, title FROM topics ORDER BY week, day")
    topics_data = cursor.fetchall()
    topic_names = [f"Week {week}, Day {day}: {title}" for id, week, day, title in topics_data]
    
    selected_topic = st.selectbox("📚 Select Topic for Context:", topic_names)
    
    # Extract topic name for knowledge base
    topic_key = selected_topic.split(": ")[1] if ": " in selected_topic else selected_topic
    
    # Sample questions from selected topic
    if selected_topic:
        # Extract topic ID
        topic_id = [id for id, week, day, title in topics_data if f"Week {week}, Day {day}: {title}" == selected_topic][0]
        
        cursor.execute("SELECT question FROM quizzes WHERE topic_id=? LIMIT 5", (topic_id,))
        sample_questions = cursor.fetchall()
        
        with st.expander("💡 Sample Questions for This Topic"):
            for i, (question,) in enumerate(sample_questions, 1):
                st.write(f"{i}. {question}")
    
    # Chat interface
    st.subheader("💬 Ask a Question")
    
    user_question = st.text_area(
        "Enter your question about pumps and compressors:",
        placeholder="e.g., What causes cavitation in pumps? How do centrifugal compressors work?...",
        height=100
    )
    
    if st.button("🚀 Get AI Answer", type="primary"):
        if user_question.strip():
            with st.spinner("🤔 Thinking..."):
                answer = get_ai_response(user_question, topic_key)
                st.markdown("---")
                st.success("### 🤖 AI Assistant Response:")
                st.info(answer)
        else:
            st.warning("Please enter a question.")

def get_ai_response(question, topic):
    """AI response system with comprehensive knowledge base"""
    
    knowledge_base = {
        "Pump Types and Fundamentals": """
**Centrifugal Pumps:**
- Use impellers to create centrifugal force
- Convert rotational energy to fluid energy
- Best for high flow, low pressure applications
- Components: Impeller, volute casing, shaft, seals

**Positive Displacement Pumps:**
- Trap fixed fluid volumes
- Force fluid through system
- Best for high pressure, low flow
- Types: Piston, gear, diaphragm, screw pumps

**Key Concepts:**
- BEP (Best Efficiency Point): Optimal operating point
- NPSH: Net Positive Suction Head requirements
- Specific speed: Characterizes pump type
""",
        
        "Compressor Types and Components": """
**Centrifugal Compressors:**
- High-speed impellers
- Continuous, pulsation-free flow
- Best for high flow, low-moderate pressure
- Multi-stage for higher pressures

**Positive Displacement Compressors:**
**Reciprocating:**
- Pistons in cylinders
- High pressure applications
- Pulsating flow
- Requires pulsation dampeners

**Rotary Screw:**
- Meshing screws
- Oil-flooded and oil-free types
- Medium pressure applications

**Key Components:**
- Intercoolers: Reduce power between stages
- Aftercoolers: Cool discharge air
- Moisture separators
- Safety valves
""",
        
        "Measurement Devices": """
**Pressure Measurement:**
- **Bourdon Tube Gauges:** Mechanical, local indication
- **Pressure Transducers:** Convert to electrical signals
- **Differential Pressure:** Flow measurement

**Flow Measurement:**
- **Venturi Tubes:** Bernoulli's principle, high accuracy
- **Orifice Plates:** Simple, cost-effective
- **Magnetic Flow Meters:** Conductive fluids only
- **Ultrasonic Flow Meters:** Non-intrusive

**Temperature Measurement:**
- **RTDs:** High accuracy, resistance-based
- **Thermocouples:** Wide range, voltage-based
- **Thermistors:** High sensitivity

**Installation Tips:**
- Proper upstream/downstream straight runs
- Calibration requirements
- Environmental considerations
""",
        
        "Safety Procedures": """
**Startup Sequence:**
1. Check lubrication levels and quality
2. Verify valve positions (suction open, discharge closed)
3. Inspect coupling alignment and guards
4. Ensure proper ventilation/cooling
5. Verify all safety devices functional
6. Start equipment
7. Gradually open discharge valve

**Shutdown Sequence:**
1. Gradually reduce load
2. Close discharge valve
3. Stop motor/engine
4. Isolate with block valves
5. Implement Lockout-Tagout for maintenance

**Safety Protocols:**
- **Lockout-Tagout (LOTO):** Essential for maintenance
- **PPE Requirements:** Gloves, safety glasses, hearing protection
- **Pressure Relief Valves:** Critical safety devices
- **Regular Inspections:** Vibration, temperature, pressure monitoring
""",
        
        "Cavitation and Pump Safety": """
**Cavitation Causes:**
- Low suction pressure
- High fluid temperature
- Clogged suction strainers
- Excessive suction lift
- Operating far from BEP

**Cavitation Effects:**
- Loud knocking/cracking noises
- Vibration and performance drop
- Impeller pitting and erosion
- Seal and bearing damage
- Reduced efficiency

**Prevention Methods:**
- Ensure NPSH Available > NPSH Required + margin
- Reduce suction line restrictions
- Operate near Best Efficiency Point
- Maintain proper fluid temperature
- Proper suction pipe design (minimize elbows, proper sizing)

**NPSH Calculation:**
- NPSH Available = System characteristic
- NPSH Required = Pump characteristic (from manufacturer)
- Safety margin: Typically 1-2 feet or 0.3-0.6 meters
""",
        
        "Performance Calculations": """
**Pump Efficiency:**
- Overall Efficiency = (Hydraulic Power / Shaft Power) × 100%
- Hydraulic Power (kW) = (Q × H × ρ × g) / 1000
  Where: Q = Flow rate (m³/s), H = Total head (m), ρ = Density (kg/m³), g = 9.81 m/s²
- Shaft Power (kW) = (2π × N × T) / 60000
  Where: N = Speed (rpm), T = Torque (N·m)

**Compressor Efficiency:**
- Isothermal Efficiency: Constant temperature assumption
- Volumetric Efficiency = (Actual Flow / Theoretical Flow) × 100%
- Adiabatic Efficiency: No heat transfer assumption
- Pressure Ratio = P_discharge / P_suction

**Characteristic Curves:**
- Head vs Flow rate
- Efficiency vs Flow rate
- Power vs Flow rate
- NPSH Required vs Flow rate

**Typical Efficiencies:**
- Centrifugal pumps: 75-85%
- Positive displacement pumps: 85-90%
- Centrifugal compressors: 70-80%
- Reciprocating compressors: 80-90%
"""
    }
    
    # Find best matching topic
    question_lower = question.lower()
    best_match = "General"
    
    for topic_name, content in knowledge_base.items():
        if any(keyword in question_lower for keyword in topic_name.lower().split()):
            best_match = topic_name
            break
        # Check for common keywords
        topic_keywords = {
            "Pump Types and Fundamentals": ["pump", "centrifugal", "positive displacement", "impeller", "volute", "BEP"],
            "Compressor Types and Components": ["compressor", "reciprocating", "rotary", "screw", "centrifugal", "surge"],
            "Measurement Devices": ["measure", "pressure", "flow", "temperature", "venturi", "transducer", "gauge"],
            "Safety Procedures": ["safety", "startup", "shutdown", "lockout", "tagout", "procedure", "maintenance"],
            "Cavitation and Pump Safety": ["cavitation", "npsh", "bubbles", "noise", "vibration", "suction"],
            "Performance Calculations": ["efficiency", "power", "calculation", "performance", "curve", "hydraulic"]
        }
        
        if any(keyword in question_lower for keyword in topic_keywords.get(topic_name, [])):
            best_match = topic_name
            break
    
    if best_match in knowledge_base:
        response = knowledge_base[best_match]
    else:
        response = """**Welcome to the Pumps and Compressors AI Assistant!** 🤖

I can help you with:
- **Pump Types & Fundamentals** (centrifugal, positive displacement)
- **Compressor Types & Components** (reciprocating, centrifugal, rotary)
- **Measurement Devices** (pressure gauges, flow meters, temperature sensors)
- **Safety Procedures** (startup/shutdown, Lockout-Tagout)
- **Cavitation & Pump Safety** (causes, prevention, NPSH)
- **Performance Calculations** (efficiency, power, curves)

Please ask me specific questions about these topics!"""

    return response

def show_progress_tracking(cursor):
    st.markdown('<div class="sub-header">📊 Learning Progress Tracking</div>', unsafe_allow_html=True)
    
    # Get progress data
    cursor.execute('''
        SELECT t.title, t.week, t.day, 
               COALESCE(up.quiz_score, 0) as score,
               COALESCE(up.completed, 0) as completed,
               COALESCE(up.timestamp, 'Never attempted') as last_attempt
        FROM topics t
        LEFT JOIN user_progress up ON t.id = up.topic_id
        ORDER BY t.week, t.day
    ''')
    
    progress_data = cursor.fetchall()
    
    if not progress_data:
        st.info("No progress data available. Complete some quizzes to track your progress!")
        return
    
    # Calculate overall statistics
    total_topics = len(progress_data)
    completed_topics = sum(1 for _, _, _, score, completed, _ in progress_data if completed)
    attempted_quizzes = sum(1 for _, _, _, score, completed, _ in progress_data if score > 0)
    average_score = sum(score for _, _, _, score, _, _ in progress_data if score > 0) / attempted_quizzes if attempted_quizzes > 0 else 0
    
    # Display statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Topics", total_topics)
    with col2:
        st.metric("Completed", completed_topics)
    with col3:
        st.metric("Quizzes Attempted", attempted_quizzes)
    with col4:
        st.metric("Average Score", f"{average_score:.1f}%")
    
    st.markdown("---")
    
    # Detailed progress table
    st.subheader("📈 Detailed Progress")
    
    for title, week, day, score, completed, last_attempt in progress_data:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
            
            with col1:
                st.write(f"**{title}**")
            
            with col2:
                st.write(f"Week {week}")
            
            with col3:
                st.write(f"Day {day}")
            
            with col4:
                status = "✅ Completed" if completed else "⏳ Not Started"
                st.write(status)
            
            with col5:
                if score > 0:
                    st.write(f"Score: **{score:.1f}%**")
                    st.progress(score/100)
                else:
                    st.write("Not attempted")
            
            # Show last attempt date if available
            if last_attempt != 'Never attempted':
                st.caption(f"Last attempt: {last_attempt}")
            
            st.markdown("---")

if __name__ == "__main__":
    main()

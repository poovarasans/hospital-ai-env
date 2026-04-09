---
title: Hospital Queue Optimization AI
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: streamlit
app_file: app.py
pinned: false
---
### 🏥 Hospital Queue Optimization AI

An intelligent, real-time hospital queue management system powered by AI-based prioritization.
This project simulates how patients are dynamically assigned to doctors based on severity and waiting time, ensuring optimal treatment flow.

⸻

## 🚀 Features
	•	🧠 AI-based Patient Prioritization
	•	Patients are selected using: priority = severity + wait_time
    •	🩺 Doctor Room Simulation
	•	Each doctor acts as a “room”
	•	Displays:
	•	🟢 Current patient (Consulting)
	•	🟡 Next patient (Up Next)
	•	🏥 Department-wise Organization
	•	Cardio, Neuro, Ortho, Pediatrics, Dental, etc.
	•	📊 Live Metrics
	•	Total reward
	•	Patients treated count
	•	👥 Dynamic Queue System
	•	Real-time patient updates
	•	Duplicate-safe queue handling
	•	⚡ Smooth UI Rendering
	•	No flickering / ghost UI
	•	Single render cycle using Streamlit placeholder
	•	📜 Treatment History
	•	Full record of treated patients

## 🧩 System Design

# 🔁 Simulation Loop
	1.	Get all patients
	2.	Compute priority
	3.	Select best patient
	4.	Assign to doctor
	5.	Update queue
	6.	Repeat until empty

# 🧠 AI Logic
    action = max(
    range(len(patients)),
    key=lambda i: patients[i]["severity"] + patients[i]["wait"]
    )

# 🏗️ Architecture
    Streamlit UI
     ↓
    Session State (env, state)
     ↓
    HospitalEnv (Simulation Engine)
     ↓
    Doctor Rooms + Queue Rendering

# 📦 Tech Stack
	•	Python 🐍
	•	Streamlit 🎯
	•	Pandas 📊
	•	Custom Simulation Environment

# ▶️ How to Run
    git clone <your-repo-url>
    cd hospital-ai
    pip install -r requirements.txt
    streamlit run app.py

# 🎮 Modes
	•	Easy
	•	Medium
	•	Hard

# Each mode changes:
	•	Patient arrival rate
	•	Severity distribution
	•	Queue complexity

# 📸 UI Overview
	•	🩺 Doctor Rooms (Top)
	•	👥 Department Queue (Bottom)
	•	📊 Metrics (Sidebar)
	•	📜 History (End)

# 🧠 Key Challenges Solved
	•	❌ Duplicate patients in queue
	•	❌ UI flickering in Streamlit
	•	❌ Improper department grouping
	•	❌ Multi-render inconsistencies

# ✔ Fixed using:
	•	Unique patient mapping
	•	Single placeholder rendering
	•	Structured layout separation

## 🌟 Future Improvements
	•	🧠 Reinforcement Learning (RL agent)
	•	📈 Doctor workload balancing
	•	⏱️ Real-time hospital data integration
	•	📱 Mobile dashboard

⸻

### 👨‍💻 Author

Poovarasan Subramani

⸻

### 🎉 Result

A clean, scalable, and intelligent hospital queue system that demonstrates real-world AI application in healthcare operations.
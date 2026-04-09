import streamlit as st
import pandas as pd
import time
from env import HospitalEnv
from collections import defaultdict

st.set_page_config(page_title="Hospital AI", layout="wide")

st.title("🏥 Hospital Queue Optimization AI")
st.markdown("### 🤖 AI-driven Hospital Queue System")

# ---------------- SIDEBAR ----------------
mode = st.sidebar.selectbox("Select Mode", ["easy", "medium", "hard"])
speed = st.sidebar.slider("Simulation Speed", 0.5, 5.0, 1.5)

# ---------------- INIT ----------------
if "env" not in st.session_state:
    st.session_state.env = None
    st.session_state.state = None
    st.session_state.done = True

if st.sidebar.button("Start Simulation"):
    st.session_state.env = HospitalEnv(mode=mode)
    st.session_state.state = st.session_state.env.reset()
    st.session_state.done = False

# ---------------- MAIN RENDER ----------------
placeholder = st.empty()

if st.session_state.env:

    with placeholder.container():

        env = st.session_state.env
        state = st.session_state.state

        # ================= STEP =================
        if not st.session_state.done:

            patients = state["patients"]

            if patients:
                action = max(
                    range(len(patients)),
                    key=lambda i: patients[i]["severity"] + patients[i]["wait"]
                )

                state, reward, done, info = env.step(action)

                st.session_state.state = state
                st.session_state.done = done
            else:
                st.session_state.done = True

        # ================= DOCTOR ROOMS =================
        st.subheader("🩺 Live Doctor Rooms")

        rooms = defaultdict(lambda: {"current": None, "queue": []})

        # current patients
        for p in env.completed:
            key = (p["category"].lower(), p["staff_name"])
            rooms[key]["current"] = p

        # queue patients
        for p in state["patients"]:
            key = (p["category"].lower(), p["staff_name"])
            rooms[key]["queue"].append(p)

        # group by department
        dept_rooms = defaultdict(list)
        for (dept, doctor), data in rooms.items():
            dept_rooms[dept].append((doctor, data))

        # render doctor rooms
        for dept, doctor_list in sorted(dept_rooms.items()):

            st.markdown(f"## 🏥 {dept.capitalize()} Department")

            for doctor, data in sorted(doctor_list):

                if not data["current"] and not data["queue"]:
                    continue

                st.markdown(f"### 👨‍⚕️ {doctor}")

                col1, col2 = st.columns(2)

                # CURRENT
                if data["current"]:
                    c = data["current"]
                    with col1:
                        st.success(f"""
                        ### Consulting
                        👤 {c['name']} ({c['age']})  
                        🩺 {c['description']}  
                        💊 {c['prescription']}
                        """)

                # NEXT
                if data["queue"]:
                    n = data["queue"][0]
                    with col2:
                        st.warning(f"""
                        ### Up Next
                        👤 {n['name']} ({n['age']})  
                        ⏳ Wait: {n['wait']}
                        """)

                st.markdown("---")

        st.markdown("___")

        # ================= QUEUE =================
        st.subheader("👥 Patients Queue (By Department)")

        # remove duplicates
        unique = {}
        for p in state["patients"]:
            unique[p["id"]] = p

        clean_patients = list(unique.values())

        queues = defaultdict(list)
        for p in clean_patients:
            queues[p["category"].lower()].append(p)

        categories = sorted(queues.keys())

        rows = [categories[i:i+2] for i in range(0, len(categories), 2)]

        for row in rows:
            cols = st.columns(len(row))

            for i, category in enumerate(row):
                with cols[i]:
                    st.markdown(f"### 🏥 {category.title()}")

                    df = pd.DataFrame(queues[category])

                    if not df.empty:
                        df["patient_info"] = df.apply(
                            lambda r: f"{r['name']} ({r['gender']}, {r['age']})",
                            axis=1
                        )

                        st.table(df[["id", "patient_info", "wait"]])

        # ================= METRICS =================
        st.sidebar.markdown("### 📊 Metrics")
        st.sidebar.metric("Total Reward", state["total_reward"])
        st.sidebar.metric("Patients Treated", state["treated"])

# ---------------- HISTORY ----------------
st.markdown("---")
st.markdown("### 📜 Treated Patients")

if st.session_state.env and st.session_state.env.completed:
    hist_df = pd.DataFrame(st.session_state.env.completed)
    hist_df.index += 1
    st.table(hist_df[["name", "category", "staff_type", "staff_name", "prescription"]])

# ---------------- END ----------------
if st.session_state.done and st.session_state.state:
    st.balloons()
    st.success("🎉 All patients treated!")

# ---------------- LOOP ----------------
if st.session_state.env and not st.session_state.done:
    time.sleep(speed)
    placeholder.empty()
    st.rerun()
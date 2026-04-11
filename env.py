from openai import OpenAI
from collections import defaultdict

import random
import os

class HospitalEnv:
    def __init__(self, mode="easy"):
        self.mode = mode
        self.patients = []
        self.time = 0
        self.total_reward = 0
        self.treated_count = 0

        self.counter = 0
        self.completed = []

        self.roles = ["doctor", "nurse", "physiotherapist", "pharmacist"]

    # patient generator
    def generate_patient(self, id):
        male_names = ["Ravi", "Suresh", "Karthik", "Dhinakar", "Thangaraj", "Sathish", "Alex", "Willsen", "Peter", "Paul", "Celester", "Baskar", "Gnanaprakash"]
        female_names = ["Anita", "Priya", "Mary", "Nancy", "Elisa Joseph", "Gowri", "Lakshmi", "Olivia", "Anbu", "Hema", "Surya", "Ragavi"]
        all_names = male_names + female_names
        name = random.choice(all_names)
        age = random.randint(0, 70)
        severity = random.randint(1, 5)

        # gender logic
        if name in male_names:
            gender = "Male"
        else:
            gender = "Female"
                
        # third gender inclusive logic
        if random.random() < 0.05:
            gender = "Third Gender"

        patient_types = ["General", "Cardio", "Neuro", "Ortho", "Dental"]

        # pediatrics logic
        if age <= 12:
            category = "Pediatrics"
        else:
            category = random.choice(patient_types)

        # Gyno inclusive logic
        if name in female_names and random.random() < 0.05:
            category = "Gyno"

        if category in ["Cardio", "Neuro", "Pediatrics", "Dental", "Gyno"]:
            staff_type = "doctor"
        elif severity <= 2:
            staff_type = "pharmacist"
        elif severity == 3:
            staff_type = "nurse"
        elif severity > 3:
            staff_type = "doctor"

        if severity <= 2 and category == "Ortho":
            staff_type = "physiotherapist"
        
        ortho_doctors = ["Dr. Kameshwaran", "Dr. Karthika", "Dr. Saravanakumar"]
        neuro_doctors = ["Dr. Thiruvarutchelvan", "Dr. Selvam", "Dr. Subramaniam"]
        gyno_doctors = ["Dr. Vaani", "Dr. Sunantha", "Dr. Valli"]
        general_doctors = ["Dr. Latheesh", "Dr. Kavipriya", "Dr. Suresh"]
        cardio_doctors = ["Dr. anbuchelvan", "Dr. Santhosh", "Dr. Karmegham"]
        pedia_doctors = ["Dr. Karthikeyan", "Dr. Latheesh", "Dr. Cheliyan"]
        dental_doctors = ["Dr. Ilavarasan", "Dr. Kiruthika", "Dr. Iniyan"]

        parma_name = ["Asif", "Ram", "gunaseelan"]
        nurse_name = ["Kanagvalli", "Sundharambal", "Sanjana"]
        physio_name = ["Dr. Kalaivaani", "Dr. Dhivakar", "Dr. Prabhu"]

        symptoms = {
            "ortho_symptoms": [
                "Severe knee pain with swelling",
                "Lower back pain after lifting weight",
                "Shoulder stiffness with limited movement",
                "Fracture suspected in right arm",
                "Joint pain with morning stiffness",
                "Muscle strain with difficulty walking",
                "Ankle swelling after injury",
                "Back pain radiating to leg"
            ],
            "neuro_symptoms": [
                "Severe headache with sensitivity to light",
                "Frequent dizziness and loss of balance",
                "Numbness in left hand and leg",
                "Short-term memory loss and confusion",
                "Blurred vision with headache",
                "Sudden weakness on one side of body",
                "Seizure episodes reported",
                "Vertigo while standing or walking"
            ],
            "gyno_symptoms": [
                "Severe lower abdominal pain with cramps",
                "Irregular menstrual cycle with heavy bleeding",
                "Pelvic pain and discomfort",
                "Missed periods with nausea",
                "Hormonal imbalance symptoms reported",
                "Severe period cramps affecting daily activity",
                "Lower abdominal pain with dizziness",
                "Unusual discharge with discomfort"
            ],
            "general_symptoms": [
                "High fever with body pain",
                "Cold and persistent cough",
                "Mild headache with fatigue",
                "Stomach pain after food intake",
                "Vomiting and nausea since morning",
                "Sore throat with slight fever",
                "General weakness and tiredness",
                "Low-grade fever with headache"
            ],
            "cardio_symptoms": [
                "Chest pain with pressure sensation",
                "Shortness of breath during walking",
                "Irregular heartbeat and dizziness",
                "Severe chest tightness radiating to left arm",
                "Fatigue with mild breathlessness",
                "Cold sweating with chest discomfort"
            ],
            "pedia_symptoms": [
                "High fever in child with irritability",
                "Cold and cough in child for 3 days",
                "Vomiting and stomach upset in child",
                "Skin rash with itching",
                "Loss of appetite and weakness",
                "Child crying with abdominal pain",
                "Mild breathing difficulty in child",
                "Loose motion since morning"
            ],
            "dental_symptoms": [
                "Severe toothache with sensitivity to cold",
                "Gum swelling with bleeding while brushing",
                "Tooth decay causing continuous pain",
                "Jaw pain while chewing food",
                "Bad breath with gum infection",
                "Loose tooth with discomfort",
                "Tooth sensitivity to hot and cold drinks",
                "Dental cavity with mild pain"
            ]
        }

        # description selection
        if category == "Ortho":
            description = random.choice(symptoms["ortho_symptoms"])
        elif category == "Neuro":
            description = random.choice(symptoms["neuro_symptoms"])
        elif category == "Gyno":
            description = random.choice(symptoms["gyno_symptoms"])
        elif category == "General":
            description = random.choice(symptoms["general_symptoms"])
        elif category == "Cardio":
            description = random.choice(symptoms["cardio_symptoms"])
        elif category == "Pediatrics":
            description = random.choice(symptoms["pedia_symptoms"])
        else:
            description = random.choice(symptoms["dental_symptoms"])

        # Staff Selection logic
        if staff_type == "doctor" and category == "Ortho":
            staff_name = random.choice(ortho_doctors)
        elif staff_type == "doctor" and category == "Neuro":
            staff_name = random.choice(neuro_doctors)
        elif staff_type == "doctor" and category == "Gyno":
            staff_name = random.choice(gyno_doctors)
        elif staff_type == "doctor" and category == "General":
            staff_name = random.choice(general_doctors)
        elif staff_type == "doctor" and category == "Cardio":
            staff_name = random.choice(cardio_doctors)
        elif staff_type == "doctor" and category == "Pediatrics":
            staff_name = random.choice(pedia_doctors)
        elif staff_type == "doctor" and category == "Dental":
            staff_name = random.choice(dental_doctors)
        elif staff_type == "nurse":
            staff_name = random.choice(nurse_name)
        elif staff_type == "pharmacist":
            staff_name = random.choice(parma_name)
        else:
            staff_name = random.choice(physio_name)

        return {
            "id": id,
            "name": name,
            "age": age,
            "gender": gender,
            "severity": severity,
            "wait": 0,
            "category": category,
            "history": random.choice(["Diabetes", "BP", "None"]),
            "last_visit": "2025-03-01",
            "address": random.choice(["Chennai", "Bangalore", "Salem"]),
            "prev_suggestion": random.choice(["Rest", "Medication", "Exercise"]),
            "description": description,
            "staff_type": staff_type,
            "staff_name":staff_name,
            "prescription": None
        }

    # Prescription using LLM
    def generate_prescription(self, patient):

        base_url = os.getenv("API_BASE_URL")
        api_key = os.getenv("API_KEY")

        # fallback preset prescription
        prescriptions = {
            "cardio": [
                "ECG + BP tablets",
                "Blood test + lifestyle changes",
                "Heart scan + medication"
            ],
            "neuro": [
                "MRI scan + neurologist consult",
                "Pain relief medication",
                "Brain scan + rest"
            ],
            "ortho": [
                "X-ray + pain relief gel",
                "Physiotherapy + rest",
                "Bone scan + calcium tablets"
            ],
            "gyno": [
                "Hormone test + medication",
                "Ultrasound scan",
                "Iron tablets + rest"
            ],
            "general": [
                "Paracetamol + rest",
                "Antibiotics course",
                "Hydration + basic meds"
            ],
            "pedia": [
                "Syrup + rest",
                "Fever medication for child",
                "Pediatric check + fluids"
            ],
            "dental": [
                "Dental cleaning + medication",
                "Tooth filling + pain relief",
                "Root canal treatment suggested",
                "Antibiotics + dental checkup"
            ]
        }

        # fallback if env not present
        if not base_url or not api_key:
            if patient["category"] == "Ortho":
                return random.choice(prescriptions["ortho"])
            elif patient["category"] == "Neuro":
                return random.choice(prescriptions["neuro"])
            elif patient["category"] == "Gyno":
                return random.choice(prescriptions["gyno"])
            elif patient["category"] == "General":
                return random.choice(prescriptions["general"])
            elif patient["category"] == "Cardio":
                return random.choice(prescriptions["cardio"])
            elif patient["category"] == "Pediatrics":
                return random.choice(prescriptions["pedia"])
            else:
                return random.choice(prescriptions["dental"])

        client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

        # getting prescription from LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a doctor."},
                {"role": "user", "content": f"Give treatment for patient: {patient}"}
            ]
        )

        return response.choices[0].message.content

    def reset(self):
        self.counter = 0
        self.completed = []

        self.patients = [self.generate_patient(i) for i in range(5)]

        self.total_reward = 0
        self.treated_count = 0

        return self.state()
    

    def get_category_queues(self):
        queues = defaultdict(list)

        for p in self.patients:
            queues[p["category"]].append(p)

        return queues

    def state(self):
        return {
            "patients": self.patients,
            "category_queues": self.get_category_queues(),
            "total_reward": self.total_reward,
            "treated": self.treated_count
        }

    def step(self, action):
        reward = 0

        if action >= len(self.patients):
            return self.state(), -5.0, False, {"error": "invalid action"}

        patient = self.patients.pop(action)

        prescription = self.generate_prescription(patient)
        patient["prescription"] = prescription

        reward += patient["severity"]

        if patient["category"] in ["Cardio", "Neuro"] and patient["staff_type"] == "doctor":
            reward += 7
        elif patient["severity"] <= 2 and patient["staff_type"] == "pharmacist":
            reward += 3
        elif patient["severity"] >= 4 and patient["staff_type"] == "doctor":
            reward += 4
        else:
            reward -= 3

        self.completed.append(patient)
        self.treated_count += 1

        for p in self.patients:
            p["wait"] += 1

        # if len(self.patients) < 5:
        #     self.counter += 1
        #     self.patients.append(self.generate_patient(self.counter))

        self.total_reward += reward

        done = len(self.patients) == 0

        reward = float(round(reward, 2))
        reward = max(-10, min(10, reward))

        return self.state(), reward, done, {
            "staff": patient["staff_type"],
            "prescription": prescription
        }
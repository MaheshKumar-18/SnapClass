# 🎓 SnapClass – AI-Powered Smart Attendance Management System

SnapClass is an AI-powered attendance management system that automates classroom attendance using **Face Recognition**, **Voice Recognition**, **Computer Vision**, **Supabase**, and **Streamlit**.

The system enables teachers to manage courses, enroll students, and take attendance using facial recognition from classroom photos or speaker recognition from classroom audio. Students can securely log in using Face ID, enroll in subjects, and track their attendance through an intuitive dashboard.

---

# ✨ Features

## 👨‍🏫 Teacher Module

* Secure teacher authentication
* Create and manage subjects
* Share subjects using QR Code or Join Link
* AI-powered Photo Attendance
* AI-powered Voice Attendance
* Attendance Reports & Analytics
* Student Management

---

## 👨‍🎓 Student Module

* Face Recognition Login
* Face Registration
* Optional Voice Enrollment
* Subject Enrollment
* QR Code Quick Enrollment
* Attendance Dashboard
* Attendance Statistics

---

## 🤖 AI Features

* Face Detection using dlib
* Face Embedding Generation
* Face Recognition using Support Vector Machine (SVM)
* Voice Embedding using Resemblyzer
* Speaker Identification
* Multi-photo Classroom Attendance
* Bulk Audio Attendance

---

# 🛠 Tech Stack

### Frontend

* Streamlit
* HTML
* CSS

### Backend

* Python

### Database

* Supabase

### Artificial Intelligence

* dlib
* Resemblyzer
* OpenCV
* NumPy
* Scikit-learn

### Other Libraries

* Pillow
* Pandas
* Segno (QR Code)
* bcrypt

---

# 📂 Project Structure

```text
SnapClass/
│
├── ai-attendance-project-app/
│   ├── src/
│   │   ├── components/
│   │   ├── database/
│   │   ├── pipelines/
│   │   ├── screens/
│   │   └── ui/
│   │
│   ├── face_recognition_models/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
└── ai-attendance-project-landing/
    ├── static/
    ├── templates/
    ├── app.py
    ├── requirements.txt
    └── README.md
```

---

# 📸 System Workflow

```text
Teacher
     │
     ▼
Create Subject
     │
     ▼
Share QR Code / Join Link
     │
     ▼
Student Enrolls
     │
     ▼
Face Registration
     │
     ▼
Voice Enrollment (Optional)
     │
     ▼
Teacher Takes Attendance
     │
     ▼
AI Recognition
     │
     ▼
Attendance Reports
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/SnapClass.git
```

Navigate to the application

```bash
cd SnapClass/ai-attendance-project-app
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 📸 Screenshots

Add screenshots of:

* Home Page
* Teacher Dashboard
* Student Dashboard
* Face Attendance
* Voice Attendance
* Attendance Reports

---

# 🚀 Future Improvements

* Email Notifications
* Mobile Application
* Real-time Attendance Dashboard
* Attendance Export (Excel/PDF)
* Face Liveness Detection
* Multi-Class Support
* Cloud Deployment

---

# 👨‍💻 Developer

**Mahesh Kumar**

B.Tech – Computer Science (AI & ML)

---

# 📄 License

This project is developed for educational and portfolio purposes.

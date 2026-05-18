AI Fitness Assistant

An AI-powered fitness assistant built using Python, OpenCV, and MediaPipe that can track body movements and count exercises in real time through a webcam.

Features
Real-time body pose detection
Exercise repetition counter
Angle calculation for posture tracking
Live webcam feedback
Clean and simple interface
Built completely in Python
Tech Stack
Python
OpenCV
MediaPipe
NumPy
Matplotlib
How It Works

The program uses MediaPipe Pose Estimation to detect body landmarks from a webcam feed.
Using those landmarks, the assistant calculates joint angles and tracks exercise movement patterns to count repetitions accurately.

Project Structure
AI-Fitness-Assistant/
│
├── main.py
├── test.py
├── requirements.txt
├── .gitignore
└── README.md
Installation

Clone the repository:

git clone https://github.com/Ary-02811/AI-Fitness-Assistant.git

Move into the project folder:

cd AI-Fitness-Assistant

Install dependencies:

pip install -r requirements.txt

Run the project:

python main.py
Future Improvements
Add multiple exercise support
Voice assistant integration
Workout history tracking
AI-based posture correction
Web or mobile deployment
Learning Outcomes

This project helped me understand:

Computer Vision basics
Pose estimation using MediaPipe
Real-time video processing
Python project structuring
Git and GitHub workflow
Author

Aryan Pillai

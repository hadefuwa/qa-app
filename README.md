# Kids Q&A App

A fun, interactive web application to help kids learn through multiple-choice quizzes on various subjects!

## Features

- 🎨 Kid-friendly, colorful interface
- 📚 Multiple quizzes on different subjects with questions organized into sections
- 📖 Expanded reading material for each section to help kids learn
- ✅ Instant feedback on answers
- 🎯 Progress tracking and score calculation
- 🏆 Graded results (Fail, Pass, Very Good, Excellent)
- 🔄 Easy navigation between sections
- 📊 Difficulty levels: Easy, Medium, and Hard
- 🌐 Accessible from any device on your local network

## Setup Instructions

1. **Install Python** (if you haven't already)
   - Make sure you have Python 3.7 or higher installed
   - You can check by running: `python --version` or `python3 --version`

2. **Install Flask**
   - Open a terminal/command prompt in this folder
   - Run: `pip install -r requirements.txt`
   - Or: `pip install Flask`

3. **Run the App**
   - In the terminal, run: `python app.py` (or `python3 app.py`)
   - You should see: "Running on http://0.0.0.0:8080"

4. **Access from Your PC**
   - Open a web browser
   - Go to: `http://localhost:8080`

5. **Access from Other Devices (Kids' PCs)**
   - Find your PC's IP address:
     - Windows: Open Command Prompt and type `ipconfig`, look for "IPv4 Address"
     - Mac/Linux: Open Terminal and type `ifconfig` or `ip addr`
   - On the kids' devices, open a web browser
   - Go to: `http://YOUR_IP_ADDRESS:8080`
     - Example: `http://192.168.1.100:8080`

## Files

- `app.py` - The main Flask application with all quiz data
- `qa.md` - Reference file with original quiz questions
- `templates/home.html` - The main menu page showing all available quizzes
- `templates/index.html` - The quiz home page showing sections
- `templates/section.html` - The section page template with reading material and questions
- `templates/results.html` - The results page showing final scores and grades
- `requirements.txt` - Python dependencies

## How It Works

1. Start at the **home page** - browse quizzes organized by difficulty (Easy, Medium, Hard)
2. Select a quiz to begin
3. Each quiz is divided into **sections** with:
   - Expanded reading material about that topic
   - Questions related to that section
   - Navigation to move between sections
4. Answer questions and get instant feedback
5. Track your progress as you complete sections
6. View your final results with a grade at the end

## Troubleshooting

- **Can't access from other devices?**
  - Make sure all devices are on the same Wi-Fi network
  - Check that your firewall allows connections on port 8080
  - Try using `http://127.0.0.1:8080` on your PC first to test

- **Port 8080 already in use?**
  - You can change the port in `app.py` (last line) to any other number like 8081, 3000, etc.

## Have Fun Learning! 🎉


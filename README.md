# Vikings Q&A App for Kids

A fun, interactive web application to help kids learn about Vikings through multiple-choice questions!

## Features

- 🎨 Kid-friendly, colorful interface
- 📚 30 questions organized into 5 separate sections (each on its own page)
- 📖 Expanded reading material for each section to help kids learn
- ✅ Instant feedback on answers
- 🎯 Score tracking per section
- 🔄 Easy navigation between sections
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

- `app.py` - The main Flask application
- `qa.md` - The quiz questions and answers (reference)
- `templates/index.html` - The home page with section navigation
- `templates/section.html` - The section page template (used for all 5 sections)
- `requirements.txt` - Python dependencies

## How It Works

1. Start at the **home page** - choose which section to explore
2. Each **section page** has:
   - Expanded reading material about that topic
   - Questions related to that section
   - Navigation to move between sections
3. Answer questions and get instant feedback
4. See your score at the end of each section

## Troubleshooting

- **Can't access from other devices?**
  - Make sure all devices are on the same Wi-Fi network
  - Check that your firewall allows connections on port 8080
  - Try using `http://127.0.0.1:8080` on your PC first to test

- **Port 8080 already in use?**
  - You can change the port in `app.py` (last line) to any other number like 8081, 3000, etc.

## Have Fun Learning! 🎉


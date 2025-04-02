# WebAppDevN
Group project for WebApp.

## 📁 Project Structure
```bash
WebAppDevN/
├── core/                        # Main Django app
│   ├── migrations/             # Database migrations
│   ├── templates/
│   │   ├── core/
│   │       ├── base.html       # Base template with navbar and sidebar
│   │       ├── manager.html    # Dashboard for manager
│   │       ├── assign-tech.html # Form to assign technicians
│   |       └── raise-ticket.html # Fault reporting form
│   │       └── navbar.html     # Reusable navbar with sidebar
│   │       
│   ├── static/
│   │   └── css/
│   │       ├── manager.css     # Styles for dashboard page
│   │       ├── assign-tech.css # Styles for technician assignment
│   │       └── raise-ticket.css# Styles for fault ticket form
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── README.md
```

> 📌 inside `WebAppDevN/core/templates/core`  → all the HTML files are placed here  
> 📌 inside `WebAppDevN/core/static/css`      → all the CSS files are placed here  
> 📌 inside `WebAppDevN/core/static/js`       → all the JavaScript files are placed here  
> 📌 inside `WebAppDevN/core/static/images`   → all the image files are placed here


## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Tiarban/WebAppDevN.git
cd WebAppDevN
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate       # On macOS/Linux
.venv\Scripts\activate         # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```


### 4. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.



## 🔄 Making Changes and Pushing to GitHub

After making changes to any files in the project (HTML, CSS, Python, etc.), follow these steps:

```bash
# 1. Check what has changed
git status

# 2. Stage the changes
git add .

# 3. Commit the changes
git commit -m "Describe what you changed"

# 4. Pull any new changes from GitHub before pushing
git pull origin main --rebase

# 5. Push your changes to GitHub
git push origin main
```


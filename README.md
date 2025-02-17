# Project Setup & Workflow

Below is a structured approach to guide this workshop. Adapt these steps to your specific requirements.

Please use the sample data provided (car data), as this has been properly prepared.

**Project folder structure:**

```bash
project/
│
├── .devcontainer/
│    └── devcontainer.json       → Configuration file for setting up the Dev Container
│
├── app.py                       → The main app file
├── Procfile                     → Configuration file for deployment (e.g. on Koyeb)
├── data/
│   ├── autoscout24_data.csv      → .csv file with car data
│   └── credentials.json          → JSON file storing the OpenAI API key
│
├── static/
│   ├── css/
|   |   ├── styles.css            → File to define styles (CSS) in HTML pages
│   ├── logo.svg                  → Logos etc. to include into the HTML pages
│   └── graphic.png               → Generated plots (saved here)
│   
├── templates/
│    ├── index.html                → Main HTML page
│    ├── data.html                 → Data describtion page
│    └── questions.html            → Example questions page
│
└── requirements.txt               → File to specify the Python libraries
```

## 1. Audit Existing Files

- Configuration: Check .devcontainer/devcontainer.json and Procfile setup.
- Backend: Discuss the required functionality of app.py in your team.
- Data: Examine autoscout24_data.csv.
- OpenAI API-key: Ensure credentials.json is available contains a valid API-key.
- Frontend: Verify templates/ and static/ files for completeness.
- Dependencies: Ensure requirements.txt includes all necessary libraries.

**Outcome:** Clear understanding of what’s available and what needs to be added.

---

## 2. Define Backend Requirements

- Framework: In this course we will use Flask.
- Data Handling: Read 'autoscout24_data.csv' and store the data in a pandas data frame.
- Routes: Ensure endpoints for / (index), /data, and /questions.
- API Integration: Securely access credentials.json and handle OpenAI queries.
- Error Handling: Implement error responses for data loading and API failures.
- Deployment: Validate Procfile for production readiness.

**Outcome:** Defined backend structure and integration roadmap.

---

## 3. Define Frontend Requirements

- HTML Templates: Ensure index.html, data.html, and questions.html display required data.
- Styling: Confirm styles.css covers layout and UI elements.
- Navigation: Verify seamless linking between pages.

**Outcome:** Frontend structure aligned with backend needs.

---

## 4. Implement Backend Logic

- Load Data: Read autoscout24_data.csv into a pandas DataFrame.
- Define Routes:  
    / → index.html  
    /data → data.html  
    /questions → questions.html  
- API Integration: Handle OpenAI queries (POST/GET requests).
- Testing: Validate functionality using a browser or Postman.

**Outcome:** Fully functional backend with necessary logic.

---

## 5. Connect Frontend to Backend

- Template Variables: Pass data from Flask to HTML.
- Visuals: Generate and store charts in static/.
- User Input: Display API responses in index.html.

**Outcome:** Seamless frontend-backend integration.

---

## 6. Prepare for Deployment

- Procfile: Ensure it correctly references web: gunicorn app:app.
- Dependencies: Verify requirements.txt includes all required packages.
- Environment Variables: Secure API keys.
- Static Files: Ensure proper handling in production.

**Outcome:** Deployment-ready project.

---

## 7. Final Testing & Iteration

- Dev Container: Run in GitHub Codespaces to confirm environment consistency.
- Deployment Testing: Push to hosting and verify routes, data, and API calls.
- Feedback & Iteration: Optimize based on user testing.

**Outcome:** A deployed, fully tested application.

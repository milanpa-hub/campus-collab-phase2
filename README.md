# misy350-final-project-app

## Campus Collab Phase 2

This project is a Phase 2 refactor of Campus Collab. It includes:
- login, registration, and logout
- two roles: Host and Contributor
- JSON persistence
- role-based dashboards
- CRUD functionality
- refactored code structure using models, data layer, services, and UI files
- OpenAI assistant support for both roles

## Test Accounts
- Host: host@udel.edu / host123
- Contributor: student@udel.edu / student123

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## AI Setup
Create `.streamlit/secrets.toml` and add your OpenAI key:
```toml
OPENAI_API_KEY = "your-key-here"
```

## Local Setup Notes
This project uses Streamlit for the application interface.  Some features may require a local `.streamlit/secrets.toml` file with API Keys that are not included in the Github Repository for security reasons. 

## Drop Down Menu AI

## Technologies Used

- Python
- Streamlit
- GitHub
- VS Code


import os

# Define the directory and file structure
structure = {
    "project-root": {
        "app.py": "# Main application file\n",
        "config.py": "# Configuration file for Flask and Azure SQL connection\n",
        "requirements.txt": "# Dependencies\n",
        "templates": {
            "index.html": "<!-- Main page after login -->\n",
            "login.html": "<!-- Login page -->\n",
            "register.html": "<!-- Registration page -->\n",
            "forgot_password.html": "<!-- Forgot password page -->\n",
            "reset_password.html": "<!-- Password reset form -->\n"
        },
        "static": {
            "css": {
                "styles.css": "/* Main CSS file */\n"
            }
        },
        "utils": {
            "db_utils.py": "# Database utility functions\n",
            "email_utils.py": "# Email sending logic\n"
        }
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Create directory and recurse
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # Create file and write content
            with open(path, 'w') as f:
                f.write(content)

if __name__ == "__main__":
    create_structure(".", structure)

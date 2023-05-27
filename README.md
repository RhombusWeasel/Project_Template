# Project_Template

# User Authentication and Management Application

This project is a full-stack web application template that handles user authentication and management.
Built using React.js, Flask, SQLite, and other technologies.

## Getting Started

Follow the instructions below to setup the project on your local machine. Each time you call the setup script, a new project will be created in the projects directory. The setup script will create a React project with the requirements, a python virtual environment, install the required Python packages, and create a SQLite database for the user login data.
You can then navigate to the new project directory and call the launch script to start the application and the backend server.

### Prerequisites

- Node.js
- Python 3
- Flask

### Installing

1. Create a folder in your home directory called `projects`.

   ```bash
   mkdir ~/projects; cd ~/projects
   ```

2. Clone the repository.

   ```bash
   git clone git@github.com:RhombusWeasel/Project_Template.git
   ```

3. Copy the flask config.ini.example file to config.ini.

   ```bash
   cp Project_Template/flask/config.ini.example Project_Template/flask/config.ini
   ```

4. Run the setup script from the projects directory.

   ```bash
   ./Project_Template/setup.sh project_name
   ```

5. Run the application.

   ```bash
   ./project_name/launch.sh
   ```

## Features

- User registration and login.
- Permission-based access control.
- Account lockout mechanism.
- Password reset functionality.
- User profile management.
- Javascript interface from the web console.

##

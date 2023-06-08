# Project_Template

# User Authentication and Management Application

This project is a full-stack web application template that handles user authentication and management.
Built using React.js, Flask, SQLite, and other technologies, it is designed to get a simple AI application up and running.

## Getting Started

Follow the instructions below to setup the project on your local machine. Each time you call the setup script, a new project will be created in the projects directory. The setup script will create a React project with the requirements, a python virtual environment, install the required Python packages, and create a SQLite database for the user login data.
You can then navigate to the new project directory and call the launch script to start the application and the backend server.

### Prerequisites

- Node.js
- Python 3.8 -> 3.10 (Tested other versions may work as well but not guaranteed)
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

## Usage

Once you have the application running, you can navigate to the web console at http://localhost:3000. From there you can register a new user, login, and manage your profile. You can also use the Javascript interface to interact with the backend server. The Javascript interface is available through the web console, type `admin` in the console to access it.

The purpose of this project template is to quickly get started with a new web application. The project is designed to be easily modified to suit your needs. The following sections will explain how to modify the project.

### Adding New Stuff

The core project is a React application with a Flask backend. The React application is located in the `src` directory, and the Flask application is located in the `backend` directory.

- `/backend` - Contains the main Flask application.
  - `/utils` - Contains utility functions for the application. This is where you can add additional interfaces to the backend.
    - `/tree` - Contains libraries for handling AI powered behaviour trees.
      - `/behaviours` - Contains the behaviours that can be used in the behaviour trees. You can add additional behaviours here.
      - `/composites` - Contains the composite nodes that can be used in the behaviour trees. You can add additional composite nodes here.
      - `/decorators` - Contains the decorator nodes that can be used in the behaviour trees. You can add additional decorator nodes here.
      - `sub_assemblies` - Create sub-assemblies that can be used in the behaviour trees.
- `/src` - Contains the React application.
  - `/templates` - Contains folders for various page/form templates
    - `/forms` - Contains forms for user registration, login, and profile management. Edit these to suit your application if needed.
    - `/pages` - Contains the main pages for the application. Edit these to suit your application if needed.
      - `/admin_page` - Contains the Jsx and css for the Admin page.
      - `/landing_page` - Contains the Jsx and css for the Landing page.
      - `/user_home` - Contains the Jsx and css for the logged in Home page.
    - `/reuseable` - Contains reuseable components that can be used in multiple pages. Edit these to suit your application if needed.
  - `/utils` - Contains utility functions for the application. This is where you can add additional interfaces to the backend.
    - `admin.jsx` - Contains the interface for the Javascript console. Add additional functions here to expose them to the console.

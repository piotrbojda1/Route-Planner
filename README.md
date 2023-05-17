# Route-Planner

Welcome to your road trip planner. To select a travel route, you must create a user account and then you will have permission to use the planner. After logging in, the user is redirected to a page with a form, where he selects the starting location, then the destination location, departure time and avoidance parameters using checkboxes. After correctly completing the travel details, confirm with the Plan your travel button and then your route will be displayed along with the planned travel time and selected parameters. I wish you a pleasant use of the application.

## Setup & Installation

Make sure you have the latest version of Python installed.

```bash
git clone https://github.com/piotrbojda1/Route-Planner.git
```

Create your virtual environment

```bash
python -m venv env
```
or
```bash
python3 -m venv env
```

Activating your virtual environment

on Windows:

```bash
env\Scripts\activate
```

on MacOS:

```bash
source venv/bin/activate on MacOS
```

Now install all needed packages

```bash
pip install -r requirements.txt
```

## Adding API KEY

To obtain an API key, create an account at https://developer.tomtom.com/. Then go to the dashboard in your user account. After copying the key, proceed to the instructions for adding the key to environment variables.

## Adding enviroments variables

To add environment variables like API key which is required create ".env" file in root folder. In this file, create a key-value pair as in the example

```bash
API_KEY="here_enter_your_api_key"
```

## Running The App

```bash
python main.py
```

## Viewing The App

Go to `http://127.0.0.1:5000`
# Running the Student API

Run these commands from the project folder (`C:\Users\AIML-LAB1-33\Desktop\env`) in PowerShell.

## Set up the environment

If the virtual environment is not already active:

```powershell
.\myenv1\Scripts\Activate.ps1
```

Install the app dependencies:

```powershell
py -m pip install -r requirements.txt
```

## Run locally

Start Flask's built-in development server:

```powershell
py app.py
```

The API is available at `http://127.0.0.1:5000`. For example, open `http://127.0.0.1:5000/students` to list students. Keep the terminal open while the server is running. Press `Ctrl+C` in that terminal to stop it.

## Run with Waitress

For a WSGI server instead of Flask's development server, install Waitress once in the active environment:

```powershell
py -m pip install waitress
```

Then start the API with:

```powershell
waitress-serve --listen=127.0.0.1:5000 app:app
```

The server is available at `http://127.0.0.1:5000`. Stop it with `Ctrl+C` in the terminal where it is running.

Student records are kept in memory, so they reset when the server process stops.

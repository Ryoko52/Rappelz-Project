# Flask Web Application

A simple Flask web application template with HTML/CSS frontend.

## Project Structure

```
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── routes.py             # Application routes
│   ├── templates/            # HTML templates
│   │   ├── index.html        # Home page
│   │   └── about.html        # About page
│   └── static/               # Static files
│       ├── css/
│       │   └── style.css     # Stylesheet
│       └── js/
│           └── script.js     # JavaScript
├── config.py                 # Configuration settings
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Requirements

- Python 3.7+
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd RappelzProject
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Ensure the virtual environment is activated:**
   ```bash
   venv\Scripts\activate
   ```

2. **Run the development server:**
   ```bash
   python run.py
   ```

3. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:5000
   ```

## Features

- Clean and modular Flask application structure
- Responsive HTML/CSS templates
- Blueprint-based routing system
- Configuration management for different environments
- Static files management (CSS, JavaScript)

## Development

### Adding New Routes

Edit `app/routes.py` and add new routes to the `main_bp` blueprint:

```python
@main_bp.route('/new-route')
def new_route():
    return render_template('new_template.html')
```

### Adding New Templates

Create new HTML files in `app/templates/` and reference them in your routes.

### Styling

Add CSS rules to `app/static/css/style.css` or create new CSS files in the static directory.

## Configuration

Configure your application by editing `config.py` for different environments (development, production, testing).

## Troubleshooting

- **Port 5000 already in use:** Change the port in `run.py`
- **Module not found errors:** Ensure all dependencies are installed with `pip install -r requirements.txt`
- **Template not found:** Verify template files are in `app/templates/`

## Future Enhancements

- Database integration (SQLAlchemy)
- User authentication
- API endpoints
- Testing framework
- Docker support

## License

This project is open source and available under the MIT License.

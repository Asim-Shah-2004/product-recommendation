# Flask Base Application

A modern, responsive Flask web application with Bootstrap 5 styling and a clean project structure.

## Features

- ✅ Flask web framework
- ✅ Bootstrap 5 for responsive design
- ✅ Template inheritance with Jinja2
- ✅ Static file serving (CSS/JS)
- ✅ Basic routing structure
- ✅ Health check API endpoint
- ✅ Modern UI with animations
- ✅ Mobile-responsive design

## Project Structure

```
baazar-recommendation/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   └── about.html        # About page
└── static/               # Static files
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── main.js       # JavaScript functionality
```

## Installation

1. **Clone or download the project**
   ```bash
   # If you have git installed
   git clone <repository-url>
   cd baazar-recommendation
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:5000`

## Available Routes

- `/` - Home page
- `/about` - About page
- `/api/health` - Health check API endpoint

## Development

### Adding New Routes

Add new routes in `app.py`:

```python
@app.route('/new-route')
def new_route():
    return render_template('new_template.html')
```

### Adding New Templates

1. Create a new HTML file in the `templates/` directory
2. Extend the base template:

```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
<!-- Your content here -->
{% endblock %}
```

### Styling

- Main styles are in `static/css/style.css`
- Bootstrap 5 is included via CDN
- Custom animations and responsive design included

### JavaScript

- Main functionality is in `static/js/main.js`
- Includes smooth scrolling, button animations, and health check functionality

## Customization

### Environment Variables

Set the `SECRET_KEY` environment variable for production:

```bash
export SECRET_KEY="your-secret-key-here"
```

### Configuration

Modify the Flask app configuration in `app.py`:

```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
```

## Production Deployment

For production deployment, consider:

1. Using a production WSGI server (Gunicorn, uWSGI)
2. Setting up a reverse proxy (Nginx)
3. Using environment variables for configuration
4. Setting `debug=False` in production

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Happy coding! 🚀** 
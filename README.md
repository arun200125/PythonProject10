# Employee Wellness & Emotion Detection System

A Flask-based web application that monitors employee wellness by detecting emotions in real-time using AI-powered facial analysis.

## Features

✅ **User Registration & Authentication** - Secure employee registration and login  
✅ **Real-time Emotion Detection** - AI analyzes facial expressions via webcam  
✅ **Live Dashboard** - View emotion metrics in real-time  
✅ **Wellness Reports** - Generate detailed emotion analysis reports  
✅ **Employee Profiles** - Store and manage employee health metrics  
✅ **Password Security** - Bcrypt-encrypted password storage  

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Bcrypt
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **AI/ML**: DeepFace (Emotion Detection)
- **Video Processing**: OpenCV

## Prerequisites

- Python 3.8+
- Webcam (required for emotion detection)
- Windows, macOS, or Linux

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/arun200125/PythonProject10.git
cd PythonProject10
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

The app will start at `http://localhost:5000`

## Usage

1. **Register**: Create a new employee account with your details
2. **Login**: Sign in with your registered email and password
3. **Dashboard**: Access the wellness dashboard
4. **Start Camera**: Click "Start Camera" to begin emotion detection
5. **View Emotions**: Monitor real-time emotion metrics
6. **Generate Report**: Click "Generate Report" to view session summary
7. **Logout**: Safely logout from your account

## Project Structure

```
PythonProject10/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── wellness.db            # SQLite database (auto-created)
├── templates/
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Main dashboard
│   └── forgot.html        # Password recovery page
└── static/                # Static files (CSS, JS, images)
```

## Database Models

### Employee Model
- **emp_id**: Unique employee identifier
- **name**: Employee name
- **email**: Unique email address
- **contact**: Contact number
- **age**: Employee age
- **height**: Height in cm
- **weight**: Weight in kg
- **password**: Hashed password

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirect to login |
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/dashboard` | GET | Main dashboard |
| `/start` | GET | Start emotion detection |
| `/stop` | GET | Stop emotion detection |
| `/video_feed` | GET | Stream camera feed |
| `/analyze` | GET | Get current emotion data |
| `/report` | GET | Generate session report |
| `/logout` | GET | User logout |
| `/forgot` | GET, POST | Password recovery |

## Emotions Detected

- Angry
- Disgust
- Fear
- Happy
- Neutral
- Sad
- Surprise

## Configuration

### Change Secret Key
Edit `app.py` line 13:
```python
app.secret_key = "your-secret-key-here"
```

### Database Location
Edit `app.py` line 16:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///path/to/wellness.db'
```

## Troubleshooting

### Webcam Not Detected
- Ensure your webcam is connected and permissions are granted
- Check if other applications are using the webcam

### DeepFace Model Download Issues
- First run downloads large AI models (~500MB)
- Ensure stable internet connection
- Models are cached after first download

### Port Already in Use
```bash
# Change port in app.py line 210:
app.run(debug=True, port=5001)
```

## Security Notes

⚠️ **Production Deployment**:
- Change the default secret key
- Use environment variables for sensitive data
- Enable HTTPS
- Set `debug=False` in production
- Use a production WSGI server (Gunicorn, uWSGI)

## Future Enhancements

- Real-time emotion graphs and charts
- Multi-user concurrent sessions
- Email notifications
- Emotion-based wellness recommendations
- Mobile app support
- Advanced analytics and trend analysis

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is open-source and available for educational purposes.

## Support

For issues or questions, please open an issue on the GitHub repository.

---

**Created by**: arun200125  
**Project ID**: PythonProject10  
**Last Updated**: 2026-05-13

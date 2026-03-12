# URL Shortener

A simple web application that converts long URLs into short links and tracks how many times each link is used.

## Features

- Shorten long URLs
- Automatic short code generation
- Redirect users to the original URL
- Track link click counts
- View all stored links in a dashboard
- Delete links from the dashboard

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS

## Project Structure

url-shortener  
│  
├── app.py  
├── requirements.txt  
├── static/  
│   └── style.css  
└── templates/  
    ├── index.html  
    └── links.html  


## Running the Project

Install dependencies:

```
pip install flask
```

Run the application:

```
python app.py
```

Open in your browser:

```
http://127.0.0.1:5000
```


## Future Improvements

- Custom short URLs
- Expiring links
- User authentication


## License

This project is shared for educational and portfolio purposes.  
Please do not reuse or redistribute the code without permission.

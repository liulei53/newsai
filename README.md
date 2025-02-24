
# Financial News Analysis with AI

This project scrapes financial news, uses AI to analyze it, and generates actionable trading suggestions. The analysis is based on the news sentiment, and the results are presented in an easy-to-understand format for users. Additionally, the project integrates with MongoDB to store and manage the data.

## Features

- **Scrapes financial news**: Retrieves real-time news from various financial sources.
- **AI-based analysis**: Uses AI models to analyze the news and generate trading suggestions.
- **MongoDB integration**: Stores the analyzed news data in a MongoDB database.
- **Cron job scheduling**: News scraping and analysis happen automatically every few hours.
- **Web interface**: Results are displayed on a simple web interface using Flask.

## Prerequisites

- **Docker**: This project uses Docker to simplify setup and deployment.
- **MongoDB**: MongoDB is used as the database to store news data.
- **Python**: The project is developed using Python 3.9.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/financial-news-analysis.git
cd financial-news-analysis
```

### 2. Create a .env file 

Create a .env file in the root directory of the project and add the following environment variables:

TUSHARE_TOKEN=your_tushare_token
DEEPSEEK_API_KEY=your_deepseek_api_key
OPENAI_BASE_URL=your_openai_base_url
MONGO_URI=mongodb://mongo:27017/financial_news_db

### 3. Build and start the Docker containers

Make sure Docker and Docker Compose are installed on your machine. Then, build and start the containers using Docker Compose.

docker-compose up --build

This will build the Docker images and start the Flask application along with the MongoDB container.

### 4. Access the Web Interface

Once the containers are running, you can access the web interface at:

http://localhost:5000

### 5. Cron job for automatic news scraping

The project includes a cron job that automatically runs the news scraping script every 3 hours to keep the database updated.

API Usage

The project uses the following APIs for financial data and analysis:
	•	Tushare API: For financial market data.
	•	Deepseek API: For AI-driven analysis.
	•	OpenAI API: For natural language processing and generating insights from news articles.

Make sure you have the necessary API keys and insert them into the .env file.

Directory Structure

.
├── Dockerfile                # Dockerfile to build the app container
├── __pycache__               # Python bytecode files
├── app.py                    # Main Flask application file
├── data                      # Folder containing scraped data (results.json)
├── getheat.py                # Heatmap generation (optional)
├── getnews.py                # News scraping and analysis script
├── requirements.txt          # Python dependencies
├── static                    # Static files for the web interface (styles.css)
├── templates                 # HTML templates for Flask
│   └── index.html            # The main page template
└── .env                      # Environment variables (not uploaded to GitHub)

Contributing

Feel free to fork the project, make changes, and create pull requests. Please ensure that your contributions follow the existing code style and add necessary tests.

Steps to contribute:
	1.	Fork the repository.
	2.	Create a new branch.
	3.	Make changes or add new features.
	4.	Write tests for your changes if necessary.
	5.	Submit a pull request with a description of the changes.

License

This project is licensed under the MIT License - see the LICENSE file for details.




# Ravencoin Mining Statistics Scraper

## Overview
This project automates the scraping of mining statistics data for Ravencoin (RVN) from the 2Miners website and stores it in a Microsoft SQL Server database. The scraping process occurs every 30 seconds, providing up-to-date information on various mining metrics.

## Requirements
- Python 3.x
- Selenium
- Selenium WebDriver
- SeleniumWire
- Chrome WebDriver
- pyodbc (Python SQL Server Database Connectivity)
- Microsoft SQL Server
- Text editor or IDE (Integrated Development Environment)

## Installation
1. Install Python from the official [Python website](https://www.python.org/).
2. Install required Python packages using pip:
    ```
    pip install selenium selenium-wire webdriver-manager pyodbc
    ```
3. Install Chrome WebDriver using [ChromeDriverManager](https://pypi.org/project/webdriver-manager/):
    ```
    pip install webdriver-manager
    ```
4. Ensure access to a Microsoft SQL Server database.
5. Download or clone this repository to your local machine.

## Configuration
1. Ensure the Chrome WebDriver is installed or modify the `configure_driver` function in `main.py` to point to the WebDriver location.
2. Adjust the XPath variables in `settings.py` to match the expressions of the data you want to scrape from the mining statistics page.
3. Update the connection string in `main.py` to connect to your SQL Server database.

## Usage
1. Run `main.py` to start scraping data and storing it in the SQL Server database:
    ```
    python main.py
    ```
2. The script continuously refreshes the mining statistics page, scrapes the required data, and stores it in the database every 30 seconds.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request to contribute to this project.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgements
- This project was created using Python and Selenium.
- Thanks to the developers of Selenium, SeleniumWire, and pyodbc for their valuable contributions.
- Special thanks to the community for their support and feedback.

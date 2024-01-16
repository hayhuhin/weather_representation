# Weather Application

![Weather App Logo](path/to/your/logo.png)

## Overview
This is my small weather web application that have the data from two different API's.
The primary goal of the Weather Comparison Web Application is to empower users with a seamless and intuitive tool for comparing weather data from two distinct sources. By showcasing temperature, chance of rain, and feels-like temperature, web application data insures you that the data sometimes can be not so accurate.

## Table of Contents

- [Usage](#usage)
- [Installation](#installation)
- [Features](#features)
- [Screenshots](#screenshots)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Usage
#### Clients
simple weather application that shows data of two different weather apis and the client can see the differences.

#### Developers
code structure that easy to understand and refactor or integrate new api.
can be integrated with different weather API's just by creating a interface api class in the api_folder.py and then instantiate the api interface in the api adapter and api_facade.

## Installation

for installing the application and using it with the current applications you will have to create accounts in couple of websites(payment not needed!) and save the key of each api in 
the local envrinment:<br>
- weatherapi.com : this is one of the API's the application is using to get the data.
- open-meteo.com : this is one of the API's the application is using to get the data.
- ipgeolocation.com : this is needed to get the geolocation of the user's ip address to show the weather information by the location
  second 
  third

```bash
# Example installation command
pip install -r requirments.txt
```
in the weather.py change the app.debug mode to False
```python
if __name__ == "__main__":
    app.secret_key = os.getenv('SECRET_FLASK_KEY')
    app.debug = False
    app.run()
```

### use the current API's
create an account in open-emeteo.com and get the key
create an account in weatherapi.com and save the key

navigate to env folder and then create the .env file
paste the keys into the folder :
```.env
OPENMETEO_URI = "https://api.open-meteo.com/v1/forecast"
OPENMETEO_KEY = "no key"
OPENMETEO_SOURCE = "openmateo_api"
GEO_API_KEY = "asdfghjjklqwertyuioozxcvvbnm"


```



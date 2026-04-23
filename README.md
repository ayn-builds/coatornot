# 🧥 CoatOrNot

A Claude Code plugin that tells you exactly what to wear based on 
real-time weather. Never leave home underdressed again!

## What it does
- 🧥 Tells you if you need a coat or not
- ☂️ Tells you if you need an umbrella
- 👗 Gives you a full outfit suggestion
- 🌡️ Shows temperature in both °C and °F
- 💧 Humidity and wind speed
- ☁️ Current weather conditions

## Installation

Install from the Claude Code marketplace:
/plugin install coatornot@claude-plugins-official

## Setup

1. Get a free API key from openweathermap.org
2. Add it to your .env file:
OPENWEATHER_API_KEY=your-key-here

## Usage

/coatornot London
/coatornot New York
/coatornot Tokyo

## Example Output

🧥 CoatOrNot — New York

🌡️ Temperature: 8°C / 46°F
💧 Humidity: 65%
💨 Wind: 14 km/h
☁️ Conditions: Overcast clouds

🧥 Coat? Yes, definitely wear a coat! 🧥 It's cold out there.
☂️ Umbrella? No umbrella needed today! ☀️
👗 Outfit: Warm coat, sweater, jeans and closed shoes.

## Requirements
- Claude Code
- OpenWeatherMap API key (free)
- Python 3.8+

## License
MIT License — see LICENSE file for details.

## Author
Built by Ayn (https://github.com/ayn-builds)

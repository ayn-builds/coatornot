import httpx
import os
import json
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Server("coatornot")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather",
            description="Get current weather and outfit suggestions for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name e.g. London"
                    }
                },
                "required": ["city"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    city = arguments["city"]
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        })
        data = response.json()

        temp_c = data["main"]["temp"]
        temp_f = round((temp_c * 9/5) + 32, 1)
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        conditions = data["weather"][0]["description"]
        rain = "rain" in conditions.lower() or "drizzle" in conditions.lower()

        # Coat recommendation
        if temp_c < 10:
            coat = "Yes, definitely wear a coat! 🧥 It's cold out there."
        elif temp_c < 16:
            coat = "A light jacket would be smart. 🧣"
        else:
            coat = "No coat needed! 😎 Enjoy the warmth."

        # Umbrella recommendation
        umbrella = "Yes, carry an umbrella! ☂️" if rain else "No umbrella needed today! ☀️"

        # Outfit suggestion
        if temp_c < 5:
            outfit = "Heavy winter coat, thermal layers, boots and gloves."
        elif temp_c < 10:
            outfit = "Warm coat, sweater, jeans and closed shoes."
        elif temp_c < 16:
            outfit = "Light jacket or hoodie with jeans."
        elif temp_c < 22:
            outfit = "T-shirt with a light layer, comfortable trousers."
        else:
            outfit = "Light clothes, shorts or summer dress — it's warm!"

        result = {
            "city": city,
            "temperature_c": temp_c,
            "temperature_f": temp_f,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "conditions": conditions,
            "coat_needed": coat,
            "umbrella_needed": umbrella,
            "outfit_suggestion": outfit
        }
        return [TextContent(type="text", text=json.dumps(result))]

async def main():
    async with stdio_server() as streams:
        await app.run(*streams, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

import httpx
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

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
        # Step 1 — Convert city to coordinates
        geo = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}
        )
        geo_data = geo.json()
        
        if not geo_data.get("results"):
            return [TextContent(type="text", text=json.dumps({
                "error": f"City '{city}' not found. Please check the spelling."
            }))]
        
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        city_name = geo_data["results"][0]["name"]
        country = geo_data["results"][0]["country"]

        # Step 2 — Get weather from Open-Meteo
        weather = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,weather_code",
                "temperature_unit": "celsius"
            }
        )
        w = weather.json()["current"]

        temp_c = w["temperature_2m"]
        temp_f = round((temp_c * 9/5) + 32, 1)
        humidity = w["relative_humidity_2m"]
        wind_speed = w["wind_speed_10m"]
        rain = w["precipitation"] > 0

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
            "city": f"{city_name}, {country}",
            "temperature_c": temp_c,
            "temperature_f": temp_f,
            "humidity": humidity,
            "wind_speed": wind_speed,
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

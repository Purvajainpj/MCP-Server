#!/usr/bin/env python3
"""
FastMCP Weather Server - Get current weather for any city
Fixed version with proper configuration
"""
from fastmcp import FastMCP

# Create FastMCP instance
mcp = FastMCP("Weather Server")

@mcp.tool()
async def get_weather(city: str) -> str:
    """
    Get current weather conditions for any city.
    
    Args:
        city: City name (e.g., 'London', 'New York', 'Tokyo')
    
    Returns:
        Current weather information including temperature, conditions, humidity, and wind
    """
    import traceback
    
    try:
        print(f" DEBUG: Starting weather request for {city}")
        
        # Test 1: Check if aiohttp is available
        try:
            import aiohttp
            print(" DEBUG: aiohttp imported successfully")
        except ImportError as e:
            error_msg = f" aiohttp import failed: {e}"
            print(error_msg)
            return error_msg
        
        # Test 2: Create URL
        url = f"https://wttr.in/{city}?format=j1"
        print(f" DEBUG: URL created: {url}")
        
        # Test 3: Make HTTP request
        print(" DEBUG: Creating aiohttp session...")
        async with aiohttp.ClientSession() as session:
            print(" DEBUG: Making HTTP request...")
            
            async with session.get(url, timeout=10) as response:
                print(f" DEBUG: Response status: {response.status}")
                print(f" DEBUG: Response headers: {dict(response.headers)}")
                
                if response.status == 200:
                    print(" DEBUG: Parsing JSON...")
                    data = await response.json()
                    print(f" DEBUG: JSON keys: {list(data.keys())}")
                    
                    if 'current_condition' in data:
                        current = data['current_condition'][0]
                        print(f" DEBUG: Current weather keys: {list(current.keys())}")
                        
                        # Extract data safely
                        temp_c = current.get('temp_C', 'N/A')
                        temp_f = current.get('temp_F', 'N/A')
                        condition = current.get('weatherDesc', [{}])[0].get('value', 'N/A')
                        wind = current.get('windspeedKmph', 'N/A')
                        humidity = current.get('humidity', 'N/A')
                        feels_c = current.get('FeelsLikeC', 'N/A')
                        feels_f = current.get('FeelsLikeF', 'N/A')
                        
                        result = f"""Weather for {city}:
                                    Temperature: {temp_c}°C ({temp_f}°F)
                                    Condition: {condition}
                                    Wind: {wind} km/h
                                    Humidity: {humidity}%
                                    Feels like: {feels_c}°C ({feels_f}°F)"""
                        
                        print(" DEBUG: Weather data formatted successfully")
                        return result
                    else:
                        error_msg = f" No current_condition in response. Keys: {list(data.keys())}"
                        print(error_msg)
                        return error_msg
                else:
                    # Get response text for debugging
                    response_text = await response.text()
                    error_msg = f" HTTP {response.status}: {response_text[:200]}"
                    print(error_msg)
                    return error_msg
                    
    except aiohttp.ClientError as e:
        error_msg = f" Network error: {str(e)}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f" Unexpected error: {str(e)}"
        print(error_msg)
        print(f" Traceback: {traceback.format_exc()}")
        return error_msg

@mcp.tool()
async def test_tool() -> str:
    """Simple test tool to verify server is working"""
    #logger.info("Test tool called")
    return "✅ Test successful! Server is working properly."

if __name__ == "__main__":
    mcp.run(transport="sse")

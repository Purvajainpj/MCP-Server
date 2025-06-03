#!/usr/bin/env python3
"""
FastMCP Weather Server - Get current weather for any city
Modified for remote hosting (Azure Web App, VM, etc.)
Uses wttr.in free weather API (no key required)
"""

import asyncio
import aiohttp
import logging
import os
from typing import List, Dict
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    try:
        # Using wttr.in - free weather API, no key required
        url = f"https://wttr.in/{city}?format=j1"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data['current_condition'][0]
                    
                    result = f"""Weather for {city}:
🌡️  Temperature: {current['temp_C']}°C ({current['temp_F']}°F)
🌤️  Condition: {current['weatherDesc'][0]['value']}
💨 Wind: {current['windspeedKmph']} km/h
💧 Humidity: {current['humidity']}%
🌡️  Feels like: {current['FeelsLikeC']}°C ({current['FeelsLikeF']}°F)"""
                    
                    return result
                else:
                    return f'Weather service unavailable (status: {response.status})'
                    
    except Exception as e:
        return f'Failed to get weather for {city}: {str(e)}'

if __name__ == "__main__":
    # For remote hosting, use HTTP server instead of stdio
    # Get port from environment variable (Azure Web Apps use PORT)
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting MCP server on {host}:{port}")
    
    # Run as HTTP server for remote access
    mcp.run_server(host=host, port=port)
 
 

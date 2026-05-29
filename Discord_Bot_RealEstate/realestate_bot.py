import os
import discord
from discord.ext import commands
import requests
import json
import asyncio

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "redacted")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

ZILLOW_API_URL = "https://www.zillow.com/async-create-search-page-state"
HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

def get_zillow_properties(count):
    """
    Fetches a list of distressed properties from Zillow's unofficial API.
    Returns a list of property dictionaries.
    """
    payload = {
        "searchQueryState": {
            "mapBounds": {
                "north": 32.514187,
                "south": 31.426075,
                "east": -110.447318,
                "west": -113.334105
            },
            "filterState": {
                "sortSelection": {
                    "value": "globalrelevanceex"
                },
                "keywords": {
                    "value": "probate,estate,auction,trustee sale,pre-foreclosure,foreclosure pending,REO,bank foreclosure,HUD owned,government owned,divorce,liquidation,receivership,bankruptcy,distressed,short sale approved,li"
                }
            },
            "usersSearchTerm": "Pima County, AZ",
            "listPriceActive": True,
            "category": "cat1",
            "regionSelection": [
                {
                    "regionId": 281,
                    "regionType": 4
                }
            ]
        },
        "wants": {
            "cat1": ["listResults"],
            "cat2": ["total"]
        },
        "requestId": 25,
        "isDebugRequest": False
    }

    try:
        response = requests.put(ZILLOW_API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        # Check if the data structure is as expected
        if 'cat1' in data and 'searchResults' in data['cat1'] and 'listResults' in data['cat1']['searchResults']:
            properties = data['cat1']['searchResults']['listResults']
            return properties[:count]
        else:
            print("Zillow API response structure is unexpected.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Zillow API: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during Zillow API call: {e}")
        return []

# --- Pima County Assessor's Office API Integration ---
ASSESSOR_API_URL_SEARCH = "https://www.asr.pima.gov/AssessorSiteData/api/get/SearchResults/"
ASSESSOR_API_URL_DETAILS = "https://www.asr.pima.gov/AssessorSiteData/api/get/parceldetails/"
ASSESSOR_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Origin': 'https://www.asr.pima.gov',
    'Referer': 'https://www.asr.pima.gov/',
    'Sec-Ch-Ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?1',
    'Sec-Ch-Ua-Platform': '"Android"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
}

def get_assessor_parcel_id(address):
    """
    Fetches parcel information for a given address from the Pima County Assessor's API.
    Returns the parcel ID or a default string if not found.
    """
    payload = {
        "search": address,
        "searchFrom": "home",
        "taxyear": 2026,
        "searchType": "addressSimple",
        "searchModel": '{"searchType":"addressSimple","search":"' + address + '","taxyear":2026}'
    }
    
    try:
        response = requests.post(ASSESSOR_API_URL_SEARCH, data=payload, headers=ASSESSOR_HEADERS)
        response.raise_for_status()
        data = response.json()
        
        if data and isinstance(data, list) and 'Parcel' in data[0]:
            return data[0]['Parcel']
        else:
            print(f"Parcel not found for address: {address}")
            return "Parcel not found"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching parcel data from Assessor's API: {e}")
        return "API Error"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Could not parse Assessor API response for {address}: {e}")
        return "Parse Error"

def get_assessor_details_from_parcel_id(parcel_id):
    """
    Fetches detailed property information from the Assessor's API using the parcel ID.
    Extracts UseCodeDesc, house SQFT, and lot size.
    """
    payload = {
        "parcel": parcel_id,
        "taxyear": 2026
    }
    
    try:
        response = requests.post(ASSESSOR_API_URL_DETAILS, json=payload, headers=ASSESSOR_HEADERS)
        response.raise_for_status()
        data = response.json()
        
        details = {
            "zoning": "N/A",
            "house_sqft": "N/A",
            "lot_size_sqft": "N/A"
        }

        # Extract zoning from the most recent valuation data
        if 'NoticedValuationData' in data and data['NoticedValuationData']:
            # Sort by tax year to get the most recent data
            sorted_data = sorted(data['NoticedValuationData'], key=lambda x: x['TaxYear'], reverse=True)
            details["zoning"] = sorted_data[0].get("UseCodeDesc", "N/A").strip()

        # Extract house square footage from residential characteristics
        if 'ResidentialChar' in data and data['ResidentialChar']:
            house_sqft = data['ResidentialChar'].get('SQFT')
            if house_sqft is not None:
                details["house_sqft"] = f"{int(house_sqft):,}"
        
        # Extract lot size from valuation area
        if 'ValuationArea' in data and data['ValuationArea']:
            lot_size_sqft = data['ValuationArea'].get('LandSqFt')
            if lot_size_sqft is not None:
                details["lot_size_sqft"] = f"{int(lot_size_sqft):,}"
        
        return details
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for parcel {parcel_id}: {e}")
        return {}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Could not parse Assessor details for parcel {parcel_id}: {e}")
        return {}

def get_avg_price_per_sqft(zip_code):
    """
    Returns the average price per square foot for a zip code from hardcoded data.
    """
    # Data is from Realtor.com, Redfin, and Rocket Homes as of July/August 2025
    real_data = {
        "85704": "$236",
        "85718": "$310",
        "85713": "$192",
        "85730": "$218",
        "85705": "$216",
        "85716": "$239",
        "85737": "$247",
        "85742": "$232",
        "85743": "$221",
        "85629": "$184",
        "85614": "$207",
        "85750": "$290"
    }
    return real_data.get(zip_code, "N/A")


# --- Discord Bot Commands ---

@bot.event
async def on_ready():
    """
    This event is called when the bot has successfully connected to Discord.
    """
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.Game(name="Finding fixer-uppers!"))

@bot.command(name='find')
async def find_properties(ctx, count: int):
    """
    A command to list a specific number of distressed properties in Pima County.
    Usage: !find <number>
    Example: !find 5
    """
    if count <= 0 or count > 10:
        await ctx.send("Please provide a number between 1 and 10 to limit the search results.")
        return

    # Hardcoded channel ID where the results should be sent
    target_channel_id = 1411106933812756540
    target_channel = bot.get_channel(target_channel_id)
    
    if not target_channel:
        await ctx.send(f"Error: Could not find channel with ID {target_channel_id}. Please check the ID and the bot's permissions.")
        return
        
    loading_message = await target_channel.send(f"Searching for {count} distressed properties in Pima County, AZ...")
    
    properties = get_zillow_properties(count)
    
    if not properties:
        await loading_message.edit(content="Sorry, I couldn't find any distressed properties at this time. Please try again later.")
        return

    await loading_message.edit(content=f"Found {len(properties)} distressed properties:")
    await asyncio.sleep(1)

    for prop in properties:
        address = prop.get("address", "Address not found")
        zip_code = prop.get("addressZipcode", "N/A")
        
        # Add a 10-second delay to respect Assessor API rate limits
        print(f"Fetching parcel info for {address}...")
        await asyncio.sleep(10)
        parcel_id = get_assessor_parcel_id(address)
        
        # Add another 10-second delay for the next Assessor API call
        print(f"Fetching detailed info for parcel {parcel_id}...")
        await asyncio.sleep(10)
        assessor_details = get_assessor_details_from_parcel_id(parcel_id)
        
        # Get average price per sqft using the updated function
        avg_price_sqft = get_avg_price_per_sqft(zip_code)

        embed = discord.Embed(
            title=f"Property: {address}",
            color=discord.Color.red() if prop.get('statusText') else discord.Color.blue()
        )
        embed.add_field(name="Zillow URL", value=prop.get("detailUrl", "N/A"), inline=False)
        embed.add_field(name="Status", value=prop.get("statusText", "N/A"), inline=True)
        embed.add_field(name="Price", value=prop.get("price", "N/A"), inline=True)
        embed.add_field(name="Beds", value=prop.get("beds", "N/A"), inline=True)
        embed.add_field(name="Baths", value=prop.get("baths", "N/A"), inline=True)
        
        # Add new fields with data from the Assessor's API
        embed.add_field(name="House Sq. Ft.", value=assessor_details.get("house_sqft", "N/A"), inline=True)
        embed.add_field(name="Lot Size", value=f"{assessor_details.get('lot_size_sqft', 'N/A')} sq. ft.", inline=True)
        embed.add_field(name="Zoning", value=assessor_details.get("zoning", "N/A"), inline=True)
        
        embed.add_field(name="Parcel ID", value=parcel_id, inline=True)
        embed.add_field(name="Avg. Price per Sq. Ft. (Zip)", value=avg_price_sqft, inline=True)
        
        embed.set_thumbnail(url=prop.get("imgSrc"))
        embed.set_footer(text="Data from Zillow and Pima County Assessor's Office.")
        await target_channel.send(embed=embed)
        await asyncio.sleep(0.5)

# Run the bot with your token.
try:
    bot.run(BOT_TOKEN)
except discord.errors.LoginFailure as e:
    print(f"Failed to log in: {e}")
    print("Please check your bot token and try again.")
    print("Ensure you have enabled the 'Message Content Intent' in your bot's settings on the Discord Developer Portal.")
    print("https://discord.com/developers/applications")
except Exception as e:
    print(f"An unknown error occurred: {e}")

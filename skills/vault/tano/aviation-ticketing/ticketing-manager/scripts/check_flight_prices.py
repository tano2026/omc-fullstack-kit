import asyncio
import json
import logging
import os
from datetime import datetime

from app.services.abtrip_client import AbtripClient
from app.services.flight_watcher import get_flight_watcher
from app.services.conversation_memory import get_memory # To ensure DB is initialized

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Telegram Bot setup (for local notifications) ---
# In a real scenario, this would likely be handled by the main app or a dedicated notification service.
# For local Hermes cron job, we'll simulate sending a message.
# You would typically use a library like `python-telegram-bot` here.
TELEGRAM_BOT_TOKEN=os.environ.get("TELEGRAM_BOT_TOKEN") # Assuming it's set in Hermes's .env
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "@Nobitan") # Default to user's chat ID

async def send_telegram_message(chat_id: str, message: str):
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN not set, cannot send Telegram message.")
        print(f"[TELEGRAM_SIMULATED] To {chat_id}: {message}") # Print to stdout for cron output
        return
    
    # In a real setup, use aiohttp or requests to call Telegram API
    # For this exercise, we'll just log and print.
    logger.info(f"Sending Telegram message to {chat_id}: {message[:100]}...")
    print(f"[TELEGRAM_MESSAGE] To {chat_id}: {message}") # Print to stdout for cron output
    # Example using requests (needs `requests` to be installed)
    # import requests
    # url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # payload = {"chat_id": chat_id, "text": message}
    # try:
    #     response = requests.post(url, json=payload)
    #     response.raise_for_status()
    #     logger.info("Telegram message sent successfully.")
    # except requests.exceptions.RequestException as e:
    #     logger.error(f"Failed to send Telegram message: {e}")

async def check_flight_prices():
    logger.info("Starting flight price check...")
    
    # Ensure memory (DB) is initialized
    get_memory()
    flight_watcher = get_flight_watcher()
    client = AbtripClient(api_base_url="https://api-abtrip.timtrungtam.com/v1") # Use real API base URL

    active_watches = flight_watcher.get_active_watches()
    logger.info("Found %d active flight watches.", len(active_watches))

    for watch in active_watches:
        watch_id = watch["watch_id"]
        session_id = watch["session_id"]
        original_flight_details = watch["original_flight_details"]
        search_params = watch["search_params"]
        target_price_threshold = watch["target_price_threshold"]
        last_checked_price = watch["last_checked_price"]

        original_price = original_flight_details.get("price_raw", original_flight_details.get("price"))
        if original_price is None:
            logger.error("Original price not found in watch %s, skipping.", watch_id)
            continue

        logger.info("Checking watch %s for %s -> %s on %s", 
                    watch_id, 
                    search_params.get("origin"), 
                    search_params.get("destination"), 
                    search_params.get("date"))

        try:
            # Perform a fresh flight search
            results = await client.search_flight(
                origin=search_params["origin"],
                destination=search_params["destination"],
                depart_date=search_params["date"],
                adults=search_params.get("adults", 1),
                children=search_params.get("children", 0),
                infants=search_params.get("infants", 0),
                cabin_class=search_params.get("cabin_class", "economy")
            )

            if not results or not results.get("Success") or not results.get("ListGroup"):
                logger.warning("No flight results found for watch %s, or API error. Message: %s", 
                               watch_id, results.get("Message", "N/A"))
                # Update last check time even if no results, to avoid re-checking too soon
                flight_watcher.update_watch_status(
                    watch_id, 
                    status="active", 
                    last_check_time=datetime.utcnow().isoformat()
                )
                continue
            
            # Find the cheapest flight in the new results
            new_cheapest_flight_price = float('inf')
            for group in results["ListGroup"]:
                for air_option in group["ListAirOption"]:
                    new_cheapest_flight_price = min(new_cheapest_flight_price, air_option["Price"])
            
            if new_cheapest_flight_price == float('inf'):
                logger.warning("Could not extract cheapest price from new results for watch %s.", watch_id)
                flight_watcher.update_watch_status(
                    watch_id, 
                    status="active", 
                    last_check_time=datetime.utcnow().isoformat()
                )
                continue

            # Calculate price reduction
            price_reduction_percentage = ((original_price - new_cheapest_flight_price) / original_price) * 100
            
            # Check if price has dropped by at least target_price_threshold and is lower than last_checked_price
            if (price_reduction_percentage >= target_price_threshold and 
                new_cheapest_flight_price < last_checked_price):
                
                message = f"🎉 **GIÁ VÉ GIẢM SỐC!** 🎉\n\n"
                message += f"Chuyến bay **{original_flight_details.get('code')}** ({original_flight_details.get('airline_name')}) từ {search_params.get('origin')} đi {search_params.get('destination')} vào ngày {search_params.get('date')} đã giảm giá!\n\n"
                message += f"Giá gốc bạn theo dõi: **{original_price:,.0f}₫**\n"
                message += f"Giá thấp nhất hiện tại: **{new_cheapest_flight_price:,.0f}₫** (giảm {price_reduction_percentage:.2f}%) 🔥\n\n"
                message += f"👉 **ĐẶT NGAY:** Bạn có thể đặt chuyến mới với giá ưu đãi này tại bot của chúng tôi."
                
                await send_telegram_message(TELEGRAM_CHAT_ID, message)

                # Update the last_checked_price to the new lowest price
                flight_watcher.update_watch_status(
                    watch_id, 
                    status="active", 
                    last_checked_price=new_cheapest_flight_price, 
                    last_check_time=datetime.utcnow().isoformat()
                )
                logger.info("Notified user about price drop for watch %s. New price: %s", watch_id, new_cheapest_flight_price)
            else:
                # Price did not meet criteria, just update check time
                flight_watcher.update_watch_status(
                    watch_id, 
                    status="active", 
                    last_check_time=datetime.utcnow().isoformat()
                )
                logger.info("No significant price change for watch %s. Current cheapest: %s", watch_id, new_cheapest_flight_price)

        except Exception as e:
            logger.error("Error checking flight prices for watch %s: %s", watch_id, e)
            flight_watcher.update_watch_status(
                watch_id, 
                status="active", 
                last_check_time=datetime.utcnow().isoformat()
            ) # Still update time to avoid constant errors

    logger.info("Flight price check completed.")

if __name__ == "__main__":
    # Ensure the database is initialized before running the check
    get_memory()
    asyncio.run(check_flight_prices())

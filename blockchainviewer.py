import asyncio
import json
import websockets


def load_config(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


async def connect(api_url, symbols):
    uri = f"{api_url}?assets={','.join(symbols)}"

    try:
        async with websockets.connect(uri) as ws:
            while True:
                message = await ws.recv()
                data = json.loads(message)

                try:
                    price = data['bitcoin']
                    print(f"Bitcoin Price: {price}")
                except KeyError as e:
                    print(f"Error: {e}. Received Data: {data}")
                # Adds a delay to avoid high resource usage.
                await asyncio.sleep(1)

    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed.")


if __name__ == "__main__":
    config = load_config("websocket_config.json")
    api_url = config.get("api_url", "wss://ws.coincap.io/prices")
    symbols = config.get("symbols", ["bitcoin"])

    try:
        asyncio.get_event_loop().run_until_complete(connect(api_url, symbols))
    except KeyboardInterrupt:
        print("WebSocket connection stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

import asyncio
import datetime

import aiofiles


async def log_to_file(data):
    async with aiofiles.open("received_data.txt", "a") as f:
        await f.write(data + "\n")


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    
    try:
        data = await reader.read(1024)
        if data:
            message = data.decode('utf-8')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[*] [{timestamp}] Received: {message}")
            await log_to_file(message)
    except Exception as e:
        print(f"[!] Error handling client {addr}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def main(host="0.0.0.0", port=9999):  # noqa: S104
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"[*] Listening on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
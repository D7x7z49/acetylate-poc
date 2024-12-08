import argparse
import asyncio
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("AsyncServer")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("server.log", maxBytes=5 * 1024 * 1024, backupCount=2)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    logger.info(f"Connection from {addr}")

    try:
        data = await reader.read(4096)
        if data:
            message = data.decode("utf-8")
            logger.info(f"[+] {message}")
    except Exception as e:
        logger.error(f"Error handling client {addr}: {e}")
    finally:
        logger.info(f"Closing connection to {addr}")
        writer.close()
        await writer.wait_closed()


async def main(port):
    host = "0.0.0.0"  # noqa: S104
    logger.info(f"Server starting on {host}:{port}")
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    logger.info(f"[*] Listening on {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Server port", required=True)
    args = parser.parse_args()

    if args.port.isdigit() and 0 < int(args.port) < 65536:
        port = int(args.port)
        asyncio.run(main(port))

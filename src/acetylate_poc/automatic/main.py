import argparse
import io
import json
from functools import wraps
from pathlib import Path

import requests
from faker import Faker
from haralyzer import HarPage, HarParser
from PIL import Image, ImageDraw, ImageFont


def text_to_image(text: str, font_path, font_size=20, padding=10, line_spacing=5):
    font = ImageFont.truetype(font_path, font_size)
    lines = text.splitlines()
    max_width = 0
    total_height = padding

    dummy_image = Image.new("RGB", (1, 1), color=(255, 255, 255))
    draw = ImageDraw.Draw(dummy_image)

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        max_width = max(max_width, width)
        total_height += height + line_spacing

    img = Image.new("RGB", (max_width + 2 * padding, total_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    y = padding
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        height = bbox[3] - bbox[1]
        draw.text((padding, y), line, font=font, fill=(0, 0, 0))
        y += height + line_spacing

    return img


def get_image_stream(img):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes


def extractor(data: list[dict], target: list[str]):
    return {item["name"]: item["value"] for item in data if item["name"] in target}


def get_requests_from_har(har_file_path: str, verify_method: str, verify_url: str) -> dict:
    target = None
    har_parser = HarParser.from_file(har_file_path)
    entries: list[dict] = har_parser.har_data["entries"]
    if len(entries) > 0:
        for entry in entries:
            method = entry.get("request").get("method")
            url = entry.get("request").get("url")
            if method == verify_method and url == verify_url:
                target = entry
                break
    else:
        raise ValueError("No requests found in the HAR file.")

    return target


def vulbox_har_upload_image(image_stream: io.BytesIO, har_path: Path | str):
    if isinstance(har_path, str):
        har_path = Path(har_path)

    target = get_requests_from_har(har_path, "POST", r"https://user.vulbox.com/api/hacker/user/image")

    url = target.get("request").get("url")
    headers = extractor(target.get("request").get("headers"), ["Authorization", "Host", "Origin", "Referer"])
    data = {"watermark": 1}
    file = {"file": ("image.png", image_stream, "image/png")}

    fake = Faker()
    headers.update(
        {
            "User-Agent": fake.user_agent(),
        }
    )

    response = requests.post(url, headers=headers, data=data, files=file, timeout=10)
    print(response.text)


if __name__ == "__main__":
    # text = "Hello, World!\nThis is a test image.\nWith multiple lines."
    # ttf = "archive\\resource\\font\\Roboto_Mono\\RobotoMono-VariableFont_wght.ttf"
    # img = text_to_image(text, font_path=ttf)
    # image_stream = get_image_stream(img)
    # vulbox_har_upload_image(image_stream, "archive\\data\\image.har")
    print("https://i.3001.net/uploads/Up_imgs/20241015-b66e869cca12a967f0f662a813b6bcbe.png!small")

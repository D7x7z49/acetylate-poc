import argparse
import csv
import io
import json
import re
from functools import wraps
from pathlib import Path
from urllib.parse import urlparse

import requests
from faker import Faker
from haralyzer import HarPage, HarParser
from PIL import Image, ImageDraw, ImageFont


class VulboxAutomatic:
    def __init__(self, authorization, referer) -> None:
        self.fake = Faker()
        self.base_headers = {
            "Authorization": authorization,
            "Host": r"user.vulbox.com",
            "Origin": r"https://user.vulbox.com",
            "Referer": referer,
            "User-Agent": self.fake.user_agent(),
        }
        self.timeout = 7

    def auto_submit_bugs(self, data: dict):
        url = r"https://user.vulbox.com/api/hacker/bugs/bugs"
        headers = self.base_headers.copy()
        response = requests.post(url, headers=headers, json=data, timeout=self.timeout)

        if response.status_code == 200:
            print(response.json())

    def upload_image(self, image_stream: io.BytesIO):
        url = r"https://user.vulbox.com/api/hacker/user/image"
        headers = self.base_headers.copy()
        data = {"watermark": 1}
        file = {"file": ("image.png", image_stream, "image/png")}
        response = requests.post(url, headers=headers, data=data, files=file, timeout=self.timeout)

        if response.status_code == 200:
            result = response.json()
            if result["code"] == 200 and result["msg"] == "success":
                return result["data"]["url"]

        return None


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


def text_to_image(
    text: str, font_path, font_size=20, padding=10, line_spacing=5, is_dark_mode=True, max_pixel_width=1500
):
    """
    将文本转换为图片，增加昼夜模式、行号显示，并基于像素宽度换行。
    """
    # 配色方案
    if is_dark_mode:
        bg_color = (40, 40, 40)  # 深色背景
        text_color = (255, 255, 255)  # 浅色文字
    else:
        bg_color = (255, 255, 255)  # 浅色背景
        text_color = (0, 0, 0)  # 深色文字

    font = ImageFont.truetype(font_path, font_size)
    lines = text.splitlines()
    total_height = padding
    max_width = 0

    dummy_image = Image.new("RGB", (1, 1), color=bg_color)
    draw = ImageDraw.Draw(dummy_image)

    formatted_lines = []

    # 对每行文本添加行号并处理基于像素宽度的换行
    for i, line in enumerate(lines, start=1):
        line_with_number = f"{i:02d}: {line}"
        words = line_with_number.split()
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]

            if width <= max_pixel_width:
                current_line = test_line
            else:
                if current_line:
                    formatted_lines.append(current_line)
                current_line = word

        if current_line:
            formatted_lines.append(current_line)

    for line in formatted_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        max_width = max(max_width, width)
        total_height += height + line_spacing

    # 创建最终图像
    img = Image.new("RGB", (max_width + 2 * padding, total_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    y = padding
    for line in formatted_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        height = bbox[3] - bbox[1]
        draw.text((padding, y), line, font=font, fill=text_color)
        y += height + line_spacing

    return img


def get_image_stream(img):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes


def extractor(data: list[dict], target: list[str]):
    return {item["name"]: item["value"] for item in data if item["name"] in target}


def read_bugs_log_iterator(log_path: Path | str, separator: str, extract: str):
    current_block = []
    extract_pattern = re.compile(extract)
    separator_pattern = re.compile(separator)
    with open(log_path, "r", encoding="utf-8") as file:
        yield file.readline().strip()

        line = file.readline()
        if not separator_pattern.match(line):
            raise ValueError("First line does not match the separator pattern.")
        key_match = extract_pattern.search(line)
        key = key_match.group(1) if key_match else None

        for line in file:
            if separator_pattern.match(line):
                yield key, "".join(current_block)
                current_block.clear()
                key_match = extract_pattern.search(line)
                key = key_match.group(1) if key_match else None
            else:
                current_block.append(line)
    if current_block:
        yield key, "".join(current_block)


def location_from_file(file_path: Path | str) -> dict:
    result = {}
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                key = row[0]
                values = row[1:]
                result[key] = values
    return result


def main():
    har = "archive\\data\\bugs.har"
    info_log = "archive\\data\\CVE-2024-4040-info-20241015-150357.log"
    ttf = "archive\\resource\\font\\Roboto_Mono\\RobotoMono-VariableFont_wght.ttf"
    separator = r"^--------\[.*\]--------\n$"
    extract = r"\[(.*?)\]"
    link_pattern = re.compile(r"https://i\.3001\.net/uploads/Up_imgs/.*?\.png!small")

    target = get_requests_from_har(har, "POST", r"https://user.vulbox.com/api/hacker/bugs/bugs")

    request_headers = extractor(target.get("request").get("headers"), ["Authorization", "Referer"])

    request_data: dict = json.loads(target.get("request").get("postData").get("text"))

    vulbox = VulboxAutomatic(request_headers.get("Authorization"), request_headers.get("Referer"))

    iterator = read_bugs_log_iterator(info_log, separator, extract)
    ip_list = []
    locations = location_from_file("archive\\data\\geo_locations.csv")
    cve = iterator.__next__()

    schedules = 0
    schedule_node = input("schedule node:")
    for key, text in iterator:
        schedules += 1
        schedule_node = int(schedule_node) if schedule_node else 0
        if schedules < schedule_node:
            continue

        print(f"[{schedules}]\t[{key}]--------")
        hostname = urlparse(key).hostname
        if hostname not in ip_list:
            ip_list.append(hostname)
        else:
            print(f"skip: {key}")
            continue

        if input("yes or no: ").strip().lower() not in ["yes", "y"]:
            continue

        request_data["bug_url"] = f"{key}{request_data['bug_url']}"

        if (location := locations.get(key)) is None:
            print(f"not find location: {key}")
            request_data["area"] = input("area: ").strip().split(" ")
        else:
            if location[0] not in ["中国", "香港", "澳门", "台湾"]:
                request_data["area"] = ["海外", "海外"]
            else:
                print(f"location: {location}")
                request_data["area"] = input("area: ").strip().split(" ")

        firm = input("name: ")
        domain = input("domain: ")
        industry = input("industry: ").strip()
        print(industry.split("/"))
        select = input("industry_category: ").strip()
        select = int(select) if select.isdigit() else 1

        if input("yes or no: ").strip().lower() not in ["yes", "y"]:
            continue

        request_data["bug_title"] = f"{firm} {cve}"
        request_data["bug_firm_name"] = firm
        request_data["domain"] = domain

        img = text_to_image(text, ttf)
        image_stream = get_image_stream(img)
        image_link = vulbox.upload_image(image_stream)
        print(f"image_link: {image_link}")

        request_data["repetition_step"] = link_pattern.sub(image_link, request_data["repetition_step"])
        request_data["industry"] = industry
        request_data["industry_category"] = industry.split("/")[select - 1]

        print(vulbox.auto_submit_bugs(request_data))


if __name__ == "__main__":
    main()

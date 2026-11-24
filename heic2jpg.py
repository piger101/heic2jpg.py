# -*- coding: utf-8 -*-
"""
HEIC 批量转 JPG 工具
用法:
    python heic2jpg.py                    # 转换当前目录下所有 HEIC
    python heic2jpg.py D:\照片            # 转换指定文件夹（含所有子目录）
    python heic2jpg.py D:\照片 -q 95      # 指定输出质量(默认90)
"""
import os
import sys
import argparse
from datetime import datetime

from PIL import Image
from pillow_heif import register_heif_opener
register_heif_opener()   # 注册后 Image.open 就能直接识别 HEIC

EXIF_TAG = 0x8769  # EXIF 信息块

def convert_one(src: str, dst: str, quality: int) -> bool:
    """转换单张图片，保留拍摄日期等 EXIF 信息"""
    try:
        with Image.open(src) as img:
            exif = img.info.get("exif")          # 提取 EXIF（拍摄时间、机型、GPS等）
            rgb = img.convert("RGB")             # HEIC 可能是 10bit/HEVC，转成通用 RGB
            if exif:
                rgb.save(dst, "JPEG", quality=quality, exif=exif)
            else:
                rgb.save(dst, "JPEG", quality=quality)
        return True
    except Exception as e:
        print(f"  [失败] {os.path.basename(src)}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="HEIC 批量转 JPG")
    parser.add_argument("src", nargs="?", default=".", help="源目录，默认当前目录")
    parser.add_argument("-o", "--out", help="输出目录，默认在源目录下新建 converted_jpg")
    parser.add_argument("-q", "--quality", type=int, default=90, help="JPG 质量 1-95，默认 90")
    args = parser.parse_args()

    src_dir = os.path.abspath(args.src)
    if not os.path.isdir(src_dir):
        print(f"目录不存在: {src_dir}")
        sys.exit(1)

    out_dir = args.out or os.path.join(src_dir, "converted_jpg")
    os.makedirs(out_dir, exist_ok=True)

    heic_files = []
    for root, _, files in os.walk(src_dir):
        if os.path.abspath(root).startswith(os.path.abspath(out_dir)):
            continue                                  # 跳过输出目录，防止重复处理
        for f in files:
            if f.lower().endswith((".heic", ".heif")):
                heic_files.append(os.path.join(root, f))

    if not heic_files:
        print("没有找到任何 .heic / .heif 文件")
        sys.exit(0)

    print(f"共发现 {len(heic_files)} 张 HEIC，开始转换（质量 q={args.quality}）...\n")
    ok, fail = 0, 0
    for i, src in enumerate(heic_files, 1):
        rel = os.path.relpath(src, src_dir)
        dst = os.path.join(out_dir, os.path.splitext(rel)[0] + ".jpg")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(dst):
            print(f"  [跳过] {rel}（已存在）")
            ok += 1
            continue
        if convert_one(src, dst, args.quality):
            ok += 1
            print(f"  [{i}/{len(heic_files)}] {rel} -> JPG")
        else:
            fail += 1

    # 生成转换报告，方便核对
    report = os.path.join(out_dir, "转换报告.txt")
    with open(report, "w", encoding="utf-8") as fp:
        fp.write(f"转换时间: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
        fp.write(f"源目录: {src_dir}\n成功: {ok} 张，失败: {fail} 张\n")

    print(f"\n全部完成！成功 {ok} 张，失败 {fail} 张")
    print(f"输出目录: {out_dir}")

if __name__ == "__main__":
    main()

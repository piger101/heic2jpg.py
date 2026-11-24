# heic2jpg.py — HEIC 批量转 JPG 工具

> 专为华为/iPhone 导出的 HEIC 照片设计：递归批量转换、保留 EXIF 拍摄信息、支持断点续转。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Dependencies](https://img.shields.io/badge/依赖-pillow%20%7C%20pillow--heif-informational)

## 特性

- **递归批量转换** — 自动深入所有子目录，目录结构原样保留
- **保留 EXIF** — 拍摄时间、机型、GPS 位置信息不丢失，图库按日期排序不乱
- **断点续转** — 已转换的文件自动跳过，中途打断重跑不重复劳动
- **原文件只读** — HEIC 原图不动，输出到独立的 `converted_jpg/` 目录，安全
- **失败容错** — 单张损坏不影响其余照片，转换结束生成报告核对
- **拖拽即用** — Windows 下可配合 `.bat` 实现"文件夹拖到图标上自动转换"

### 安装依赖

```bash
pip install pillow pillow-heif
```

> `pillow-heif` 自带 HEVC 解码器（预编译轮子），无需在 Windows 上安装微软的 HEVC 扩展。
> 若安装报错，尝试：`pip install pillow-heif --only-binary :all:`

然后把 `heic2jpg.py` 下载/克隆到任意目录即可，无需其他配置。

### 基本用法

```bash
# 转换指定文件夹（含所有子目录），输出到 converted_jpg/
python heic2jpg.py "D:\手机照片"

# 指定输出质量（1-95，默认 90）
python heic2jpg.py "D:\手机照片" -q 95

# 指定输出目录（-o / -O / --out 均可）
python heic2jpg.py "D:\手机照片" -o "E:\JPG输出"

# 不带参数则转换当前目录
python heic2jpg.py
```

## 命令行参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `src` | 源目录（递归扫描） | 当前目录 `.` |
| `-o, -O, --out` | 输出目录 | 源目录下 `converted_jpg/` |
| `-q, --quality` | JPG 质量（1-95） | `90` |

## Windows 拖拽用法（可选）

新建 `heic转jpg.bat`（与 `heic2jpg.py` 放同一目录），以后把文件夹直接拖到图标上即可：

```bat
@echo off
chcp 65001 >nul
python "%~dp0heic2jpg.py" %1
pause
```


## FAQ

**Q: 转出来的 JPG 在图库里日期乱了？**
A: 不会。工具会保留 EXIF 拍摄时间，`-q` 参数也不影响 EXIF。若个别照片日期异常，多为原图本身无 EXIF（如截图）。

**Q: `-o` 报错 unrecognized arguments？**
A: 检查是否输入了其他非标准写法。本工具 `-o`、`-O`、`--out`、`--OUT` 均已支持。

**Q: pip 安装 pillow-heif 失败？**
A: 优先尝试 `pip install pillow-heif --only-binary :all:`；仍失败请先升级 pip：`pip install --upgrade pip`。

**Q: 路径含中文/空格报错？**
A: 给路径加双引号：`python heic2jpg.py "D:\我的 照片"`。

**Q: 会不会删掉或覆盖我的 HEIC 原图？**
A: 不会。原文件全程只读，转换结果写入独立的 `converted_jpg/` 目录，已有同名 JPG 会跳过。

**Q: 想要 GUI 图形界面版？**
A: 当前为命令行版，欢迎提 Issue 或 PR 贡献 tkinter 界面。

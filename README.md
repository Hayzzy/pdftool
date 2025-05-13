# 📄 All-in-One PDF Tool 🔧

This repo offers a simple **command-line PDF toolkit** to automate common PDF tasks with ease using **OCR (Optical Character Recognition)** and powerful libraries.

## ✨ Features

1. 🔄 *Auto-Rotate* PDF pages using **smart OCR** detection
2. 📂 *Split* PDF into individual pages and bundle them into a **ZIP**
3. 🧠 *Extract text* from scanned PDF pages in a ZIP using **OCR** and save as **JSON**

---

## 🛠 Prerequisites

Make sure to install all necessary libraries listed in the [`requirements.txt`](./requirements.txt) file.  
Some key Python libraries used:

- `PyMuPDF` (`fitz`)
- `Pillow`
- `pytesseract`
- `PyPDF2`
- `tqdm`
- `zipfile`, `json`, `io`, `os`

🧪 *Tesseract OCR engine* must also be installed on your system.  
> [Installation Guide for Tesseract](https://github.com/tesseract-ocr/tesseract)

---

## 💻 Usage
Install requirements.txt using the following script:

```bash
pip install -r requirements.txt
```
Just run the script and follow the menu:

```bash
python pdf_tool.py

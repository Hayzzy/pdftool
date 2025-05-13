import fitz
from PIL import Image
import pytesseract
import io
import os
import zipfile
import json
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm

def get_image_orientation(img):
    try:
        osd = pytesseract.image_to_osd(img)
        if "Orientation in degrees: 90" in osd or "Orientation in degrees: 270" in osd:
            return 'landscape'
        else:
            return 'portrait'
    except:
        return 'portrait'

def auto_rotate_smart(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    output = fitz.open()
    print(f"\n🔄 Rotating pages in {input_pdf}...\n")

    for i in tqdm(range(len(doc)), desc="Rotating", unit="page"):
        page = doc[i]
        pix = page.get_pixmap(dpi=150)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        orientation = get_image_orientation(img)

        if orientation == 'landscape':
            img = img.rotate(270, expand=True)

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_pdf = fitz.open("pdf", fitz.open("png", img_byte_arr.getvalue()).convert_to_pdf())
        output.insert_pdf(img_pdf)

    output.save(output_pdf)
    output.close()
    doc.close()
    print(f"\n✅ Final PDF saved as: {output_pdf}")

def split_pdf_to_zip(input_pdf_path, output_zip_path):
    temp_folder = "split_pages"
    os.makedirs(temp_folder, exist_ok=True)
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    print(f"\n🔄 Splitting {total_pages} pages...\n")
    page_paths = []

    for i in tqdm(range(total_pages), desc="Splitting", unit="page"):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        filename = f"page_{i+1}.pdf"
        filepath = os.path.join(temp_folder, filename)
        with open(filepath, "wb") as f:
            writer.write(f)
        page_paths.append(filepath)

    print("\n📦 Zipping pages...")
    with zipfile.ZipFile(output_zip_path, "w") as zipf:
        for file_path in page_paths:
            zipf.write(file_path, os.path.basename(file_path))

    print(f"\n✅ Created ZIP: {output_zip_path}")
    for file_path in page_paths:
        os.remove(file_path)
    os.rmdir(temp_folder)
    print("🧹 Temporary files cleaned up.")

def extract_ocr_from_zip(zip_path, output_json):
    temp_dir = "unzipped_scanned"
    os.makedirs(temp_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    files = sorted([f for f in os.listdir(temp_dir) if f.endswith(".pdf")])
    page_data = {}
    print(f"🟡 Starting OCR for {len(files)} scanned PDFs...\n")

    for idx, filename in enumerate(tqdm(files, desc="OCR", unit="file")):
        pdf_path = os.path.join(temp_dir, filename)
        doc = fitz.open(pdf_path)
        text = ""

        for page_num, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = pytesseract.image_to_string(img)
            text += ocr_text

        page_id = filename.replace(".pdf", "")
        page_data[f"Page {page_id}"] = text.strip()

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(page_data, f, indent=4, ensure_ascii=False)

    print(f"\n🎉 Done! OCR results saved to: {output_json}")

def menu():
    while True:
        print("\n--- PDF TOOL MENU ---")
        print("1. Auto-Rotate PDF Pages (Smart OCR)")
        print("2. Split PDF into Individual Pages and ZIP")
        print("3. Extract OCR Text from Zipped PDF Pages")
        print("4. Exit")

        choice = input("Select an option (1-4): ")

        if choice == '1':
            input_pdf = input("Enter input PDF filename: ")
            output_pdf = input("Enter output rotated PDF filename: ")
            auto_rotate_smart(input_pdf, output_pdf)

        elif choice == '2':
            input_pdf = input("Enter input PDF filename: ")
            output_zip = input("Enter output ZIP filename: ")
            split_pdf_to_zip(input_pdf, output_zip)

        elif choice == '3':
            zip_path = input("Enter input ZIP filename: ")
            output_json = input("Enter output JSON filename: ")
            extract_ocr_from_zip(zip_path, output_json)

        elif choice == '4':
            print("👋 Exiting.")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    menu()

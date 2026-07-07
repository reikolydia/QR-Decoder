import os
import io
import unicodedata
import tempfile
from pathlib import Path
from urllib.parse import unquote, unquote_to_bytes
from PIL import Image, ImageOps, ImageEnhance, ImageGrab
import pyrxing
import msvcrt
os.system('')
from rich.traceback import install
install(max_frames=10, extra_lines=5, word_wrap=True)
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.table import Table
from rich.align import Align
import pyperclip
import re
console = Console()
width = console.width

def code39_fix(raw_text):
    try:
        slash_shift = {
            ':': 'J',
            ';': 'K',
            '<': 'L',
            '-': 'M',
            '.': 'N',
            '/': 'O',
            '0': 'P',
            '1': 'Q',
            '2': 'R',
            '3': 'S',
            '4': 'T',
            '5': 'U',
            '6': 'V',
            '7': 'W',
            '8': 'X',
            '9': 'Y',
            '0': 'Z'
        }
    text = raw_text
    if len(text) != 8 or not text.startswith("/"):
        first_char = text[0]
        if first_char in slash_shift:
            text = "/" + slash_shift[first_char] + text[1:]
    if len(text) == 8 and text.startswith("/"):
        if re.match(r'^/[A-Z0-9+\-.]+$', text):
            return text
    except:
        return ""

def decode_image(img_path_str):
    try:
        img_path = os.path.abspath(img_path_str)
    except:
        img_path = img_path_str
    img_oath = os.path.join(tempfile.gettempdir(), "temp_clip_qr.png")
    try:
        raw_img = Image.open(img_path)
        source = "File"
    except:
        img_path.save(img_oath, format='PNG')
        raw_img = Image.open(img_oath)
        source = Clipboard"
    w,h = raw_img.size
    x3 = (w*3,h*3)
    raw_image = raw_image.resize(x3)
    try:
        proc_img = ImageOps.expand(raw_img, border=100, fill='white')
        proc_img = ImageOps.grayscale(proc_img)
        enhancer = ImageEnhance.Contrast(proc_img)
        proc_img = enhancer.enhance(3.0)
        results = pyrxing.read_barcodes(proc_img)
        proc_img.save(os.path.join(os.getcwd(), " temp_img.png"), format='PNG')

        if os.path.exists(img_oath):
            os.remove(img_oath)
        if not results:
            print(" NOTHING DETECTED!"
            return []
        else:
            print(f"\n[{len(results)}] data format{'s' if len(results) > 1 else ''} detected..")
        count = 1
        for code in results:
            kind = code.format
            if kind == 'Code39':
                data = code39_fix(code.text)
            else:
                data = code.text
            if data:
                process_img(data, source, kind, count, img_path)
            else:
                raise('error')
            count = count + 1
    except Exception as e:
        print(f"Error processing: {e}")
        return []

def decode_string(encoded_str, fromLoc):
    try:
        raw_bytes = unquote_to_bytes(encoded_str)
        decoded = raw_bytes.decode("utf-8", errors="replace")
        decode_length = len(unquote(encoded_str))
        if fromLoc = "string":
            string_table = Table(width=width-4, expand=True, show_edge=False, show_header=False)
            string_table.add_column("Type", justify='right', no_wrap=True, ratio=1)
            string_table.add_column("Value", justify='left', ratio=4)
            string_table.add_row("RAW COUNT", f"{len(encoded_str)}")
            string_table.add_row("UTF-8 COUNT", f"{decode_length}")
            string_table.add_row("RAW INPUT", f"{encoded_str}")
            string_table.add_row("UTF-8 DECODE", f"{decoded}")
            string_table_c = Align.center(string_table)
            string_panel = Panel(string_table_c, expand=True, title="[bold]String Analysis[/bold]")
            console.print(string_panel)
        char_confirm = Confirm.ask("\nProceed with individual character analysis?")
        print("")
        if char_confirm:
            CONTROL_NAMES = {
                0x00: "NULL",
                0x01: "START OF HEADING", 
                0x02: "START OF TEXT",
                0x03: "END OF TEXT",
                0x04: "END OF TRANSMISSION",
                0x05: "ENQUIRY",
                0x06: "ACKNOWLEDGE",
                0x07: "BELL",
                0x08: "BACKSPACE",
                0x09: "HORIZONTAL TABULATION",
                0x0A: "LINE FEED",
                0x0B: "VERTICAL TABULATION",
                0x0C: "FORM FEED",
                0x0D: "CARRIAGE RETURN",
                0x0E: "SHIFT OUT",
                0x0F: "SHIFT IN",
                0x10: "DATA LINK ESCAPE",
                0x11: "DEVICE CONTROL ONE",
                0x12: "DEVICE CONTROL TWO",
                0x13: "DEVICE CONTROL THREE",
                0x14: "DEVICE CONTROL FOUR",
                0x15: "NEGATIVE ACKNOWLEDGE",
                0x16: "SYNCHRONOUS IDLE",
                0x17: "END OF TRANSMISSION BLOCK",
                0x18: "CANCEL",
                0x19: "END OF MEDIUM",
                0x1A: "SUBSTITUTE",
                0x1B: "ESCAPE",
                0x1C: "FILE SEPARATOR",
                0x1D: "GROUP SEPARATOR",
                0x1E: "RECORD SEPARATOR",
                0x1F: "UNIT SEPARATOR",
                0x7F: "DELETE"
            }
            i = 0
            for idx, ch in enumerate(decoded, 1):
                ch_bytes = ch.encode("utf-8")
                seg = raw_bytes[i:i+len(ch_bytes)]
                percent_seg = "".join(f"%{b:02X}" for b in seg)
                i += len(ch_bytes)
                dec_val = ord(ch)
                hex_val = f"{dec_val:04X}"
                oct_val = f"{dec_val:0}"
                bin_val = f"{dec_val:b}"
                name = unicodedata.name(ch, None)
                if name is None:
                    name = CONTROL_NAMES.get(dec_val, "< NO NAME >")
                char_table = Table(width=width-4, expand=True, show_edge=False, show_header=False)
                char_table.add_column("Type", justify='right', no_wrap=True, ratio=1)
                char_table.add_column("Value", justify='left', ratio=4)
                char_table.add_row("%", f"{percent_seg}")
                char_table.add_row("CHARACTER", f"{ch}")
                char_table.add_row("NAME", f"[U+{hex_val}] {name}")
                char_table.add_row("DEC", f"{dec_val}")
                char_table.add_row("OCT", f"{oct_val}")
                char_table.add_row("HEX", f"0x{hex_val}")
                char_table.add_row("BIN", f"{bin_val}")
                char_table_c = Align.center(char_table)
                char_panel = Panel(char_table_c,title=f"[bold]{idx}[/bold]", expand=True, padding=0)
                console.print(char_panel)
            print("")
        else:
            return
    except:
        console.print(Panel(Text(f"ERROR ANALYZING: {encoded_str}", justify='center', style='red bold'), border_style='red'))
        print(f"ERROR ANALYZING: {encoded_str}")

def process_img(final_list, source_name, kind, count, img_path=none):
    data_decoded = unquote(final_list)
    decoded_table = Table(width=width-4, expand=True, show_edge=False, show_header=False)
    decoded_table.add_column("Type", justify='right', no_wrap=True, ratio=1)
    decoded_table.add_column("Value", justify='left', ratio=5, no_wrap=True, overflow='fold')
    if source_name == 'File':
        decoded_table.add_row("File", f"{Path(img_path).name}")
        decoded_table.add_row("Location", f"{img_path}")
    decoded_table.add_row("Type", f"{kind}")
    decoded_table.add_row("Raw Length", f"{len(final_list)} characters (as red from image)")
    decoded_table.add_row("Decoded Length", f"{len(data_decoded)} characters")
    decoded_table.add_row("Raw Contents", f"{final_list}")
    decoded_table.add_row("Decoded Contents", f"{data_decoded}")
    decoded_table_c = Align.center(decoded_table)
    decoded_panel = Panel(decoded_table_c, title=f"[bold][green]Decoded Image[/green] [[cyan]{count}]/cyan]][/bold]", subtitle="[yellow italic]Copied Raw Contents to Clipboard![/yellow italic]", expand=True, padding=0)
    console.print(decoded_panel)
    pyperclip.copy(final_list)
    decode_string(final_list, "image")

def get_choice(prompt):
    print(prompt, end=" ", flush=True)
    while True:
        char = msvcrt.getch().decode('utf-8', errors='ignore').lower()
        if char == 'y':
            print('y')
            return True
        if char == 'n':
            print('n')
            return False

def main():
    clipboard_check = ImageGrab.grabclipboard()
    if isinstance(clipboard_check, Image.Image):
        w,h = clipboard_check.size
        console.print(f" \n[CLIPBOARD] Found an image: (W: {w} x H: {h} px)")
        clipboard_choice = Confirm.ask("[CLIPBOARD] Use image?")
        if clipboard_choice:
            print(f"\nDecoding clipboard..")
            decode_image(clipboard_check)
    else:
        user_input = Prompt.ask("\nEnter image path or URL-encoded strong:\n").strip('"').strip("'")
        if os.path. isfile(user_input):
            print(f"\nDecoding image..")
            results = decode_image(user_input)
            if results:
                for data in results:
                    decode_string(user_input, "string")
    if Confirm.ask("Decode next?"):
        main()

if __name__ == "__main__":
    console.print(Panel(Text("Barcode / QR code DECODER", justify='center', style='green bold'), border_style='white'))
    main()

import tkinter as tk # type: ignore
from tkinter import ttk # type: ignore
import difflib # type: ignore
from domain_dictionaries import dictionaries, basic_english_words # type: ignore

def message_box(message, bg_color = '#d9534f'):
    message_box_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3, bg = '#f5f5f5')
    close_btn = tk.Button(message_box_fm, text = "X", bd = 0, font = ('bold', 13), fg = bg_color, bg = '#f5f5f5', command = lambda: message_box_fm.destroy())
    close_btn.place(x = 291, y = 0)
    message_lb = tk.Label(message_box_fm, text = message, font = ('bold', 15), bg = '#f5f5f5', fg = '#000000')
    message_lb.pack(expand = True)
    message_box_fm.place(x = 265, y = 175, width = 320, height = 200)

def suggestions_box(message, suggestions, bg_color = '#1e88e5', text_color = '#000000'):
    suggestion_pages = [suggestions[i:i + 5] for i in range(0, len(suggestions), 5)]
    current_page = 0

    def update_suggestions_box(page):
        nonlocal current_page
        current_page = page
        if current_page < len(suggestion_pages):
            suggestion_text = "\n".join(suggestion_pages[current_page])
            message_lb.config(text = f"{message}\n\n{suggestion_text}")
            next_btn.config(text = "Next" if current_page < len(suggestion_pages) - 1 else "Close", command = lambda: message_box_fm.destroy() if current_page == len(suggestion_pages) - 1 else update_suggestions_box(current_page + 1))
    message_box_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 2, bg = '#f5f5f5')
    message_box_fm.place(x = 225, y = 150, width = 400, height = 250)
    close_btn = tk.Button(message_box_fm, text = "X", bd = 0, font = ('helvetica', 13, 'bold'), fg = bg_color, bg = '#f5f5f5', command = lambda: message_box_fm.destroy())
    close_btn.place(x = 374, y = 0)
    message_lb = tk.Label(message_box_fm, text = "", font = ('helvetica', 12, 'bold'), fg = text_color, bg = '#f5f5f5', justify = 'center', wraplength = 350)
    message_lb.pack(expand = True, pady = 20)
    next_btn = tk.Button(message_box_fm, text = "Next", font = ('helvetica', 10, 'bold'), bg = bg_color, fg = '#ffffff', command = lambda: update_suggestions_box(current_page + 1))
    next_btn.pack(pady = 10)
    update_suggestions_box(current_page)

def highlight_misspelled_words(event = None):
    text_content = text_box.get("1.0", tk.END).strip()
    words = text_content.split()
    selected_domain = domain_var.get()
    text_box.tag_remove("misspelled", "1.0", tk.END)
    if selected_domain == "Select Domain":
        return
    domain_dict = dictionaries.get(selected_domain, [])
    for word in words:
        if word.lower() not in basic_english_words and word.lower() not in domain_dict:
            start_idx = f"1.0+{text_content.find(word)}c"
            end_idx = f"{start_idx}+{len(word)}c"
            text_box.tag_add("misspelled", start_idx, end_idx)
    text_box.tag_configure("misspelled", foreground = 'red')

def check_spelling():
    selected_domain = domain_var.get()
    text_content = text_box.get("1.0", tk.END).strip()
    if selected_domain == "Select Domain" or not text_content:
        message_box("Error: Please select a domain\nand input some words.")
        return
    domain_dict = dictionaries.get(selected_domain, [])
    words = text_content.split()
    incorrect_words = [word for word in words if word.lower() not in basic_english_words and word.lower() not in domain_dict]
    if not incorrect_words:
        message_box("All words are correct!")
        return
    suggestions = {}
    for word in incorrect_words:
        similar_words = [w for w in domain_dict if difflib.SequenceMatcher(None, word.lower(), w.lower()).ratio() >= 0.7]
        suggestions[word] = similar_words if similar_words else "No match found."
    suggestion_list = [f"{word}: {', '.join(suggestions[word]) if isinstance(suggestions[word], list) else suggestions[word]}" for word in incorrect_words]
    suggestions_box("Suggestions:", suggestion_list, bg_color = '#f0ad4e')

root = tk.Tk()
root.title("Domain-Specific Spell Checker Tool | Mahesh Kakde")
root.geometry('850x650')
root.configure(bg = '#f1f3f4')
root.resizable(False, False)

header_frame = tk.Frame(root, bg = '#004d99')
header_frame.pack(fill = 'x', pady = 5)
header_label = tk.Label(header_frame, text = "Domain-Specific Spell Checker Tool", font = ('helvetica', 20, 'bold'), bg = '#004d99', fg = '#ffffff')
header_label.pack(pady = 15)

domain_frame = ttk.Frame(root)
domain_frame.pack(pady = 20)
ttk.Label(domain_frame, text = "Domain:", font = ('helvetica', 13)).grid(row = 0, column = 0, padx = 10, pady = 10)
domain_var = tk.StringVar()
domain_var.set("Select Domain")
domain_menu = ttk.Combobox(domain_frame, textvariable = domain_var, values = list(dictionaries.keys()), state = 'readonly', width = 25)
domain_menu.grid(row = 0, column = 1)

text_frame = tk.Frame(root, padx = 20, pady = 20, bg = '#f1f3f4')
text_frame.pack(pady = 15, fill = 'both', expand = True)
text_box = tk.Text(text_frame, wrap = 'word', width = 80, height = 15, font = ('helvetica', 13), undo = True, bg = '#ffffff', fg = '#333333', relief = 'flat', bd = 2, highlightbackground = '#004d99', highlightthickness = 1)
text_box.pack(side = 'left', fill = 'both', expand = True)
text_scroll = ttk.Scrollbar(text_frame, orient = 'vertical', command = text_box.yview)
text_scroll.pack(side = 'right', fill = 'y')
text_box['yscrollcommand'] = text_scroll.set

text_box.bind("<KeyRelease>", highlight_misspelled_words)

check_button = ttk.Button(root, text = "Check Spelling", command = check_spelling, style = "Accent.TButton")
check_button.pack(pady = 25, ipadx = 25, ipady = 8)

footer_label = tk.Label(root, text = "Developed by Mahesh Kakde", font = ('arial', 10, 'italic'))
footer_label.pack(side = 'bottom')

root.mainloop()
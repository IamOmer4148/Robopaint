import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk, ImageOps

root = tk.Tk()
root.title("Robopaint")
root.geometry("900x700")

current_color = "#000000"
bg_color = "#ffffff"
brush_size = 5
drawing = False
last_x, last_y = None, None
language = "EN"

image = Image.new("RGB", (800, 600), bg_color)
draw = ImageDraw.Draw(image)


canvas = tk.Canvas(root, bg=bg_color, width=800, height=600)
canvas.pack(pady=20)


def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")])
    if file_path:
        global image, draw
        opened_image = Image.open(file_path)
        opened_image = ImageOps.contain(opened_image, (800, 600))
        image.paste(opened_image, (0, 0))
        draw = ImageDraw.Draw(image)
        update_canvas()


def update_canvas():
    global tk_image
    tk_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=tk_image)


def set_last_pos(event):
    global drawing, last_x, last_y
    drawing = True
    last_x, last_y = event.x, event.y

def draw_line(event):
    global last_x, last_y
    if drawing:
        x, y = event.x, event.y
        canvas.create_line((last_x, last_y, x, y), fill=current_color, width=brush_size)
        draw.line((last_x, last_y, x, y), fill=current_color, width=brush_size)
        last_x, last_y = x, y

def reset_drawing(event):
    global drawing
    drawing = False


def choose_color():
    global current_color
    color = colorchooser.askcolor(title="Renk Seç", initialcolor=current_color)
    if color[1] is not None:
        current_color = color[1]


def change_bg_color():
    global bg_color, image, draw
    color = colorchooser.askcolor(title="Arka Plan Rengi Seç", initialcolor=bg_color)
    if color[1] is not None:
        bg_color = color[1]
        canvas.config(bg=bg_color)
        image = Image.new("RGB", (800, 600), bg_color)
        draw = ImageDraw.Draw(image)
        update_canvas()


def set_brush_size(size):
    global brush_size
    brush_size = size


def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                             filetypes=[("JPEG Files", "*.jpg"), ("All Files", "*.*"), ("PNG Files", "*.png")])
    if file_path:
        image.save(file_path, "JPEG")
        messagebox.showinfo(get_text("Saved"), f"{get_text('Image saved')}: {file_path}")


def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title(get_text("Settings"))
    settings_window.geometry("300x200")

    tk.Label(settings_window, text=get_text("Language Selection")).pack(pady=10)

    lang_var = tk.StringVar(value="TR")
    

    tk.Radiobutton(settings_window, text="Türkçe", variable=lang_var, value="TR", command=lambda: set_language("TR")).pack(anchor=tk.W)
    tk.Radiobutton(settings_window, text="English", variable=lang_var, value="EN", command=lambda: set_language("EN")).pack(anchor=tk.W)

    tk.Label(settings_window, text="Made by Robosan").pack(pady=20)
    tk.Label(settings_window, text="Version v0.3").pack(pady=20)

def set_language(lang):
    global language
    language = lang
    update_texts()

def get_text(key):

    texts = {
        "TR": {
            "Settings": "Ayarlar",
            "Language Selection": "Dil Seçimi",
            "Saved": "Kaydedildi",
            "Image saved": "Resim kaydedildi",
        },
        "EN": {
            "Settings": "Settings",
            "Language Selection": "Language Selection",
            "Saved": "Saved",
            "Image saved": "Image saved",
        }
    }
    return texts[language].get(key, key)

def update_texts():
    
    control_frame.children['!button'].config(text=get_text("Color Select"))
    control_frame.children['!button2'].config(text=get_text("Change Background"))
    control_frame.children['!button3'].config(text=get_text("Save"))
    control_frame.children['!button4'].config(text=get_text("Open"))
    control_frame.children['!label'].config(text=get_text("Brush Size:"))
    control_frame.children['!button5'].config(text=get_text("Small"))
    control_frame.children['!button6'].config(text=get_text("Medium"))
    control_frame.children['!button7'].config(text=get_text("Large"))
    control_frame.children['!button8'].config(text=get_text("Settings"))


control_frame = tk.Frame(root)
control_frame.pack(pady=10)

tk.Button(control_frame, text="Renk Seç", command=choose_color).grid(row=0, column=0, padx=10)
tk.Button(control_frame, text="Arka Planı Değiştir", command=change_bg_color).grid(row=0, column=1, padx=10)
tk.Button(control_frame, text="Kaydet", command=save_image).grid(row=0, column=2, padx=10)
tk.Button(control_frame, text="Aç", command=open_image).grid(row=0, column=3, padx=10)

tk.Label(control_frame, text="Fırça Boyutu:").grid(row=0, column=4, padx=10)
tk.Button(control_frame, text="Küçük", command=lambda: set_brush_size(3)).grid(row=0, column=5, padx=5)
tk.Button(control_frame, text="Orta", command=lambda: set_brush_size(5)).grid(row=0, column=6, padx=5)
tk.Button(control_frame, text="Büyük", command=lambda: set_brush_size(8)).grid(row=0, column=7, padx=5)

tk.Button(control_frame, text="Ayarlar", command=open_settings).grid(row=0, column=8, padx=10)

canvas.bind("<Button-1>", set_last_pos)
canvas.bind("<B1-Motion>", draw_line)
canvas.bind("<ButtonRelease-1>", reset_drawing)

root.mainloop()


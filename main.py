import tkinter as tk
from tkinter import filedialog, colorchooser, ttk
from zoneinfo import reset_tzpath

from PIL import Image, ImageTk, ImageDraw, ImageFont
import os


# DARK VERSION
# BG_COLOR = "#252422"
# PANEL_COLOR = "#403d39"
# TEXT_COLOR = "#ccc5b9"
# SECONDARY_TEXT = "#fffcf2"
# ACCENT_COLOR = "#eb5e28"
# BORDER_COLOR = "#403d39"

# LIGHT VERSION
BG_COLOR = "#F5F5F5"
PANEL_COLOR = "#FFFFFF"
TEXT_COLOR = "#111111"
SECONDARY_TEXT = "#6B6B6B"
ACCENT_COLOR = "#b4b8ab"
BORDER_COLOR = "#DCDCDC"

img_tk = None
watermark_image = None
font_path = '/System/Library/Fonts/NewYork.ttf'
original_image = None
watermark_color = (255, 255, 255)

def open_image():
    global original_image, watermark_image
    filename = filedialog.askopenfilename()
    if not filename:
        return
    original_image = Image.open(filename)
    watermark_image = None
    display_image()
    set_status(f'Image loaded: {os.path.basename(filename)}')
    placeholder_title.place_forget()
    placeholder_subtitle.place_forget()

def choose_font():
    global font_path
    font_path = filedialog.askopenfilename()
    if not font_path:
        return
    font_label.configure(text=os.path.basename(font_path))
    update_preview()

def update_font_size(value):
    font_size_value_label.configure(text=str(int(float(value))))
    update_preview()

def update_opacity(value):
    opacity_value_label.configure(text=f'{int(float(value))}%')
    update_preview()

def choose_color():
    global watermark_color
    color = colorchooser.askcolor()
    if color[0] is None:
        return
    watermark_color = color[0]
    color_preview.configure(background=color[1])
    update_preview()

def select_position(value):
    position.set(value)
    for button in position_buttons.values():
        button.configure(style='Position.TButton')
    position_buttons[value].configure(style='Selected.Position.TButton')
    update_preview()

def update_preview():
    global watermark_image

    if original_image is None:
        return

    watermark_text = watermark_input.get()
    if not watermark_text:
        watermark_image = None
        display_image()
        return

    font_size_value = int(font_size.get())
    font = ImageFont.truetype(
        font_path,
        font_size_value
    )

    watermark_layer = Image.new('RGBA', original_image.size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(watermark_layer)

    bbox = draw.textbbox(
        (0,0),
        text=watermark_text,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    margin = 10
    selected_position = position.get()

    if selected_position == 'top_left':
        x=margin
        y=margin
    elif selected_position == 'top_right':
        x= original_image.width - text_width - margin
        y=margin
    elif selected_position == 'bottom_left':
        x=margin
        y= original_image.height - text_height - 2*margin
    elif selected_position == 'bottom_right':
        x = original_image.width - text_width - margin
        y = original_image.height - text_height - 2*margin
    else:
        x = (original_image.width - text_width) / 2
        y = (original_image.height - text_height) / 2

    selected_opacity = int(opacity.get())
    opacity_value = int(selected_opacity * 255 / 100)

    draw.text(
        (x, y),
        text=watermark_text,
        font=font,
        fill=(*watermark_color, opacity_value)
    )

    watermark_image = Image.alpha_composite(original_image.convert('RGBA'), watermark_layer)

    display_image()
    save_button.configure(state='normal' if watermark_image is not None else 'disabled')
    reset_button.configure(state='normal' if watermark_image is not None else 'disabled')
    set_status('Watermark updated')

def save():
    global watermark_image
    if watermark_image is None:
        return
    image_mark = filedialog.asksaveasfile(defaultextension='.jpg')
    if image_mark:
        watermark_image.convert('RGB').save(image_mark)
    set_status('Image saved')

def display_image():
    global img_tk
    image_to_display = watermark_image or original_image
    if image_to_display is None:
        return
    preview_width = preview_frame.winfo_width()
    preview_height = preview_frame.winfo_height()
    if preview_width <= 1 or preview_height <= 1:
        return
    img_thumbnail = image_to_display.copy()
    img_thumbnail.thumbnail((preview_width - 20, preview_height - 20))
    img_tk = ImageTk.PhotoImage(img_thumbnail)
    image_label.configure(image=img_tk)

def reset():
    global font_path, watermark_color, watermark_image
    watermark_input.delete(0, tk.END)
    font_path = '/System/Library/Fonts/NewYork.ttf'
    font_label.configure(text=os.path.basename(font_path))
    font_size.set(40)
    opacity.set(100)
    font_size_value_label.configure(text='40')
    opacity_value_label.configure(text='100%')
    watermark_color = (255, 255, 255)
    color_preview.configure(background='#FFFFFF')
    select_position('bottom_right')
    watermark_image = None
    display_image()
    save_button.configure(state='disabled')
    set_status('Reset')

def set_status(message):
    status_text.set(f'●  {message}')


root = tk.Tk()
root.title("Watermarker")
window_width = 1200
window_height = 850
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.minsize(1200, 850)
root.configure(background=BG_COLOR)
root.focus_force()

    # STYLE

style = ttk.Style()
style.theme_use('clam')
style.configure(
    'Accent.TButton',
    font=('Helvetica', 11, 'bold'),
    padding=(20, 10),
    foreground=TEXT_COLOR,
    background=ACCENT_COLOR
)
style.configure(
    'Secondary.TButton',
    font=('Helvetica', 10),
    padding=(15, 8),
    foreground=TEXT_COLOR,
    background=PANEL_COLOR
)

style.configure(
    'Dark.TEntry',
    fieldbackground=PANEL_COLOR,
    foreground=TEXT_COLOR,
    insertcolor=TEXT_COLOR,
    borderwidth=0,
    padding=8
)

style.configure(
    'Dark.TButton',
    font=('Helvetica', 10, 'bold'),
    foreground=TEXT_COLOR,
    background=ACCENT_COLOR,
    padding=(15,8),
    borderwidth=0,
)
style.configure(
    'Title.TLabel',
    font=('Helvetica', 10, 'bold'),
    foreground=TEXT_COLOR,
    background=PANEL_COLOR,
)
style.configure(
    'Text.TLabel',
    font=('Helvetica', 9),
    foreground=SECONDARY_TEXT,
    background=PANEL_COLOR,
)
style.configure(
    'Value.TLabel',
    font=('Helvetica', 9, 'bold'),
    foreground=TEXT_COLOR,
    background=PANEL_COLOR,
)
style.configure(
    'Info.TLabel',
    font=('Helvetica', 9),
    foreground=SECONDARY_TEXT,
    background=PANEL_COLOR,
)
style.configure(
    'Dark.Horizontal.TScale',
    background=PANEL_COLOR,
    troughcolor=BORDER_COLOR,
)
style.configure(
    'Preview.TLabel',
    font=('Helvetica', 14),
    background=BG_COLOR,
    foreground=SECONDARY_TEXT
)
style.configure(
    'Position.TButton',
    font=('Helvetica', 9, 'bold'),
    foreground=TEXT_COLOR,
    background=PANEL_COLOR,
    padding=8
)
style.configure(
    'Selected.Position.TButton',
    font=('Helvetica', 9, 'bold'),
    foreground=TEXT_COLOR,
    background=ACCENT_COLOR,
    padding=8
)
style.configure(
    'Status.TLabel',
    font=('Helvetica', 9),
    foreground=SECONDARY_TEXT,
    background=PANEL_COLOR,
)

    # HEADER

header_frame = tk.Frame(root, background=BG_COLOR)
header_frame.pack(fill='x')

title_label = tk.Label(
    header_frame,
    text='W A T E R M A R K E R',
    font=("Didot", 30),
    background=BG_COLOR,
    foreground=TEXT_COLOR
)
title_label.pack(pady=(20,0))

subtitle_label = tk.Label(
    header_frame,
    text='Add your signature to any image',
    font=('Helvetica', 11),
    background=BG_COLOR,
    foreground=SECONDARY_TEXT
)
subtitle_label.pack(pady=(0, 20))

    # MAIN

main_frame = tk.Frame(root, background=BG_COLOR)
main_frame.pack(fill='both', expand=True)

preview_frame = tk.Frame(main_frame, background=BG_COLOR)
preview_frame.configure(highlightthickness=1, highlightbackground=BORDER_COLOR)
preview_frame.pack(side='left', fill='both', expand=True)
preview_frame.bind("<Configure>", lambda event: display_image())

# separator = tk.Frame(
#     main_frame,
#     width=10,
#     background=BORDER_COLOR,
# )
# separator.pack(side='left', fill='y')

controls_frame = tk.Frame(main_frame, background=PANEL_COLOR, width=320)
controls_frame.pack(side='right', fill='y')
controls_frame.pack_propagate(False)

    # PREVIEW

# image_label = ttk.Label(
#     preview_frame,
#     text='No image selected',
#     style='Preview.TLabel',
# )
# image_label.pack(expand=True)
image_label = tk.Label(
    preview_frame,
    background=BG_COLOR,
)
image_label.configure(anchor='center')
image_label.pack(fill='both', expand=True)
placeholder_title = ttk.Label(
    preview_frame,
    text='NO IMAGE SELECTED',
    font=('Helvetica', 12, 'bold'),
    foreground=TEXT_COLOR,
    background=BG_COLOR,
)
placeholder_title.place(
    relx=0.5,
    rely=0.48,
    anchor='center'
)
placeholder_subtitle = ttk.Label(
    preview_frame,
    text='Open an image to get started',
    font=('Helvetica', 9),
    foreground=SECONDARY_TEXT,
    background=BG_COLOR,
)
placeholder_subtitle.place(
    relx=0.5,
    rely=0.54,
    anchor='center'
)
    # CONTROLS

controls_title = tk.Label(
    controls_frame,
    text='WATERMARK',
    font=('Helvetica', 14, 'bold'),
    background=PANEL_COLOR,
    foreground=TEXT_COLOR
)
controls_title.pack(anchor='w', padx=20, pady=(20, 20))

text_section = tk.Frame(
    controls_frame,
    background=PANEL_COLOR,
)
text_section.pack(
    fill='x',
    padx=20,
    pady=(0,20)
)
text_label = ttk.Label(
    text_section,
    text='TEXT',
    style='Title.TLabel'
)
text_label.pack(anchor='w', pady=(0,5))
watermark_input = ttk.Entry(text_section, style='Dark.TEntry')
watermark_input.bind('<KeyRelease>', lambda event: update_preview())
watermark_input.pack(fill='x')
watermark_input.insert(0, "Your watermark text")

font_section = tk.Frame(
    controls_frame,
    background=PANEL_COLOR,
)
font_section.pack(
    fill='x',
    padx=20,
    pady=(0,20)
)
font_label_title = ttk.Label(
    font_section,
    text='FONT',
    style='Title.TLabel'
)
font_label_title.pack(anchor='w', pady=(0,5))
button_font = ttk.Button(
    font_section,
    text="CHOOSE FONT",
    command=choose_font,
    style='Dark.TButton')
button_font.pack(fill='x')
font_label = ttk.Label(
    font_section,
    text=os.path.basename(font_path),
    style='Info.TLabel'
)
font_label.pack(anchor='w', pady=(0,5))

appearance_section = tk.Frame(
    controls_frame,
    background=PANEL_COLOR,
)
appearance_section.pack(fill='x', padx=20, pady=(0,20))
appearance_title = ttk.Label(
    appearance_section,
    text="APPEARANCE",
    style='Title.TLabel'
)
appearance_title.pack(anchor='w', pady=(0,5))
font_size_row = tk.Frame(
    appearance_section,
    background=PANEL_COLOR,
)
font_size_row.pack(fill='x', pady=(0,5))
font_size_label = ttk.Label(
    font_size_row,
    text="Font Size",
    style="Text.TLabel"
)
font_size_label.pack(side='left')
font_size = tk.IntVar(value=40)

font_size_input = ttk.Scale(
    appearance_section,
    from_=10,
    to=100,
    variable=font_size,
    orient='horizontal',
    style='Dark.Horizontal.TScale',
    command=update_font_size,
)
font_size_input.pack(fill='x')
font_size_value_label = ttk.Label(
    font_size_row,
    text='40',
    style='Value.TLabel'
)
font_size_value_label.pack(side='right')

opacity_row = tk.Frame(
    appearance_section,
    background=PANEL_COLOR,
)
opacity_row.pack(fill='x', pady=(12,5))
opacity_label = ttk.Label(
    opacity_row,
    text='Opacity',
    style='Text.TLabel'
)
opacity_label.pack(side='left')

opacity = tk.IntVar(value=100)
opacity_input = ttk.Scale(
    appearance_section,
    from_=10,
    to=100,
    variable=opacity,
    orient='horizontal',
    style='Dark.Horizontal.TScale',
    command=update_opacity
)
opacity_input.pack(fill='x')
opacity_value_label = ttk.Label(
    opacity_row,
    text='100%',
    style='Value.TLabel'
)
opacity_value_label.pack(side='right')

color_section = tk.Frame(
    controls_frame,
    background=PANEL_COLOR,
)
color_section.pack(fill='x', padx=20, pady=(0,20))
color_title = ttk.Label(
    color_section,
    text="COLOR",
    style='Title.TLabel'
)
color_title.pack(anchor='w', pady=(0,5))
color_button = ttk.Button(
    color_section,
    text="CHOOSE COLOR",
    command=choose_color,
    style='Dark.TButton'
)
color_button.pack(fill='x')
color_preview = tk.Frame(
    color_section,
    background='#FFFFFF',
    height=20,
)
color_preview.pack(fill='x', pady=(5,0))

position_section = tk.Frame(
    controls_frame,
    background=PANEL_COLOR,
)
position_section.pack(fill='x', padx=20, pady=(0,20))
position_title = ttk.Label(
    position_section,
    text='POSITION',
    style='Title.TLabel'
)
position_title.pack(anchor='w', pady=(0,5))
position = tk.StringVar(value='bottom_right')
position_grid = tk.Frame(position_section, background=PANEL_COLOR)
position_grid.pack()
position_buttons = {}
positions = {
    "top_left": "↖",
    "top_right": "↗",
    "center": "●",
    "bottom_left": "↙",
    "bottom_right": "↘"
}
position_layout = [
    ("top_left", 0, 0),
    ("top_right", 0, 2),
    ("center", 1, 1),
    ("bottom_left", 2, 0),
    ("bottom_right", 2, 2)
]
for value, row, column in position_layout:
    button = ttk.Button(
        position_grid,
        text=positions[value],
        command=lambda value=value: select_position(value),
        style='Position.TButton',
        width=4
    )
    button.grid(row=row, column=column, padx=2, pady=2)
    position_buttons[value] = button
select_position(position.get())

reset_button = ttk.Button(
    position_section,
    text='RESET',
    command=reset,
    style='Dark.TButton',
    state='disabled'
)
reset_button.pack(fill='x', pady=(20,0))
    # FOOTER

footer_frame = tk.Frame(root, background=BG_COLOR)
footer_frame.pack(fill='x')

upload_button = ttk.Button(
    footer_frame,
    text='OPEN IMAGE',
    command=open_image,
    style='Secondary.TButton'
)
upload_button.pack(
    side='left',
    padx=20,
    pady=15
)

save_button = ttk.Button(
    footer_frame,
    text='SAVE IMAGE',
    command=save,
    style='Accent.TButton',
    width=34,
    state='disabled'
)
save_button.pack(side='right', padx=20, pady=15)

status_frame = tk.Frame(
    root,
    background=PANEL_COLOR,
    height=28
)
status_frame.pack(
    fill='x',
    side='bottom'
)
status_text = tk.StringVar(value='●  Ready')
status_label = ttk.Label(
    status_frame,
    textvariable=status_text,
    style='Status.TLabel'
)
status_label.pack(
    side='left',
    padx=15,
    pady=5
)

root.mainloop()
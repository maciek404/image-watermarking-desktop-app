from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

img_tk = None
watermark_image = None
font_path = '/System/Library/Fonts/NewYork.ttf'
original_image = None
watermark_color = (255, 255, 255)

def upload():
    global img_tk, original_image, watermark_image
    filename = filedialog.askopenfilename()
    if not filename:
        return
    original_image = Image.open(filename)
    watermark_image = None
    img_thumbnail = original_image.copy()
    img_thumbnail.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img_thumbnail)
    image_label.configure(image=img_tk)

def add_watermark():
    global img_tk, watermark_image, font_path, original_image, watermark_color

    if original_image is None:
        return

    watermark_text = watermark_input.get()
    if not watermark_text:
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

    img_thumbnail = watermark_image.copy()
    img_thumbnail.thumbnail((400, 400))

    img_tk = ImageTk.PhotoImage(img_thumbnail)
    image_label.configure(image=img_tk)

def save():
    global watermark_image
    if watermark_image is None:
        return
    image_mark = filedialog.asksaveasfile(defaultextension='.jpg')
    if image_mark:
        watermark_image.convert('RGB').save(image_mark)

def choose_font():
    global font_path
    font_path = filedialog.askopenfilename()
    if not font_path:
        return
    font_label.configure(text=os.path.basename(font_path))

def choose_color():
    global watermark_color
    color = colorchooser.askcolor()
    if color[0] is None:
        return
    print(color)
    watermark_color = color[0]
    color_label.configure(background=color[1])


root = Tk()
root.title("Image Watermarking")
# root.geometry("500x500")

button_upload = Button(text="Upload Image", command=upload)
button_upload.pack()
image_label = Label(root)
image_label.pack()

watermark_input = Entry(root)
watermark_input.pack()

button_font = Button(root, text="Choose Font", command=choose_font)
button_font.pack()
font_label = Label(root, text=os.path.basename(font_path))
font_label.pack()

Label(root, text='Opacity:').pack()
opacity = StringVar(value='100')

opacity_input = Spinbox(
    root,
    from_=10,
    to=100,
    width=5,
    textvariable=opacity
)
opacity_input.pack()

Label(root, text='Position:').pack()
position = StringVar()
position.set('bottom_right')
Radiobutton(root, text='Top Left', variable=position, value='top_left').pack()
Radiobutton(root, text='Top Right', variable=position, value='top_right').pack()
Radiobutton(root, text='Center', variable=position, value='center').pack()
Radiobutton(root, text='Bottom Left', variable=position, value='bottom_left').pack()
Radiobutton(root, text='Bottom Right', variable=position, value='bottom_right').pack()

Label(root, text='Font Size:').pack()
font_size = StringVar(value='40')
font_size_input = Spinbox(
    root,
    from_=10,
    to=100,
    width=5,
    textvariable=font_size
)
font_size_input.pack()

color_button = Button(root, text="Choose Color", command=choose_color)
color_button.pack()
color_label = Label(root, text='        ', background='white')
color_label.pack()

watermark_button = Button(text="Add Watermark", command=add_watermark)
watermark_button.pack()

save_button = Button(text="Save Image", command=save)
save_button.pack()


root.mainloop()
import tkinter as tk
from tkinter import ttk, filedialog
from ttkbootstrap import Button, Label
from PIL import Image, ImageTk
import os


class PngToPdfConverterTool(ttk.Frame):
    def __init__(self, container, settings):
        super().__init__(container)
        self.settings = settings

        # Text defaults
        self.button_initiate = "Select PNG"
        self.button_execute = "Convert to PDF"
        self.alert_execute_success = "PDF created successfully at:\n"
        self.alert_execute_warning = "Please select a PNG file first."
        self.waiting_on_user = "Ready to convert ..."
        self.no_file_selected = "No PNG selected."
        self.choose_save_location = "Choose the location you want to save the PDF."

        # Left Section Frame for Tool Name and Instructions
        left_frame = ttk.Frame(self, width=settings["left_frame_width"])
        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=settings["left_frame_padx"],
            pady=settings["left_frame_pady"],
        )
        left_frame.pack_propagate(False)

        # Tool title
        tool_name_frame = ttk.Frame(left_frame, height=80)
        tool_name_frame.pack(pady=20, padx=10, fill="x", anchor="nw")
        tool_name_frame.pack_propagate(False)
        tool_name_label = Label(
            tool_name_frame,
            text="PNG to PDF Converter",
            font=settings["text_h1"],
            wraplength=190,
        )
        tool_name_label.pack(anchor="nw")

        # Instructions
        instructions_frame = ttk.Frame(left_frame)
        instructions_frame.pack(fill="x", padx=20)
        self.instructions_label_title = Label(
            instructions_frame,
            text="Instructions",
            font=settings["text_h2"],
            wraplength=190,
        )
        self.instructions_label_title.pack(anchor="nw")

        # Step 1 Frame
        step1_frame = ttk.Frame(instructions_frame)
        step1_frame.pack(fill="x", padx=10, pady=2)
        self.instructions_label1_number = Label(
            step1_frame,
            text="1.",
            font=settings["text_base_bold"],
        )
        self.instructions_label1_number.pack(side="left", anchor="nw")
        self.instructions_label1 = Label(
            step1_frame,
            text="Click the 'Select PNG' button on the right, and choose the .png image you want to convert.",
            font=settings["text_base"],
            wraplength=190,
        )
        self.instructions_label1.pack(side="left", padx=5)

        # Step 2 Frame
        step2_frame = ttk.Frame(instructions_frame)
        step2_frame.pack(fill="x", padx=10, pady=10)
        self.instructions_label2_number = Label(
            step2_frame,
            text="2.",
            font=settings["text_base_bold"],
        )
        self.instructions_label2_number.pack(side="left", anchor="nw")
        self.instructions_label2 = Label(
            step2_frame,
            text="Click the 'Convert to PDF' button under the thumbnail image to convert the selected image to PDF.",
            font=settings["text_base"],
            wraplength=190,
        )
        self.instructions_label2.pack(side="left", padx=5)

        # Step 3 Frame
        step3_frame = ttk.Frame(instructions_frame)
        step3_frame.pack(fill="x", padx=10, pady=5)
        self.instructions_label3_number = Label(
            step3_frame,
            text="3.",
            font=settings["text_base_bold"],
        )
        self.instructions_label3_number.pack(side="left", anchor="nw")
        self.instructions_label3 = Label(
            step3_frame,
            text=self.choose_save_location,
            font=settings["text_base"],
            wraplength=190,
        )
        self.instructions_label3.pack(side="left", padx=5)

        # Vertical Separator
        separator = ttk.Separator(self, orient="vertical")
        separator.pack(side="left", fill="y", padx=5)

        # Right Section Frame for Interactive Elements
        right_frame = ttk.Frame(self, width=settings["right_frame_width"])
        right_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=settings["right_frame_padx"],
            pady=settings["right_frame_pady"],
        )
        right_frame.pack_propagate(False)

        # Interactive elements (Select button, canvas, status label, etc.)
        self.select_button = Button(
            right_frame, text=self.button_initiate, width="20", command=self.select_png
        )
        self.select_button.pack(pady=10, padx=10)

        # Frame for the thumbnail image, file name and convert button
        image_thumb_frame = ttk.Frame(right_frame)
        image_thumb_frame.pack(fill="x", padx=10, pady=5)
        self.selected_png_label = Label(
            image_thumb_frame,
            text=self.no_file_selected,
            font=settings["text_base_italic"],
        )
        self.selected_png_label.pack(pady=5, padx=10)

        self.canvas = tk.Canvas(image_thumb_frame, width=200, height=200, bg="white")
        self.canvas.pack(pady=10, padx=10)

        self.convert_button = Button(
            image_thumb_frame,
            text=self.button_execute,
            width="20",
            style="success.TButton",
            command=self.convert_to_pdf,
        )

        self.status_label = Label(
            image_thumb_frame,
            text=self.waiting_on_user,
            font=settings["text_base_italic"],
        )

        # Variable to store the selected PNG file path
        self.selected_png = None

    def select_png(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            self.selected_png = file_path
            self.selected_png_label.config(
                text=os.path.basename(file_path), font=self.settings["text_base_bold"]
            )
            self.preview_image(file_path)

    def preview_image(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Clear the canvas and create a new image
        self.canvas.delete("all")
        self.canvas.create_image(100, 100, image=photo)
        self.canvas.image = photo  # Keep a reference to avoid garbage collection
        # Show the status text and convert button
        self.status_label.pack(pady=5, padx=10)
        self.convert_button.pack(padx=10)

    def convert_to_pdf(self):
        if self.selected_png:
            try:
                image = Image.open(self.selected_png)
                pdf_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
                )
                if pdf_path:
                    image.convert("RGB").save(pdf_path)

                    # Inform the user of successful PDF creation
                    tk.messagebox.showinfo(
                        "Success", self.alert_execute_success + pdf_path
                    )

                    self.reset_screen()
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            tk.messagebox.showinfo("Info", self.alert_execute_warning)

    def reset_screen(self):
        # Reset the selected PNG file path
        self.selected_png = None
        self.selected_png_label.config(
            text=self.no_file_selected, font=self.settings["text_base_italic"]
        )
        self.status_label.pack_forget()
        self.convert_button.pack_forget()
        self.canvas.delete("all")

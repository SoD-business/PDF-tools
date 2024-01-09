from tkinter import ttk, filedialog, messagebox
from ttkbootstrap import Button, Label
from PyPDF2 import PdfReader, PdfWriter
import os

# TODO: Add a small thumbnail for the selected start and end page, like when you print pages
# TODO: Redesign PDF Split page layout


class SplitPdfTool(ttk.Frame):
    def __init__(self, container, settings):
        super().__init__(container)
        self.settings = settings

        # Text defaults
        self.button_initiate = "Select PDF"
        self.button_execute = "Split PDF"
        self.alert_execute_success = "PDF Split Successfully!"
        self.alert_execute_warning = ""
        self.alert_execute_error = "No file selected or invalid page range!"
        self.waiting_on_user = ""
        self.no_file_selected = "No file selected."
        self.choose_save_location = ""

        # Tool title and instructions modification
        left_frame = ttk.Frame(self, width=settings["left_frame_width"])
        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=settings["left_frame_padx"],
            pady=settings["left_frame_pady"],
        )
        left_frame.pack_propagate(False)

        tool_name_frame = ttk.Frame(left_frame, height=80)
        tool_name_frame.pack(pady=20, padx=10, fill="x", anchor="nw")
        tool_name_frame.pack_propagate(False)
        tool_name_label = Label(
            tool_name_frame,
            text="Split PDF",
            font=settings["text_h1"],
            wraplength=settings["text_h1_wrap"],
        )
        tool_name_label.pack(anchor="nw")

        instructions_frame = ttk.Frame(left_frame)
        instructions_frame.pack(fill="x", padx=20)
        self.instructions_label_title = Label(
            instructions_frame,
            text="Instructions",
            font=settings["text_h2"],
            wraplength=settings["text_h1_wrap"],
        )
        self.instructions_label_title.pack(anchor="nw")

        # Step 1 Frame
        step1_frame = ttk.Frame(instructions_frame)
        step1_frame.pack(fill="x", padx=10, pady=2)
        self.instructions_label1_number = Label(
            step1_frame, text="1.", font=settings["text_base_bold"]
        )
        self.instructions_label1_number.pack(side="left", anchor="nw")
        self.instructions_label1 = Label(
            step1_frame,
            text="Click 'Select PDF' and choose the PDF file you want to split.",
            font=("Arial", 10),
            wraplength=settings["text_h1_wrap"],
        )
        self.instructions_label1.pack(side="left", padx=5)

        # Step 2 Frame
        step2_frame = ttk.Frame(instructions_frame)
        step2_frame.pack(fill="x", padx=10, pady=10)
        self.instructions_label2_number = Label(
            step2_frame, text="2.", font=settings["text_base_bold"]
        )
        self.instructions_label2_number.pack(side="left", anchor="nw")
        self.instructions_label2 = Label(
            step2_frame,
            text="Enter the start and end page numbers for the split.",
            font=("Arial", 10),
            wraplength=settings["text_h1_wrap"],
        )
        self.instructions_label2.pack(side="left", padx=5)

        # Step 3 Frame
        step3_frame = ttk.Frame(instructions_frame)
        step3_frame.pack(fill="x", padx=10, pady=5)
        self.instructions_label3_number = Label(
            step3_frame, text="3.", font=settings["text_base_bold"]
        )
        self.instructions_label3_number.pack(side="left", anchor="nw")
        self.instructions_label3 = Label(
            step3_frame,
            text="Click 'Split PDF' to split the file.",
            font=("Arial", 10),
            wraplength=settings["text_h1_wrap"],
        )
        self.instructions_label3.pack(side="left", padx=5)

        # Separator
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

        # Select PDF Button
        self.select_button = Button(
            right_frame, text=self.button_initiate, width="20", command=self.select_file
        )
        self.select_button.pack(pady=10, padx=10)

        # Entry for Start Page
        self.start_page_label = Label(
            right_frame, text="Start Page:", font=settings["text_base"]
        )
        self.start_page_label.pack(pady=2)
        self.start_page_entry = ttk.Entry(right_frame)
        self.start_page_entry.pack(pady=2)

        # Entry for End Page
        self.end_page_label = Label(
            right_frame, text="End Page:", font=settings["text_base"]
        )
        self.end_page_label.pack(pady=2)
        self.end_page_entry = ttk.Entry(right_frame)
        self.end_page_entry.pack(pady=2)

        # Split PDF Button
        self.split_button = Button(
            right_frame,
            text=self.button_execute,
            width="20",
            style="success.TButton",
            command=self.split_pdf,
        )
        self.split_button.pack(pady=10, padx=10)

        # Split Every Page Button
        self.split_every_button = Button(
            right_frame,
            text="Split Every Page",
            width="20",
            style="info.TButton",
            command=self.split_every_page,
        )
        self.split_every_button.pack(pady=10, padx=10)

        # File name label
        self.file_label = Label(
            right_frame, text=self.no_file_selected, font=settings["text_base_italic"]
        )
        self.file_label.pack(pady=10, padx=10)

        self.selected_file = None

    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file:
            self.selected_file = file
            self.file_label.config(text=os.path.basename(file))
        else:
            self.file_label.config(text=self.no_file_selected)
            self.selected_file = None

    def split_pdf(self):
        if not self.selected_file:
            messagebox.showerror("Error", self.alert_execute_error)
            return

        start_page = self.start_page_entry.get()
        end_page = self.end_page_entry.get()

        if not start_page.isdigit() or not end_page.isdigit():
            messagebox.showerror("Error", self.alert_execute_error)
            return

        start_page, end_page = int(start_page), int(end_page)

        try:
            reader = PdfReader(self.selected_file)
            writer = PdfWriter()

            for i in range(start_page - 1, end_page):
                writer.add_page(reader.pages[i])

            output_path = filedialog.asksaveasfilename(
                defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
            )
            if not output_path:
                return

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            messagebox.showinfo("Success", self.alert_execute_success)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def split_every_page(self):
        if not self.selected_file:
            messagebox.showerror("Error", self.alert_execute_error)
            return

        try:
            reader = PdfReader(self.selected_file)
            file_base_name = os.path.basename(self.selected_file)
            folder_name = f"{os.path.splitext(file_base_name)[0]}_pages".replace(
                " ", "_"
            )
            output_directory = os.path.join(
                os.path.dirname(self.selected_file), folder_name
            )

            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            for i in range(len(reader.pages)):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                output_file_name = f"page_{i+1}.pdf"
                output_path = os.path.join(output_directory, output_file_name)

                with open(output_path, "wb") as output_file:
                    writer.write(output_file)

            messagebox.showinfo(
                "Success", f"Split into {len(reader.pages)} files in '{folder_name}'"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

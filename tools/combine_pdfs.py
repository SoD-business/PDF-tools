from tkinter import ttk, filedialog, messagebox
from ttkbootstrap import Button, Label
from ttkbootstrap.scrolled import ScrolledFrame
from PyPDF2 import PdfMerger
import os


class CombinePdfsTool(ttk.Frame):
    def __init__(self, container, settings):
        super().__init__(container)
        self.settings = settings

        # Text defaults
        self.button_initiate = "Select PDFs"
        self.button_execute = "Combine PDFs"
        self.alert_execute_success = ""
        self.alert_execute_warning = ""
        self.alert_execute_error = "No files selected!"
        self.waiting_on_user = ""
        self.no_file_selected = "No files selected."
        self.choose_save_location = ""

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
            text="Combine PDFs",
            font=settings["text_h1"],
            wraplength=settings["text_h1_wrap"],
        )
        tool_name_label.pack(anchor="nw")

        # Instructions
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
            step1_frame,
            text="1.",
            font=settings["text_base_bold"],
        )
        self.instructions_label1_number.pack(side="left", anchor="nw")
        self.instructions_label1 = Label(
            step1_frame,
            text="Click 'Select PDFs' and choose the PDF files you want to merge.",
            font=("Arial", 10),
            wraplength=settings["text_h1_wrap"],
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
            text="Re-order the files by clicking the buttons to the left of each file name.",
            font=("Arial", 10),
            wraplength=settings["text_h1_wrap"],
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
            text="Click 'Merge PDFs' to combine the files and save the merged document.",
            font=("Arial", 10),
            wraplength=settings["text_h1_wrap"],
        )
        self.instructions_label3.pack(side="left", padx=5)

        # Vertical Separator
        separator = ttk.Separator(self, orient="vertical")
        separator.pack(side="left", fill="y", padx=5)

        # TODO: Bug: When scrolled to the bottom and deleting files, the middle mousewheel button doesn't work

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

        # Interactive elements (Select button, Listbox, scrollbar, and status label)
        self.select_button = Button(
            right_frame,
            text=self.button_initiate,
            width="20",
            command=self.select_files,
        )
        self.select_button.pack(pady=10, padx=10)

        # Scrolled Frame for the listbox
        self.scrolled_frame = ScrolledFrame(right_frame)
        self.scrolled_frame.pack(fill="both", expand=True)

        # List of frames for each file
        self.file_frames = []
        # Label to show when no files are selected
        self.no_files_label = Label(
            self.scrolled_frame,
            text=self.no_file_selected,
            font=settings["text_base_italic"],
        )
        self.no_files_label.pack(pady=10, padx=10)

        self.merge_button = Button(
            right_frame,
            text=self.button_execute,
            width="20",
            style="success.TButton",
            command=self.merge_pdfs,
        )

        self.file_frames = []

    def select_files(self):
        new_files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if new_files:
            for file in new_files:
                self.add_file_label(file)
            # Show the merge button if there are files
            self.merge_button.pack(pady=10, padx=10)
            self.no_files_label.pack_forget()  # Hide the "No files selected" message
        elif not self.file_frames:
            self.no_files_label.pack(pady=10, padx=10)

    def add_file_label(self, file_path):
        frame = ttk.Frame(self.scrolled_frame)
        frame.pack(pady=2, anchor="w")

        button_width = 2  # Set a small width for the buttons
        button_padding = 2  # Set a small padding for the buttons

        up_button = ttk.Button(
            frame,
            text="↑",
            width=button_width,
            command=lambda: self.move_file(frame, -1),
        )
        up_button.pack(side="left", padx=button_padding)

        down_button = ttk.Button(
            frame,
            text="↓",
            width=button_width,
            style="warning.TButton",
            command=lambda: self.move_file(frame, 1),
        )
        down_button.pack(side="left", padx=button_padding)

        delete_button = ttk.Button(
            frame,
            text="🗑️",
            width=button_width,
            style="danger.TButton",
            command=lambda: self.delete_file(frame),
        )
        delete_button.pack(side="left", padx=button_padding)

        label = ttk.Label(frame, text=os.path.basename(file_path))
        label.pack(side="left", fill="x", expand=True)

        # Store the file path as an attribute of the frame
        frame.file_path = file_path
        self.file_frames.append(frame)

    def move_file(self, frame, direction):
        idx = self.file_frames.index(frame)
        if 0 <= idx + direction < len(self.file_frames):
            self.file_frames[idx], self.file_frames[idx + direction] = (
                self.file_frames[idx + direction],
                self.file_frames[idx],
            )

            # Re-pack all frames in the new order
            for f in self.file_frames:
                f.pack_forget()
                f.pack(pady=2, anchor="w")

    def delete_file(self, frame):
        self.file_frames.remove(frame)
        frame.pack_forget()
        frame.destroy()

        if not self.file_frames:
            self.no_files_label.pack(pady=10, padx=10)

    def merge_pdfs(self):
        if not self.file_frames:
            messagebox.showerror("Error", self.alert_execute_error)
            return

        files = [f.file_path for f in self.file_frames]

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if not output_path:
            return

        try:
            merger = PdfMerger()
            for file_name in files:
                merger.append(file_name)

            merger.write(output_path)
            merger.close()
            messagebox.showinfo(
                "Success", f"Combined into {os.path.basename(output_path)}"
            )

            self.reset_screen()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_screen(self):
        # Clear the list of file frames
        for frame in self.file_frames:
            frame.pack_forget()
            frame.destroy()
        self.file_frames.clear()

        # Show the "No files selected" message
        self.no_files_label.pack(pady=10, padx=10)

        # Hide the "Combine PDFs" button
        self.merge_button.pack_forget()

from tkinter import ttk
import ttkbootstrap as ttkb
from tools import PngToPdfConverterTool, CombinePdfsTool, SplitPdfTool


class PdfToolsApp:
    def __init__(self, root):
        self.root = root
        root.title("PDF Tools")
        root.geometry("800x600")

        # Create a dictionary of settings
        self.settings = {
            "left_frame_width": 200,
            "left_frame_padx": 10,
            "left_frame_pady": 10,
            "right_frame_width": 400,
            "right_frame_padx": 10,
            "right_frame_pady": 50,
            "text_base": ("Arial", 10),
            "text_h1": ("Arial Black", 16),
            "text_h1_wrap": 180,
            "text_h2": ("Arial", 14),
            "text_h3": ("Arial", 12),
            "text_base_bold": ("Arial", 10, "bold"),
            "text_base_italic": ("Arial", 10, "italic"),
        }

        # Create a style with the superhero theme
        self.style = ttkb.Style(theme="superhero")

        # App title
        self.title_label = ttk.Label(root, text="PDF Tools", font=("Arial Black", 20))
        self.title_label.pack(pady=20)

        # Tab control
        self.tabControl = ttk.Notebook(root)
        self.tabControl.pack(expand=1, fill="both")

        # Home tab
        self.home_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.home_tab, text="Home")

        # Split PDFs tab
        self.split_pdf_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.split_pdf_tab, text="Split PDF")
        self.split_pdfs_tool = SplitPdfTool(self.split_pdf_tab, self.settings)
        self.split_pdfs_tool.pack(expand=True, fill="both")

        # Combine PDFs tab
        self.combine_pdf_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.combine_pdf_tab, text="Combine PDFs")
        self.combine_pdfs_tool = CombinePdfsTool(self.combine_pdf_tab, self.settings)
        self.combine_pdfs_tool.pack(expand=True, fill="both")

        # PNG to PDF tab
        self.convert_png_pdf_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.convert_png_pdf_tab, text="PNG to PDF")
        self.png_to_pdf_tool = PngToPdfConverterTool(
            self.convert_png_pdf_tab, self.settings
        )
        self.png_to_pdf_tool.pack(expand=True, fill="both")

        # Home tab content
        self.home_label = ttk.Label(
            self.home_tab,
            text="Welcome to PDF Tools\n\nPlease use the tabs above to access the different PDF utilities currently available.\n\nMore tools will be added in the future.\n\nThank you for using PDF Tools!",
            font=("Arial", 14),
        )
        self.home_label.pack(pady=30, padx=30, anchor="nw", fill="x")

        # Home tab copyright
        self.copyright_label = ttk.Label(
            self.home_tab,
            text="© Copyright 2024 Sound of Dialup.",
            font=("Arial", 9),
        )
        self.copyright_label.pack(pady=30, padx=30, anchor="se", side="bottom")


# Create the main window and run the application
root = ttkb.Window(themename="superhero")
app = PdfToolsApp(root)
root.mainloop()

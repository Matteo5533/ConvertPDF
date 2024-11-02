import os
from tkinter import Tk, Button, Listbox, Entry, Label, filedialog, messagebox, END
from PIL import Image

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        
        # List to contain selected file paths
        self.selected_files = []

        # Graphical interface
        self.setup_gui()

    def setup_gui(self):
        # Button to select image files
        Button(self.root, text="Select Images", command=self.select_images).grid(row=0, column=0, padx=10, pady=10)
        
        # List of selected files
        self.file_listbox = Listbox(self.root, width=50, height=10)
        self.file_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Field to enter the name of the final PDF file
        Label(self.root, text="Final PDF file name:").grid(row=2, column=0, padx=10, pady=(10, 0))
        self.output_name_entry = Entry(self.root, width=40)
        self.output_name_entry.grid(row=3, column=0, padx=10, pady=5)
        
        # Button to choose the save directory
        Button(self.root, text="Select Storage Folder", command=self.select_output_folder).grid(row=4, column=0, padx=10, pady=10)

        # Button to create the PDF file
        Button(self.root, text="Create PDF", command=self.create_pdf).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def select_images(self):
        # Select image files
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        
        if file_paths:
            self.selected_files.extend(file_paths)
            self.update_file_listbox()

    def update_file_listbox(self):
        # Update the list of selected files
        self.file_listbox.delete(0, END)
        for file in self.selected_files:
            self.file_listbox.insert(END, os.path.basename(file))

    def select_output_folder(self):
        # Select save directory
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            messagebox.showinfo("Selected Folder", f"It saves the PDF in: {self.output_folder}")

    def create_pdf(self):
        # Check that there are selected files and a name for the PDF
        if not self.selected_files:
            messagebox.showerror("Error", "No image file selected.")
            return

        if not self.output_name_entry.get():
            messagebox.showerror("Error", "Enter a name for the final PDF file.")
            return

        if not hasattr(self, 'output_folder'):
            messagebox.showerror("Error", "Select a save directory.")
            return

        # Prepare PDF file name
        pdf_name = self.output_name_entry.get() + ".pdf"
        output_path = os.path.join(self.output_folder, pdf_name)

        try:
            # Converts images into a PDF
            image_list = []
            for file in self.selected_files:
                with Image.open(file) as img:
                    img = img.convert("RGB")  # Convert in RGB
                    image_list.append(img.copy())  # Copy the image to avoid file descriptor problems
            
            # Save the PDF
            if image_list:
                image_list[0].save(output_path, save_all=True, append_images=image_list[1:])
            
            messagebox.showinfo("Success", f"PDF successfully created in:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the PDF:\n{e}")

# Create the main window
root = Tk()
app = ImageToPDFConverter(root)
root.mainloop()

# # gui_destination_selector.py

# import os
# import sys
# import tkinter as tk
# from tkinter import filedialog, messagebox


# def browse_folder(folder_var):
#     folder = filedialog.askdirectory()
#     if folder:
#         folder_var.set(folder)


# def browse_file(file_var):
#     file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
#     if file_path:
#         file_var.set(file_path)


# def proceed(app_data, choice_var, folder_var, file_name_var, existing_file_var, root):
#     from doc_task import doc_manager  # import inside to avoid circular import issues

#     choice = choice_var.get()
    
#     # 1️⃣ Validate that user has selected an option
#     if not choice:
#         messagebox.showwarning("Selection Error", "Please choose 'Create New' or 'Open Existing'.")
#         return

#     if choice == "create":  # Create New
#         folder = folder_var.get()
#         file_name = file_name_var.get()

#         if not folder:
#             messagebox.showwarning("Missing Folder", "Please select a folder.")
#             return
#         if not file_name.strip():
#             messagebox.showwarning("Missing File Name", "Please enter a file name.")
#             return

#         full_path = folder + "/" + file_name + ".docx"

#         # Check if file already exists
#         if os.path.exists(full_path):
#             overwrite = messagebox.askyesno(
#                 "File Exists",
#                 f"A file named '{file_name}.docx' already exists in the selected folder.\nDo you want to overwrite it?"
#             )
#             if not overwrite:
#                 return  # user chose not to overwrite

#         try:
#             doc_manager.create_docx(full_path)
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to create file:\n{e}")
#             return


#         # Appdata obeject , setter methods used to set file/folder loc 
#         app_data.set_folder_path(os.path.dirname(full_path))
#         # app_data.set_file_name(file_name + ".docx")
#         app_data.set_file_name(os.path.basename(full_path))

#         messagebox.showinfo("Success", f"New file created:\n{full_path}")
#         root.destroy()

#     elif choice == "open":  # Open Existing
#         file_path = existing_file_var.get()
#         if not file_path or not os.path.isfile(file_path):
#             messagebox.showwarning("Invalid File", "Please select a valid DOCX file.")
#             return

#         # Appdata obeject , setter methods used to set file/folder loc 
#         app_data.set_folder_path(os.path.dirname(file_path))
#         app_data.set_file_name(os.path.basename(file_path))

#         messagebox.showinfo("Success", f"Existing file selected:\n{file_path}")
#         root.destroy()



# def start_folder_selection(app_data):
#     root = tk.Tk()
#     root.title("NoteItUp - Select File")
#     root.geometry("600x250")
#     root.configure(bg="white")

#     # Handle window close (X button)
#     def on_close():
#         root.destroy()
#         sys.exit(0)  # exit whole program if window closed

#     root.protocol("WM_DELETE_WINDOW", on_close)

#     # Choice between Create New and Open Existing
#     choice_var = tk.StringVar()
#     choice_var.set(None)  # ensures no option is pre-selected

#     folder_var = tk.StringVar()
#     file_name_var = tk.StringVar()
#     existing_file_var = tk.StringVar()

#     # Create New Section
#     create_radio = tk.Radiobutton(root, text="Create New", variable=choice_var, value="create", bg="white", fg="black")
#     create_radio.grid(row=0, column=0, sticky="w", padx=10, pady=5)

#     tk.Label(root, text="Folder:", bg="white", fg="black").grid(row=1, column=0, sticky="w", padx=20)
#     folder_entry = tk.Entry(root, textvariable=folder_var, width=40)
#     folder_entry.grid(row=1, column=1, padx=5)
#     tk.Button(root, text="Browse", command=lambda: browse_folder(folder_var)).grid(row=1, column=2, padx=5)

#     tk.Label(root, text="File Name:", bg="white", fg="black").grid(row=2, column=0, sticky="w", padx=20)
#     file_name_entry = tk.Entry(root, textvariable=file_name_var, width=40)
#     file_name_entry.grid(row=2, column=1, padx=5)

#     # Open Existing Section
#     open_radio = tk.Radiobutton(root, text="Open Existing", variable=choice_var, value="open", bg="white", fg="black")
#     open_radio.grid(row=3, column=0, sticky="w", padx=10, pady=15)

#     existing_entry = tk.Entry(root, textvariable=existing_file_var, width=40)
#     existing_entry.grid(row=3, column=1, padx=5)
#     tk.Button(root, text="Browse", command=lambda: browse_file(existing_file_var)).grid(row=3, column=2, padx=5)

#     # Proceed Button
#     proceed_btn = tk.Button(
#         root,
#         text="Proceed",
#         bg="black",
#         fg="white",
#         command=lambda: proceed(app_data, choice_var, folder_var, file_name_var, existing_file_var, root),
#     )
#     proceed_btn.grid(row=4, column=1, pady=20)

#     root.mainloop()

# -------------------------------------------------------------------------------------
# gui_destination_selector.py

# import os
# import sys
# import tkinter as tk
# from tkinter import filedialog, messagebox


# # ------------------ Browsing Helpers ------------------
# def browse_folder(folder_var):
#     folder = filedialog.askdirectory()
#     if folder:
#         folder_var.set(folder)


# def browse_file(file_var):
#     file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
#     if file_path:
#         file_var.set(file_path)


# # ------------------ Proceed Handler ------------------
# def proceed(app_data, choice_var, folder_var, file_name_var, existing_file_var, root):
#     from doc_task import doc_manager  # avoid circular import

#     choice = choice_var.get()

#     if not choice:
#         messagebox.showwarning("Selection Error",
#                                "Please choose 'Create New' or 'Open Existing'.")
#         return

#     # --------------------------------------------------
#     # CREATE NEW DOCX
#     # --------------------------------------------------
#     if choice == "create":
#         folder = folder_var.get()
#         file_name = file_name_var.get().strip()

#         if not folder:
#             messagebox.showwarning("Missing Folder", "Please select a folder.")
#             return

#         if not file_name:
#             messagebox.showwarning("Missing File Name", "Please enter a file name.")
#             return

#         full_path = os.path.join(folder, file_name + ".docx")

#         # File conflict check
#         if os.path.exists(full_path):
#             ow = messagebox.askyesno(
#                 "File Exists",
#                 f"A file named '{file_name}.docx' already exists.\nOverwrite?"
#             )
#             if not ow:
#                 return

#         # Create file
#         try:
#             doc_manager.create_docx(full_path)
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to create file:\n{e}")
#             return

#         # SAVE to AppData
#         app_data.set_folder_path(folder)
#         app_data.set_file_name(file_name + ".docx")

#         messagebox.showinfo("Success", f"New file created:\n{full_path}")
#         root.destroy()

#     # --------------------------------------------------
#     # OPEN EXISTING DOCX
#     # --------------------------------------------------
#     elif choice == "open":
#         file_path = existing_file_var.get()

#         if not file_path or not os.path.isfile(file_path):
#             messagebox.showwarning("Invalid File", "Please select a valid DOCX file.")
#             return

#         folder = os.path.dirname(file_path)
#         fname = os.path.basename(file_path)

#         # SAVE to AppData
#         app_data.set_folder_path(folder)
#         app_data.set_file_name(fname)

#         messagebox.showinfo("Success", f"Existing file selected:\n{file_path}")
#         root.destroy()


# # ------------------ UI Launcher ------------------
# def start_folder_selection(app_data):
#     root = tk.Tk()
#     root.title("SpectraNote - Select File")
#     root.geometry("600x250")
#     root.configure(bg="white")

#     # Make this window modal (blocks main)
#     root.grab_set()

#     def on_close():
#         root.destroy()
#         sys.exit(0)

#     root.protocol("WM_DELETE_WINDOW", on_close)

#     # Variables
#     choice_var = tk.StringVar(value=None)
#     folder_var = tk.StringVar()
#     file_name_var = tk.StringVar()
#     existing_file_var = tk.StringVar()

#     # ------------------ CREATE NEW ------------------
#     tk.Radiobutton(root, text="Create New", variable=choice_var, value="create",
#                    bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)

#     tk.Label(root, text="Folder:", bg="white").grid(row=1, column=0, sticky="w", padx=20)
#     tk.Entry(root, textvariable=folder_var, width=40).grid(row=1, column=1, padx=5)
#     tk.Button(root, text="Browse",
#               command=lambda: browse_folder(folder_var)).grid(row=1, column=2, padx=5)

#     tk.Label(root, text="File Name:", bg="white").grid(row=2, column=0, sticky="w", padx=20)
#     tk.Entry(root, textvariable=file_name_var, width=40).grid(row=2, column=1, padx=5)

#     # ------------------ OPEN EXISTING ------------------
#     tk.Radiobutton(root, text="Open Existing", variable=choice_var, value="open",
#                    bg="white").grid(row=3, column=0, sticky="w", padx=10, pady=15)

#     tk.Entry(root, textvariable=existing_file_var, width=40).grid(row=3, column=1, padx=5)
#     tk.Button(root, text="Browse",
#               command=lambda: browse_file(existing_file_var)).grid(row=3, column=2, padx=5)

#     # ------------------ PROCEED ------------------
#     tk.Button(
#         root,
#         text="Proceed",
#         bg="black",
#         fg="white",
#         command=lambda: proceed(app_data, choice_var, folder_var,
#                                 file_name_var, existing_file_var, root)
#     ).grid(row=4, column=1, pady=20)

#     root.mainloop()



# gui_destination_selector.py

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


def browse_folder(folder_var):
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)


def browse_file(file_var):
    file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
    if file_path:
        file_var.set(file_path)


def proceed(app_data, choice_var, folder_var, file_name_var, existing_file_var, root):
    from doc_task import doc_manager  # import inside to avoid circular import issues

    choice = choice_var.get()
    
    # 1️⃣ Validate that user has selected an option
    if not choice:
        messagebox.showwarning("Selection Error", "Please choose 'Create New' or 'Open Existing'.")
        return

    if choice == "create":  # Create New
        folder = folder_var.get()
        file_name = file_name_var.get()

        if not folder:
            messagebox.showwarning("Missing Folder", "Please select a folder.")
            return
        if not file_name.strip():
            messagebox.showwarning("Missing File Name", "Please enter a file name.")
            return

        full_path = folder + "/" + file_name + ".docx"

        # Check if file already exists
        if os.path.exists(full_path):
            overwrite = messagebox.askyesno(
                "File Exists",
                f"A file named '{file_name}.docx' already exists in the selected folder.\nDo you want to overwrite it?"
            )
            if not overwrite:
                return  # user chose not to overwrite

        try:
            doc_manager.create_docx(full_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create file:\n{e}")
            return


        # Appdata obeject , setter methods used to set file/folder loc 
        app_data.set_folder_path(os.path.dirname(full_path))
        # app_data.set_file_name(file_name + ".docx")
        app_data.set_file_name(os.path.basename(full_path))

        messagebox.showinfo("Success", f"New file created:\n{full_path}")
        root.destroy()

    elif choice == "open":  # Open Existing
        file_path = existing_file_var.get()
        if not file_path or not os.path.isfile(file_path):
            messagebox.showwarning("Invalid File", "Please select a valid DOCX file.")
            return

        # Appdata obeject , setter methods used to set file/folder loc 
        app_data.set_folder_path(os.path.dirname(file_path))
        app_data.set_file_name(os.path.basename(file_path))

        messagebox.showinfo("Success", f"Existing file selected:\n{file_path}")
        root.destroy()



def start_folder_selection(app_data):
    root = tk.Tk()
    root.title("NoteItUp - Select File")
    root.geometry("600x250")
    root.configure(bg="white")

    # Handle window close (X button)
    def on_close():
        root.destroy()
        sys.exit(0)  # exit whole program if window closed

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Choice between Create New and Open Existing
    choice_var = tk.StringVar()
    choice_var.set(None)  # ensures no option is pre-selected

    folder_var = tk.StringVar()
    file_name_var = tk.StringVar()
    existing_file_var = tk.StringVar()

    # Create New Section
    create_radio = tk.Radiobutton(root, text="Create New", variable=choice_var, value="create", bg="white", fg="black")
    create_radio.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    tk.Label(root, text="Folder:", bg="white", fg="black").grid(row=1, column=0, sticky="w", padx=20)
    folder_entry = tk.Entry(root, textvariable=folder_var, width=40)
    folder_entry.grid(row=1, column=1, padx=5)
    tk.Button(root, text="Browse", command=lambda: browse_folder(folder_var)).grid(row=1, column=2, padx=5)

    tk.Label(root, text="File Name:", bg="white", fg="black").grid(row=2, column=0, sticky="w", padx=20)
    file_name_entry = tk.Entry(root, textvariable=file_name_var, width=40)
    file_name_entry.grid(row=2, column=1, padx=5)

    # Open Existing Section
    open_radio = tk.Radiobutton(root, text="Open Existing", variable=choice_var, value="open", bg="white", fg="black")
    open_radio.grid(row=3, column=0, sticky="w", padx=10, pady=15)

    existing_entry = tk.Entry(root, textvariable=existing_file_var, width=40)
    existing_entry.grid(row=3, column=1, padx=5)
    tk.Button(root, text="Browse", command=lambda: browse_file(existing_file_var)).grid(row=3, column=2, padx=5)

    # Proceed Button
    proceed_btn = tk.Button(
        root,
        text="Proceed",
        bg="black",
        fg="white",
        command=lambda: proceed(app_data, choice_var, folder_var, file_name_var, existing_file_var, root),
    )
    proceed_btn.grid(row=4, column=1, pady=20)

    root.mainloop()

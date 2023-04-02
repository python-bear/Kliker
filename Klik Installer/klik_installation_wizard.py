import os
import shutil
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import zipfile


install_dir = None


def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        path_var.set(directory)


def install():
    global install_dir

    try:
        # Get the selected installation directory
        install_dir = path_var.get()

        # Unzip the Klik.zip file to a temporary directory
        temp_dir = os.path.join(os.getcwd(), "temp")
        with zipfile.ZipFile(os.path.join(os.getcwd(), "Klik.zip"), "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # Move the Klik directory from the temporary directory to the installation directory
        klik_dir = os.path.join(temp_dir, "Klik")
        shutil.move(klik_dir, os.path.join(install_dir, "Klik"))

        # Create a shortcut to the kliker.exe file on the desktop
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, "Kliker.lnk")
            target_path = os.path.join(install_dir, "Klik", "klikit.exe")
            create_shortcut(target_path, shortcut_path)

        except Exception as e1:
            try:
                desktop = os.path.join(os.path.expanduser("~"), "OneDrive\\Desktop")
                shortcut_path = os.path.join(desktop, "Kliker.lnk")
                target_path = os.path.join(install_dir, "Klik", "klikit.exe")
                create_shortcut(target_path, shortcut_path)

            except Exception as e2:
                # Show an error message if creating the shortcut failed
                messagebox.showerror("Error", f"Failed to create shortcut: {e2}")

        # Show a success message
        messagebox.showinfo("Success", "Installation complete.")

    except Exception as e:
        # Show an error message if the installation failed
        messagebox.showerror("Error", f"Installation failed: {e}")

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)


def create_shortcut(target_path, shortcut_path):
    global install_dir

    # Import the required modules for creating a shortcut on Windows
    import pythoncom
    from win32com.shell import shell, shellcon

    # Create the shortcut object
    shortcut = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink
    )
    
    # Set the path to the target file and the working directory
    shortcut.SetPath(target_path)
    shortcut.SetWorkingDirectory(os.path.dirname(target_path))
    
    # Set the icon of the shortcut
    shortcut.SetIconLocation(os.path.join(install_dir, 'Klik\\Lib\\klik_icon.ico'), 0)

    # Save the shortcut to disk
    persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
    persist_file.Save(shortcut_path, 0)


# Create the main window
FONT = ('Courier New', '15')
root = tk.Tk()
root.title("Klik Installer")
root.iconphoto(False, tk.PhotoImage(file='klik_icon.png'))
root.configure(background='#6bc2e7')
root.resizable(False, False)

# Create a label and entry for the installation directory
path_var = tk.StringVar()
path_label = tk.Label(root, text="Select installation directory:", font=FONT)
path_label.configure(background='#6bc2e7')
path_entry = tk.Entry(root, textvariable=path_var, font=FONT)
path_button = tk.Button(root, text="Browse...", command=select_directory, font=FONT)
path_button.configure(background='#21759A')

# Create a button to install the program
install_button = tk.Button(root, text="Install", command=install, font=FONT)
install_button.configure(background='#FE0000')

# Add the widgets to the window
path_label.grid(row=0, column=0, padx=5, pady=5)
path_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
path_button.grid(row=1, column=1, padx=5, pady=5)
install_button.grid(row=2, column=0, padx=5, pady=5)

# Start the main loop
root.mainloop()

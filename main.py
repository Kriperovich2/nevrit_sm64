import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class LanguageDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Выбор языка / Language")
        self.resizable(False, False)
        
        ttk.Label(self, text="Выберите язык / Choose language:").pack(pady=10)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="Русский", command=lambda: self.set_language("ru")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="English", command=lambda: self.set_language("en")).pack(side=tk.LEFT, padx=5)
        
        self.language = None
        
    def set_language(self, lang):
        self.language = lang
        self.destroy()

class NevritApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nevrit")
        self.root.resizable(False, False)
        
        # Загрузка иконки
        try:
            self.root.iconphoto(False, tk.PhotoImage(file="icon.png"))
        except:
            pass
        
        # Загрузка локализации
        self.load_language()
        
        # Переменные для путей
        self.texture_pack_path = tk.StringVar()
        self.textures_path = tk.StringVar()
        
        # Загрузка сохраненных путей
        self.load_paths()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка превью
        self.load_previews()
    
    def load_language(self):
        # Создаем диалог выбора языка
        lang_dialog = LanguageDialog(self.root)
        self.root.wait_window(lang_dialog)
        
        lang = lang_dialog.language if lang_dialog.language else "en"
        lang_file = "ru_lang.json" if lang == "ru" else "en_lang.json"
        
        try:
            with open(lang_file, "r", encoding="utf-8") as f:
                self.lang = json.load(f)
        except FileNotFoundError:
            # Fallback на английский
            self.lang = {
                "texture_pack_label": "Texture pack folder:",
                "textures_label": "Textures folder (with eyes and cap subfolders):",
                "change_eyes": "Move eyes",
                "back_eyes": "Return eyes",
                "change_cap": "Move cap logo",
                "back_cap": "Return cap logo",
                "no_textures": "No textures found",
                "confirm_lang": "Language set to English"
            }
            messagebox.showinfo("Info", self.lang["confirm_lang"])
    
    def load_paths(self):
        # Загрузка сохраненных путей из файла
        try:
            with open("paths.json", "r") as f:
                paths = json.load(f)
                self.texture_pack_path.set(paths.get("texture_pack_path", ""))
                self.textures_path.set(paths.get("textures_path", ""))
        except FileNotFoundError:
            pass
    
    def save_paths(self):
        # Сохранение путей в файл
        with open("paths.json", "w") as f:
            json.dump({
                "texture_pack_path": self.texture_pack_path.get(),
                "textures_path": self.textures_path.get()
            }, f)
    
    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Поле для пути к texture pack
        ttk.Label(main_frame, text=self.lang.get("texture_pack_label", "Texture pack folder:")).grid(row=0, column=0, sticky=tk.W)
        texture_pack_entry = ttk.Entry(main_frame, textvariable=self.texture_pack_path, width=50)
        texture_pack_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        ttk.Button(main_frame, text="...", command=lambda: self.browse_folder(self.texture_pack_path)).grid(row=0, column=2, padx=5)
        
        # Поле для пути к textures
        ttk.Label(main_frame, text=self.lang.get("textures_label", "Textures folder (with eyes and cap subfolders):")).grid(row=1, column=0, sticky=tk.W)
        textures_entry = ttk.Entry(main_frame, textvariable=self.textures_path, width=50)
        textures_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        ttk.Button(main_frame, text="...", command=lambda: self.browse_folder(self.textures_path)).grid(row=1, column=2, padx=5)
        
        # Фрейм для превью
        self.preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        self.preview_frame.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=10)
        
        # Кнопки
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, sticky=tk.EW)
        
        ttk.Button(buttons_frame, text=self.lang.get("change_eyes", "Move eyes"), 
                  command=self.move_eyes).pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text=self.lang.get("back_eyes", "Return eyes"), 
                  command=self.return_eyes).pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text=self.lang.get("change_cap", "Move cap logo"), 
                  command=self.move_cap).pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        ttk.Button(buttons_frame, text=self.lang.get("back_cap", "Return cap logo"), 
                  command=self.return_cap).pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        # Привязка событий для обновления превью при изменении путей
        self.texture_pack_path.trace_add("write", lambda *args: self.save_paths())
        self.textures_path.trace_add("write", lambda *args: (self.save_paths(), self.load_previews()))
    
    def browse_folder(self, path_var):
        folder = filedialog.askdirectory()
        if folder:
            path_var.set(folder)
    
    def load_previews(self):
        # Очистка превью
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        textures_path = self.textures_path.get()
        if not textures_path or not os.path.exists(textures_path):
            ttk.Label(self.preview_frame, text=self.lang.get("no_textures", "No textures found")).pack()
            return
        
        # Превью глаз
        eye_files = [
            "SUPER MARIO 64#5D6B0678#0#2_all.png",
            "SUPER MARIO 64#6B8D43C4#0#2_all.png",
            "SUPER MARIO 64#9FBECEF9#0#2_all.png"
        ]
        
        eyes_path = os.path.join(textures_path, "eyes")
        if os.path.exists(eyes_path):
            eyes_frame = ttk.Frame(self.preview_frame)
            eyes_frame.pack(fill=tk.X, pady=5)
            ttk.Label(eyes_frame, text="Eyes:").pack(anchor=tk.W)
            
            images_frame = ttk.Frame(eyes_frame)
            images_frame.pack(fill=tk.X)
            
            for eye_file in eye_files:
                eye_path = os.path.join(eyes_path, eye_file)
                if os.path.exists(eye_path):
                    try:
                        photo = tk.PhotoImage(file=eye_path)
                        label = ttk.Label(images_frame, image=photo)
                        label.image = photo  # сохраняем ссылку
                        label.pack(side=tk.LEFT, padx=5)
                    except:
                        continue
        
        # Превью шляпы
        cap_file = "SUPER MARIO 64#905D3214#0#2_all.png"
        cap_path = os.path.join(textures_path, "cap")
        if os.path.exists(cap_path):
            cap_frame = ttk.Frame(self.preview_frame)
            cap_frame.pack(fill=tk.X, pady=5)
            ttk.Label(cap_frame, text="Cap:").pack(anchor=tk.W)
            
            cap_image_path = os.path.join(cap_path, cap_file)
            if os.path.exists(cap_image_path):
                try:
                    photo = tk.PhotoImage(file=cap_image_path)
                    label = ttk.Label(cap_frame, image=photo)
                    label.image = photo  # сохраняем ссылку
                    label.pack(side=tk.LEFT, padx=5)
                except:
                    pass
    
    def move_files(self, src_folder, files, dest_folder, operation_name):
        if not self.texture_pack_path.get() or not self.textures_path.get():
            messagebox.showerror("Error", "Please set both folder paths first")
            return
        
        src_path = os.path.join(self.textures_path.get(), src_folder)
        dest_path = self.texture_pack_path.get()
        
        if not os.path.exists(src_path) or not os.path.exists(dest_path):
            messagebox.showerror("Error", "One of the folders doesn't exist")
            return
        
        moved_files = 0
        for file in files:
            src_file = os.path.join(src_path, file)
            dest_file = os.path.join(dest_path, file)
            
            if os.path.exists(src_file):
                try:
                    shutil.move(src_file, dest_file)
                    moved_files += 1
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to move {file}: {str(e)}")
        
        if moved_files > 0:
            messagebox.showinfo("Success", f"Moved {moved_files} {operation_name} files")
            self.load_previews()
    
    def return_files(self, src_folder, files, dest_subfolder, operation_name):
        if not self.texture_pack_path.get() or not self.textures_path.get():
            messagebox.showerror("Error", "Please set both folder paths first")
            return
        
        dest_path = os.path.join(self.textures_path.get(), dest_subfolder)
        src_path = self.texture_pack_path.get()
        
        if not os.path.exists(dest_path):
            os.makedirs(dest_path, exist_ok=True)
        
        if not os.path.exists(src_path):
            messagebox.showerror("Error", "Source folder doesn't exist")
            return
        
        returned_files = 0
        for file in files:
            src_file = os.path.join(src_path, file)
            dest_file = os.path.join(dest_path, file)
            
            if os.path.exists(src_file):
                try:
                    shutil.move(src_file, dest_file)
                    returned_files += 1
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to return {file}: {str(e)}")
        
        if returned_files > 0:
            messagebox.showinfo("Success", f"Returned {returned_files} {operation_name} files")
            self.load_previews()
    
    def move_eyes(self):
        eye_files = [
            "SUPER MARIO 64#5D6B0678#0#2_all.png",
            "SUPER MARIO 64#6B8D43C4#0#2_all.png",
            "SUPER MARIO 64#9FBECEF9#0#2_all.png"
        ]
        self.move_files("eyes", eye_files, "", "eyes")
    
    def return_eyes(self):
        eye_files = [
            "SUPER MARIO 64#5D6B0678#0#2_all.png",
            "SUPER MARIO 64#6B8D43C4#0#2_all.png",
            "SUPER MARIO 64#9FBECEF9#0#2_all.png"
        ]
        self.return_files("", eye_files, "eyes", "eyes")
    
    def move_cap(self):
        cap_file = ["SUPER MARIO 64#905D3214#0#2_all.png"]
        self.move_files("cap", cap_file, "", "cap logo")
    
    def return_cap(self):
        cap_file = ["SUPER MARIO 64#905D3214#0#2_all.png"]
        self.return_files("", cap_file, "cap", "cap logo")

if __name__ == "__main__":
    root = tk.Tk()
    app = NevritApp(root)
    root.mainloop()

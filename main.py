import tkinter as tk
from tkinter import ttk, filedialog, messagebox  # ✅ thêm messagebox
from datetime import datetime
from CAManimalS import start_monitoring_with_config, get_all_animal_names
from VIDandPIC import detect_animals_in_image, detect_animals_in_video

def open_config_window():
    config_window = tk.Toplevel(root)
    config_window.title("Cấu hình giám sát động vật")
    config_window.geometry("400x500")

    # Thời gian giám sát
    tk.Label(config_window, text="⏰ Thời gian bắt đầu (HH:MM):").pack()
    start_time_entry = tk.Entry(config_window)
    start_time_entry.pack()
    start_time_entry.insert(0, "00:00")

    tk.Label(config_window, text="⏰ Thời gian kết thúc (HH:MM):").pack()
    end_time_entry = tk.Entry(config_window)
    end_time_entry.pack()
    end_time_entry.insert(0, "23:59")

    # Danh sách động vật
    tk.Label(config_window, text="🐾 Chọn động vật muốn giám sát:").pack()

    frame = tk.Frame(config_window)
    frame.pack(expand=True, fill="both")

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    animal_entries = {}
    all_animals = get_all_animal_names()

    for animal in all_animals:
        row = tk.Frame(scroll_frame)
        row.pack(fill="x", pady=2)
        label = tk.Label(row, text=animal, width=25, anchor="w")
        label.pack(side="left")
        spin = tk.Spinbox(row, from_=0, to=10, width=5)
        spin.pack(side="left")
        animal_entries[animal] = spin

    # Nút Bắt đầu và Hủy
    def on_start_monitoring():
        try:
            start_time = datetime.strptime(start_time_entry.get(), "%H:%M").time()
            end_time = datetime.strptime(end_time_entry.get(), "%H:%M").time()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng thời gian HH:MM.")
            return

        selected_animals = {}
        for animal, spin in animal_entries.items():
            count = int(spin.get())
            if count > 0:
                selected_animals[animal] = count

        if not selected_animals:
            messagebox.showwarning("Chưa chọn động vật", "Vui lòng chọn ít nhất một loài động vật để giám sát.")
            return

        config_window.destroy()
        start_monitoring_with_config(selected_animals, start_time, end_time)

    tk.Button(config_window, text="▶️ Bắt đầu giám sát", command=on_start_monitoring).pack(pady=10)
    tk.Button(config_window, text="❌ Hủy", command=config_window.destroy).pack()

def on_detect_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if file_path:
        detect_animals_in_image(file_path)

def on_detect_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
    if file_path:
        detect_animals_in_video(file_path)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("🦁 Hệ thống Giám sát Động vật thông minh")
root.geometry("400x300")

tk.Label(root, text="CHỌN CHỨC NĂNG", font=("Helvetica", 16, "bold")).pack(pady=20)

tk.Button(root, text="🐾 Giám sát động vật", font=("Helvetica", 12), width=30, command=open_config_window).pack(pady=10)
tk.Button(root, text="🖼️ Nhận diện động vật với ảnh", font=("Helvetica", 12), width=30, command=on_detect_image).pack(pady=10)
tk.Button(root, text="🎞️ Nhận diện động vật với video", font=("Helvetica", 12), width=30, command=on_detect_video).pack(pady=10)

root.mainloop()

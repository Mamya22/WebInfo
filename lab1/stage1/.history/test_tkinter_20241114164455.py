import tkinter as tk

def start_tkinter():
    root = tk.Tk()
    root.title("Boolean Match System")
    root.geometry("1500x1000")
    mode_var = tk.StringVar(value="book")
    tk.Label(root, text="Select mode:").pack()
    tk.Radiobutton(root, text="Book", variable=mode_var, value="book").pack()
    tk.Radiobutton(root, text="Movie", variable=mode_var, value="movie").pack()

    tk.Label(root, text="Enter query:").pack()
    query_entry = tk.Entry(root, width=50)
    query_entry.pack()

    search_button = tk.Button(root, text="Search", command=search)
    search_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()
    root.mainloop()

if __name__ == "__main__":
    start_tkinter()
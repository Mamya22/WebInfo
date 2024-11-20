import tkinter as tk

def start_tkinter():
    def search():
        user_mode = mode_var.get()
        user_query = query_entry.get()
        # error = bm.Search(user_query, user_mode)
        # if error:
        #     result_label.config(text="Some error occurred in your query.", fg="red")
        # else:
        #     result_label.config(text="Search completed. Check console for details.", fg="green")
    root = tk.Tk()
    root.title("Boolean Match System")
    root.geometry("1500x1000")
    mode_var = tk.StringVar(value="book")
    tk.Label(root, text="Select mode:",font=("Arival",50)).pack()
    tk.Radiobutton(root, text="Book", variable=mode_var, value="book",font=("Arival",50)).pack()
    tk.Radiobutton(root, text="Movie", variable=mode_var, value="movie",font=("Arival",50)).pack()

    tk.Label(root, text="Enter query:",font=("Arival",50)).pack()
    query_entry = tk.Entry(root, width=100,font=("Arival",30))
    query_entry.pack()

    search_button = tk.Button(root, text="Search", command=search,font=("Arival",30))
    search_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()
    root.mainloop()
    return mode_var.get(), query_entry.get()

if __name__ == "__main__":
    mode,query = start_tkinter()
    print(mode,query)
import tkinter as tk
from tkinter import ttk, simpledialog

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do Neon")
        self.root.geometry("430x530")
        self.root.configure(bg="black")

        # Estilo neon
        style = ttk.Style()
        style.configure(
            "Treeview",
            background="black",
            foreground="#00ffff",
            fieldbackground="black",
            font=("Consolas", 13)
        )
        style.map("Treeview", background=[("selected", "#003333")])

        # Frame de entrada e botões
        top_frame = tk.Frame(root, bg="black")
        top_frame.pack(fill="x", padx=10, pady=10)

        # Campo de entrada
        self.entry = tk.Entry(
            top_frame, bg="#202020", fg="#00ffff",
            insertbackground="#00ffff", font=("Consolas", 13)
        )
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.add_task)

        # Botão adicionar
        self.add_button = tk.Button(
            top_frame, text="+", command=self.add_task,
            bg="#00ffff", fg="black", font=("Consolas", 14, "bold"),
            width=3
        )
        self.add_button.pack(side="left", padx=5)

        # Botão deletar
        self.delete_button = tk.Button(
            top_frame, text="🗑", command=self.delete_selected,
            bg="#00ffff", fg="black", font=("Consolas", 13, "bold"),
            width=3
        )
        self.delete_button.pack(side="left")

        # Lista de tarefas
        self.tree = ttk.Treeview(root, show="tree", selectmode="browse")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Vincular eventos
        self.tree.bind("<Button-1>", self.toggle_done)
        self.tree.bind("<Double-1>", self.edit_task)
        self.tree.bind("<ButtonPress-1>", self.start_drag)
        self.tree.bind("<B1-Motion>", self.drag_task)
        self.tree.bind("<ButtonRelease-1>", self.stop_drag)

        self.dragging_item = None
        self.done_items = set()

    # Adicionar tarefa
    def add_task(self, event=None):
        task = self.entry.get().strip()
        if task:
            new_item = self.tree.insert("", "end", text=task, tags=("task",))
            self.tree.tag_configure("task", background="#202020", foreground="#00ffff")
            self.entry.delete(0, "end")

    # Marcar como concluída (clique único)
    def toggle_done(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            if item in self.done_items:
                self.tree.item(item, tags=("task",))
                self.tree.tag_configure("task", foreground="#00ffff", font=("Consolas", 13))
                self.done_items.remove(item)
            else:
                self.tree.item(item, tags=("done",))
                self.tree.tag_configure("done", foreground="#00ffff", font=("Consolas", 13, "overstrike"))
                self.done_items.add(item)

    # Editar tarefa (duplo clique)
    def edit_task(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            current_text = self.tree.item(item, "text")
            new_text = simpledialog.askstring("Editar tarefa", "Edite o texto:", initialvalue=current_text)
            if new_text:
                self.tree.item(item, text=new_text)

    # Início do arraste
    def start_drag(self, event):
        self.dragging_item = self.tree.identify_row(event.y)

    # Reordenar tarefas
    def drag_task(self, event):
        if self.dragging_item:
            target = self.tree.identify_row(event.y)
            if target and target != self.dragging_item:
                parent = ""
                idx_target = self.tree.index(target)
                self.tree.move(self.dragging_item, parent, idx_target)

    # Fim do arraste
    def stop_drag(self, event):
        self.dragging_item = None

    # Deletar tarefa selecionada
    def delete_selected(self):
        selected = self.tree.selection()
        for item in selected:
            self.tree.delete(item)
            if item in self.done_items:
                self.done_items.remove(item)


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

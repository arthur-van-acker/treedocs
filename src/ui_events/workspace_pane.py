import os
from logic.workspace import set_last_selected_folder

def on_tree_select(tree):
    selected = tree.selection()
    if selected:
        node_id = selected[0]
        item_text = tree.item(node_id, 'text')
        if item_text.startswith('Workspace:'):
            set_last_selected_folder(None)
        else:
            values = tree.item(node_id, 'values')
            if values and len(values) > 0:
                path = values[0]
                if os.path.isdir(path):
                    set_last_selected_folder(path)

def populate_tree(tree, folder, parent="", prefix=""):
    try:
        entries = os.listdir(folder)
        entries.sort()
        for i, entry in enumerate(entries):
            path = os.path.join(folder, entry)
            is_last = (i == len(entries) - 1)
            ascii_prefix = prefix + ("└ " if is_last else "├ ")
            display_text = ascii_prefix + ("[" + entry + "]" if os.path.isdir(path) else entry)
            node = tree.insert(parent, "end", text=display_text, values=(path,), open=False)
            if os.path.isdir(path):
                new_prefix = prefix + ("    " if is_last else "│   ")
                populate_tree(tree, path, node, new_prefix)
    except Exception as e:
        tree.insert(parent, "end", text=f"Error: {e}")

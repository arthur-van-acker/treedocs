import tkinter as tk

def show_tip(widget, text, tipwindow_ref):
    if tipwindow_ref[0] or not text:
        return
    x, y, _, _ = widget.bbox("insert") if hasattr(widget, "bbox") else (0, 0, 0, 0)
    x = x + widget.winfo_rootx() + 40
    y = y + widget.winfo_rooty() + 10
    tipwindow_ref[0] = tw = tk.Toplevel(widget)
    tw.wm_overrideredirect(True)
    tw.wm_geometry(f"+{x}+{y}")
    label = tk.Label(tw, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=("tahoma", "8", "normal"))
    label.pack(ipadx=4)

def hide_tip(tipwindow_ref):
    tw = tipwindow_ref[0]
    tipwindow_ref[0] = None
    if tw:
        tw.destroy()

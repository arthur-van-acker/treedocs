from ui_events.tooltip import show_tip, hide_tip

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow_ref = [None]
        widget.bind("<Enter>", lambda _event: show_tip(self.widget, self.text, self.tipwindow_ref))
        widget.bind("<Leave>", lambda _event: hide_tip(self.tipwindow_ref))

"""
Test script for PreviewPane: loads sample .txt and .md files to verify display and formatting.
"""
import os
from ui.app_window import AppWindow

def create_sample_files():
    txt_path = 'sample_test.txt'
    md_path = 'sample_test.md'
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write('This is a sample text file.\nSecond line.')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('# Sample Markdown\n\n- Item 1\n- Item 2\n\n**Bold text** and `code`.')
    return txt_path, md_path

def run_preview_test():
    txt_path, md_path = create_sample_files()
    app = AppWindow()
    # Show .txt file in preview
    app.preview_pane.load_file_content(txt_path)
    app.after(2000, lambda: app.preview_pane.load_file_content(md_path))
    app.mainloop()

if __name__ == '__main__':
    run_preview_test()
from ui.app_window import AppWindow
import sys

def global_exception_hook(exctype, value, traceback):
	print(f'[GLOBAL EXCEPTION] {exctype.__name__}: {value}')
	import traceback as tb
	tb.print_tb(traceback)
	# Do not exit the app

sys.excepthook = global_exception_hook

if __name__ == "__main__":
	print('[MAIN] Starting AppWindow')
	app = AppWindow()
	print('[MAIN] Entering mainloop')
	app.mainloop()
	print('[MAIN] mainloop exited')




from pywinauto.application import Application

def open_app(file_path = "notepad.exe"):
  app = Application().start(file_path)
  return app

def select_menu(app_object = app.UntitledNotepad, menu_item = "Help->About Notepad"):
  app_object.menu_select(menu_item)

def click_item(app_object = app.AboutNotepad.OK):
  app_object.click()
  
def type_in(app_object = app.UntitledNotepad.Edit., data = "pywinauto Works!"):
  app_object.type_keys(data, with_spaces = True)
  
 

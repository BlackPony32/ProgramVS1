pyinstaller --onefile --noconsole ProgramPack/main.py
Pyrcc5 Image_resource.qrc -o Image_resource_rendered.py
pyinstaller --icon=ProgramPack\ProgramIco.ico --noconsole ProgramPack/main.py
pyinstaller main.spec

#основне вікно завантажується,далі додав фото(зарендерив

іконка не відображається в застосунку,нада пофіксить


ще перевірить ієрархію класів 
після цього решту вікон,роботу кнопок,далі базу даних)
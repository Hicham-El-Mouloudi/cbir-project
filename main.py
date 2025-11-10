from ui import MainUI
from logic import IndexDBCreator, Toolbox, ImageSearcher

toolbox = Toolbox()
indexDBCreator = IndexDBCreator(".\\dataset", toolbox)
imageSearcher = ImageSearcher("indexDB.json", toolbox)
mainUi = MainUI(imageSearcher=imageSearcher ,indexDBCreator=indexDBCreator, toolbox=toolbox)
mainUi.setupUI()
mainUi.startUI()
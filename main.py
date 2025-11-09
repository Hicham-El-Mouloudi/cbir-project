from ui import MainUI
from logic import IndexDBCreator, Toolbox

toolbox = Toolbox()
indexDBCreator = IndexDBCreator(".\\testData", toolbox)
mainUi = MainUI(indexDBCreator=indexDBCreator)
mainUi.setupUI()
mainUi.startUI()
from ui import MainUI
from logic import IndexDBCreator

indexDBCreator = IndexDBCreator(".\\testData")
mainUi = MainUI(indexDBCreator=indexDBCreator)
mainUi.setupUI()
mainUi.startUI()
"""
Visual GUI for the file renamer.

Author: Okane (Zinnia Scans)
    - Twitter: @Okaneeeeeeeee_e / @ZinniaScans
    - Github: https://github.com/Okaneeee
    - MangaDex: https://mangadex.org/group/8bd939e5-dbcd-4ec8-b105-e6a19e8d8862/zinnia-scans
"""

# imports
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QHBoxLayout, QLineEdit, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from fileRenamer import FileRenamer
from os import path, startfile

# classes
class popup(QWidget):
    def __init__(self, popupText: str, path: str = ...) -> None:
        # default
        super().__init__()
        self.resize(200, 80) ; self.setFixedSize(self.size())
        self.path = path

        # layouts
        self.mainLayout: QVBoxLayout = QVBoxLayout() ; self.setLayout(self.mainLayout)
        self.buttonsLayout: QHBoxLayout = QHBoxLayout()

        # widgets
        # --- warning message ---
        if (popupText == "warning"):
            self.setWindowTitle("Warning")
            self.setWindowIcon(QIcon("assets/warning.png"))
            self.pText: QLabel = QLabel("Something is wrong!")
        else:
            self.setWindowTitle("Notice")
            self.setWindowIcon(QIcon("assets/checkmark.png"))
            self.pText: QLabel = QLabel("Done!")

        self.pText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.pText)

        # --- close button ---
        if(popupText == "done"):
            self.openFolderButton: QPushButton = QPushButton("Open Folder")
            self.buttonsLayout.addWidget(self.openFolderButton)
            # signal
            self.openFolderButton.clicked.connect(self.openFolderCallback)

        self.closeButton: QPushButton = QPushButton("Close")
        self.buttonsLayout.addWidget(self.closeButton)

        self.mainLayout.addLayout(self.buttonsLayout)

        # signal
        self.closeButton.clicked.connect(self.closeCallback)

    # callbacks
    def closeCallback(self) -> None:
        self.close()

    def openFolderCallback(self) -> None:
        startfile(self.path)

class renameView(QWidget):
    def __init__(self) -> None:
        # default
        super().__init__()
        self.setWindowTitle("Files Renamer") ; self.setWindowIcon(QIcon("assets/icon.png"))
        self.resize(500, 250) ; self.setFixedSize(self.size())
        self.fr: FileRenamer = FileRenamer()

        # main layout
        self.topLayout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.topLayout)
        
        # QLine layout
        self.lineLayout1: QHBoxLayout = QHBoxLayout()
        self.lineLayout2: QHBoxLayout = QHBoxLayout()
        self.linesLayout: QVBoxLayout = QVBoxLayout()

        self.linesLayout.addLayout(self.lineLayout1) ; self.linesLayout.addLayout(self.lineLayout2)
        self.topLayout.addLayout(self.linesLayout)

        # Buttons layout
        self.buttonsLayout: QVBoxLayout = QVBoxLayout()
        self.topLayout.addLayout(self.buttonsLayout)

        self.downButtonsLayout: QHBoxLayout = QHBoxLayout()
        self.topLayout.addLayout(self.downButtonsLayout)

        # Folder selection layout
        self.folderLayout: QVBoxLayout = QVBoxLayout() ; self.folderLayout.addStretch()
        self.buttonsLayout.addLayout(self.folderLayout)

        # widgets
        # --- folder selection ---
        self.folderLoader: QPushButton = QPushButton("Select folder") ; self.folderLayout.addWidget(self.folderLoader)
        self.selectedFolder: QLabel = QLabel("No folder selected") ; self.folderLayout.addWidget(self.selectedFolder)
        self.selectedFolder.setAlignment(Qt.AlignmentFlag.AlignCenter) ; self.folderLayout.addStretch()

        # --- rename parameters ---
        self.startFileName: QLineEdit = QLineEdit() ; self.startFileName.setPlaceholderText("Name of the first file to rename (+1)")
        self.startFileName.setFixedWidth(235) ; self.lineLayout1.addWidget(self.startFileName)
        
        self.startNumber: QLineEdit = QLineEdit() ; self.startNumber.setPlaceholderText("Number of the first file to rename")
        self.startNumber.setFixedWidth(235) ; self.lineLayout1.addWidget(self.startNumber)
        
        self.renameFormat: QLineEdit = QLineEdit() ; self.renameFormat.setPlaceholderText("Format of the renamed files")
        self.renameFormat.setFixedWidth(235) ; self.lineLayout2.addWidget(self.renameFormat)
        
        self.fileExtension: QComboBox = QComboBox() ; self.fileExtension.addItems(["", ".jpg", ".jpeg", ".png ", ".psd" , ".txt"]) ; self.fileExtension.setEditable(True)
        self.fileExtension.setFixedWidth(235) ; self.lineLayout2.addWidget(self.fileExtension)
        
        # --- rename ---
        self.renameButton: QPushButton = QPushButton("Rename") ; self.buttonsLayout.addWidget(self.renameButton)

        # --- down buttons ---
        self.closeButton: QPushButton = QPushButton("Close")
        self.downButtonsLayout.addWidget(self.closeButton)

        # signals
        self.folderLoader.clicked.connect(self.open)
        self.renameButton.clicked.connect(self.rename)
        self.closeButton.clicked.connect(self.closeWindow)
        
        # show GUI
        self.show()

    # callbacks
    def open(self) -> None:
        folder = str(QFileDialog.getExistingDirectory(self, "Select Folder"))
        self.selectedFolder.setText(folder)

    def rename(self) -> None:
        # Texts
        folder: str = self.selectedFolder.text().strip() + '/'
        startFile: str = self.startFileName.text().strip()
        startNb: str = self.startNumber.text().strip()
        renameFrmt: str = self.renameFormat.text().strip()
        fileExt: str = self.fileExtension.currentText().strip()

        # Checks
        selectedFolderCheck: bool = (path.isdir(folder))
        startFileCheck: bool = bool(startFile)
        startNumberCheck: bool = bool(startNb.isdigit())
        renameFormatCheck: bool = bool(renameFrmt)
        fileExtCheck: bool = bool(fileExt) and ("." in self.fileExtension.currentText().strip()) and (self.fileExtension.currentText().strip() != ".")

        if(selectedFolderCheck and startFileCheck and startNumberCheck and renameFormatCheck and fileExtCheck):
            self.fr.rename(folder, fileExt, startFile, int(startNb), renameFrmt)
            self.popUp: popup = popup("done", folder) ; self.popUp.show()
        else:
            self.popUp: popup = popup("warning") ; self.popUp.show()

    def closeWindow(self) -> None:
        self.close()

# test
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from sys import argv, exit
    app: QApplication = QApplication(argv)
    window = renameView()

    # show GUI
    exit(app.exec())
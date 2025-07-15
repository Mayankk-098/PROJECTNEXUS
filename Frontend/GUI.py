from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy 
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os
env_vars=dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message =""
TempDirPath=rf"{current_dir}\Frontend\Files"
GraphicsDirPath=rf"{current_dir}\Frontend\Graphics"
def AnswerModifier(Answer):
    lines=Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer
def QueryModifier(Query):
    new_query= Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]
    if any(word + " " in new_query for word in question_words):
        
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words [-1][-1] in ['.', '?' '!']: 
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()
def SetMicrophoneStatus(Command):
    with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
        file.write(Command)
def GetMicrophoneStatus():
    with open(rf'{TempDirPath}\Mic.data', "r", encoding='utf-8') as file: 
        Status=file.read()
    return Status
def SetAssistantStatus (Status):
    with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
        file.write(Status)
def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status.data', "r", encoding='utf-8') as file: 
        Status = file.read()
    return Status
def MicButtonInitialed():
    SetMicrophoneStatus("False")
def MicButtonClosed():
    SetMicrophoneStatus("True")
def GraphicsDirectoryPath(Filename):
    Path = rf'{GraphicsDirPath}\{Filename}' 
    return Path
def TempDirectoryPath(Filename):
    Path = rf'{TempDirPath}\{Filename}' 
    return Path
def ShowTextToScreen(Text):
    with open(rf'{TempDirPath}\Responses.data', "w", encoding='utf-8') as file:
        file.write(Text)
class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Create the QTextEdit for chat messages
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)

        # Set the style for the chat section
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        # Set the font and text color for the chat
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)

        # Create the QLabel for the GIF
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        self.gif_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.gif_label.setScaledContents(True)
        self.gif_label.setMaximumSize(500,300)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setMovie(movie)
        movie.start()

        # Add the GIF to the layout
        layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)

        # Create the QLabel for the status messages
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-top: 10px; border: none;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)

        # Set the font for the chat text
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)

        # Set up a timer to load messages and update the status
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(100)  # Adjusted timer interval to 100ms
        self.chat_text_edit.viewport().installEventFilter(self)

        # Set the scrollbar style
        self.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                background: black;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                height: 10px;
            }
            QScrollBar::sub-line:vertical {
                background: black;
                subcontrol-position: top;
                subcontrol-origin: margin;
                height: 10px;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
                color: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
    
    def loadMessages(self):
        global old_chat_message
        with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file: 
            messages=file.read()
            if None==messages:
                pass
            elif len(messages)<= 1:
                pass
            elif str(old_chat_message)==str(messages):
                pass
            else:
                self.addMessage(message=messages, color='White') 
                old_chat_message = messages
    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file: 
            messages = file.read()
            self.label.setText(messages)
    def load_icon(self, path, width=60, height=60): 
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height) 
        self.icon_label.setPixmap(new_pixmap)
    def toggle_icon (self, event=None):
        if self.toggled:
            self.load_icon (GraphicsDirectoryPath('voice.png'), 60, 60) 
            MicButtonInitialed()
        else:  
            self.load_icon(GraphicsDirectoryPath('mic.png'), 60, 60)
            MicButtonClosed()
        self.toggled=not self.toggled
    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor() 
        format = QTextCharFormat()
        formatm=QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground (QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat (formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)
class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.primaryScreen()
        screen_width = desktop.size().width()
        screen_height = desktop.size().height()

        # Create the main layout
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 50)  # Added bottom margin

        # Create the QLabel for the GIF
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))

        # Set a fixed size for the GIF
        max_gif_width = 800  # Set the desired width
        max_gif_height = 800  # Reduced height to make more room
        movie.setScaledSize(QSize(max_gif_width, max_gif_height))  # Scale the GIF
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)  # Center the GIF
        gif_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        gif_label.setMaximumSize(max_gif_width, max_gif_height)  # Set maximum size

        movie.start()

        # Create a QLabel for the assistant status
        self.status_label = QLabel("Available ...")
        self.status_label.setStyleSheet("color: white; font-size: 16px; margin-bottom: 15px;")  # Increased margin
        self.status_label.setAlignment(Qt.AlignCenter)

        # Create a QPushButton for the microphone icon
        mic_button = QPushButton()
        mic_button.setIcon(QIcon(GraphicsDirectoryPath('Mic_on.png')))
        mic_button.setIconSize(QSize(70, 70))  # Increased icon size
        mic_button.setFixedSize(100, 100)  # Increased button size
        mic_button.setStyleSheet("border: none; background-color: transparent; margin-bottom: 30px;")  # Added margin
        mic_button.clicked.connect(self.toggle_icon)

        # Add the GIF, status label, and microphone to the layout
        content_layout.addStretch(1)  # Reduced top stretch
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addStretch(1)  # Adjusted middle stretch
        content_layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(mic_button, alignment=Qt.AlignCenter)
        content_layout.addStretch(1)  # Reduced bottom stretch

        # Set the layout and window properties
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")

        # Initialize microphone toggle state
        self.toggled = True

        # Set up a timer to update the status
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(100)  # Update every 100ms

    def update_status(self):
        with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
            status = file.read()
            self.status_label.setText(status)

    def load_icon(self, path, width=70, height=70):  # Updated default size
        # Update the microphone icon
        mic_button = self.findChild(QPushButton)
        if mic_button:
            mic_button.setIcon(QIcon(path))
            mic_button.setIconSize(QSize(width, height))

    def toggle_icon(self):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 70, 70)  # Updated size
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 70, 70)  # Updated size
            MicButtonClosed()
        self.toggled = not self.toggled

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        
        screen_height = desktop.screenGeometry().height() 
        layout=QVBoxLayout()
        label = QLabel("") 
        layout.addWidget(label)
        chat_section= ChatSection()
        layout.addWidget(chat_section) 
        self.setLayout(layout)
        self.setStyleSheet ("background-color: black;") 
        self.setFixedHeight (screen_height) 
        self.setFixedWidth(screen_width)
class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen= None 
        self.stacked_widget=stacked_widget
    def initUI(self):
    
        self.setFixedHeight(50)
        layout=QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        home_button= QPushButton()
        home_icon =QIcon(GraphicsDirectoryPath("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText(" Home")
        home_button.setStyleSheet ("height:40px; line-height: 40px; background-color: white; color: black") 
        message_button = QPushButton()
        message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText(" Chat")
        message_button.setStyleSheet("height:40px; line-height:40px; background-color: white; color: black")
        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicsDirectoryPath('Minimize2.png'))
        

        minimize_icon= QIcon (GraphicsDirectoryPath('Minimize2.png')) 
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet ("background-color:white")
        minimize_button.clicked.connect(self.minimizeWindow) 
        self.maximize_button = QPushButton()
        self.maximize_icon =QIcon (GraphicsDirectoryPath('Maximize.png')) 
        self.restore_icon =QIcon(GraphicsDirectoryPath('Minimize.png'))
        
        
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat (True)
        self.maximize_button.setStyleSheet ("background-color: white")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        close_button = QPushButton()
        close_icon = QIcon (GraphicsDirectoryPath('Close.png')) 
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:white") 
        close_button.clicked.connect(self.closeWindow)
        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape (QFrame.HLine) 
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: black;")
        title_label = QLabel(f" {str(Assistantname).capitalize()} AI    ")
        title_label.setStyleSheet("color: black; font-size: 18px;; background-color:white") 
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0)) 
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button) 
        layout.addWidget(self.maximize_button) 
        layout.addWidget(close_button)
        layout.addWidget(line_frame) 
        self.draggable = True 
        self.offset = None
    def paintEvent(self, event): 
        painter=QPainter(self) 
        painter.fillRect(self.rect(), Qt.white) 
        super().paintEvent(event)
    def minimizeWindow(self):
        self.parent().showMinimized()
    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)
    def closeWindow(self):
        self.parent().close()

        

    def mousePressEvent(self, event): 
        if self.draggable:
            self.offset=event.pos()
    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset 
            self.parent().move(new_pos)
    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        message_screen = MessageScreen(self) 
        layout= self.parent().layout() 
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen= message_screen
    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        initial_screen=InitialScreen(self) 
        layout = self.parent().layout() 
        if layout is not None:
            layout.addWidget(initial_screen)
        self.current_screen= initial_screen
class MainWindow(QMainWindow):
    

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint) 
        self.initUI()
    def initUI(self):
        desktop=QApplication.desktop()
        screen_width=  desktop.screenGeometry().width() 
        
        screen_height= desktop.screenGeometry().height() 
        stacked_widget=QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen() 
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen) 
        self.setGeometry(0, 0, screen_width, screen_height) 
        self.setStyleSheet ("background-color: black;") 
        top_bar=CustomTopBar(self, stacked_widget) 
        self.setMenuWidget(top_bar) 
        self.setCentralWidget(stacked_widget)
def GraphicalUserInterface():

    app=QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    GraphicalUserInterface()
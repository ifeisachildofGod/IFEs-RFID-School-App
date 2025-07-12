
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QApplication,
    QLineEdit, QPushButton, QScrollArea,
    QTableWidget, QLabel, QFrame,
    QAbstractItemView, QHeaderView, QMenu, QSizePolicy,
    QProgressBar, QCheckBox, QMainWindow,
    QStackedWidget, QMessageBox, QFileDialog, QToolBar,
    QRadioButton
)

import json
import os
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

# dark_theme = {
#   "palette": {
#     "Window": "#383838",
#     "WindowText": "#ffffff",
#     "Base": "#2d2d30",
#     "AlternateBase": "#3e3e42",
#     "ToolTipBase": "#f5f5f5",
#     "ToolTipText": "#111111",
#     "Text": "#ffffff",
#     "Button": "#3a3a3d",
#     "ButtonText": "#ffffff",
#     "BrightText": "#ff0000",
#     "Highlight": "#007acc",
#     "HighlightedText": "#ffffff",
#     "Link": "#3794ff",
#     "Light": "#2d2d30",
#     "Midlight": "#3e3e42",
#     "Dark": "#121212",
#     "Mid": "#2a2a2e",
#     "Shadow": "#000000"
#   },
#   "stylesheet": """
#     QWidget {
#       font-family: 'Segoe UI', sans-serif;
#       font-size: 14px;
#       background-color: #1e1e1e;
#       color: #ffffff;
#     }

#     QPushButton {
#       background-color: #0e639c;
#       color: white;
#       padding: 6px 12px;
#       border-radius: 4px;
#     }

#     QPushButton:hover {
#       background-color: #1177bb;
#     }

#     QPushButton:pressed {
#       background-color: #0b5081;
#     }

#     QLineEdit, QTextEdit, QPlainTextEdit {
#       background-color: #2d2d30;
#       color: #ffffff;
#       border: 1px solid #555;
#       border-radius: 4px;
#       padding: 4px;
#     }

#     QScrollBar:vertical {
#       background: #2d2d30;
#       width: 10px;
#     }

#     QScrollBar::handle:vertical {
#       background: #555;
#       min-height: 20px;
#       border-radius: 4px;
#     }

#     QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
#       height: 0px;
#     }

#     QToolTip {
#       background-color: #ffffff;
#       color: #000000;
#       border: 1px solid #aaaaaa;
#     }
#   """
# }

# light_theme = {
#   "palette": {
#     "Window": "#f5f5f5",
#     "WindowText": "#000000",
#     "Base": "#ffffff",
#     "AlternateBase": "#eaeaea",
#     "ToolTipBase": "#333333",
#     "ToolTipText": "#ffffff",
#     "Text": "#000000",
#     "Button": "#e0e0e0",
#     "ButtonText": "#000000",
#     "BrightText": "#ff0000",
#     "Highlight": "#0078d4",
#     "HighlightedText": "#ffffff",
#     "Link": "#0066cc",
#     "Light": "#ffffff",
#     "Midlight": "#eeeeee",
#     "Dark": "#cccccc",
#     "Mid": "#bbbbbb",
#     "Shadow": "#aaaaaa"
#   },
#   "stylesheet": """
#     QWidget {
#       font-family: 'Segoe UI', sans-serif;
#       font-size: 14px;
#       background-color: #f5f5f5;
#       color: #000000;
#     }

#     QPushButton {
#       background-color: #0078d4;
#       color: white;
#       padding: 6px 12px;
#       border-radius: 4px;
#     }

#     QPushButton:hover {
#       background-color: #2899f5;
#     }

#     QPushButton:pressed {
#       background-color: #005a9e;
#     }

#     QLineEdit, QTextEdit, QPlainTextEdit {
#       background-color: #ffffff;
#       color: #000000;
#       border: 1px solid #ccc;
#       border-radius: 4px;
#       padding: 4px;
#     }

#     QScrollBar:vertical {
#       background: #f5f5f5;
#       width: 10px;
#     }

#     QScrollBar::handle:vertical {
#       background: #999;
#       min-height: 20px;
#       border-radius: 4px;
#     }

#     QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
#       height: 0px;
#     }

#     QToolTip {
#       background-color: #333333;
#       color: #ffffff;
#       border: 1px solid #444444;
#     }
#   """
# }

# with open("dark.json", 'w') as f1:
#     json.dump(dark_theme, f1, indent=2)
# with open("light.json", 'w') as f2:
#     json.dump(light_theme, f2, indent=2)

stylesheet = '''
    QWidget {{
      background-color: {bg};
      color: {text};
      font-family: 'Segoe UI', sans-serif;
      font-size: 13px;
    }}

    QLineEdit, QTextEdit, QPlainTextEdit {{
      background-color: {input_bg};
      color: {text};
      border: 1px solid {input_border};
      border-radius: 5px;
      padding: 5px;
    }}

    QPushButton {{
      background-color: {primary};
      color: white;
      border: none;
      border-radius: 4px;
      padding: 6px 12px;
    }}

    QPushButton:hover {{
      background-color: {primary_hover};
    }}

    QPushButton:pressed {{
      background-color: {primary_pressed};
    }}

    QComboBox {{
      background-color: {input_bg};
      color: {text};
      border: 1px solid {input_border};
      border-radius: 4px;
      padding: 4px;
    }}

    QComboBox QAbstractItemView {{
      background-color: {input_bg};
      selection-background-color: {highlight};
    }}

    QCheckBox, QRadioButton {{
      spacing: 6px;
    }}

    QCheckBox::indicator, QRadioButton::indicator {{
      width: 14px;
      height: 14px;
    }}

    QScrollBar {{
      background: {bg};
      border: none;
    }}

    QScrollBar:vertical, QScrollBar:horizontal {{
      background: {bg};
      border: none;
      width: 10px;
    }}

    QScrollBar::handle {{
      background: {scrollbar};
      border-radius: 4px;
      min-height: 20px;
    }}

    QToolTip {{
      background-color: {tooltip_bg};
      color: {tooltip_text};
      border: 1px solid {border};
      padding: 5px;
      border-radius: 3px;
    }}

    QTabWidget::pane {{
      border: 1px solid {border};
    }}

    QTabBar::tab {{
      background: {secondary};
      color: {text};
      padding: 6px;
      border-top-left-radius: 4px;
      border-top-right-radius: 4px;
    }}

    QTabBar::tab:selected {{
      background: {input_bg};
      font-weight: bold;
    }}

    QMenu {{
      background-color: {input_bg};
      color: {text};
      border: 1px solid {border};
    }}

    QMenu::item:selected {{
      background-color: {highlight};
    }}

    QTableView {{
      background-color: {bg};
      color: {text};
      gridline-color: {border};
      selection-background-color: {highlight};
    }}

    QWidget.TeacherWidget * {{
        border: 2px solid red;
    }}
'''

class ThemeManager:
    def __init__(self):
        self.themes: dict[str, dict[str, dict[str, str] | str]] = {}
        self.current_theme = None

    def add_theme(self, name: str, theme_dict: dict):
        """Add a theme directly from a dict"""
        self.themes[name] = theme_dict

    def load_theme_from_file(self, file_path: str):
        """Load theme from a JSON file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Theme file not found: {file_path}")
        with open(file_path, 'r') as f:
            theme = json.load(f)
            for name, palette in theme.items():
                self.add_theme(name, {"palette": palette, "stylesheet": stylesheet})

    def apply_theme(self, app: QApplication, name: str):
        """Apply a stylesheet-only theme using values from JSON"""
        if name not in self.themes:
            raise ValueError(f"Theme '{name}' not loaded.")
        
        theme = self.themes[name]
        self.current_theme = name

        palette_vars = theme.get("palette")
        stylesheet_template = theme.get("stylesheet")

        # Inject palette variables into stylesheet using string formatting
        try:
            applied_stylesheet = stylesheet_template.format(**palette_vars)
        except KeyError as e:
            raise KeyError(f"Missing color value for: {e}")
        
        app.theme = theme
        app.setStyleSheet(applied_stylesheet)

    def get_current_theme(self):
        theme: dict[str, dict[str, str] | str] = self.themes.get(self.current_theme, None)
        
        return theme

    def get_theme_names(self):
        return list(self.themes.keys())

THEME_MANAGER = ThemeManager()
THEME_MANAGER.load_theme_from_file("themes.json")


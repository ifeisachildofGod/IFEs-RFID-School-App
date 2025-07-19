
import os
import json
from PyQt6.QtWidgets import QApplication


stylesheet = '''
  QWidget {{
    background-color: {bg};
    color: {text};
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    margin: 0px
  }}
  
  QLabel:disabled {{
    color: {disabled};
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
    color: {text};
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

  QMenu, .option-menu {{
    background-color: {input_bg};
    color: {text};
    border: 1px solid {border};
  }}
  
  .option-menu QPushButton {{
    border-radius: 0px;
    margin: 0px;
    border: none;
    background-color: {input_bg};
  }}
  
  .option-menu QPushButton:hover {{
    background-color: {highlight};
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
  
  QPushButton.VerticalTab {{
      width: 100%;
      height: 50px;
      border-radius: 0px;
      border-left: 3px solid {bg2};
      background-color: {bg2};
  }}
  
  QPushButton.VerticalTab:checked {{
      border-left-color: {primary};
      background-color: {secondary};
  }}
  
  QPushButton.VerticalTab:checked:hover {{
      background-color: {hover3};
  }}
  
  QPushButton.HorizontalTab {{
      width: 100%;
      height: 30px;
      border-top: 3px solid {bg2};
      background-color: {bg2};
      border-radius: 0px;
  }}
  
  QPushButton.HorizontalTab:hover {{
    border-top-color: {hover2};
    background-color: {hover2};
  }}
  
  QPushButton.HorizontalTab:checked {{
      border-top-color: {primary};
      background-color: {secondary};
  }}
  
  QPushButton.HorizontalTab:checked:hover {{
      background-color: {hover3};
  }}
  QCheckBox {{
      color: {text};
      spacing: 8px;
      padding: 4px;
  }}
  QCheckBox::indicator {{
      width: 18px;
      height: 18px;
      border-radius: 3px;
      border: 1px solid {border};
  }}
  QCheckBox::indicator:unchecked {{
      background-color: {bg};
  }}
  QCheckBox::indicator:checked {{
      background-color: {primary};
      border-color: {primary};
  }}
  QCheckBox::indicator:hover {{
      border-color: {primary_hover};
  }}

  .labeled-widget {{
    border: 1px solid {hover3};
  }}
  .labeled-widget:disabled {{
    border: 1px solid {disabled};
  }}
  
  .labeled-title {{
		color: {hover3};
  }}
  .labeled-title:disabled {{
		color: {disabled};
  }}
  
  .options-button {{
    font-size: 25px;
  }}
  
  QWidget.AttendanceTeacherWidget *, QWidget.EditorTeacherWidget * {{
      background-color: {teacher};
  }}
  
  QWidget.AttendancePrefectWidget *, QWidget.EditorPrefectWidget * {{
    background-color: {prefect};
  }}
  
  QWidget.EditorTeacherWidget,
  QWidget.EditorPrefectWidget,
  QWidget.AttendanceTeacherWidget,
  QWidget.AttendancePrefectWidget
  {{
    border-radius: 25px;
    padding: 50px;
    border: 2px solid grey;
  }}
  
  QWidget.EditorTeacherWidget * QLabel,
	QWidget.AttendanceTeacherWidget * QLabel
  {{
		color: white;
	}}
  
  QWidget.EditorPrefectWidget * QLabel,
  QWidget.AttendancePrefectWidget * QLabel
  {{
		color: black;
	}}
 
  QWidget.EditorTeacherWidget * .labeled-title,
  QWidget.EditorTeacherWidget * .options-button,
  QWidget.AttendanceTeacherWidget * .labeled-title,
  QWidget.AttendanceTeacherWidget * .options-button
  {{
		color: {title_text_teacher};
	}}
 
  QWidget.EditorPrefectWidget * .labeled-title,
  QWidget.EditorPrefectWidget * .options-button,
  QWidget.AttendancePrefectWidget * .labeled-title,
  QWidget.AttendancePrefectWidget * .options-button
  {{
		color: {title_text_prefect};
	}}
  
  QWidget.AttendanceTeacherWidget * .labeled-widget,
  QWidget.EditorTeacherWidget * .labeled-widget
  {{
    border: 1px solid {title_text_teacher};
  }}
  
  QWidget.AttendancePrefectWidget * .labeled-widget,
  QWidget.EditorPrefectWidget * .labeled-widget
  {{
    border: 1px solid {title_text_prefect};
  }}
  
  .labeled-title {{
    font-size: 11px;
    padding: 0 4px;
    padding-bottom: 0px;
  }}
  
  .labeled-widget {{
    border-radius: 6px;
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
            raise KeyError(f"Missing color value for: {e} on line {stylesheet_template[:stylesheet_template.find(str(e))].count("\n") + 1}")
        
        app.theme = theme
        app.setStyleSheet(applied_stylesheet)

    def get_current_theme(self):
        theme: dict[str, dict[str, str] | str] = self.themes.get(self.current_theme, None)
        
        return theme
    
    def get_current_palette(self):
      theme = self.get_current_theme()
      
      if theme is not None:
        return theme["palette"]

    def get_theme_names(self):
        return list(self.themes.keys())

THEME_MANAGER = ThemeManager()
THEME_MANAGER.load_theme_from_file("theme/themes.json")


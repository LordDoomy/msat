import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QGridLayout, QLabel, QPushButton, 
                               QLineEdit, QFrame, QDialog, QMessageBox, QFileDialog,
                               QScrollArea, QMenu, QRadioButton, QButtonGroup)
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QSize, QRect
from PySide6.QtGui import QFont, QColor, QCursor, QIcon
import pygame
import os
import json
import threading

# Gestor de los idiomas, carga archivos JSON de la carpeta lang y proporciona traducciones mediante la función i18n(key).
class LanguageManager:
    def __init__(self, lang="es"):
        self.lang = lang
        self.translations = {}
        self.load_language(lang)
    
    def load_language(self, lang):
        lang_file = os.path.join("lang", f"{lang}.json")
        try:
            with open(lang_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
                self.lang = lang
        except Exception:
            print(f"Error cargando idioma {lang}, usando español")
            with open(os.path.join("lang", "es.json"), "r", encoding="utf-8") as f:
                self.translations = json.load(f)
                self.lang = "es"
    
    def get(self, key, default=""):
        return self.translations.get(key, default)
    
    def get_available_languages(self):
        langs = {}
        lang_dir = "lang"
        if os.path.exists(lang_dir):
            for file in os.listdir(lang_dir):
                if file.endswith(".json"):
                    lang_code = file.replace(".json", "")
                    langs[lang_code] = lang_code.upper()
        return langs

# Idioma por defecto (cargado al iniciar la aplicación)
lang_manager = LanguageManager("es")

def i18n(key):
    return lang_manager.get(key)

# Paleta de colores
BG          = "#060608"
BG_PANEL    = "#0c0c0f"
BG_ENTRY    = "#12100a"
ORANGE      = "#FF6B00"
ORANGE_GLOW = "#FF8C2A"
ORANGE_DIM  = "#7A3300"
ORANGE_DARK = "#3D1900"
TEXT_DIM    = "#4a2200"
GREEN_DOT   = "#00FF88"

THEMES = {
    "orange": {
        "accent": "#FF6B00",
        "accent_glow": "#FF8C2A",
        "accent_dim": "#7A3300",
        "accent_dark": "#3D1900"
    },
    "cyan": {
        "accent": "#00D0FF",
        "accent_glow": "#7CEBFF",
        "accent_dim": "#1D6D7A",
        "accent_dark": "#103E47"
    },
    "purple": {
        "accent": "#BB42FF",
        "accent_glow": "#D684FF",
        "accent_dim": "#6C2F74",
        "accent_dark": "#3B1541"
    },
    "lime": {
        "accent": "#9CFF00",
        "accent_glow": "#D3FF66",
        "accent_dim": "#728B1C",
        "accent_dark": "#3B490A"
    }
}
DEFAULT_THEME = "orange"
RED_STOP    = "#CC2200"
RED_DIM     = "#5a0e00"


FONT_FAMILY = "Helvetica"
FONT_LOGO = (FONT_FAMILY, 70, QFont.Bold)
FONT_BIG_TITLE = (FONT_FAMILY, 40, QFont.Bold)
FONT_TITLE = (FONT_FAMILY, 13, QFont.Bold)
FONT_HEAD  = (FONT_FAMILY, 11, QFont.Bold)
FONT_BTN   = (FONT_FAMILY, 10, QFont.Bold)
FONT_SMALL = (FONT_FAMILY, 8)
FONT_TINY  = (FONT_FAMILY, 7)

CONFIG_FILE = "msat_audio_config.json"
LANGUAGE_CONFIG = "msat_language_config.json"
AUDIO_FOLDER = "audio_files"
COLS        = 3   # columnas en la cuadrícula de botones


# Panel del Botón Añadir
class AddButtonPanel(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        self.setWindowTitle(i18n("add_module_title"))
        self.setGeometry(0, 0, 480, 110)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel(i18n("add_new_module"))
        font = QFont(*FONT_HEAD)
        title.setFont(font)
        title.setStyleSheet(f"color: {ORANGE};")
        layout.addWidget(title)
        
        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background-color: {ORANGE_DARK};")
        layout.addWidget(sep)
        
        # Body
        body_layout = QVBoxLayout()
        
        # Nombre
        name_label = QLabel(i18n("label_name"))
        name_label.setStyleSheet(f"color: {ORANGE_DIM};")
        body_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {BG_ENTRY};
                color: {ORANGE};
                border: 1px solid {ORANGE_DARK};
                padding: 4px;
            }}
        """)
        body_layout.addWidget(self.name_input)
        
        # Ruta de archivo
        path_label = QLabel(i18n("label_audio_path"))
        path_label.setStyleSheet(f"color: {ORANGE_DIM};")
        body_layout.addWidget(path_label)
        
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {BG_ENTRY};
                color: {ORANGE};
                border: 1px solid {ORANGE_DARK};
                padding: 4px;
            }}
        """)
        path_layout.addWidget(self.path_input)
        
        browse_btn = QPushButton(f"[ {i18n('browse')} ]")
        browse_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_PANEL};
                color: {ORANGE};
                border: none;
                padding: 3px 6px;
                font: bold 8pt "{FONT_FAMILY}";
            }}
            QPushButton:hover {{
                background-color: {ORANGE_GLOW};
                color: {BG};
            }}
        """)
        browse_btn.clicked.connect(self.browse_file)
        path_layout.addWidget(browse_btn)
        body_layout.addLayout(path_layout)
        
        layout.addLayout(body_layout)
        
        # Botones de confirmación
        btn_layout = QHBoxLayout()
        
        confirm_btn = QPushButton(f"[ {i18n('confirm')} ]")
        confirm_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ORANGE};
                color: {BG};
                border: none;
                padding: 6px;
                font: bold 10pt "{FONT_FAMILY}";
            }}
            QPushButton:hover {{
                background-color: {ORANGE_GLOW};
            }}
        """)
        confirm_btn.clicked.connect(self.confirm)
        btn_layout.addWidget(confirm_btn)
        
        cancel_btn = QPushButton(f"[ {i18n('cancel')} ]")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_PANEL};
                color: {ORANGE};
                border: none;
                padding: 6px;
                font: bold 10pt "{FONT_FAMILY}";
            }}
            QPushButton:hover {{
                background-color: {ORANGE_GLOW};
                color: {BG};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.setStyleSheet(f"QDialog {{ background-color: {BG_PANEL}; }}")

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            i18n("select_audio_file"),
            "",
            f"{i18n('audio_files')} (*.mp3 *.wav *.ogg *.flac *.m4a *.aac);;{i18n('all_files')} (*.*)")
        if path:
            import shutil
            filename = os.path.basename(path)
            dest_path = os.path.join(AUDIO_FOLDER, filename)
            try:
                shutil.copy2(path, dest_path)
                self.path_input.setText(filename)
            except Exception as e:
                QMessageBox.critical(self, i18n("copy_error"),
                                   i18n("could_not_copy") + f"\n{e}")

    def confirm(self):
        name = self.name_input.text().strip()
        filename = self.path_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, i18n("input_error"), i18n("name_empty"))
            return
        if not filename:
            QMessageBox.warning(self, i18n("input_error"), i18n("file_required"))
            return
        
        full_path = os.path.join(AUDIO_FOLDER, filename)
        if not os.path.exists(full_path):
            QMessageBox.warning(self, i18n("file_error"), 
                              i18n("file_not_found") + f"\n{full_path}")
            return
        
        self.result = {"name": name, "path": filename}
        self.accept()


#  Dialogo de información del sistema
class SystemInfo(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        # ... otros atributos ...
        self.scroll_area = None
        self.btn_grid = None
        self.btn_grid_widget = None
        self.right_panel = None
        self.module_count_lbl = None
        self.status_label = None
        self.stop_all_btn = None
        self.setWindowTitle(i18n("system_info"))
        self.setGeometry(0, 0, 600, 100)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel(i18n("app_title"))
        font = QFont(*FONT_TITLE)
        title.setFont(font)
        title.setStyleSheet(f"color: {ORANGE}; padding: 5px;")
        layout.addWidget(title)
        
        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background-color: {ORANGE_DARK};")
        layout.addWidget(sep)
        
        # Información del sistema
        body_layout = QVBoxLayout()
        rows = [
            (i18n("version"),    i18n("version_num")),
            (i18n("build_date"), i18n("build_date_num")),
            (i18n("platform"),   i18n("platform_val")),
            (i18n("status"),     i18n("status_val")),
            (i18n("developer"),  i18n("developer_val")),
            (i18n("author"),     i18n("author_val")),
            (i18n("division"),   i18n("division_val")),
            (i18n("contact"),    i18n("contact_val")),
            (i18n("clearance"),  i18n("clearance_val")),
            (i18n("info_retro"), i18n("info_instant")),
        ]
        for k, v in rows:
            if not k and not v:
                body_layout.addSpacing(4)
                continue
            row = QHBoxLayout()
            if k:
                label_key = QLabel(f"{k:<12}")
                label_key.setStyleSheet(f"color: {ORANGE_DIM};")
                label_key.setFont(QFont(*FONT_SMALL))
                row.addWidget(label_key)
                text = f":  {v}"
            else:
                text = f"   {v}"
            
            label_val = QLabel(text)
            label_val.setStyleSheet(f"color: {ORANGE};")
            label_val.setFont(QFont(*FONT_TINY))
            row.addWidget(label_val)
            body_layout.addLayout(row)
        
        layout.addLayout(body_layout)
        
        # Separador final
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setStyleSheet(f"background-color: {ORANGE_DARK};")
        layout.addWidget(sep2)
        
        # Botón de cierre
        close_btn = QPushButton(i18n("close_terminal"))
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_PANEL};
                color: {ORANGE};
                border: none;
                padding: 6px;
                font: bold 10pt "{FONT_FAMILY}";
            }}
            QPushButton:hover {{
                background-color: {ORANGE};
                color: {BG};
            }}
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        self.setStyleSheet(f"QDialog {{ background-color: {BG_PANEL}; }}")


class SettingsDialog(QDialog):
    def __init__(self, parent, selected_theme, selected_language):
        super().__init__(parent)
        self.selected_theme = selected_theme
        self.selected_language = selected_language
        self.setWindowTitle(i18n("configuration"))
        self.setGeometry(0, 0, 520, 260)
        self.setModal(True)

        layout = QVBoxLayout()

        title = QLabel(i18n("configuration"))
        title.setFont(QFont(*FONT_HEAD))
        title.setStyleSheet(f"color: {ORANGE};")
        layout.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background-color: {ORANGE_DARK};")
        layout.addWidget(sep)

        color_label = QLabel(i18n("choose_color"))
        color_label.setFont(QFont(*FONT_SMALL))
        color_label.setStyleSheet(f"color: {ORANGE_DIM};")
        layout.addWidget(color_label)

        theme_layout = QHBoxLayout()
        self.theme_group = QButtonGroup(self)
        self.theme_buttons = []
        for theme_id in THEMES.keys():
            theme_name = i18n(f"theme_{theme_id}") or theme_id.capitalize()
            button = QRadioButton(theme_name)
            button.setStyleSheet(self._radio_style())
            button.theme_id = theme_id
            if theme_id == selected_theme:
                button.setChecked(True)
            button.toggled.connect(self._preview_theme)
            self.theme_group.addButton(button)
            self.theme_buttons.append(button)
            theme_layout.addWidget(button)
        layout.addLayout(theme_layout)

        lang_label = QLabel(i18n("choose_language"))
        lang_label.setFont(QFont(*FONT_SMALL))
        lang_label.setStyleSheet(f"color: {ORANGE_DIM};")
        layout.addWidget(lang_label)

        language_layout = QHBoxLayout()
        self.language_group = QButtonGroup(self)
        self.language_buttons = []
        for lang_code, lang_name in lang_manager.get_available_languages().items():
            label_text = i18n(lang_code) if i18n(lang_code) else lang_name.upper()
            button = QRadioButton(label_text)
            button.setStyleSheet(self._radio_style())
            button.lang_code = lang_code
            if lang_code == selected_language:
                button.setChecked(True)
            self.language_group.addButton(button)
            self.language_buttons.append(button)
            language_layout.addWidget(button)
        layout.addLayout(language_layout)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.cancel_btn = QPushButton(f"[ {i18n('cancel')} ]")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        self.confirm_btn = QPushButton(f"[ {i18n('confirm')} ]")
        self.confirm_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.confirm_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.setStyleSheet(f"QDialog {{ background-color: {BG_PANEL}; }}")
        self._update_preview_theme()

    def _radio_style(self):
        return f"""
            QRadioButton {{
                color: {ORANGE};
                spacing: 8px;
                padding: 4px;
            }}
            QRadioButton::indicator {{
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 1px solid {ORANGE};
                background: transparent;
            }}
            QRadioButton::indicator:checked {{
                background-color: {ORANGE};
                border: 1px solid {ORANGE};
            }}
        """

    def _update_preview_theme(self):
        preview_theme = self.selected_theme
        for button in self.theme_group.buttons():
            if button.isChecked():
                preview_theme = button.theme_id
                break
        colors = THEMES.get(preview_theme, THEMES[DEFAULT_THEME])
        accent = colors["accent"]
        accent_dark = colors["accent_dark"]
        accent_dim = colors["accent_dim"]

        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_PANEL};
                color: {accent};
                border: 1px solid {accent_dark};
                padding: 6px;
                font: bold 10pt \"{FONT_FAMILY}\";
            }}
            QPushButton:hover {{
                background-color: {accent};
                color: {BG};
            }}
        """)

        self.confirm_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {accent};
                color: {BG};
                border: none;
                padding: 6px;
                font: bold 10pt \"{FONT_FAMILY}\";
            }}
            QPushButton:hover {{
                background-color: {colors['accent_glow']};
            }}
        """)

        for button in self.theme_buttons + self.language_buttons:
            button.setStyleSheet(self._radio_style())

    def _preview_theme(self):
        self._update_preview_theme()

    def accept(self):
        selected_theme = self.selected_theme
        for button in self.theme_group.buttons():
            if button.isChecked():
                selected_theme = button.theme_id
                break
        selected_lang = self.selected_language
        for button in self.language_group.buttons():
            if button.isChecked():
                selected_lang = button.lang_code
                break
        self.selected_theme = selected_theme
        self.selected_language = selected_lang
        super().accept()


# Aplicación principal
class MentorAudioApp(QMainWindow):
    #Aplicar estilos generales a la aplicación
    def _apply_styles(self):
            stylesheet = f"""
                QWidget {{
                    background-color: {BG};
                    color: {ORANGE};
                }}
                QLabel {{
                    color: {ORANGE};
                }}
                QPushButton {{
                    background-color: {BG_PANEL};
                    color: {ORANGE};
                    border: none;
                    padding: 6px;
                }}
                QPushButton:hover {{
                    background-color: {ORANGE};
                    color: {BG};
                }}
                QLineEdit {{
                    background-color: {BG_ENTRY};
                    color: {ORANGE};
                    border: 1px solid {ORANGE_DARK};
                    padding: 4px;
                }}
            """
            self.setStyleSheet(stylesheet)

    # Inicializa la aplicación, carga configuraciones, configura la interfaz y maneja la lógica de reproducción y estado de los botones.
    def __init__(self):
        super().__init__()
        self.buttons_data = []
        self.blink_state  = True
        self.playing_idx  = None   # Índice del botón actualmente reproduciendo, o None si no hay ninguno
        self.btn_refs     = {}     # Diccionario para almacenar referencias a widgets de cada botón por índice, ej: {0: {"btn": ..., "outer": ..., "name": ...}, ...}
        self.theme        = DEFAULT_THEME
        self.language     = "es"
        
        # Cargar preferencias de idioma y tema antes de aplicar estilos
        self._load_preferences()
        self._apply_styles()
        
        # Crear carpeta de audios si no existe
        if not os.path.exists(AUDIO_FOLDER):
            os.makedirs(AUDIO_FOLDER)
        
        self._load_config()

        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Configurar la ventana principal
        self.setWindowTitle(i18n("app_title"))
        self.setGeometry(100, 100, 960, 640)
        self.setMinimumSize(700, 480)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Aplicar estilo oscuro
        self._apply_styles()

        self._build_ui()
        self._start_blink()
        self._poll_music()
        self.show()

    # Persistencia de idioma y tema
    def _load_preferences(self):
        try:
            with open(LANGUAGE_CONFIG) as f:
                config = json.load(f)
                self.language = config.get("language", "es")
                self.theme = config.get("theme", DEFAULT_THEME)
        except Exception:
            self.language = "es"
            self.theme = DEFAULT_THEME

        self._apply_theme(self.theme)
        lang_manager.load_language(self.language)

    def _save_preferences(self):
        try:
            with open(LANGUAGE_CONFIG, "w") as f:
                json.dump({"language": self.language, "theme": self.theme}, f, indent=2)
        except Exception:
            pass

    def _apply_theme(self, theme_name):
        theme = THEMES.get(theme_name, THEMES[DEFAULT_THEME])
        global ORANGE, ORANGE_GLOW, ORANGE_DIM, ORANGE_DARK, TEXT_DIM
        ORANGE = theme["accent"]
        ORANGE_GLOW = theme["accent_glow"]
        ORANGE_DIM = theme["accent_dim"]
        ORANGE_DARK = theme["accent_dark"]
        TEXT_DIM = theme["accent_dim"]
        self.theme = theme_name

    def _change_language(self, lang):
        self._stop_all()
        self.language = lang
        lang_manager.load_language(lang)
        self._save_preferences()
        self.setWindowTitle(i18n("app_title"))
        self._rebuild_ui()

    # Reconstruye la interfaz con el nuevo idioma
    def _rebuild_ui(self):

        # Limpiar el widget central
        central_widget = self.centralWidget()
        if central_widget:
            central_widget.deleteLater()
        
        # Crear nuevo widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        self._build_ui()

    # Cargar configuración de botones desde un archivo JSON. Si hay un error, se inicializa con una lista vacía.
    def _load_config(self):
        try:
            with open(CONFIG_FILE) as f:
                self.buttons_data = json.load(f)
        except Exception:
            self.buttons_data = []

    # Guardar configuración de botones en un archivo JSON. Si hay un error, se ignora.
    def _save_config(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.buttons_data, f, indent=2)
        except Exception:
            pass

    # Construye la interfaz principal con cabecera, cuerpo y barra de estado.
    def _build_ui(self):
        # Widget central
        central_widget = self.centralWidget()        
        main_layout = central_widget.layout()
        
        # Cabecera
        self._build_header()
        
        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background-color: {ORANGE}; min-height: 2px;")
        main_layout.addWidget(sep)
        
        # Cuerpo
        self._build_body()
        
        # Barra de estado
        self._build_statusbar()

    #Menú desplegable personalizado para INFO.
    def _show_info_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {BG_PANEL};
                color: {ORANGE};
                border: 1px solid {ORANGE_DARK};
            }}
            QMenu::item:selected {{
                background-color: {ORANGE};
                color: {BG};
            }}
        """)
        
        # Opción de configuración
        config_action = menu.addAction("// " + i18n("configuration"))
        config_action.triggered.connect(self._cmd_settings)
        
        menu.addSeparator()
        
        # Opción de información del sistema
        info_action = menu.addAction("// " + i18n("system_info"))
        info_action.triggered.connect(self._cmd_about)
        
        menu.addSeparator()
        
        # Opción de salir
        exit_action = menu.addAction("// " + i18n("exit"))
        exit_action.triggered.connect(self.close)
        
        menu.setMinimumWidth(220)
        menu.exec(pos)
    
    def _cmd_settings(self):
        dlg = SettingsDialog(self, selected_theme=self.theme, selected_language=self.language)
        if dlg.exec() == QDialog.Accepted:
            theme_changed = dlg.selected_theme != self.theme
            language_changed = dlg.selected_language != self.language
            if theme_changed:
                self._stop_all()
                self._apply_theme(dlg.selected_theme)
                self.theme = dlg.selected_theme
            if language_changed:
                self._stop_all()
                self.language = dlg.selected_language
                lang_manager.load_language(self.language)
            if theme_changed or language_changed:
                self._save_preferences()
                self.setWindowTitle(i18n("app_title"))
                self._rebuild_ui()
    
    #Muestra/oculta el panel derecho de sistema.
    def _toggle_system_panel(self):
        if self.right_panel.isVisible():
            self.right_panel.hide()
        else:
            self.right_panel.show()

    # Cabecera con logo, título, menú y estado de la estación.
    def _build_header(self):
        central_widget = self.centralWidget()
        main_layout = central_widget.layout()
        
        hdr = QWidget()
        hdr_layout = QHBoxLayout()
        hdr.setLayout(hdr_layout)
        hdr.setStyleSheet(f"background-color: {BG}; padding: 10px 22px;")
        
        # Logo MS
        logo_box = QFrame()
        logo_box.setStyleSheet(f"background-color: {ORANGE}; padding: 1px;")
        logo_inner = QLabel("MS")
        logo_inner.setFont(QFont(*FONT_LOGO))
        logo_inner.setStyleSheet(f"color: {ORANGE}; background-color: {BG}; padding: 5px; margin: 0px;")
        logo_layout = QVBoxLayout()
        logo_layout.addWidget(logo_inner)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_box.setLayout(logo_layout)
        hdr_layout.addWidget(logo_box)
        
        # Título y subtítulo
        title_col = QWidget()
        title_layout = QVBoxLayout()
        title_col.setLayout(title_layout)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        main_title = QLabel("M.S.A.T.")
        main_title.setFont(QFont(*FONT_BIG_TITLE))
        main_title.setStyleSheet(f"color: {ORANGE};")
        title_layout.addWidget(main_title)
        
        sub_title = QLabel("Mentor  Studios  Audio  Terminal  v1.0")
        sub_title.setFont(QFont(*FONT_SMALL))
        sub_title.setStyleSheet(f"color: {ORANGE_DIM};")
        title_layout.addWidget(sub_title)
        
        hdr_layout.addWidget(title_col)
        hdr_layout.addStretch()
        
        # Botones y estado en la derecha
        right_col = QWidget()
        right_layout = QVBoxLayout()
        right_col.setLayout(right_layout)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Botones de menú
        menu_frame = QWidget()
        menu_layout = QHBoxLayout()
        menu_frame.setLayout(menu_layout)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        
        btn_system = QPushButton(i18n("system"))
        btn_system.setFont(QFont(*FONT_SMALL))
        btn_system.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG};
                color: {ORANGE};
                border: none;
                padding: 2px 6px;
            }}
            QPushButton:hover {{
                color: {ORANGE_GLOW};
            }}
        """)
        btn_system.clicked.connect(self._toggle_system_panel)
        menu_layout.addWidget(btn_system)
        
        btn_info = QPushButton(i18n("info"))
        btn_info.setFont(QFont(*FONT_SMALL))
        btn_info.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG};
                color: {ORANGE};
                border: none;
                padding: 2px 6px;
            }}
            QPushButton:hover {{
                color: {ORANGE_GLOW};
            }}
        """)
        btn_info.clicked.connect(lambda: self._show_info_menu(btn_info.mapToGlobal(btn_info.rect().bottomLeft())))
        menu_layout.addWidget(btn_info)
        
        right_layout.addWidget(menu_frame)
        
        # Estado de la estación
        status_frame = QWidget()
        status_layout = QVBoxLayout()
        status_frame.setLayout(status_layout)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(0)
        
        for line in (i18n("station"), i18n("sector"), i18n("crew")):
            label = QLabel(line)
            label.setFont(QFont(*FONT_TINY))
            label.setStyleSheet(f"color: {ORANGE_DIM};")
            label.setAlignment(Qt.AlignRight)
            status_layout.addWidget(label)
        
        right_layout.addWidget(status_frame)
        
        hdr_layout.addWidget(right_col)
        
        main_layout.addWidget(hdr)
            
    # Cuerpo principal dividido en panel de botones (izquierda) y panel de sistema (derecha).
    def _build_body(self):
        central_widget = self.centralWidget()
        main_layout = central_widget.layout()
        
        body = QWidget()
        body_layout = QHBoxLayout()
        body.setLayout(body_layout)
        body.setStyleSheet(f"background-color: {BG};")
        
        # Izquierda: panel de botones
        left = QWidget()
        left_layout = QVBoxLayout()
        left.setLayout(left_layout)
        
        sub = QWidget()
        sub_layout = QHBoxLayout()
        sub.setLayout(sub_layout)
        sub_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(i18n("main_audio_control"))
        title_label.setFont(QFont(*FONT_HEAD))
        title_label.setStyleSheet(f"color: {ORANGE};")
        sub_layout.addWidget(title_label)
        
        self.module_count_lbl = QLabel("")
        self.module_count_lbl.setFont(QFont(*FONT_SMALL))
        self.module_count_lbl.setStyleSheet(f"color: {ORANGE_DIM};")
        sub_layout.addStretch()
        sub_layout.addWidget(self.module_count_lbl)
        left_layout.addWidget(sub)
        
        # Área de botones con scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {BG};
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {ORANGE_DARK};
                width: 12px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {ORANGE};
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {ORANGE_GLOW};
            }}
        """)
        
        self.btn_grid_widget = QWidget()
        self.btn_grid = QGridLayout()
        self.btn_grid.setSpacing(9)
        self.btn_grid.setContentsMargins(0, 0, 0, 0)
        self.btn_grid_widget.setLayout(self.btn_grid)
        self.scroll_area.setWidget(self.btn_grid_widget)
        self.scroll_area.setWidgetResizable(True)
        left_layout.addWidget(self.scroll_area)
        
        body_layout.addWidget(left, 1)
        
        # Derecha: panel de estado del sistema
        self.right_panel = QWidget()
        self.right_panel.setMaximumWidth(200)
        right_layout = QVBoxLayout()
        self.right_panel.setLayout(right_layout)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Panel de estado
        status_box = QFrame()
        status_box.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_PANEL};
                border: 1px solid {ORANGE_DARK};
            }}
        """)
        status_layout = QVBoxLayout()
        status_box.setLayout(status_layout)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        status_title = QLabel("// " + i18n("system_status"))
        status_title.setFont(QFont(*FONT_SMALL))
        status_title.setStyleSheet(f"color: {ORANGE_DIM}; padding: 6px;")
        status_layout.addWidget(status_title)
        
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background-color: {ORANGE_DARK};")
        status_layout.addWidget(sep)
        
        for k, v in [(i18n("mixer"), i18n("mixer_val")), 
                     (i18n("channels"), i18n("channels_val")), 
                     (i18n("freq"), i18n("freq_val")), 
                     (i18n("buffer"), i18n("buffer_val"))]:
            r = QWidget()
            r_layout = QHBoxLayout()
            r.setLayout(r_layout)
            r_layout.setContentsMargins(10, 2, 10, 2)
            
            label_key = QLabel(k)
            label_key.setFont(QFont(*FONT_TINY))
            label_key.setStyleSheet(f"color: {ORANGE_DIM};")
            r_layout.addWidget(label_key)
            
            label_val = QLabel(v)
            label_val.setFont(QFont(*FONT_TINY))
            label_val.setStyleSheet(f"color: {ORANGE};")
            r_layout.addStretch()
            r_layout.addWidget(label_val)
            
            status_layout.addWidget(r)
        
        status_layout.addSpacing(8)
        right_layout.addWidget(status_box)
        
        # Botón ADD MODULE
        add_box = QFrame()
        add_box.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_PANEL};
                border: 1px solid {ORANGE_DARK};
            }}
        """)
        add_layout = QVBoxLayout()
        add_box.setLayout(add_layout)
        add_layout.setContentsMargins(0, 0, 0, 0)
        
        add_btn = QPushButton("+  " + i18n("add_module"))
        add_btn.setFont(QFont(*FONT_BTN))
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_PANEL};
                color: {ORANGE};
                border: none;
                padding: 8px 14px;
            }}
            QPushButton:hover {{
                background-color: {ORANGE};
                color: {BG};
            }}
        """)
        add_btn.clicked.connect(self._cmd_add)
        add_layout.addWidget(add_btn)
        right_layout.addWidget(add_box)
        
        # Botón STOP ALL
        stop_box = QFrame()
        stop_box.setStyleSheet(f"""
            QFrame {{
                background-color: {RED_DIM};
                border: 1px solid {RED_DIM};
            }}
        """)
        stop_layout = QVBoxLayout()
        stop_box.setLayout(stop_layout)
        stop_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stop_all_btn = QPushButton("■  " + i18n("stop_all"))
        self.stop_all_btn.setFont(QFont(*FONT_BTN))
        self.stop_all_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_PANEL};
                color: {RED_STOP};
                border: none;
                padding: 8px 14px;
            }}
            QPushButton:hover {{
                background-color: {RED_STOP};
                color: {BG};
            }}
        """)
        self.stop_all_btn.clicked.connect(self._stop_all)
        stop_layout.addWidget(self.stop_all_btn)
        right_layout.addWidget(stop_box)
        
        right_layout.addStretch()
        
        body_layout.addWidget(self.right_panel, 0, Qt.AlignTop)
        self.right_panel.hide()  # Ocultarlo inicialmente
        
        main_layout.addWidget(body)
        self._render_buttons()

    # Barra inferior con instrucciones de navegación y estado de reproducción.
    def _build_statusbar(self):
        central_widget = self.centralWidget()
        main_layout = central_widget.layout()
        
        bar = QWidget()
        bar.setStyleSheet(f"background-color: {BG_ENTRY}; padding: 5px;")
        bar_layout = QHBoxLayout()
        bar.setLayout(bar_layout)
        
        lf = QWidget()
        lf_layout = QHBoxLayout()
        lf.setLayout(lf_layout)
        lf_layout.setContentsMargins(0, 0, 0, 0)
        
        nav_label = QLabel(i18n("navigate"))
        nav_label.setFont(QFont(*FONT_TINY))
        nav_label.setStyleSheet(f"color: {ORANGE_DIM};")
        lf_layout.addWidget(nav_label)
        lf_layout.addSpacing(14)
        
        enter_label = QLabel(i18n("enter_select"))
        enter_label.setFont(QFont(*FONT_TINY))
        enter_label.setStyleSheet(f"color: {ORANGE_DIM};")
        lf_layout.addWidget(enter_label)
        
        bar_layout.addWidget(lf)
        bar_layout.addStretch()
        
        rf = QWidget()
        rf_layout = QHBoxLayout()
        rf.setLayout(rf_layout)
        rf_layout.setContentsMargins(0, 0, 0, 0)
        
        # Punto indicador de estado (LED)
        self.dot_frame = QFrame()
        self.dot_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {GREEN_DOT};
                border-radius: 4px;
            }}
        """)
        self.dot_frame.setFixedSize(8, 8)
        rf_layout.addWidget(self.dot_frame)
        rf_layout.addSpacing(6)
        
        self.status_label = QLabel(i18n("ready"))
        self.status_label.setFont(QFont(*FONT_SMALL))
        self.status_label.setStyleSheet(f"color: {ORANGE_DIM};")
        rf_layout.addWidget(self.status_label)
        
        bar_layout.addWidget(rf)
        bar_layout.setContentsMargins(14, 0, 14, 0)
        
        main_layout.addWidget(bar)

    # Parrilla de botones
    def _render_buttons(self):
        # Limpiar layout anterior
        while self.btn_grid.count():
            child = self.btn_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.btn_refs.clear()
        self.playing_idx = None
        
        count = len(self.buttons_data)
        modules_text = i18n("modules") if count != 1 else i18n("module")
        self.module_count_lbl.setText(f"[ {count} {modules_text} ]")
        
        if not count:
            empty_label = QLabel("\n" + i18n("no_audio_modules") + "\n\n" +
                                i18n("use_system_add") + "\n" +
                                i18n("or_click_add"))
            empty_label.setFont(QFont(*FONT_BTN))
            empty_label.setStyleSheet(f"color: {ORANGE_DIM};")
            empty_label.setAlignment(Qt.AlignCenter)
            self.btn_grid.addWidget(empty_label, 0, 0, 1, COLS)
            return
        
        # Configurar columnas con peso uniforme
        for c in range(COLS):
            self.btn_grid.setColumnStretch(c, 1)
        
        for i, item in enumerate(self.buttons_data):
            r, c = divmod(i, COLS)
            self._make_audio_btn(item, i, r, c)

    # Crea un botón con borde naranja oscuro y fondo de panel
    def _make_audio_btn(self, item, idx, row, col):
        # Marco exterior (borde)
        outer = QFrame()
        outer.setStyleSheet(f"""
            QFrame {{
                background-color: {ORANGE_DARK};
                border: 1px solid {ORANGE_DARK};
                padding: 1px;
            }}
        """)
        
        # Marco interior (contenido)
        inner = QWidget()
        inner_layout = QVBoxLayout()
        inner.setLayout(inner_layout)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner.setStyleSheet(f"background-color: {BG_PANEL};")
        
        outer_layout = QVBoxLayout()
        outer.setLayout(outer_layout)
        outer_layout.addWidget(inner)
        outer_layout.setContentsMargins(1, 1, 1, 1)
        
        name_text = item["name"].upper()
        fname = os.path.basename(item["path"])
        
        # Botón de reproducción
        btn = QPushButton(f"\u25b6  {name_text}")
        btn.setFont(QFont(*FONT_BTN))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_PANEL};
                color: {ORANGE};
                border: none;
                padding: 12px 16px;
            }}
            QPushButton:hover {{
                background-color: {ORANGE};
                color: {BG};
            }}
        """)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.clicked.connect(lambda checked=False, i=idx: self._toggle(i))
        btn.setContextMenuPolicy(Qt.CustomContextMenu)
        btn.customContextMenuRequested.connect(lambda pos, i=idx: self._show_button_menu(pos, i, btn))
        inner_layout.addWidget(btn)
        
        # Etiqueta del archivo
        sub = QLabel(fname)
        sub.setFont(QFont(*FONT_TINY))
        sub.setStyleSheet(f"color: {ORANGE_DIM}; padding: 4px;")
        sub.setAlignment(Qt.AlignCenter)
        sub.setWordWrap(True)
        sub.setContextMenuPolicy(Qt.CustomContextMenu)
        sub.customContextMenuRequested.connect(lambda pos, i=idx: self._show_button_menu(pos, i, btn))
        inner_layout.addWidget(sub)
        
        # Guardar referencias
        self.btn_refs[idx] = {"btn": btn, "outer": outer, "inner": inner, "name": item["name"]}
        
        # Agregar a la grilla
        self.btn_grid.addWidget(outer, row, col)
        self.btn_grid.setRowStretch(row, 1)

    # Menú contextual para botones
    def _show_button_menu(self, pos, idx, btn):
        ctx = QMenu(self)
        ctx.setStyleSheet(f"""
            QMenu {{
                background-color: {BG_PANEL};
                color: {ORANGE};
                border: 1px solid {ORANGE_DARK};
            }}
            QMenu::item:selected {{
                background-color: {ORANGE};
                color: {BG};
            }}
        """)
        
        play_action = ctx.addAction("  \u25b6  " + i18n("play"))
        play_action.triggered.connect(lambda checked=False, i=idx: self._toggle(i))
        
        stop_action = ctx.addAction("  \u25a0  " + i18n("stop"))
        stop_action.triggered.connect(self._stop_all)
        
        ctx.addSeparator()
        
        remove_action = ctx.addAction("  \u2715  " + i18n("remove_this_module"))
        remove_action.triggered.connect(lambda checked=False, i=idx: self._remove_button(i))
        
        ctx.exec(btn.mapToGlobal(pos))

    # Lógica de reproducción / detención
    def _toggle(self, idx):
        """Mismo botón: detener. Botón diferente o ocioso: reproducir."""
        if self.playing_idx == idx:
            self._stop_all()
        else:
            self._play(idx)

    # Reproducir el audio del botón seleccionado.
    def _play(self, idx):
        item = self.buttons_data[idx]
        filename, name = item["path"], item["name"]
        path = os.path.join(AUDIO_FOLDER, filename)
        
        if not os.path.exists(path):
            QMessageBox.critical(self, i18n("file_error"), 
                               i18n("file_not_found") + f"\n{path}")
            return
        
        # Reiniciar botón anterior si es diferente
        self._reset_btn_ui(self.playing_idx)
        
        # Cambiar estado del nuevo botón a "playing"
        self.playing_idx = idx
        self._set_btn_playing(idx)
        self.status_label.setText(
            f"\u25b6 " + i18n("playing") + f"  {name.upper()}  //  {os.path.basename(path)}")
        
        def _do():
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
            except Exception as ex:
                self.status_label.setText(f"ERROR: {ex}")
        
        threading.Thread(target=_do, daemon=True).start()

    # Detiene toda reproducción
    def _stop_all(self):
        pygame.mixer.music.stop()
        self._reset_btn_ui(self.playing_idx)
        self.playing_idx = None
        self.status_label.setText(i18n("ready"))

    # Cambiar el botón a apariencia de "STOP" rojo
    def _set_btn_playing(self, idx):
        if idx is None or idx not in self.btn_refs:
            return
        ref = self.btn_refs[idx]
        name = ref["name"].upper()
        ref["btn"].setText(f"\u25a0  {name}")
        ref["btn"].setStyleSheet(f"""
            QPushButton {{
                background-color: {RED_STOP};
                color: {BG};
                border: none;
                padding: 12px 16px;
            }}
            QPushButton:hover {{
                background-color: {RED_DIM};
                color: {ORANGE};
            }}
        """)
        ref["outer"].setStyleSheet(f"""
            QFrame {{
                background-color: {RED_STOP};
                border: 1px solid {RED_STOP};
                padding: 1px;
            }}
        """)

    # Restaurar el botón a la apariencia de "PLAY" naranja
    def _reset_btn_ui(self, idx):
        if idx is None or idx not in self.btn_refs:
            return
        ref = self.btn_refs[idx]
        name = ref["name"].upper()
        ref["btn"].setText(f"\u25b6  {name}")
        ref["btn"].setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_PANEL};
                color: {ORANGE};
                border: none;
                padding: 12px 16px;
            }}
            QPushButton:hover {{
                background-color: {ORANGE};
                color: {BG};
            }}
        """)
        ref["outer"].setStyleSheet(f"""
            QFrame {{
                background-color: {ORANGE_DARK};
                border: 1px solid {ORANGE_DARK};
                padding: 1px;
            }}
        """)

    # Auto-reset cuando la pista termina naturalmente
    def _poll_music(self):
        if self.playing_idx is not None and not pygame.mixer.music.get_busy():
            self._reset_btn_ui(self.playing_idx)
            self.playing_idx = None
            self.status_label.setText(i18n("ready"))
        QTimer.singleShot(300, self._poll_music)

    # Comandos del menú
    def _cmd_add(self):
        dlg = AddButtonPanel(self)
        if dlg.exec() == QDialog.Accepted and dlg.result:
            self.buttons_data.append(dlg.result)
            self._save_config()
            self._render_buttons()

    # Eliminar el botón seleccionado
    def _remove_button(self, idx):
        name = self.buttons_data[idx]["name"]
        reply = QMessageBox.question(self, i18n("remove_module"), 
                                    i18n("remove_module_confirm") + f' "{name.upper()}"?')
        if reply == QMessageBox.Yes:
            if self.playing_idx == idx:
                self._stop_all()
            del self.buttons_data[idx]
            self._save_config()
            self._render_buttons()

    # Mostrar diálogo de información del sistema
    def _cmd_about(self):
        SystemInfo(self).exec()

    # Inicia un parpadeo del punto de estado
    def _start_blink(self):
        def tick():
            if not hasattr(self, "dot_frame") or self.dot_frame is None:
                return

            self.blink_state = not self.blink_state
            color = GREEN_DOT if self.blink_state else BG_PANEL
            self.dot_frame.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
            QTimer.singleShot(800, tick)

        tick()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MentorAudioApp()
    sys.exit(app.exec())
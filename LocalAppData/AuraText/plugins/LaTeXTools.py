import os
import shutil
import subprocess
import importlib

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from auratext import Plugin
from auratext.Core.window import Window


class LaTeXTools(Plugin):
    def __init__(self, window: Window) -> None:
        super().__init__(window)
        self.window = window

        # load_plugins() can run more than once; avoid duplicate UI registrations.
        if getattr(self.window, "_latex_tools_loaded", False):
            return
        self.window._latex_tools_loaded = True

        self.last_pdf_path = ""
        self._pdf_backend = "none"

        self.latex_menu = QMenu("&LaTeX", self.window)
        self._build_menu_actions()
        self.window.menuBar().addMenu(self.latex_menu)

        self._create_pdf_dock()

        self.window.tab_widget.currentChanged.connect(self._update_menu_visibility)
        self.latex_menu.aboutToShow.connect(lambda: self._update_menu_visibility(self.window.tab_widget.currentIndex()))
        self._update_menu_visibility(self.window.tab_widget.currentIndex())

    def _build_menu_actions(self) -> None:
        export_action = QAction("Export to PDF", self.window)
        export_action.triggered.connect(self.export_to_pdf)

        show_preview_action = QAction("Show PDF Preview Dock", self.window)
        show_preview_action.triggered.connect(self.show_preview_dock)

        self.latex_menu.addAction(export_action)
        self.latex_menu.addAction(show_preview_action)
        self.latex_menu.addSeparator()

        headline_action = QAction("Insert Headline", self.window)
        headline_action.triggered.connect(
            lambda: self._insert_snippet(
                "\\title{Your Title}\\n"
                "\\author{Your Name}\\n"
                "\\date{\\today}\\n"
                "\\maketitle\\n"
            )
        )

        section_action = QAction("Insert Section", self.window)
        section_action.triggered.connect(lambda: self._insert_snippet("\\section{Section Title}\\n"))

        subsection_action = QAction("Insert Subsection", self.window)
        subsection_action.triggered.connect(
            lambda: self._insert_snippet("\\subsection{Subsection Title}\\n")
        )

        subsubsection_action = QAction("Insert Subsubsection", self.window)
        subsubsection_action.triggered.connect(
            lambda: self._insert_snippet("\\subsubsection{Subsubsection Title}\\n")
        )

        itemize_action = QAction("Insert Itemize Block", self.window)
        itemize_action.triggered.connect(
            lambda: self._insert_snippet(
                "\\begin{itemize}\\n"
                "    \\item First item\\n"
                "\\end{itemize}\\n"
            )
        )

        self.latex_menu.addAction(headline_action)
        self.latex_menu.addAction(section_action)
        self.latex_menu.addAction(subsection_action)
        self.latex_menu.addAction(subsubsection_action)
        self.latex_menu.addAction(itemize_action)

    def _create_pdf_dock(self) -> None:
        self.pdf_dock = QDockWidget("LaTeX PDF Preview", self.window)
        self.pdf_dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.pdf_dock.setMinimumWidth(420)

        container = QWidget(self.pdf_dock)
        layout = QVBoxLayout(container)

        self.preview_status = QLabel("Export a .tex file to generate and preview its PDF.")
        self.preview_status.setWordWrap(True)

        self.controls_row = QHBoxLayout()
        self.open_btn = QPushButton("Open Generated PDF")
        self.open_btn.clicked.connect(self.open_generated_pdf)
        self.reload_btn = QPushButton("Reload")
        self.reload_btn.clicked.connect(self.reload_pdf)
        self.prev_page_btn = QPushButton("Prev")
        self.prev_page_btn.clicked.connect(lambda: self._pdf_page_navigate(-1))
        self.next_page_btn = QPushButton("Next")
        self.next_page_btn.clicked.connect(lambda: self._pdf_page_navigate(1))
        self.zoom_out_btn = QPushButton("Zoom-")
        self.zoom_out_btn.clicked.connect(lambda: self._zoom_pdf(-0.1))
        self.zoom_in_btn = QPushButton("Zoom+")
        self.zoom_in_btn.clicked.connect(lambda: self._zoom_pdf(0.1))
        self.controls_row.addWidget(self.open_btn)
        self.controls_row.addWidget(self.reload_btn)
        self.controls_row.addWidget(self.prev_page_btn)
        self.controls_row.addWidget(self.next_page_btn)
        self.controls_row.addWidget(self.zoom_out_btn)
        self.controls_row.addWidget(self.zoom_in_btn)

        self.pdf_viewer = self._build_pdf_viewer_widget()

        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setPlaceholderText("LaTeX build logs will appear here.")
        self.log_view.setMaximumHeight(160)

        layout.addWidget(self.preview_status)
        layout.addLayout(self.controls_row)
        layout.addWidget(self.pdf_viewer, 1)
        layout.addWidget(self.log_view)

        self.pdf_dock.setWidget(container)
        self.window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.pdf_dock)
        self.pdf_dock.hide()

    def _build_pdf_viewer_widget(self):
        try:
            from PyQt6.QtPdf import QPdfDocument
            from PyQt6.QtPdfWidgets import QPdfView

            self._pdf_backend = "qtpdf"
            self.pdf_document = QPdfDocument(self)
            view = QPdfView()
            view.setDocument(self.pdf_document)
            return view
        except Exception:
            try:
                webengine_module = importlib.import_module("PyQt6.QtWebEngineWidgets")
                QWebEngineView = getattr(webengine_module, "QWebEngineView")

                self._pdf_backend = "webengine"
                return QWebEngineView()
            except Exception:
                self._pdf_backend = "fallback"
                fallback = QTextBrowser()
                fallback.setOpenExternalLinks(False)
                fallback.anchorClicked.connect(self._on_pdf_anchor_clicked)
                fallback.setHtml("<b>No embedded PDF backend available.</b><br>Export still works.")
                return fallback

    def _insert_snippet(self, text: str) -> None:
        if not self._is_tex_tab():
            QMessageBox.information(self.window, "LaTeX", "Switch to a .tex tab to insert LaTeX snippets.")
            return

        editor = getattr(self.window, "current_editor", None)
        if not editor:
            return

        editor.insert(text)

    def _current_file_path(self) -> str:
        index = self.window.tab_widget.currentIndex()
        if index < 0:
            return ""
        return self.window.tab_file_paths.get(index, "")

    def _is_tex_tab(self) -> bool:
        index = self.window.tab_widget.currentIndex()
        if index < 0:
            return False

        path = self._current_file_path().lower()
        if path.endswith(".tex"):
            return True

        tab_name = self.window.tab_widget.tabText(index).strip().rstrip("*").strip().lower()
        return tab_name.endswith(".tex")

    def _update_menu_visibility(self, _index: int) -> None:
        self.latex_menu.menuAction().setVisible(self._is_tex_tab())

    def show_preview_dock(self) -> None:
        self.pdf_dock.show()
        self.pdf_dock.raise_()

    def open_generated_pdf(self) -> None:
        if not self.last_pdf_path or not os.path.exists(self.last_pdf_path):
            QMessageBox.information(self.window, "LaTeX", "No generated PDF found yet.")
            return
        self._load_pdf(self.last_pdf_path)
        self.preview_status.setText(f"Previewing: {self.last_pdf_path}")
        self.show_preview_dock()

    def reload_pdf(self) -> None:
        self.open_generated_pdf()

    def _pdf_page_navigate(self, delta: int) -> None:
        if self._pdf_backend != "qtpdf":
            return
        navigator = getattr(self.pdf_viewer, "pageNavigator", lambda: None)()
        page_count = self.pdf_document.pageCount()
        if not navigator or page_count <= 0:
            return
        current_page = navigator.currentPage()
        next_page = max(0, min(page_count - 1, current_page + delta))
        if next_page != current_page:
            navigator.jump(next_page, navigator.currentLocation(), navigator.currentZoom())

    def _zoom_pdf(self, delta: float) -> None:
        if self._pdf_backend == "qtpdf":
            current = self.pdf_viewer.zoomFactor()
            self.pdf_viewer.setZoomFactor(max(0.25, min(4.0, current + delta)))
            return
        if self._pdf_backend == "webengine" and self.last_pdf_path:
            current = self.pdf_viewer.zoomFactor()
            self.pdf_viewer.setZoomFactor(max(0.25, min(4.0, current + delta)))

    def _on_pdf_anchor_clicked(self, url: QUrl) -> None:
        if url.isLocalFile():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(".pdf"):
                self.last_pdf_path = file_path
                self.open_generated_pdf()
                return

    def export_to_pdf(self) -> None:
        if not self._is_tex_tab():
            QMessageBox.information(self.window, "LaTeX", "Open a .tex file tab first.")
            return

        tex_path = self._current_file_path()
        if not tex_path:
            QMessageBox.information(
                self.window,
                "Save Required",
                "Save this LaTeX file first, then export to PDF.",
            )
            self.window.save_document_as()
            tex_path = self._current_file_path()

        if not tex_path or not tex_path.lower().endswith(".tex"):
            QMessageBox.warning(self.window, "LaTeX", "Export works only for saved .tex files.")
            return

        self.window.save_document()

        pdflatex = shutil.which("pdflatex")
        if not pdflatex:
            QMessageBox.warning(
                self.window,
                "pdflatex Not Found",
                "Could not find 'pdflatex' in PATH. Install a TeX distribution (MiKTeX/TeX Live).",
            )
            return

        working_dir = os.path.dirname(tex_path)
        tex_name = os.path.basename(tex_path)
        compile_log = []

        for _ in range(2):
            result = subprocess.run(
                [pdflatex, "-interaction=nonstopmode", "-halt-on-error", tex_name],
                cwd=working_dir,
                capture_output=True,
                text=True,
            )
            compile_log.append(result.stdout)
            compile_log.append(result.stderr)
            if result.returncode != 0:
                self.log_view.setPlainText("\n".join(compile_log).strip())
                self.preview_status.setText("LaTeX build failed. See build log below.")
                self.show_preview_dock()
                QMessageBox.critical(self.window, "LaTeX Build Failed", "pdflatex returned an error.")
                return

        pdf_path = os.path.splitext(tex_path)[0] + ".pdf"
        if not os.path.exists(pdf_path):
            self.log_view.setPlainText("\n".join(compile_log).strip())
            self.preview_status.setText("Build finished but PDF was not generated.")
            self.show_preview_dock()
            QMessageBox.warning(self.window, "LaTeX", "No PDF output file was found.")
            return

        self.last_pdf_path = pdf_path
        self.log_view.setPlainText("\n".join(compile_log).strip())
        self._load_pdf(pdf_path)
        self.preview_status.setText(f"Previewing: {pdf_path}")
        self.show_preview_dock()

    def _load_pdf(self, pdf_path: str) -> None:
        if self._pdf_backend == "qtpdf":
            self.pdf_document.load(pdf_path)
            navigator = getattr(self.pdf_viewer, "pageNavigator", lambda: None)()
            if navigator and self.pdf_document.pageCount() > 0:
                navigator.jump(0, navigator.currentLocation(), self.pdf_viewer.zoomFactor())
            return

        if self._pdf_backend == "webengine":
            self.pdf_viewer.setUrl(QUrl.fromLocalFile(pdf_path))
            return

        safe_path = pdf_path.replace("&", "&amp;")
        self.pdf_viewer.setHtml(
            "<b>Embedded preview unavailable.</b><br>"
            "Use the dock controls to open inside Aura Text when a backend is available.<br>"
            f"Load PDF: <a href='file:///{safe_path}'>{pdf_path}</a>"
        )

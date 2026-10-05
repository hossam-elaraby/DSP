import os
import sys
from typing import Dict, List, Optional, Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QComboBox, QSpinBox, QDoubleSpinBox,
    QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QMessageBox, QFrame, QTextEdit, QSplitter, QScrollArea, QTabWidget
)

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from signal_model import Signal, read_signal_from_file, write_signal_to_file
from algorithm import get_registered_algorithms, DSPAlgorithm, AlgorithmParam
from test_runner import run_lab1_tests


COLOR_SIG1 = "#2563eb"
COLOR_SIG2 = "#ea580c"
COLOR_SIG3 = "#8b5cf6"
COLOR_SIG4 = "#0891b2"
COLOR_SIG5 = "#d97706"
COLOR_RESULT = "#16a34a"

PALETTE = [COLOR_SIG1, COLOR_SIG2, COLOR_SIG3, COLOR_SIG4, COLOR_SIG5]
MARKERS = ['o', 's', 'D', 'v', '^', 'p', '*']


QSS_STYLE = """
QMainWindow {
    background-color: #f8fafc;
}
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #1e293b;
    font-size: 13px;
}
.CardWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}
.CardHeader {
    font-size: 14px;
    font-weight: 700;
    color: #0f172a;
}
QTabWidget::pane {
    border: none;
    background: transparent;
}
QTabBar::tab {
    background: #f1f5f9;
    color: #475569;
    font-weight: 600;
    font-size: 13px;
    padding: 7px 20px;
    border: 1px solid #cbd5e1;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 4px;
}
QTabBar::tab:selected {
    background: #ffffff;
    color: #2563eb;
    border-bottom: 2px solid #2563eb;
}
QTabBar::tab:hover {
    background: #e2e8f0;
}
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    gridline-color: #f1f5f9;
    border-radius: 4px;
    font-size: 12px;
}
QTableWidget::item {
    padding: 4px;
}
QTableWidget::item:selected {
    background-color: #eff6ff;
    color: #1d4ed8;
}
QHeaderView::section {
    background-color: #f8fafc;
    color: #475569;
    font-weight: 600;
    border: none;
    border-bottom: 1px solid #e2e8f0;
    padding: 5px;
    font-size: 12px;
}
QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 4px 8px;
    color: #0f172a;
    font-size: 12px;
}
QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {
    border: 1px solid #2563eb;
}
QPushButton {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 5px 12px;
    font-weight: 600;
    color: #334155;
    font-size: 12px;
}
QPushButton:hover {
    background-color: #f1f5f9;
}
QPushButton:disabled {
    background-color: #f8fafc;
    color: #94a3b8;
    border-color: #e2e8f0;
}
#PrimaryButton {
    background-color: #2563eb;
    color: #ffffff;
    border: 1px solid #1d4ed8;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 700;
    border-radius: 6px;
}
#PrimaryButton:hover {
    background-color: #1d4ed8;
}
#DangerButton {
    background-color: #fff1f2;
    color: #e11d48;
    border: 1px solid #fecdd3;
}
#DangerButton:hover {
    background-color: #ffe4e6;
}
#DangerButton:disabled {
    background-color: #f8fafc;
    color: #cbd5e1;
    border-color: #e2e8f0;
}
#StatusBadge {
    background-color: #f1f5f9;
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 4px 8px;
    font-weight: 600;
    font-size: 12px;
}
#ActiveSignalBanner {
    background-color: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 5px;
    padding: 6px 10px;
    font-weight: 600;
    color: #1d4ed8;
    font-size: 12px;
}
#SignalsContainerBox, #ParamContainerBox {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
}
QSplitter::handle:vertical {
    background-color: #e2e8f0;
    height: 4px;
    border-radius: 2px;
}
QSplitter::handle:vertical:hover {
    background-color: #3b82f6;
}
QScrollBar:vertical {
    border: none;
    background: #f1f5f9;
    width: 6px;
    border-radius: 3px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #cbd5e1;
    min-height: 20px;
    border-radius: 3px;
}
QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    border: none;
    background: #f1f5f9;
    height: 6px;
    border-radius: 3px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #cbd5e1;
    min-width: 20px;
    border-radius: 3px;
}
QScrollBar::handle:horizontal:hover {
    background: #94a3b8;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""


class SignalCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(8, 3.2), dpi=100, facecolor='#ffffff')
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.show_stems = True
        self.show_lines = True
        self.show_grid = True
        self.fig.tight_layout(pad=2.0)
        self.setMinimumHeight(200)

    def plot_signals(self, visible_signals: List[Signal], result_signal: Optional[Signal] = None, show_result: bool = True):
        self.ax.clear()
        self.ax.set_facecolor('#ffffff')

        if self.show_grid:
            self.ax.grid(True, linestyle='-', color='#f1f5f9', linewidth=1.0)
            self.ax.axhline(0, color='#cbd5e1', linewidth=1.0, linestyle='--')

        for idx, sig in enumerate(visible_signals):
            if sig.n_samples == 0:
                continue

            color = PALETTE[idx % len(PALETTE)]
            marker = MARKERS[idx % len(MARKERS)]
            label = f"{sig.name} ({sig.alias})"

            if self.show_stems:
                markerline, stemlines, _ = self.ax.stem(
                    sig.indices, sig.samples,
                    linefmt=color, markerfmt=marker, basefmt=" "
                )
                markerline.set_markerfacecolor(color)
                markerline.set_markeredgecolor(color)
                markerline.set_markersize(5)
                stemlines.set_linewidth(1.0)
                stemlines.set_alpha(0.65)
                markerline.set_label(label if not self.show_lines else "_nolegend_")

            if self.show_lines:
                self.ax.plot(
                    sig.indices, sig.samples,
                    color=color, marker=marker, markersize=5,
                    linewidth=1.2, label=label
                )

        if show_result and result_signal is not None and result_signal.n_samples > 0:
            res_color = COLOR_RESULT
            res_marker = '^'
            res_label = f"{result_signal.name}"

            if self.show_stems:
                markerline, stemlines, _ = self.ax.stem(
                    result_signal.indices, result_signal.samples,
                    linefmt=res_color, markerfmt=res_marker, basefmt=" "
                )
                markerline.set_markerfacecolor(res_color)
                markerline.set_markeredgecolor(res_color)
                markerline.set_markersize(6)
                stemlines.set_linewidth(1.2)
                stemlines.set_alpha(0.75)
                markerline.set_label(res_label if not self.show_lines else "_nolegend_")

            if self.show_lines:
                self.ax.plot(
                    result_signal.indices, result_signal.samples,
                    color=res_color, marker=res_marker, markersize=6,
                    linewidth=1.5, linestyle='-', label=res_label
                )

        self.ax.set_xlabel("Sample Index", fontsize=10, fontweight='bold', color='#334155')
        self.ax.set_ylabel("Amplitude", fontsize=10, fontweight='bold', color='#334155')
        self.ax.tick_params(colors='#475569', labelsize=9)

        for spine in self.ax.spines.values():
            spine.set_color('#cbd5e1')
            spine.set_linewidth(0.8)

        handles, labels = self.ax.get_legend_handles_labels()
        if labels:
            self.ax.legend(loc='upper right', frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', fontsize=9)

        self.fig.tight_layout(pad=1.8)
        self.draw()


class DSPMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DSP Signal Processing Tool")
        self.resize(1140, 780)
        self.setMinimumSize(920, 600)

        self.signals: List[Signal] = []
        self.result_signal: Optional[Signal] = None
        self.show_result: bool = True
        self.active_signal_name: Optional[str] = None
        
        self.registered_algorithms: List[DSPAlgorithm] = get_registered_algorithms()
        self.signal_widgets: Dict[str, dict] = {}
        self.param_inputs: Dict[str, QWidget] = {}

        self.current_operation_name: str = "None"
        self.procedural_steps: List[str] = []
        self.last_test_results: List[dict] = []

        self._init_ui()
        self._load_initial_signals()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._enforce_plot_ratio()

    def showEvent(self, event):
        super().showEvent(event)
        self._enforce_plot_ratio()

    def _enforce_plot_ratio(self):
        if hasattr(self, 'main_splitter'):
            total_h = self.main_splitter.height()
            if total_h > 150:
                h_plot = int(total_h * 0.60)
                h_bottom = total_h - h_plot
                self.main_splitter.setSizes([h_plot, h_bottom])

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(10, 10, 10, 10)
        root_layout.setSpacing(6)

        self.tabs = QTabWidget()
        root_layout.addWidget(self.tabs)

        studio_tab = self._create_studio_tab()
        self.tabs.addTab(studio_tab, "Main")

        test_tab = self._create_test_tab()
        self.tabs.addTab(test_tab, "Test")

    def _create_studio_tab(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.main_splitter = QSplitter(Qt.Orientation.Vertical)
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.setHandleWidth(5)

        viz_card = self._create_visualization_card()
        viz_card.setMinimumHeight(220)
        self.main_splitter.addWidget(viz_card)

        bottom_container = QWidget()
        bottom_row = QHBoxLayout(bottom_container)
        bottom_row.setContentsMargins(0, 8, 0, 0)
        bottom_row.setSpacing(10)

        bottom_row.addWidget(self._create_details_card(), stretch=4)
        bottom_row.addWidget(self._create_operations_card(), stretch=6)

        self.main_splitter.addWidget(bottom_container)
        self.main_splitter.setStretchFactor(0, 60)
        self.main_splitter.setStretchFactor(1, 40)

        layout.addWidget(self.main_splitter)
        return container

    def _create_visualization_card(self) -> QWidget:
        card = QFrame()
        card.setProperty("class", "CardWidget")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)

        hdr = QHBoxLayout()
        title = QLabel("Signal Visualization")
        title.setProperty("class", "CardHeader")
        hdr.addWidget(title)
        hdr.addStretch()

        self.btn_stems = QPushButton("Stems: ON")
        self.btn_stems.setCheckable(True)
        self.btn_stems.setChecked(True)
        self.btn_stems.clicked.connect(self._toggle_stems)
        hdr.addWidget(self.btn_stems)

        self.btn_lines = QPushButton("Lines: ON")
        self.btn_lines.setCheckable(True)
        self.btn_lines.setChecked(True)
        self.btn_lines.clicked.connect(self._toggle_lines)
        hdr.addWidget(self.btn_lines)

        self.btn_grid = QPushButton("Grid: ON")
        self.btn_grid.setCheckable(True)
        self.btn_grid.setChecked(True)
        self.btn_grid.clicked.connect(self._toggle_grid)
        hdr.addWidget(self.btn_grid)

        layout.addLayout(hdr)

        self.canvas = SignalCanvas(self)
        layout.addWidget(self.canvas)
        return card

    def _create_details_card(self) -> QWidget:
        card = QFrame()
        card.setProperty("class", "CardWidget")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        self.lbl_details_title = QLabel("Signal Details")
        self.lbl_details_title.setProperty("class", "CardHeader")
        layout.addWidget(self.lbl_details_title)

        self.table_details = QTableWidget()
        self.table_details.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_details.verticalHeader().setVisible(False)
        self.table_details.setAlternatingRowColors(True)
        layout.addWidget(self.table_details)
        return card

    def _create_operations_card(self) -> QWidget:
        card = QFrame()
        card.setProperty("class", "CardWidget")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_layout.setSpacing(6)

        title = QLabel("Operations")
        title.setProperty("class", "CardHeader")
        card_layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(2, 2, 6, 2)
        layout.setSpacing(6)

        lbl_signals = QLabel("Signals (Click to Select, Check to Show/Hide)")
        lbl_signals.setStyleSheet("font-weight: 600; font-size: 12px; color: #334155; margin-bottom: 2px;")
        layout.addWidget(lbl_signals)

        sig_box = QFrame()
        sig_box.setObjectName("SignalsContainerBox")
        self.sig_box_layout = QVBoxLayout(sig_box)
        self.sig_box_layout.setContentsMargins(6, 6, 6, 6)
        self.sig_box_layout.setSpacing(4)

        self.signals_scroll = QScrollArea()
        self.signals_scroll.setWidgetResizable(True)
        self.signals_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.signals_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.signals_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.signals_container = QWidget()
        self.signals_container_layout = QVBoxLayout(self.signals_container)
        self.signals_container_layout.setContentsMargins(0, 0, 0, 0)
        self.signals_container_layout.setSpacing(3)
        self.signals_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.signals_scroll.setWidget(self.signals_container)
        self.signals_scroll.setMinimumHeight(65)
        self.signals_scroll.setMaximumHeight(115)
        self.sig_box_layout.addWidget(self.signals_scroll)

        sig_btn_layout = QHBoxLayout()
        btn_add = QPushButton("+ Add Signal (.txt)")
        btn_add.clicked.connect(self._on_load_signal_clicked)
        btn_remove = QPushButton("Remove")
        btn_remove.setObjectName("DangerButton")
        btn_remove.clicked.connect(self._on_remove_signal_clicked)
        sig_btn_layout.addWidget(btn_add)
        sig_btn_layout.addWidget(btn_remove)
        self.sig_box_layout.addLayout(sig_btn_layout)

        layout.addWidget(sig_box)

        self.lbl_active_signal = QLabel("Target Signal: None")
        self.lbl_active_signal.setObjectName("ActiveSignalBanner")
        layout.addWidget(self.lbl_active_signal)

        op_row = QHBoxLayout()
        lbl_op = QLabel("Operation:")
        lbl_op.setStyleSheet("font-weight: 600; color: #334155;")
        op_row.addWidget(lbl_op)
        self.combo_op = QComboBox()
        
        for algo in self.registered_algorithms:
            self.combo_op.addItem(algo.name, algo)

        self.combo_op.currentIndexChanged.connect(self._on_operation_changed)
        op_row.addWidget(self.combo_op)
        layout.addLayout(op_row)

        lbl_params = QLabel("Operation Parameters")
        lbl_params.setStyleSheet("font-weight: 600; font-size: 12px; color: #334155; margin-top: 4px; margin-bottom: 2px;")
        layout.addWidget(lbl_params)

        self.param_box = QFrame()
        self.param_box.setObjectName("ParamContainerBox")
        self.param_box_layout = QVBoxLayout(self.param_box)
        self.param_box_layout.setContentsMargins(8, 8, 8, 8)
        self.param_box_layout.setSpacing(6)

        self.widget_two_signals = QWidget()
        two_layout = QGridLayout(self.widget_two_signals)
        two_layout.setContentsMargins(0, 0, 0, 0)
        two_layout.addWidget(QLabel("First Signal (A):"), 0, 0)
        self.combo_sig_a = QComboBox()
        two_layout.addWidget(self.combo_sig_a, 0, 1)
        two_layout.addWidget(QLabel("Second Signal (B):"), 1, 0)
        self.combo_sig_b = QComboBox()
        two_layout.addWidget(self.combo_sig_b, 1, 1)
        self.param_box_layout.addWidget(self.widget_two_signals)

        self.dynamic_params_container = QWidget()
        self.dynamic_params_layout = QVBoxLayout(self.dynamic_params_container)
        self.dynamic_params_layout.setContentsMargins(0, 0, 0, 0)
        self.dynamic_params_layout.setSpacing(6)
        self.param_box_layout.addWidget(self.dynamic_params_container)

        layout.addWidget(self.param_box)

        self.btn_apply = QPushButton("Apply Operation")
        self.btn_apply.setObjectName("PrimaryButton")
        self.btn_apply.clicked.connect(self._on_apply_operation_clicked)
        layout.addWidget(self.btn_apply)

        res_btn_layout = QHBoxLayout()
        self.btn_save_result = QPushButton("Save Result (.txt)")
        self.btn_save_result.clicked.connect(self._on_save_result_clicked)
        self.btn_save_result.setEnabled(False)

        self.btn_clear_result = QPushButton("Clear Result")
        self.btn_clear_result.setObjectName("DangerButton")
        self.btn_clear_result.clicked.connect(self._on_clear_result_clicked)
        self.btn_clear_result.setEnabled(False)

        res_btn_layout.addWidget(self.btn_save_result)
        res_btn_layout.addWidget(self.btn_clear_result)
        layout.addLayout(res_btn_layout)

        self.lbl_status_badge = QLabel("Ready.")
        self.lbl_status_badge.setObjectName("StatusBadge")
        layout.addWidget(self.lbl_status_badge)

        scroll.setWidget(content)
        card_layout.addWidget(scroll)

        self._on_operation_changed(self.combo_op.currentIndex())
        return card

    def _create_test_tab(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        left_card = QFrame()
        left_card.setProperty("class", "CardWidget")
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(14, 12, 14, 12)
        left_layout.setSpacing(10)

        lbl_test_title = QLabel("Lab 1 Task Verification")
        lbl_test_title.setProperty("class", "CardHeader")
        left_layout.addWidget(lbl_test_title)

        btn_run_all = QPushButton("Run All Tests")
        btn_run_all.setObjectName("PrimaryButton")
        btn_run_all.clicked.connect(self._run_all_tests)
        left_layout.addWidget(btn_run_all)

        self.table_test_results = QTableWidget()
        self.table_test_results.setColumnCount(3)
        self.table_test_results.setHorizontalHeaderLabels(["Test Case", "Status", "Message"])
        self.table_test_results.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table_test_results.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_test_results.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table_test_results.verticalHeader().setVisible(False)
        self.table_test_results.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_test_results.itemSelectionChanged.connect(self._on_test_row_selected)
        left_layout.addWidget(self.table_test_results)

        btn_load_to_main = QPushButton("Load Selected Result into Main")
        btn_load_to_main.clicked.connect(self._load_test_to_main)
        left_layout.addWidget(btn_load_to_main)

        layout.addWidget(left_card, stretch=5)

        right_card = QFrame()
        right_card.setProperty("class", "CardWidget")
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(14, 12, 14, 12)
        right_layout.setSpacing(10)

        lbl_viz_title = QLabel("Test Signal Visualization")
        lbl_viz_title.setProperty("class", "CardHeader")
        right_layout.addWidget(lbl_viz_title)

        self.test_canvas = SignalCanvas(self)
        right_layout.addWidget(self.test_canvas, stretch=6)

        lbl_log = QLabel("Test Output Log")
        lbl_log.setStyleSheet("font-weight: 600; font-size: 12px; color: #334155;")
        right_layout.addWidget(lbl_log)

        self.txt_test_log = QTextEdit()
        self.txt_test_log.setReadOnly(True)
        self.txt_test_log.setStyleSheet("background-color: #f8fafc; font-size: 12px; border: 1px solid #e2e8f0; border-radius: 4px;")
        right_layout.addWidget(self.txt_test_log, stretch=4)

        layout.addWidget(right_card, stretch=5)
        return container

    def _run_all_tests(self):
        self.last_test_results = run_lab1_tests()
        self.table_test_results.setRowCount(len(self.last_test_results))

        log_lines = []
        for row, res in enumerate(self.last_test_results):
            item_name = QTableWidgetItem(res["name"])
            self.table_test_results.setItem(row, 0, item_name)

            status_text = "PASSED" if res["passed"] else "FAILED"
            item_status = QTableWidgetItem(status_text)
            item_status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_status.setForeground(QColor("#16a34a" if res["passed"] else "#dc2626"))
            font = item_status.font()
            font.setBold(True)
            item_status.setFont(font)
            self.table_test_results.setItem(row, 1, item_status)

            item_msg = QTableWidgetItem(res["message"])
            self.table_test_results.setItem(row, 2, item_msg)

            log_lines.append(f"[{status_text}] {res['name']}: {res['message']}")

        self.txt_test_log.setPlainText("\n".join(log_lines))

        if self.last_test_results:
            self.table_test_results.selectRow(0)

    def _on_test_row_selected(self):
        selected = self.table_test_results.selectedItems()
        if not selected or not hasattr(self, 'last_test_results'):
            return
        row = self.table_test_results.currentRow()
        if 0 <= row < len(self.last_test_results):
            data = self.last_test_results[row]
            res_sig = data.get("result_signal")
            s1 = data.get("s1")
            s2 = data.get("s2")

            vis = []
            if s1:
                vis.append(s1)
            if s2 and "Signal2" in data["name"]:
                vis.append(s2)

            self.test_canvas.plot_signals(vis, res_sig, show_result=(res_sig is not None))

    def _load_test_to_main(self):
        selected = self.table_test_results.selectedItems()
        if not selected or not hasattr(self, 'last_test_results'):
            return
        row = self.table_test_results.currentRow()
        if 0 <= row < len(self.last_test_results):
            data = self.last_test_results[row]
            res_sig = data.get("result_signal")
            s1 = data.get("s1")
            s2 = data.get("s2")

            self.signals = []
            if s1:
                self.signals.append(s1.copy())
            if s2 and "Signal2" in data["name"]:
                self.signals.append(s2.copy())

            self.result_signal = res_sig.copy(new_name="Result") if res_sig else None
            self.current_operation_name = data["name"]
            self.procedural_steps = [data["message"]]
            self._rebuild_signals_ui()
            self._update_views()
            self.tabs.setCurrentIndex(0)

    def _on_operation_changed(self, index: int):
        data = self.combo_op.currentData()
        if not data:
            return
        
        while self.dynamic_params_layout.count():
            item = self.dynamic_params_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.param_inputs = {}

        algo: DSPAlgorithm = data

        if algo.category == "two_signals":
            self.widget_two_signals.setVisible(True)
        else:
            self.widget_two_signals.setVisible(False)

        if algo.params:
            self.dynamic_params_container.setVisible(True)
            for param in algo.params:
                row = QWidget()
                row_l = QHBoxLayout(row)
                row_l.setContentsMargins(0, 0, 0, 0)
                
                lbl = QLabel(param.label)
                row_l.addWidget(lbl)
                row_l.addStretch()

                if param.param_type == "float":
                    spin = QDoubleSpinBox()
                    spin.setRange(param.min_value or -10000.0, param.max_value or 10000.0)
                    spin.setValue(float(param.default_value))
                    spin.setSingleStep(param.step or 0.5)
                    spin.setFixedWidth(100)
                    row_l.addWidget(spin)
                    self.param_inputs[param.name] = spin

                elif param.param_type == "int":
                    spin_int = QSpinBox()
                    spin_int.setRange(int(param.min_value or -1000), int(param.max_value or 1000))
                    spin_int.setValue(int(param.default_value))
                    spin_int.setSingleStep(int(param.step or 1))
                    spin_int.setFixedWidth(100)
                    row_l.addWidget(spin_int)
                    self.param_inputs[param.name] = spin_int

                elif param.param_type == "choice":
                    combo = QComboBox()
                    combo.addItems(param.options)
                    if param.default_value in param.options:
                        combo.setCurrentText(str(param.default_value))
                    row_l.addWidget(combo)
                    self.param_inputs[param.name] = combo

                elif param.param_type == "bool":
                    chk = QCheckBox()
                    chk.setChecked(bool(param.default_value))
                    row_l.addWidget(chk)
                    self.param_inputs[param.name] = chk

                self.dynamic_params_layout.addWidget(row)
        else:
            self.dynamic_params_container.setVisible(False)

    def _get_dynamic_param_values(self) -> Dict[str, Any]:
        vals = {}
        for name, widget in self.param_inputs.items():
            if isinstance(widget, (QDoubleSpinBox, QSpinBox)):
                vals[name] = widget.value()
            elif isinstance(widget, QComboBox):
                vals[name] = widget.currentText()
            elif isinstance(widget, QCheckBox):
                vals[name] = widget.isChecked()
        return vals

    def _rebuild_signals_ui(self):
        prev_states = {}
        for name, data in self.signal_widgets.items():
            if "chk" in data:
                prev_states[name] = data["chk"].isChecked()

        while self.signals_container_layout.count():
            item = self.signals_container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.signal_widgets = {}
        letters = ['X', 'Y', 'Z', 'W', 'A', 'B', 'C', 'D', 'E']

        for i, sig in enumerate(self.signals):
            if not sig.alias or sig.alias.startswith('S') or len(sig.alias) > 3:
                sig.alias = letters[i] if i < len(letters) else f"S{i+1}"
            
            row = self._create_signal_row(
                name=sig.name,
                alias=sig.alias,
                color=PALETTE[i % len(PALETTE)],
                is_result=False,
                was_checked=prev_states.get(sig.name, True)
            )
            self.signals_container_layout.addWidget(row)

        if self.result_signal is not None:
            res_row = self._create_signal_row(
                name=self.result_signal.name,
                alias="R",
                color=COLOR_RESULT,
                is_result=True,
                was_checked=self.show_result
            )
            self.signals_container_layout.addWidget(res_row)

        self.combo_sig_a.clear()
        self.combo_sig_b.clear()
        for sig in self.signals:
            self.combo_sig_a.addItem(f"{sig.name} ({sig.alias})", sig)
            self.combo_sig_b.addItem(f"{sig.name} ({sig.alias})", sig)
        if len(self.signals) >= 2:
            self.combo_sig_b.setCurrentIndex(1)

        if not self.active_signal_name or not self._get_signal_by_name(self.active_signal_name):
            if self.signals:
                self._set_active_signal(self.signals[0].name)
            elif self.result_signal:
                self._set_active_signal(self.result_signal.name)
            else:
                self.active_signal_name = None
                self.lbl_active_signal.setText("Target Signal: None")
        else:
            self._set_active_signal(self.active_signal_name)

    def _create_signal_row(self, name: str, alias: str, color: str, is_result: bool, was_checked: bool) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 5px; }")
        row_l = QHBoxLayout(frame)
        row_l.setContentsMargins(6, 3, 6, 3)
        row_l.setSpacing(6)

        chk = QCheckBox()
        chk.setChecked(was_checked)
        if is_result:
            chk.toggled.connect(self._on_result_visibility_toggled)
        else:
            chk.toggled.connect(lambda _: self._update_views())
        row_l.addWidget(chk)

        swatch = QFrame()
        swatch.setFixedSize(10, 10)
        swatch.setStyleSheet(f"background-color: {color}; border-radius: 5px; border: none;")
        row_l.addWidget(swatch)

        btn = QPushButton(f"{name} ({alias})")
        btn.setStyleSheet(f"QPushButton {{ text-align: left; border: none; background: transparent; color: {color}; font-weight: 600; padding: 2px 4px; }} QPushButton:hover {{ background-color: #f1f5f9; }}")
        btn.clicked.connect(lambda _, n=name: self._set_active_signal(n))
        row_l.addWidget(btn, stretch=1)

        self.signal_widgets[name] = {"frame": frame, "chk": chk, "btn": btn, "is_result": is_result}
        return frame

    def _set_active_signal(self, name: str):
        self.active_signal_name = name

        for sig_name, data in self.signal_widgets.items():
            frame = data["frame"]
            if sig_name == name:
                frame.setStyleSheet("QFrame { background-color: #eff6ff; border: 1.5px solid #2563eb; border-radius: 5px; }")
            else:
                frame.setStyleSheet("QFrame { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 5px; }")

        sig = self._get_signal_by_name(name)
        if sig:
            self.lbl_active_signal.setText(f"Target Signal: {sig.name} ({sig.alias})")
            for i in range(self.combo_sig_a.count()):
                if self.combo_sig_a.itemData(i) == sig:
                    self.combo_sig_a.setCurrentIndex(i)
                    break
        else:
            self.lbl_active_signal.setText(f"Target Signal: {name}")

        self._update_details_table()

    def _get_signal_by_name(self, name: str) -> Optional[Signal]:
        for s in self.signals:
            if s.name == name or s.alias == name:
                return s
        if self.result_signal and (self.result_signal.name == name or name == "Result"):
            return self.result_signal
        return None

    def _get_active_signal(self) -> Optional[Signal]:
        if self.active_signal_name:
            sig = self._get_signal_by_name(self.active_signal_name)
            if sig:
                return sig
        visible = self._get_visible_signals()
        if visible:
            return visible[0]
        if self.signals:
            return self.signals[0]
        return self.result_signal

    def _on_result_visibility_toggled(self, checked: bool):
        self.show_result = checked
        self._update_views()

    def _get_visible_signals(self) -> List[Signal]:
        visible = []
        for sig in self.signals:
            if sig.name in self.signal_widgets:
                if self.signal_widgets[sig.name]["chk"].isChecked():
                    visible.append(sig)
            else:
                visible.append(sig)
        return visible

    def _update_views(self):
        visible_signals = self._get_visible_signals()
        effective_result = self.result_signal if (self.result_signal is not None and self.show_result) else None

        self.canvas.plot_signals(visible_signals, effective_result, show_result=self.show_result)
        self._update_details_table()

        has_result = (self.result_signal is not None)
        self.btn_save_result.setEnabled(has_result)
        self.btn_clear_result.setEnabled(has_result)

    def _update_details_table(self):
        target_sig = self._get_active_signal()
        if target_sig is None or target_sig.n_samples == 0:
            if hasattr(self, 'lbl_details_title'):
                self.lbl_details_title.setText("Signal Details")
            self.table_details.setRowCount(0)
            self.table_details.setColumnCount(0)
            return

        if hasattr(self, 'lbl_details_title'):
            self.lbl_details_title.setText(f"Signal Details: {target_sig.name} ({target_sig.alias})")

        headers = ["Index (n)", f"Value ({target_sig.alias})"]
        self.table_details.setColumnCount(2)
        self.table_details.setHorizontalHeaderLabels(headers)
        self.table_details.setRowCount(target_sig.n_samples)

        is_result = (self.result_signal is not None and target_sig == self.result_signal)
        for row, (n, val) in enumerate(zip(target_sig.indices, target_sig.samples)):
            item_idx = QTableWidgetItem(str(int(n)))
            item_idx.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_details.setItem(row, 0, item_idx)

            item_val = QTableWidgetItem(f"{val:.2f}")
            item_val.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if is_result:
                item_val.setForeground(QColor("#16a34a"))
            self.table_details.setItem(row, 1, item_val)

    def _on_apply_operation_clicked(self):
        algo: DSPAlgorithm = self.combo_op.currentData()
        if not algo:
            return

        self.procedural_steps = []

        try:
            params = self._get_dynamic_param_values()

            if algo.category == "single_signal":
                target_sig = self._get_active_signal()
                if not target_sig:
                    QMessageBox.warning(self, "No Target Signal", "Please click a signal to select it.")
                    return
                self.result_signal = algo.run_func(target_sig, **params)
                self.current_operation_name = f"{algo.name} on {target_sig.name}"
                self.lbl_status_badge.setText(f"{algo.name} executed successfully.")

            elif algo.category == "multi_signals":
                visible = self._get_visible_signals()
                if not visible:
                    QMessageBox.warning(self, "No Signals Selected", "Please check at least one signal.")
                    return
                self.result_signal = algo.run_func(visible, **params)
                self.current_operation_name = f"{algo.name} on {len(visible)} signals"
                self.lbl_status_badge.setText(f"{algo.name} executed successfully.")

            elif algo.category == "two_signals":
                sig_a = self.combo_sig_a.currentData()
                sig_b = self.combo_sig_b.currentData()
                if not sig_a or not sig_b:
                    QMessageBox.warning(self, "Missing Signals", "Two signals are required.")
                    return
                self.result_signal = algo.run_func(sig_a, sig_b, **params)
                self.current_operation_name = f"{algo.name}: {sig_a.name} and {sig_b.name}"
                self.lbl_status_badge.setText(f"{algo.name} executed successfully.")

            self.show_result = True
            self._rebuild_signals_ui()
            self._update_views()

        except Exception as e:
            QMessageBox.critical(self, "Operation Error", str(e))
            self.lbl_status_badge.setText(f"Error: {e}")

    def _on_load_signal_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Signal File", "", "Text Files (*.txt);;All Files (*)"
        )
        if not file_path:
            return

        try:
            letters = ['X', 'Y', 'Z', 'W', 'A', 'B', 'C', 'D']
            next_idx = len(self.signals)
            default_alias = letters[next_idx] if next_idx < len(letters) else f"S{next_idx + 1}"
            sig_name = os.path.splitext(os.path.basename(file_path))[0]

            sig = read_signal_from_file(file_path, default_name=sig_name, default_alias=default_alias)
            self.signals.append(sig)
            self.active_signal_name = sig.name

            self._rebuild_signals_ui()
            self._update_views()
            self.lbl_status_badge.setText(f"Loaded '{sig.name}' ({sig.n_samples} samples).")

        except Exception as e:
            QMessageBox.critical(self, "File Load Error", f"Could not load signal file:\n{str(e)}")

    def _on_remove_signal_clicked(self):
        if not self.signals:
            return

        target_sig = self._get_active_signal()
        if not target_sig:
            target_sig = self.signals[-1]

        if target_sig in self.signals:
            self.signals.remove(target_sig)
            self.lbl_status_badge.setText(f"Removed signal '{target_sig.name}'.")
            self.active_signal_name = self.signals[0].name if self.signals else None
            self._rebuild_signals_ui()
            self._update_views()

    def _on_save_result_clicked(self):
        if self.result_signal is None:
            QMessageBox.warning(self, "No Result", "No result signal to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Result Signal", "result_signal.txt", "Text Files (*.txt);;All Files (*)"
        )
        if not file_path:
            return

        try:
            write_signal_to_file(self.result_signal, file_path)
            self.lbl_status_badge.setText(f"Result saved to {os.path.basename(file_path)}.")
            QMessageBox.information(self, "Saved", f"Result signal saved successfully to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Could not save file:\n{str(e)}")

    def _on_clear_result_clicked(self):
        self.result_signal = None
        self.current_operation_name = "None"
        self.procedural_steps = []
        if self.active_signal_name == "Result":
            self.active_signal_name = self.signals[0].name if self.signals else None

        self._rebuild_signals_ui()
        self._update_views()
        self.lbl_status_badge.setText("Result cleared.")

    def _load_initial_signals(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        task_dir = os.path.join(base_dir, "tasks", "Lab 1", "Task 1 testcases and testing functions")
        s1 = os.path.join(task_dir, "Signal1.txt")
        s2 = os.path.join(task_dir, "Signal2.txt")
        if os.path.exists(s1) and os.path.exists(s2):
            self.signals = [
                read_signal_from_file(s1, default_name="Signal 1", default_alias="X"),
                read_signal_from_file(s2, default_name="Signal 2", default_alias="Y")
            ]
        self.result_signal = None
        self._rebuild_signals_ui()
        self._update_views()

    def _toggle_stems(self):
        self.canvas.show_stems = self.btn_stems.isChecked()
        self.btn_stems.setText("Stems: ON" if self.canvas.show_stems else "Stems: OFF")
        self._update_views()

    def _toggle_lines(self):
        self.canvas.show_lines = self.btn_lines.isChecked()
        self.btn_lines.setText("Lines: ON" if self.canvas.show_lines else "Lines: OFF")
        self._update_views()

    def _toggle_grid(self):
        self.canvas.show_grid = self.btn_grid.isChecked()
        self.btn_grid.setText("Grid: ON" if self.canvas.show_grid else "Grid: OFF")
        self._update_views()


def run_app():
    app = QApplication.instance() or QApplication(sys.argv)
    app.setStyleSheet(QSS_STYLE)
    win = DSPMainWindow()
    win.show()
    return app.exec()


"""
File Combiner Application
=========================

File Name: file_combiner_app.py
Description:
    A PySide6-based GUI application that allows users to select multiple text files, view their contents,
    and combine them into a single output file. The application provides functionality to add files,
    remove files from the list, rearrange them via drag-and-drop, and view the contents of the selected file.
    Once combined, the files are written to a new text file with a header for each file.

Author: Curtis Mechling <cmechlin@gmail.com>
Date: October 18, 2024

Copyright:
----------
© 2024 Curtis Mechling, 2bithack. All rights reserved.


License:
--------
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Revision History:
-----------------
- 1.0.0 (2024-10-18): Initial version with file addition, removal, drag-and-drop reordering,
                      file content display, and file combination functionality.
"""

import sys
import datetime
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QAbstractItemView,
    QHeaderView,
    QHBoxLayout,
)
from PySide6.QtCore import Qt, QSettings


class FileCombinerApp(QMainWindow):
    """
    Main application class for the File Combiner GUI.

    This class handles the creation of the user interface, management of the file list,
    and execution of file-related actions, such as adding files, viewing contents,
     and combining files.
    """

    def __init__(self):
        """
        Initializes the FileCombinerApp window and its widgets.

        Sets up the layout, buttons, file table, and text boxes for displaying file contents and
         log messages.
        Connects user actions to corresponding event handlers.
        """

        super().__init__()

        # Initialize QSettings to store and retrieve app settings
        self.settings = QSettings("2bithack", "FileCombinerApp")

        # Retrieve the last used directory, if available
        self.last_directory = self.settings.value("last_directory", "")

        # Main layout
        self.setWindowTitle("File Combiner")
        self.resize(800, 600)
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # File List (QTableWidget)
        self.file_table = QTableWidget(0, 2)
        self.file_table.setHorizontalHeaderLabels(["Filename", "Path"])
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.file_table.setDragDropMode(QAbstractItemView.InternalMove)
        self.file_table.setDragEnabled(True)
        self.file_table.setDragDropOverwriteMode(False)
        self.file_table.dropEvent = self.dropEvent
        self.file_table.setAcceptDrops(True)
        self.file_table.setDropIndicatorShown(True)
        self.file_table.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.file_table)

        # Textbox to display selected file contents
        self.content_textbox = QTextEdit()
        self.content_textbox.setReadOnly(True)
        layout.addWidget(self.content_textbox)

        # Log Textbox
        self.log_textbox = QTextEdit()
        self.log_textbox.setReadOnly(True)
        layout.addWidget(self.log_textbox)

        # Button layout
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Files")
        self.add_button.clicked.connect(self.add_files)
        self.process_button = QPushButton("Combine Files")
        self.process_button.clicked.connect(self.combine_files)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.process_button)

        layout.addLayout(button_layout)
        self.setCentralWidget(central_widget)

        # Store file information
        self.file_list = []

        # Connect file table selection to content display
        self.file_table.itemSelectionChanged.connect(self.display_file_content)

    def read_file(self, file_path):
        """
        Reads the content of a file and returns it as a string.

        Args:
            file_path (str): The path to the file to read.

        Returns:
            str: The content of the file as a string.
        """

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            self.log_textbox.append(f"File not found: {file_path}")
        except PermissionError:
            self.log_textbox.append(f"Permission denied: {file_path}")
        except OSError as e:
            self.log_textbox.append(f"Error reading file: {str(e)}")

    def add_files(self):
        """
        Handles the action of adding files to the file list.

        Opens a QFileDialog for selecting multiple files.
         Adds the selected files to the file table and stores their paths.
        Logs the file addition event in the log text box.
        """

        file_dialog = QFileDialog()
        files, _ = file_dialog.getOpenFileNames(
            self, "Select Files", self.last_directory
        )
        if files:
            # Update the last directory to the one where the files were selected
            self.last_directory = files[0].rsplit("/", 1)[0]
            self.settings.setValue("last_directory", self.last_directory)

            for file in files:
                self.log_textbox.append(f"Added file: {file}")
                self.file_list.append(file)
            self.populate_table()

    def populate_table(self):
        """
        Populates the file table with the files in the file list.

        Clears the existing table contents and adds the files from the file list.
        """

        # self.file_table.clearContents()
        self.file_table.setRowCount(0)
        for file in self.file_list:
            filename = file.split("/")[-1]
            row_position = self.file_table.rowCount()
            self.file_table.insertRow(row_position)
            self.file_table.setItem(row_position, 0, QTableWidgetItem(filename))
            self.file_table.setItem(row_position, 1, QTableWidgetItem(file))

    def display_file_content(self):
        """
        Displays the content of the currently selected file in the content text box.

        Triggered when the user selects a file from the file list.
         Reads the file content and shows it in the content text box.
        Logs the file viewing action in the log text box.
        """

        selected_items = self.file_table.selectedItems()
        if selected_items:
            selected_file = selected_items[1].text()
            content = self.read_file(selected_file)
            self.content_textbox.setText(content)

    def dropEvent(self, event):
        """
        Custom drop event to handle reordering of files in both the table and the file_list list.
        This ensures the underlying data matches the visual order in the table after dragging rows.
        """
        if event.source() == self.file_table:
            event.setDropAction(Qt.MoveAction)
            event.accept()

            selected_row = self.file_table.currentRow()
            target_row = self.file_table.indexAt(event.pos()).row()

            if target_row >= 0 and target_row != selected_row:
                # Swap file paths in file_list
                self.file_list[selected_row], self.file_list[target_row] = (
                    self.file_list[target_row],
                    self.file_list[selected_row],
                )
                self.populate_table()

        super().dropEvent(event)

    def combine_files(self):
        """
        Handles the action of combining the listed files into a single output file.

        Prompts the user with a QFileDialog to select a save location for the combined file.
        Creates a new file and appends the contents of each file from the file list,
        with headers marking each file.
        Logs the result of the file combination process in the log text box.
        """

        # Get the current date in YYYYMMDD format
        current_date = datetime.datetime.now().strftime("%Y%m%d")

        # Provide a default filename using the current date
        default_filename = f"combined_{current_date}.txt"

        save_dialog = QFileDialog()
        save_file, _ = save_dialog.getSaveFileName(
            self,
            "Save Combined File",
            f"{self.last_directory}/{default_filename}",
            filter="Text Files (*.txt);;All Files (*)",
        )
        if save_file:
            # Update the last directory
            self.last_directory = save_file.rsplit("/", 1)[0]
            self.settings.setValue("last_directory", self.last_directory)

            try:
                with open(save_file, "w", encoding="utf-8") as f:
                    seperator = "************************************************************************\n"
                    for file_path in self.file_list:
                        content = self.read_file(file_path)
                        f.write(f"{seperator}{file_path}\n{seperator}")
                        f.write(content)
                        f.write("\n\n")
                    self.log_textbox.append("Files combined successfully.")
                self.log_textbox.append(f"Combined file saved as: {save_file}")
            except FileNotFoundError:
                self.log_textbox.append(f"Destination file not found: {save_file}")
            except PermissionError:
                self.log_textbox.append(
                    f"Permission denied for destination file: {save_file}"
                )
            except OSError as e:
                self.log_textbox.append(f"Error saving combined file: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = FileCombinerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

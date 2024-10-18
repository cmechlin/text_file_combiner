# File Combiner Application

A PySide6-based GUI application that allows users to select multiple text files, view their contents, and combine them into a single output file. The application provides functionality to add files, remove files from the list, rearrange them via drag-and-drop, and view the contents of the selected file.

## Features

- **Add Files**: Select multiple files using a file dialog and add them to the list.
- **View File Contents**: Select a file from the list to view its contents.
- **Drag-and-Drop Reordering**: Reorder the list of files by dragging and dropping them within the table.
- **Combine Files**: Combine all listed files into a single text file, with a custom separator between files.

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/cmechlin/file-combiner-app.git
   ```

2. Install the required dependencies using `pip`:

   ```bash
   pip install PySide6
   ```

3. Run the application:

   ```bash
   python app.py
   ```

## Screenshots

## How It Works

- **File Selection**: Use the "Add Files" button to open a file dialog and select one or more text files. These files will be added to the list.
- **Reordering**: Drag and drop rows within the list to reorder the files. The internal file list will automatically update to reflect the new order.
- **File Viewing**: When a file is selected in the list, its contents are displayed in the text area below.
- **File Combining**: Click "Combine Files" to create a new file that contains the contents of all the selected files, separated by a custom header.

## Future Improvements

- **File Removal**: Add a feature to allow users to remove a file from the list.
- **Custom Headers and Separators**: Allow users to customize the separator/header text between files in the combined output.
- **File Encoding Support**: Add support for different file encodings (e.g., UTF-16) and handle encoding errors more gracefully.
- **Error Handling for File Formats**: Add error handling for non-text files or unsupported file formats that may be accidentally selected.
- **Theme Support**: Add dark mode or other themes to improve the user experience.

## Known Issues

- **No File Deletion**: Currently, there is no way to remove files from the list once they are added.
- **Limited Error Handling**: Error handling is limited to basic file-related errors such as permission issues or missing files. More specific error messages and handling for invalid file formats are needed.
- **File Overwrite Warning**: There's no warning if the user selects an existing file name when saving the combined file, which could lead to accidental overwriting.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Curtis Mechling** - [cmechlin@gmail.com](mailto:cmechlin@gmail.com)

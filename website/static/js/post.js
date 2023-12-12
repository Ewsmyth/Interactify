function updateLabel(input) {
    const fileLabel = document.getElementById('file_label');
    if (input.files.length > 0) {
        fileLabel.innerText = input.files[0].name; // Display the selected filename
    } else {
        fileLabel.innerText = 'Photo/video'; // Reset label if no file selected
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Load the URL from storage and set it in the input field
    browser.storage.local.get('pyytsync_url')
        .then(data => {
            if (data.pyytsync_url) {
                document.getElementById('pyytsyncURL').value = data.pyytsync_url;
            }
        })
        .catch(error => console.error('Error loading URL:', error));
});

document.getElementById('save').addEventListener('click', function() {
    const url = document.getElementById('pyytsyncURL').value;
    if (url) {
        browser.storage.local.set({ pyytsync_url: url })
            .then(() => alert('URL saved successfully!'))
            .catch(error => console.error('Error saving URL:', error));
    } else {
        alert('Please enter a valid URL.');
    }
});

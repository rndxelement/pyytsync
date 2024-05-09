// Create a context menu item to allow users to send a video to pyytsync
// This menu item appears when right-clicking on a link
browser.contextMenus.create({
    id: "send-video-to-pyytsync",
    title: "Send video to pyytsync",
    contexts: ["link"],
}, () => {
    // Clear any runtime errors to prevent a persistent error icon
    void browser.runtime.lastError;
});

/**
 * Parse a YouTube URL to extract the video ID.
 * @param {string} url - The YouTube URL to parse.
 * @returns {string|boolean} The extracted video ID, or false if the URL is invalid.
 */
function youtube_parser(url) {
    const regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    const match = url.match(regExp);
    return (match && match[7].length == 11) ? match[7] : false;
}

/**
 * Fetch the title of a YouTube video based on its ID.
 * This function scrapes the title from the video's page since it's a simple way to avoid needing an API key.
 * @param {string} videoId - The ID of the YouTube video.
 * @returns {Promise<string|null>} A promise that resolves to the video title, or null if fetching fails.
 */
function getVideoTitle(videoId) {
    return fetch(`https://www.youtube.com/watch?v=${videoId}`)
        .then(response => response.text())
        .then(html => {
            const doc = new DOMParser().parseFromString(html, "text/html");
            const title = doc.querySelector('meta[name="title"]').content;
            return title;
        })
        .catch(error => {
            console.error("Failed to fetch YouTube title", error);
            return null;
        });
}

// Add a listener for clicks on the context menu item
browser.contextMenus.onClicked.addListener(async (info, tab) => {
    if (info.menuItemId === "send-video-to-pyytsync") {
        const url = info.linkUrl;
        const video_id = youtube_parser(url);
        if (video_id) {
            const video_title = await getVideoTitle(video_id);
            if (video_title) {
                sendToServer(video_id, video_title);
            }
        }
    }
});

// Generates a system notification
function genNotification(m) {
    const title = "Notification from pyytsync extension";
    browser.notifications.create({
      type: "basic",
      title,
      message: m,
    });
}

/**
 * Send a video to the pyytsync server.
 * This function sends a GET request to the server to add the video to a playlist.
 * @param {string} videoId - The ID of the YouTube video.
 * @param {string} videoTitle - The title of the YouTube video.
 */
function sendToServer(videoId, videoTitle) {
    // Fetch URL from storage
    browser.storage.local.get('pyytsync_url')
        .then(data => {
            const serverUrl = `${data.pyytsync_url || 'https://defaulturl.com'}/add-vid-to-playlist?video_id=${videoId}&video_title=${encodeURIComponent(videoTitle)}`;
            console.log("Sending request to: " + serverUrl);
            return fetch(serverUrl);
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
        })
        .then(data => {
            console.log("Server response:", data);
        })
        .catch(error => {
            console.error("Error:", error);
            genNotification("Failed sending request to pyytsync instance. Error: " + error.message);
        });
}

// Function to create the image gallery
function createImageGallery(data) {
    const gallery = document.getElementById('image-gallery');

    data.forEach(item => {
        if (item.img_preview) {
            const imageElement = document.createElement('img');
            imageElement.src = item.img_preview;
            const linkElement = document.createElement('a');
            linkElement.href = item.site_redirect;

            // Check if is_animated is true in the JSON data
            if (item.is_animated) {
                // If it's true, add an orange border to the image
                imageElement.classList.add('animated-image');
            }

            linkElement.appendChild(imageElement);
            gallery.appendChild(linkElement);
        } else {
            // Create and display a default image with a link when img_preview is None
            const defaultImageElement = document.createElement('img');
            defaultImageElement.src = 'assets/images/Unavailable.jpg';
            const defaultLinkElement = document.createElement('a');
            defaultLinkElement.href = item.site_redirect;
            defaultLinkElement.appendChild(defaultImageElement);
            gallery.appendChild(defaultLinkElement);
        }
    });
}

// Load the JSON files in order (to minimize user confusion when images change on reload)
fetch('api_json_output/danbooru_images.json')
    .then(response => response.json())
    .then(imageData => {
        createImageGallery(imageData);
        // After the first JSON file is loaded and processed, load the second JSON file
        return fetch('api_json_output/gelbooru_images.json');
    })
    .then(response => response.json())
    .then(imageData => {
        createImageGallery(imageData);
        // After the second JSON file is loaded and processed, load the third JSON file
        return fetch('api_json_output/aibooru_images.json');
    })
    .then(response => response.json())
    .then(imageData => {
        createImageGallery(imageData);
        // After the third JSON file is loaded and processed, load the fourth JSON file
        return fetch('api_json_output/pixiv_images.json');
    })
    .then(response => response.json())
    .then(imageData => {
        createImageGallery(imageData);
    })
    .catch(error => {
        console.error('Error fetching JSON:', error);
    });

// Function to debounce a function
const debounce = (mainFunction, delay) => {
    // Declare a variable called 'timer' to store the timer ID
    let timer;
  
    // Return an anonymous function that takes in any number of arguments
    return function (...args) {
      // Clear the previous timer to prevent the execution of 'mainFunction'
      clearTimeout(timer);
  
      // Set a new timer that will execute 'mainFunction' after the specified delay
      timer = setTimeout(() => {
        mainFunction(...args);
      }, delay);
    };
  };

// Function to create the image gallery
const allTagsSet = new Set();

function createImageGallery(data) {
    // Images
    const gallery = document.getElementById('image-gallery');

    data.images.forEach(item => {
        const imageElement = document.createElement('img');
        const linkElement = document.createElement('a');

        if (item.img_preview) {
            imageElement.src = item.img_preview;
        } else {
            imageElement.src = 'assets/images/Unavailable.jpg';
        }

        linkElement.href = item.site_redirect;
        linkElement.appendChild(imageElement);

        // Add a class for animated images
        if (item.is_animated) {
            imageElement.classList.add('animated-image');
        }

        // Store the image tags as data attributes
        imageElement.setAttribute('data-tags', item.tags.join(' ')); // Assuming tags is an array

        // Add a class based on the image tags
        item.tags.forEach(tag => {
            linkElement.classList.add(`tag-${tag}`);
        });

        gallery.appendChild(linkElement);
    });

    // Tags for search bar
    data.tag_set.forEach(item => {
        allTagsSet.add(item);
    });
}



// Function to update the image gallery based on checkbox state
function updateImageGallery() {
    const checkboxes = document.querySelectorAll('#image-source-switches input[type="checkbox"]');
    const checkedSources = Array.from(checkboxes).filter(checkbox => checkbox.checked).map(checkbox => checkbox.value);

    // Reset gallery
    clearImageGallery();

    // Fetch and create image galleries for selected sources
    fetchImageGalleries(checkedSources);
    
}

// Debounced version of function
const debouncedUpdateImageGallery = debounce(updateImageGallery, 500)

// Function to clear the image gallery
function clearImageGallery() {
    const gallery = document.getElementById('image-gallery');
    gallery.innerHTML = ''; // Clear the gallery content
    allTagsSet.clear() // Clear existing tag set
    autofillList.innerHTML = "";
    searchInput.value = ''
}

// Function to fetch and create image galleries for selected sources
function fetchImageGalleries(selectedSources) {

    // Fetch and create image galleries for selected sources using express API
    selectedSources.forEach(source => {
        let file_name = source + '_images';
        fetch(`/jsonData/${file_name}`)
            .then(response => {
                if (response.status === 200) {
                    return response.json();
                } else {
                    throw new Error(`Error fetching JSON for ${source}`);
                }
            })
            .then(imageData => {
                createImageGallery(imageData);
            })
            .catch(error => {
                console.error(error);
            });
    });
}


// Add event listeners to checkboxes to update the image gallery
const checkboxes = document.querySelectorAll('#image-source-switches input[type="checkbox"]');
checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', debouncedUpdateImageGallery);
});

// Listener for refresh button to call python script through express API
const retrieveButton = document.getElementById('retrieve-button');
retrieveButton.addEventListener('click', () => {
    retrieveButton.disabled = true; // Dont allow more than one click at a time
    fetch('/runPython')
    .then(response => {
        retrieveButton.disabled = false; // Re-enable button
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        console.log('Response data:', data);
        updateImageGallery(); // Display new json data
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


// Function to update the autofill list
const searchInput = document.getElementById("search-input");
const autofillList = document.getElementById("autofill-list");
const maxSuggestions = 40; // Maximum number of suggestions to display

function updateAutofillList() {
    const inputValue = searchInput.value.trim().toLowerCase(); // Remove leading/trailing spaces
    autofillList.innerHTML = ''; // Clear the previous suggestions

    let suggestionCount = 0; // Counter for displayed suggestions

    const lastWord = inputValue.split(' ').pop(); // Get the last word after splitting by spaces

    for (const suggestion of allTagsSet) {
        if (suggestionCount >= maxSuggestions) {
            break; // Stop adding suggestions once the limit is reached
        }

        if (suggestion.toLowerCase().startsWith(lastWord)) {
            const listItem = document.createElement('li');
            listItem.textContent = suggestion;
            listItem.addEventListener('click', () => {
                // Fill in the input field with the selected suggestion
                searchInput.value = inputValue.replace(new RegExp(lastWord + '$'), suggestion);
                // Clear the autofill list
                autofillList.innerHTML = '';
            });
            autofillList.appendChild(listItem);
            suggestionCount++; // Increment the counter
        }
    }
}


// Listen for input events on the search input
searchInput.addEventListener("input", updateAutofillList);

// Listen for "keydown" event on the search input
searchInput.addEventListener("keydown", (event) => {
    if (event.key === 'Enter') {
        // Prevent the default behavior of the Enter key (e.g., form submission)
        event.preventDefault();
        searchTags();
    }
});

// Function to get tags off search click
function searchTags() {
    const tagsInput = searchInput.value;
    const tagsList = tagsInput.split(' ').filter(tag => tag.trim() !== '');

    // Hide or show gallery images based on tags
    const gallery = document.getElementById('image-gallery');
    const imageLinks = gallery.querySelectorAll('a');

    imageLinks.forEach(linkElement => {
        let hideImage = false;
        tagsList.forEach(tag => {
            if (!linkElement.classList.contains(`tag-${tag}`)) {
                hideImage = true;
            }
        });

        if (hideImage) {
            linkElement.style.display = 'none';
        } else {
            linkElement.style.display = 'block';
        }
    }
)}

// Listen for click on search button
const searchButton = document.getElementById("search-button")
searchButton.addEventListener("click", searchTags);

// Handle clicks outside of the autofill list to clear it
document.addEventListener("click", (event) => {
    if (event.target !== searchInput && event.target !== autofillList) {
        autofillList.innerHTML = "";
    }
});


// Bootup gallery
updateImageGallery();
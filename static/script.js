window.onload = function () {
    document.getElementById('searchBtn').addEventListener('click', sendInput);
    document.getElementById('generateBtn').addEventListener('click', generateImages);
}


function sendInput() {
    let userInput = document.getElementById('userInput').value;

    let loadingIndicator = document.getElementById('loadingIndicator');
    loadingIndicator.classList.remove('hidden');
    fetch('/api/search_images?input=' + userInput)
        .then(response => response.json())
        .then(json => {
            let serverResponse = document.getElementById('serverResponse');
            // Clear the serverResponse div
            serverResponse.innerHTML = '';

            // Create a new img element for each image and append it to the serverResponse div
            for (let image of json) {
                let newImg = document.createElement('img');
                newImg.src = image.image_path;
                newImg.alt = image.user_input;
                newImg.title = image.user_input;
                newImg.className = 'w-32 h-32';

                serverResponse.appendChild(newImg);
            }

            // Hide the loading indicator again
            loadingIndicator.classList.add('hidden');
        })
        .catch(error => {
            loadingIndicator.classList.add('hidden');
            console.error('Error:', error);
        });
}

function generateImages() {
    let userInput = document.getElementById('userInput').value;

    // Get the loading indicator and show it
    let loadingIndicator = document.getElementById('loadingIndicator');
    loadingIndicator.classList.remove('hidden');
    fetch('/api/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            input: userInput
        })
    })
        .then(response => response.json())
        .then(json => {
            if (json.error) {
                loadingIndicator.classList.add('hidden');
                throw new Error(json.error);
            } else {
                // Fetch the list of images after a new one is generated
                return fetch('/api/search_images?input=any');
            }
        })
        .then(response => response.json())
        .then(json => {
            let serverResponse = document.getElementById('serverResponse');
            // reset the input again
            document.getElementById('userInput').value = "";

            // Clear the serverResponse div
            serverResponse.innerHTML = '';

            // Create a new img element for each image and append it to the serverResponse div
            for (let image of json) {
                let newImg = document.createElement('img');
                newImg.src = image.image_path;
                newImg.alt = image.user_input;
                newImg.title = image.user_input;
                newImg.className = 'w-32 h-32';

                serverResponse.appendChild(newImg);
            }

            // Hide the loading indicator again
            loadingIndicator.classList.add('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            loadingIndicator.classList.add('hidden');
        });
}

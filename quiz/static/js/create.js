// Set Django URL and CSRF token for JS
const createFolderUrl = "{% url 'create_folder' %}";
const csrfToken = "{{ csrf_token }}";

// Show popup when add button is clicked
document.getElementById("addbtn").addEventListener("click", function() {
    document.getElementById("popup").style.display = "block";
});

// Close popup when close button is clicked
document.getElementById("closePopup").addEventListener("click", function() {
    document.getElementById("popup").style.display = "none";
});

// Handle Enter key inside input box
document.getElementById("inputBox").addEventListener("keypress", function (event) {
    if (event.key === "Enter" && this.value.trim() !== "") {
        event.preventDefault();
        let name = this.value.trim();

        fetch(createFolderUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrfToken
            },
            body: `folder_name=${encodeURIComponent(name)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Failed to create folder: " + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred: ' + error.message);
        });

        document.getElementById("popup").style.display = "none";
        this.value = "";
    }
});
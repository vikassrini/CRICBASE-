function submitForm() {
    // Create a new object to store the form data
    var playerData = {};
    // Iterate through the form inputs and add their values to the object
    var formElements = document.getElementById("player-form").elements;
    for (var i = 0; i < formElements.length; i++) {
        var element = formElements[i];
        if (element.name) {
            playerData[element.name] = element.value;
        }
    }

    // Convert the player data object to a JSON string
    var playerDataJson = JSON.stringify(playerData);

    // Use the Fetch API to send the JSON to the /players endpoint
    fetch("/players", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: playerDataJson
    })
    .then(response => response.text())
    .then(data => {
        // Display the response from the server
        alert(data);
    })
    .catch(error => console.error("Error:", error));
}

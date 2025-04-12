//Listener to verify user is logged in - runs first before loading user data
document.addEventListener("DOMContentLoaded", function() {
    //only can view other profiles if logged in
    if (!localStorage.getItem("user_id")) {
        window.location.href = "/"; //redirect to home if not logged in
    }

    //button listeners
    document.getElementById("skip").addEventListener("click", handleSkipClick);
    document.getElementById("like").addEventListener("click", handleLikeClick);

    getNextProfile(); //call to display first profile on page load
});

function getNextProfile(lastSeenId = null) {
    const headers = {
        "Content-Type": "application/json",
        "User-Id": localStorage.getItem("user_id")
    }

    //debug
    console.log("Sending User-Id:", localStorage.getItem("user_id"));

    //get value of last seen profile if sent in header
    if (lastSeenId) headers["Last-Seen-Id"] = lastSeenId

    //GET - client side display profile data
    fetch("/api/view-recommendations", { method: "GET", headers })
    .then(response => response.json())
    .then(data => {
        const profileContainer = document.getElementById("profileContainer");

        if(data.msg) {
            profileContainer.innerHTML = '<p>No more profiles available</p>';
            return;
        }

        //display profile information
        if (data.username) {
            profileContainer.innerHTML = `
                <p><strong>First Name:</strong> ${data.first}</p>
                <p><strong>Age:</strong> ${data.age}</p>
                <p><strong>Family Plans:</strong> ${data.wantChildren}</p>
                <p><strong>Have Children?:</strong> ${data.haveChildren}</p>
                <p><strong>Political Offiliation:</strong> ${data.politics}</p>
                <p><strong>Religion:</strong> ${data.religion}</p>
                <p><strong>Gender:</strong> ${data.gender}</p>
            `;

            //store current profile ID for buttons
            document.getElementById("skip").dataset.profileId = data._id;
            document.getElementById("like").dataset.profileId = data._id;
        } else {
            profileContainer.innerHTML = "<p>Error: Profile data not found.</p>";
        }        
    })
    .catch(error => console.error("Error:", error));
}

//button functions
//Next button
function handleSkipClick() {
    //may be better to move userId and currentUserId to global variables
    const userId = localStorage.getItem("user_id");
    const currentUserId = document.getElementById("skip").dataset.profileId;
    console.log("Skip button clicked. Fetching profile after:", currentUserId);

    if (!currentUserId) {
        console.error("Error: No profile selected to like.");
        return;
    }

    fetch("/api/skip-profile", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "User-Id": userId
        },
        body: JSON.stringify({ skipped_user_id: currentUserId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Error: ", data.error);
            return;
        }

        console.log("Profile skipped successfully: ", currentUserId);
        getNextProfile(currentUserId); //call function to move to next profile after liking
    })
    .catch(error => console.error("Error:", error));
}

//Like button
function handleLikeClick() {
    const userId = localStorage.getItem("user_id");
    const currentUserId = document.getElementById("like").dataset.profileId;

    if (!currentUserId) {
        console.error("Error: No profile selected to like.");
        return;
    }

    fetch("/api/like-profile", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "User-Id": userId
        },
        body: JSON.stringify({ liked_user_id: currentUserId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Error: ", data.error);
            return;
        }

        console.log("Profile liked successfully: ", currentUserId);
        getNextProfile(currentUserId); //call function to move to next profile after liking
    })
    .catch(error => console.error("Error:", error));
}
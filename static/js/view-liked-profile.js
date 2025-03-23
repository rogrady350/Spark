//Listener to verify user is logged in - runs first before loading user data
document.addEventListener("DOMContentLoaded", function() {
    //only can view other profiles if logged in
    if (!localStorage.getItem("user_id")) {
        window.location.href = "/"; //redirect to home if not logged in
        return;
    }

    //profile of desired like to view
    const viewUserId = new URLSearchParams(window.location.search).get("user_id");

    //handle manual navigation to page or broken id errors
    if (!viewUserId) {
        alert("Unavailable. No user selected");
        return;
    }

    //display selected profile on page load
    loadProfile(viewUserId);

    //button listeners
    //skip button
    document.getElementById("skip").addEventListener("click", function() {
        skipProfile(viewUserId) ;
    });

    //like button
    document.getElementById("like").addEventListener("click", function() {
        likeProfile(viewUserId);
    });
});

//view  userprofile of selected like
function loadProfile(userId) {
    //GET - client side view profile data
    fetch("/api/view-profile", { 
        method: "GET", 
        headers: {
            "Content-Type": "application/json",
            "User-Id": userId,
        },
    })
    .then(response => response.json())
    .then(data => {
        const profileContainer = document.getElementById("profileContainer");

        if(data.error) {
            profileContainer.innerHTML = '<p>No more profiles available</p>';
            return;
        }

        if (data.username) {
            profileContainer.innerHTML = `
                <p><strong>First Name:</strong> ${data.first}</p>
                <p><strong>Age:</strong> ${data.age}</p>
                <p><strong>Family Plans:</strong> ${data.haveChildren}</p>
                <p><strong>Have Children?:</strong> ${data.wantChildren}</p>
                <p><strong>Match With:</strong> ${data.matchPreferences}</p>
                <p><strong>Political Offiliation:</strong> ${data.politics}</p>
                <p><strong>Religion:</strong> ${data.religion}</p>
            `;
        } else {
            profileContainer.innerHTML = "<p>Error: Profile data not found.</p>";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("profileContainer").innerHTML = "<p>Unable to load profile. Please try again later.</p>";
    });
}

//button functions
//skip button
function skipProfile(skippedUserId) {
    fetch("/api/skip-profile", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "User-Id": localStorage.getItem("user_id")
        },
        body: JSON.stringify({ skipped_user_id: skippedUserId })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.msg || "Profile Skipped")
        window.location.href = "/view-likes"; //redirect back to likes page if skipped
    });
}

//like button
function likeProfile (likedUserId) {
    fetch("/api/match-profile", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "User-Id": localStorage.getItem("user_id"),
        },
        body: JSON.stringify({ liked_user_id: likedUserId }),
    })
    .then((response) => response.json())
    .then((data) => {
        alert(data.msg || "You Matched!");
        window.location.href = "/view-likes"; //redirect back to likes page
    });
}
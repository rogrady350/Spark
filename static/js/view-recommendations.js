//Listener to verify user is logged in - runs first before loading user data
document.addEventListener("DOMContentLoaded", function() {
    if (!localStorage.getItem("user_id")) {
        window.location.href = "/"; //redirect to home if not logged in
    }     

    //GET - client side display profile data. only runs if user logged in
    fetch("/api/view-profile", {
        method: "GET",
        headers: { 
            "Content-Type": "application/json" ,
            "User-Id": localStorage.getItem("user_id") //change to other profiles
        }
    })
    .then(response => response.json())
    .then(data => {
        const profileContainer = document.getElementById("profileContainer");
        profileContainer.innerHTML = ""; //clear previous data

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
    .catch(error => console.error("Error:", error));
});
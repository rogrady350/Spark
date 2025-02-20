//Listener to verify user is logged in - runs first before loading user data
document.addEventListener("DOMContentLoaded", function() {
    if (!localStorage.getItem("user_id")) {
        window.location.href = "/"; //redirect to home if not logged in
    }
});

//GET - client side display profile data. only runs if user logged in
fetch("/api/view-profile", {
    method: "GET",
    headers: { "Content-Type": "application/json" }
})
.then(response => response.json())
.then(data => {
    const profileContainer = document.getElementById("profileContainer");
    profileContainer.innerHTML = ""; //clear previous data

    if (data.username) {
        profileContainer.innerHTML = `
            <p><strong>Username:</strong> ${data.username}</p>
            <p><strong>First Name:</strong> ${data.first}</p>
            <p><strong>Last Name:</strong> ${data.last}</p>
            <p><strong>Email:</strong> ${data.email}</p>
            <p><strong>Age:</strong> ${data.age}</p>
        `;
    } else {
        profileContainer.innerHTML = "<p>Error: Profile data not found.</p>";
    }
})
.catch(error => console.error("Error:", error));
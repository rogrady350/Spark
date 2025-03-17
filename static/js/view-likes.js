document.addEventListener("DOMContentLoaded", function(){
    //can only view likes if logged in
    const userId = localStorage.getItem("user_id");

    if (!userId) {
        window.location.href = "/"; 
        return;
    }

    fetch("/api/view-likes", {
        method: "GET",
        headers: { 
            "Content-Type": "application/json",
            "User-Id": userId
        }
    })
    .then(response => response.json())
    .then(data => {
        const likesContainer = document.getElementById("likes-container");

        //show empty table if user has no likes at this time
        if (!data || data.length === 0) {
            likesContainer.innerHTML = "<tr><td colspan='3'>No liked profiles yet.</td></tr>";
            return;
        }

        //populate table with profiles that liked user
        likesContainer.innerHTML = "";
        data.forEach(profile => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${profile.first || "Unknown"}</td>
                <td>${profile.username || "Unkonwn"}</td>
                <td>
                    <button class="view-profile-btn" data-id="${profile._id}">View Profile</button>
                </td>
            `;
            likesContainer.appendChild(row);
        });

        //attach listeners to all "View Profile" buttons
        document.querySelectorAll(".view-profile-btn").forEach(button => {
            button.addEventListener("click", function() {
                const profileId = this.getAttribute("data-id")
                window.location.href = `/view-liked-profile?user_id=${profileId}`
            });
        });
    })
    .catch(error => console.error("Error:", error));
});
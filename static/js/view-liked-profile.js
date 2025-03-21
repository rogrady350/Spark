//Listener to verify user is logged in - runs first before loading user data
document.addEventListener("DOMContentLoaded", function() {
    //only can view other profiles if logged in
    if (!localStorage.getItem("user_id")) {
        window.location.href = "/"; //redirect to home if not logged in
    }

    //GET - client side display profile data
    fetch("/api/view-profile", { method: "GET", headers })
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

        //listeners
        //next button
        document.getElementById("next").addEventListener("click", function() {
            console.log("Next button clicked. Fetching profile after:", data._id);
            getNextProfile(data._id)
        });

        //like button
        document.getElementById("like").addEventListener("click", function() {});
    })
    .catch(error => console.error("Error:", error));
});


function skipProfile() {

}


function likeProfile () {
    
}
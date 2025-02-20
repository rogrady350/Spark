//button display based on user being logged in
document.addEventListener("DOMContentLoaded", function() {
    const userId = localStorage.getItem("user_id");

    const profileLink = document.getElementById("profile-link");
    const recommendationsLink = document.getElementById("recommendations-link");
    const logoutBtn = document.getElementById("logout-btn");

    //if not logged in hide all links besides home
    if (!userId) {
        if (profileLink) profileLink.style.display = "none";
        if (recommendationsLink) recommendationsLink.style.display = "none";
        if(logoutBtn) logoutBtn.style.display = "none";
    }

    //logout button listener
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function() {
            localStorage.removeItem("user_id");
            window.location.href = "home"; //redirect to home when logging out
        });
    }
});
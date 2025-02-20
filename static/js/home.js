document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("login");
    const loginButton = document.getElementById("login-btn");

    //Login button listener
    if (loginButton) {
        loginButton.addEventListener("click", function (event) {
            event.preventDefault();  //prevent form from refreshing the page

            //get the values entered by the user
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            //POST - client side send login request to backend
            fetch("/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: username, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    localStorage.setItem("user_id", data.user_id); //store user ID
                    window.location.href = "view-profile"; //redirect to profile page
                } else {
                    alert("Login failed: " + data.msg);  //show error message from backend if login fails
                }
            })
            .catch(error => console.error("Error:", error));
        });   
    }
});
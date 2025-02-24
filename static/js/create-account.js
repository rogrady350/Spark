//submit form
document.addEventListener("DOMContentLoaded", function() {
    //form submission
    document.getElementById("submit").addEventListener("click", function(event) {
        event.preventDefault(); //prevent default form sumbission

        //collect form data
        var profileData =  {
            username: document.getElementById("username").value,
            password: document.getElementById("password").value,
            first: document.getElementById("first").value,
            last: document.getElementById("last").value,
            email: document.getElementById("email").value,
            age: document.getElementById("age").value,
        };

        //POST - client side create-account data
        fetch("/api/create-account", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(profileData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.msg === "SUCCESS") {
                alert("Data Saved");
                window.location.href = "/"; //redirect to home page
            } else {
                console.log(data.msg);
            }
        })
        .catch(error => console.error("Error:", error));
    });

    //clear entire form
    document.getElementById("clear").addEventListener("click", function() {
        document.getElementById("profileForm").reset();
    });

    //cancel filling out profile and return to home page
    document.getElementById("cancel").addEventListener("click", function() {
        window.location.href = "/";
    });
});
document.addEventListener("DOMContentLoaded", function(){
    //only can view likes if logged in
    if (!localStorage.getItem("user_id")) {
        window.location.href = "/"; //redirect to home if not logged in
    }

    fetch
})
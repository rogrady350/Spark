//show/hide text block for other gender
function toggleOtherInput(selectElement) {
    let otherInput = selectElement.nextElementSibling;

    if (selectElement.value === "other") {
        otherInput.style.display = "block";
    } else {
        otherInput.style.display = "none";
        otherInput.value = "";
    }
}

//check all boex if all is checked
function toggleAll() {
    var selectAll = document.getElementById("selectAll");
    var checkboxes = document.querySelectorAll(".matchOption");

    checkboxes.forEach(function(checkbox){
        checkbox.checked = selectAll.checked;
    });
}

//uncheck everyone if another box is manually unchecked
document.querySelectorAll(".matchOption").forEach(function(checkbox) {
    checkbox.addEventListener("change", function() {
        var allChecked = document.querySelectorAll(".matchOption:checked").length === document.querySelectorAll(".matchOption").length;
        document.getElementById("selectAll").checked = allChecked;
    });
});

//submit form
document.addEventListener("DOMContentLoaded", function() {
    //can only update if logged in
    if (!localStorage.getItem("user_id")) {
        window.location.href = "/"; 
        return;
    }
    
    //get selected checkbox values, by className
    function getCheckedValues(className) {
        var selectedValues = [] //array to hold values

        //add checked values to array
        document.querySelectorAll("." + className + ":checked").forEach(function(checkbox) {
            selectedValues.push(checkbox.value);
        });

        return selectedValues;
    }

    //form submission
    document.getElementById("submit").addEventListener("click", function(event) {
        event.preventDefault(); //prevent default form sumbission

        //collect form data
        var profileData =  {
            username: document.getElementById("username").value || undefined,
            password: document.getElementById("password").value || undefined,
            first: document.getElementById("first").value || undefined,
            last: document.getElementById("last").value || undefined,
            email: document.getElementById("email").value || undefined,
            age: document.getElementById("age").value || undefined,
            occupation: document.getElementById("occupation").value || undefined,
            gender: document.getElementById("gender").value || undefined,
            matchPreferences: getCheckedValues("matchOption") || undefined,
            politics: document.getElementById("politics").value || undefined,
            religion: document.getElementById("religion").value || undefined,
            wantChildren: document.getElementById("wantChildren").value || undefined,
            haveChildren: document.getElementById("haveChildren").value || undefined
        };

        /*remove fileds from that were not filled out from submission
          prevent overwriting existing data with blank or null values*/
        Object.keys(profileData).forEach(key => {
            if (profileData[key] == undefined) {
                delete profileData[key];
            }
        });

        //PUT - client side update profile data
        fetch("/api/update-profile", {
            method: "PUT",
            headers: { 
                "Content-Type": "application/json", 
                "User-Id": localStorage.getItem("user_id") 
            },
            body: JSON.stringify(profileData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.msg === "profile updated sucessfully") {
                alert("Profile Updated");
                window.location.href = "/view-profile";
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
        window.location.replace("/view-profile");
    });
});
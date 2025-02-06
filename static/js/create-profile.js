//show/hide text bock for other gender
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
            first: document.getElementById("first").value,
            last: document.getElementById("last").value,
            email: document.getElementById("email").value,
            age: document.getElementById("age").value,
            occupation: document.getElementById("occupation").value,
            gender: document.getElementById("gender").value,
            matchPreferences: getCheckedValues("matchOption"),
            politics: document.getElementById("politics").value,
            religion: document.getElementById("religion").value,
            wantChildren: document.getElementById("wantChildren").value,
            haveChildren: document.getElementById("haveChildren").value
        };

        //POST - client side add profile data
        fetch("/api/create-profile", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(profileData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.msg === "SUCCESS") {
                alert("Data Saved");
            } else {
                console.log(data.msg);
            }
        })
        .catch(error => console.error("Error:", error));
    });

    //clear entire form
    document.getElementById("clear").addEventListener("click", function() {
        document.getElementById("reservation").reset();
    });
});
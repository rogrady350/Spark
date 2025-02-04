//show/hide text bock for other gender
function otherInput() {
    var dropdown = document.getElementById("gender");
    var otherInput = document.getElementById("otherInput");

    if (dropdown.value === "other") {
        otherInput.style.display = "block";
    } else {
        otherInput.style.display = "none";
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
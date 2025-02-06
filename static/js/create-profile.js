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
$("#submit").click(function() {
    //store checkbox values, by className
    function getCheckedValues(className) {
        var selectedValues = [] //array to hold values

        //add values to array
        $("." + className + ":checked").each(function() {
            selectedValues.push($(this).val());
        });

        return selectedValues;
    }

    var profileData =  {
        first: $('#first').val(),
        last: $('#last').val(),
        email: $('#email').val(),
        age: $('#age').val(),
        occupation: $('#occupation').val(),
        gender: $('#gender').val(),
        matchPreferences: getCheckedValues("matchOption"),
        politics: $('#politics').val(),
        religion: $('#religion').val(),
        wantChildren: $('#wantChildren').val(),
        haveChildren: $('#haveChildren').val()
    };

    //POST - client side add data
    $.ajax({
        url: restaurantUrl + "/write-record",
        type: "post",
        data: jsonString,
        success: function(response) {
            var data = JSON.parse(response);
            if(data.msg = "SUCCESS") {
                alert("Data Saved");
            } else {
                console.log(data.msg);
            }
        },
        error: function(err){
            console.log(err);
        }
    })
    return false;
});

//clear entire form
$("#clear").click(function() {
    $("#reservation")[0].reset();
});
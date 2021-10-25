var filterInput = document.querySelector(".user-stamps-header input");
var table = document.querySelector(".bdr table");
var rows = document.querySelectorAll(".bdr table tr");

function searchTable(){

    for (var i=0; i<rows.length; i++){
        var td = rows[i].querySelector("td");
        if (td) {
            txtValue = td.textContent || td.innerText;

            if (txtValue.toUpperCase().indexOf(filterInput.value.toUpperCase()) > -1) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            };
        };
    };
};


filterInput.addEventListener("input", searchTable);
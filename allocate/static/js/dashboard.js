


var invoiceList = document.querySelectorAll("tr td:first-child");
var batchAddButton = document.querySelector("#batch-add");
var checkboxes = document.querySelectorAll(".invoice-add-stamp");
var rows = document.querySelectorAll(".bdr table tr");
var filterInput = document.querySelector(".filter-table input");

//Functions



function getCheckedInvoices(){
    var invoicesToAdd = [];

    for (var i=0; i<checkboxes.length; i++){
        var checkbox = checkboxes[i];
        if (checkbox.checked) {
            invoicesToAdd.push(checkbox.dataset.invoiceid);
        };
    };

    return invoicesToAdd
}

function batchAddStamp(){
    var invoicesToAdd = getCheckedInvoices();

    fetch("/invoicestamp/add/batch", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({invoice_ids: invoicesToAdd,
                            stamp_id: document.getElementById("chosenStamp").value})
        }).then(response => window.location.reload(false))
    };

function batchPrintStamps(){
    var invoicesToPrint = getCheckedInvoices();

    fetch("/printstamp/add/batch", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(invoicesToPrint)
        }).then(response => response.text()).then(function(text){
            window.location.href = "/invoices/send/"+text;
        })
};

function batchDeleteInvoices(){
    var invoicesToDelete = getCheckedInvoices();

    fetch("/invoice/delete/batch", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(invoicesToDelete)
        }).then(response => window.location.reload(false))
}

function toggleChecks(check){

    for (var i=0; i<checkboxes.length; i++){
        var checkbox = checkboxes[i];
        checkbox.checked = check
    };
};

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


//EventListeners

for (var i=0;i<invoiceList.length;i++){
    invoiceList[i].addEventListener("mouseenter",function(){
    this.querySelector(".thumbnail").style.display = "block";
    });
}

for (var i=0;i<invoiceList.length;i++){
    invoiceList[i].addEventListener("mouseleave",function(){
    this.querySelector(".thumbnail").style.display = "none";
    });
}

batchAddButton.addEventListener("click", batchAddStamp);
filterInput.addEventListener("input", searchTable);
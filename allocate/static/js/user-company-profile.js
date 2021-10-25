var emailToAdd = document.querySelector("button[onclick='addUser()']").parentElement.querySelector("input");


function addUser(){
    console.log("im in console");
    fetch("/company/add/"+emailToAdd.value, {
        method: "POST"
    }).then(response=>window.location.reload(false))
};
var companyChoice = document.querySelector(".register-choice-company");
var userChoice = document.querySelector(".register-choice-user");
var companyChoiceInfo = document.querySelector(".register-choice-company-info");
var userChoiceInfo = document.querySelector(".register-choice-user-info");
var activeClassName = "register-choice-chosen"

companyChoice.addEventListener("click", function(){
    userChoice.classList.remove(activeClassName);
    companyChoice.classList.add(activeClassName);

    userChoiceInfo.style.display = "none";
    companyChoiceInfo.style.display = "block";
});

userChoice.addEventListener("click", function(){
    companyChoice.classList.remove(activeClassName);
    userChoice.classList.add(activeClassName);

    companyChoiceInfo.style.display = "none";
    userChoiceInfo.style.display = "block";
})
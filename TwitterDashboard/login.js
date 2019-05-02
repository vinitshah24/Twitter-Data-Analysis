//Focus on Username field when page loads
window.onload = function () {
    document.getElementById("username").focus();
};

//Auto-click on submit button when user clicks Enter on password field
$(document).ready(function(){
    $('#password').keypress(function(e){
      if(e.keyCode==13)
      $('#submit-button').click();
    });
});

//Login verifiaction to access the website
var loginAttempt = 3;
function validate() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    if (username == "admin" && password == "admin123") {
        alert("Welcome to Twitter Dashboard");
        window.location = "index.html";
        return false;
    }
    else {
        loginAttempt--;
        alert("Only " + loginAttempt + " loginAttempt left!");
        if (loginAttempt == 0) {
            document.getElementById("username").disabled = true;
            document.getElementById("password").disabled = true;
            document.getElementById("submit-button").disabled = true;
            return false;
        }
    }
}
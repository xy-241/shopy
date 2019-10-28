//menu
function menuFunction(x){
  x.classList.toggle("change");
}


var toggleNavStatus = false;

var toggleNav = function(){
  var getSideNav = document.querySelector(".sideNav");
  var getSideNavUl = document.querySelector(".sideNav ul");
  var getSideNavA = document.querySelectorAll(".sideNav a");

  var getSection = document.querySelector("article");
  var getMainNav = document.querySelector(".navMain"); //navMain
  var getFooter = document.querySelector('footer');

  var getBody = document.querySelector("body"); //body

  if(toggleNavStatus == false){
    getSideNavUl.style.visibility = "visible";

    getSideNav.style.display ="block"; //Nav

    getMainNav.style.backgroundColor = "black";
    getMainNav.style.borderBottom = "1.49px grey solid";

    //getMainNav.style.height = "calc(100vh)"; //Testing
    getMainNav.style.backgroundColor = "black";
    getBody.style.backgroundColor ="black"; //Testing

    getSection.style.display ="none"; //Content
    toggleNavStatus = true;
    getFooter.style.display = "none";
  }
  else if (toggleNavStatus == true){
    getSideNavUl.style.visibility = "hidden";

    getSideNav.style.display ="none"; //Nav

    getMainNav.style.backgroundColor = "#262729";
    //getMainNav.style.height = "50px"; //testing

    getMainNav.style.borderBottom = "1px black solid";


    getSection.style.display ="block"; //Content
    getBody.style.backgroundColor = "white"; //testing
    toggleNavStatus = false;
    getFooter.style.display = "block";
  }
}

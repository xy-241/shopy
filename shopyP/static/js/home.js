if(document.readyState == "loading"){
  document.addEventListener("DOMContentLoaded", ready);
} else{
  ready();
}




function ready(){
  //Tab Actions
  var tabs = document.getElementsByClassName("tabButton");
  for(var i = 0; i< tabs.length; i++){
    tabs[i].addEventListener("click", displayItems);
  }
  //Tab Actions

  //Modal
  window.addToCartModal = document.getElementsByClassName("addToCartModal")[0];
  document.getElementsByClassName("closeBtn")[0].addEventListener("click", removeModal);
  window.addEventListener("click", clickOutsideModal);
  //Modal
  //Add to cart
  var addToCart = document.getElementsByClassName("addToCart");
  for(var i = 0; i<addToCart.length; i++){
    addToCart[i].addEventListener("click", addToCartFunc);
  }

}


function removeModal(event){
  var button = event.target;

  button.parentElement.parentElement.parentElement.style.display = "none";
}
function clickOutsideModal(event){
  var area = event.target;
  if(area == window.addToCartModal){
    window.addToCartModal.style.display = "none";
  }
}
function addToCartFunc(event){
  //MOdal

  window.addToCartModal.style.display = "block";
  //MOdal
  var button = event.target;
  var item = button.parentElement.parentElement;
  var itemRow = document.createElement("div");


  var itemName = item.getElementsByClassName("itemName")[0].innerText;

  var entry = {
    title: itemName,
  }
  console.log(entry);

  fetch(`${window.origin}/addToCart/item`, {
    method: 'POST',
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json",
      'Accept': 'application/json'
    })
  })
  .then(function (response){
    if (response.status !== 200 ){
      console.log(`Response status was not 200: ${response.status}`);
      return;
    }
    response.json().then(function (data){
      console.log(data);
    })

  })

  return;
}



function displayItems(event){
  //Get the item Page Name
  var button = event.target;
  subPageName = button.value;

  //Making sure only one subPage is displayed
  var subPages = document.getElementsByClassName("subPage");
  for(var i=0; i< subPages.length; i++){
    subPages[i].style.display = "none";
  }

  document.getElementsByClassName(subPageName)[0].style.display = "block"; //Display the page that is required
  //Making sure only one subPage is displayed
}

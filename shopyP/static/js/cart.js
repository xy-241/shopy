

if(document.readyState == "loading"){
  document.addEventListener("DOMContentLoaded", ready);

} else{
  ready();

}
//localStorage
var data = localStorage.getItem("storedCartItems");
if(data ==null){
  var storedCartItems = [];

} else{
  var storedCartItems = JSON.parse(data);
}
//localStorage



function ready(){


  //NumSelected
  var quantityInputs = document.getElementsByClassName("cartItemNum");
  for(var i=0; i<quantityInputs.length; i++){
    quantityInputs[i].addEventListener("change", quantityInputUpdate);
  }
  //NumSelected

  //Remove Button
  var removeButtons = document.getElementsByClassName("removeButton");
  for(var i=0; i<removeButtons.length; i++){
    removeButtons[i].addEventListener("click", removeItemFromCart);
  }
  //Remove Button

  //Checkout Button
  var checkoutButton = document.getElementsByClassName("checkout")[0];
  checkoutButton.addEventListener("click", checkoutClearCart);
  //Checkout Button

  //Check if carts has anything
  var cartItemNumber = document.getElementsByClassName("cartItems")[0].childElementCount;
  if(cartItemNumber == 0){
    document.getElementsByClassName("cartTotal")[0].style.display = "none";
    document.getElementsByClassName("cartEmpty")[0].style.display = "block";
  }
  else{
    document.getElementsByClassName("cartTotal")[0].style.display = "flex";
    document.getElementsByClassName("cartEmpty")[0].style.display = "none";
  }
  //Check if carts has anything
  updateTheCart();
}

/*
function justFourSweetie(event){
  alert("Sweetie, you are cute 💖 ;)");
}*/

//checkout
function checkoutClearCart(event){
  var button = event.target;

  var cartItems = document.getElementsByClassName("cartItems")[0];
  //alert(cartItems.length);
  while(cartItems.hasChildNodes()){
    cartItems.removeChild(cartItems.firstChild);
  }

  //Clear everything in the localStorage
  storedCartItems = [];
  localStorage.setItem("storedCartItems", JSON.stringify(storedCartItems));
  //Clear everything in the localStorage

  updateTheCart();
}
//checkout
//Check Cart Status
function checkCartStatus(){
  var cartItemNumber = document.getElementsByClassName("cartItems")[0].childElementCount;
  if(cartItemNumber == 0){
    document.getElementsByClassName("cartTotal")[0].style.display = "none";
    document.getElementsByClassName("cartEmpty")[0].style.display = "block";
  }
  else{
    document.getElementsByClassName("cartTotal")[0].style.display = "flex";
    document.getElementsByClassName("cartEmpty")[0].style.display = "none";
  }
}
//Check Cart Status

function removeItemFromCart(event){
  var button = event.target;

  //Remove items away from the local storage
  var cartItemName = button.parentElement.getElementsByClassName("cartItemName")[0].innerText;
  var entry = {
    title: cartItemName
  }

  fetch(`${window.origin}/cart/removeItem`, {
    method: 'POST',
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
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

  button.parentElement.remove();
  updateTheCart();
}
function quantityInputUpdate(event){
  var button = event.target;

  //Making sure the cartItem is one or bigger

  if(button.value < 1 || isNaN(button.value)){
    button.value = 1;
  }
  var roundedValue = Math.round(button.value);
  var itemName = button.parentElement.parentElement.parentElement.getElementsByClassName("cartItemName")[0].innerText;

  var entry = {
    title: itemName,
    value: roundedValue
  }

  fetch(`${window.origin}/cart/valueUpdate`, {
    method: 'POST',
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
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
  updateTheCart();
}

function updateTheCart(){
  var cartItems = document.getElementsByClassName("cartItems")[0];
  var cartItem = cartItems.getElementsByClassName("cartItem");
  var sum = 0;
  var amountToPay = document.getElementsByClassName("amountToPay")[0];

  for(var i = 0; i<cartItem.length; i++){
    var price =  parseFloat(cartItem[i].getElementsByClassName("cartItemPrice")[0].innerText.replace("S$", ""));
    var number = parseFloat(cartItem[i].getElementsByClassName("cartItemNum")[0].value);
    sum += (price * number);
  }

  sum = Math.round(sum * 100) /100;
  amountToPay.innerText = "$" + sum;

  //Check if carts has anything
  checkCartStatus();
  //Check if carts has anything

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

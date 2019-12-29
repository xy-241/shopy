

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
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
for(var i=0; i<storedCartItems.length; i++){
  //Get the 4 types of values from the localStorage
  var itemName = storedCartItems[i]["name"];
  var itemPrice = storedCartItems[i]["price"];
  var src = storedCartItems[i]["src"];
  var value = storedCartItems[i]["value"];

  //Get the 4 types of values from the localStorage

  var itemRow = document.createElement("div");
  itemRow.setAttribute("class", "cartItem");
  var itemContent = `
    <div class="cartItemDes">
      <div class="cartItemPic">
        <img src=${src}>
      </div>

      <div class="cartItemInfo">
        <p class="cartItemName">${itemName}</p>
        <div class="cartItemBuyingInfo">
          <p class="cartItemPrice">${itemPrice}</p>

          <div class="cartItemNumWrapper">
            <input type="number" class="cartItemNum" value="${value}">
          </div>
        </div>
      </div> <!--End of cart Info-->
    </div> <!--End of cart Des-->

    <button type="button" class="removeButton">Remove</button>
  `;
  itemRow.innerHTML = itemContent;

  var cartList = document.getElementsByClassName("cartItems")[0];
  cartList.append(itemRow);

  //Give the newly created button an event handler
  //NumSelected
  var quantityInputs = document.getElementsByClassName("cartItemNum");
  for(var j=0; j<quantityInputs.length; j++){
    quantityInputs[j].addEventListener("change", quantityInputUpdate);
  }
  //NumSelected
  //Remove Button
  var removeButtons = document.getElementsByClassName("removeButton");
  for(var j=0; j<removeButtons.length; j++){
    removeButtons[j].addEventListener("click", removeItemFromCart);
  }
  //Remove Button
}
  updateTheCart()   //Update the cart!!!

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
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




  //Go to cart button
  var goToShoppingCart = document.getElementsByClassName("goToShoppingCart")[0];
  goToShoppingCart.addEventListener("click", showShoppingCart);



  //Go to cart button

  //Go Back Button
  // var goBack = document.getElementsByClassName("goBack")[0];
  // goBack.addEventListener("click", showShoppingItems);
  //
  // goBack = document.getElementsByClassName("shopLogo")[0];
  // goBack.addEventListener("click", showShoppingItems);
  //Go Back Button




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
  for(var i=0; i<storedCartItems.length; i++){
    if(storedCartItems[i]["name"] == cartItemName){
      storedCartItems.splice(i,1);
      localStorage.setItem("storedCartItems", JSON.stringify(storedCartItems));
    }
  }
  //Remove items away from the local storage
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
  button.value = roundedValue;
  //Making sure changes to cart items are recorded back to the localStorage
  var itemName = button.parentElement.parentElement.parentElement.getElementsByClassName("cartItemName")[0].innerText;
  for(var i=0; i<storedCartItems.length; i++){
    if(storedCartItems[i]["name"] == itemName){
      storedCartItems[i]["value"] = button.value;
      localStorage.setItem("storedCartItems", JSON.stringify(storedCartItems));
    }
  }
  storedCartItems
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
function removeModal(event){
  var button = event.target;

  button.parentElement.parentElement.parentElement.style.display = "none";
}
function clickOutsideModal(event){
  var area = event.target;
  if(area == window.addToCartModal){
    window.addToCartModal.style.display = "block";
  }

}
function addToCartFunc(event){
  //Modal
  window.addToCartModal.style.display = "block";
  //Modal
  var button = event.target;
  var item = button.parentElement.parentElement;
  var itemRow = document.createElement("div");
  itemRow.setAttribute("class", "cartItem");

  var itemName = item.getElementsByClassName("itemName")[0].innerText;
  var src = item.getElementsByTagName("img")[0].src;
  var itemPrice = item.getElementsByClassName("itemPrice")[0].innerText;

  var cartItems = document.getElementsByClassName("cartItems")[0];
  var cartItemNames = cartItems.getElementsByClassName("cartItemName");

  //Add 1 to value if item is already inside, and return to quit the function
  for(var i = 0; i<cartItemNames.length; i++){
    if(cartItemNames[i].innerText == itemName){

      var currentValue = parseInt(cartItemNames[i].parentElement.getElementsByClassName("cartItemNum")[0].value);
      cartItemNames[i].parentElement.getElementsByClassName("cartItemNum")[0].value = currentValue+1;
      updateTheCart();  //Update the cart!!!

      //Local Strong Value changes
      for(var i=0; i<storedCartItems.length; i++){
        if(storedCartItems[i]["name"] == itemName){
          storedCartItems[i]["value"] = parseInt(storedCartItems[i]["value"]) + 1;
          localStorage.setItem("storedCartItems", JSON.stringify(storedCartItems));
        }
      }
      //Local Strong Value changes
      return;
    }
  }

  var itemContent = `
    <div class="cartItemDes">
      <div class="cartItemPic">
        <img src=${src}>
      </div>

      <div class="cartItemInfo">
        <p class="cartItemName">${itemName}</p>
        <div class="cartItemBuyingInfo">
          <p class="cartItemPrice">${itemPrice}</p>

          <div class="cartItemNumWrapper">
            <input type="number" class="cartItemNum" value="1">
          </div>
        </div>
      </div> <!--End of cart Info-->
    </div> <!--End of cart Des-->

    <button type="button" class="removeButton">Remove</button>
  `;
  itemRow.innerHTML = itemContent;

  var cartList = document.getElementsByClassName("cartItems")[0];
  cartList.append(itemRow);

  //Store to localStorage RMB TO REMOVE when checkout/remove clicked
  storedCartItems.push({"name": itemName, "price": itemPrice, "src": src, "value": parseInt(cartItemNames[i].parentElement.getElementsByClassName("cartItemNum")[0].value)});
  localStorage.setItem("storedCartItems", JSON.stringify(storedCartItems));
  //Store to localStorage RMB TO REMOVE when checkout/remove clicked

  //Give the newly created button an event handler
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

  updateTheCart()   //Update the cart!!!
  return;
}




//Go To Cart
function showShoppingCart(event){
  //HIde the shopping items
  document.getElementsByClassName("sellingItems")[0].style.display = "none";
  document.getElementsByClassName("itemsAvailable")[0].style.display = "none";
  document.getElementsByClassName("goToShoppingCart")[0].style.display = "none";
  //HIde the shopping items

  //Display shopping cart
  document.getElementsByClassName("shoppingCart")[0].style.display = "block";
  // document.getElementsByClassName("goBack")[0].style.display = "block";
  document.getElementsByClassName("checkout")[0].style.display = "block";
  document.getElementsByClassName("shopLogo")[0].style.display = "block";
  //Display shopping cart
}
//Go Back
function showShoppingItems(event){
  //Display the shopping items
  document.getElementsByClassName("sellingItems")[0].style.display = "block";
  document.getElementsByClassName("itemsAvailable")[0].style.display = "block";
  document.getElementsByClassName("goToShoppingCart")[0].style.display = "block";
  //Display the shopping items

  //Hide shopping cart
  document.getElementsByClassName("shoppingCart")[0].style.display = "none";
  // document.getElementsByClassName("goBack")[0].style.display = "none";
  document.getElementsByClassName("checkout")[0].style.display = "none";
  document.getElementsByClassName("shopLogo")[0].style.display = "none";
  //Hide shopping cart
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

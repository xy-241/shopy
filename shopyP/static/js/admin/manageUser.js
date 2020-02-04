if(document.readyState == "loading"){
  document.addEventListener("DOMContentLoaded", ready);

} else{
  ready();
}

function ready(){
  //Remove Button
  var removeButtons = document.getElementsByClassName("removeButton");
  for(var i=0; i<removeButtons.length; i++){
    removeButtons[i].addEventListener("click", removeUser);
  }
  //Remove Button

  function removeUser(event){
    var button = event.target;

    //Remove items away from the local storage
    var userName = button.parentElement.parentElement.getElementsByClassName("userName")[0].innerText;
    var entry = {
      username: userName
    }

    fetch(`${window.origin}/manageUser/delete`, {
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

    button.parentElement.parentElement.remove();
  }
}

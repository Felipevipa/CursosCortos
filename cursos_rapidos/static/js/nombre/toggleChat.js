function toggle() {
  let chatWindow = document.getElementById('chatWindow');
  console.log(chatWindow.style.display)
  if(chatWindow.style.display === "none"){
    chatWindow.style.display = "block";
  } else if(chatWindow.style.display === "block") {
    chatWindow.style.display = "none";
  } else {
    console.log("Opcion desconocida")
  }
}
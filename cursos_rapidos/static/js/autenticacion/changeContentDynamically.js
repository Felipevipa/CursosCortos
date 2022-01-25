$('input').click(function() {
  let content = document.getElementById('dynamicContent');
  if(this.name === "loginWithPassword"){
    // content.innerHTML = this.name;
    document.getElementById("loginWithPasswordDiv").style.display = "block";
    document.getElementById("loginWithCameraDiv").style.display = "none";
  } else if(this.name === "loginWithCamera") {
    // content.innerHTML = this.name;
    document.getElementById("loginWithPasswordDiv").style.display = "none";
    document.getElementById("loginWithCameraDiv").style.display = "block";
  } else {
    console.log("Opcion desconocida")
  }
}); 
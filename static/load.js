 var myVar;
 function myFunction(){
    myVar = setTimeout(showPage,3500);
 }

 function showPage(){
    document.getElementById("loading-screen").style.display = "none";
    document.getElementById("login").style.display = "block";
 }

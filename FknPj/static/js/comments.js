/* // read-more script 


function toggleContent(button) {
  var content = button.previousElementSibling;
  
  if (content.style.overflow === "hidden") {
    content.style.overflow = "visible";
    content.style.maxHeight = "none";
    button.innerText = "Read Less";
  } else {
    content.style.overflow = "hidden";
    content.style.maxHeight = "70px"; // Adjust this value to match initial height
    button.innerText = "Read More";
  }
  }
  
  document.addEventListener("DOMContentLoaded", function() {
  var contentDivs = document.querySelectorAll(".content");
  
  contentDivs.forEach(function(contentDiv) {
    var words = contentDiv.textContent.trim().split(/\s+/).length;
    var button = contentDiv.nextElementSibling;
    
    if (words > 35) {
      contentDiv.style.overflow = "hidden";
      contentDiv.style.maxHeight = "70px"; // Adjust this value to match initial height
      button.style.display = "inline-block";
    } else {
      button.style.display = "none";
    }
  });
  });
  

   */


  function toggleContent(button) {
    var content = button.previousElementSibling;

    if (content.classList.contains('expanded')) {
      content.style.height = "55px"; // Adjust this value to match initial height
      content.classList.remove('expanded');
      button.innerText = "Read More";
    } else {
      content.style.height = content.scrollHeight + "px";
      content.classList.add('expanded');
      button.innerText = "Read Less";
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var contentDivs = document.querySelectorAll(".content");

    contentDivs.forEach(function (contentDiv) {
      var words = contentDiv.textContent.trim().split(/\s+/).length;
      var button = contentDiv.nextElementSibling;

      if (words > 25) {
        contentDiv.style.overflow = "hidden";
        contentDiv.style.height = "55px"; // Adjust this value to match initial height
        button.style.display = "inline-block";
      } else {
        button.style.display = "none";
      }
    });
  });


  
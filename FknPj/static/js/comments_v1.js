


  function toggleContent(button) {
    var content = button.previousElementSibling;

    if (content.classList.contains('expanded')) {
      content.style.height = "55px"; // Adjust this value to match initial height
      content.classList.remove('expanded');
      button.innerText = "Read the post";
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

      if (words > 15) {
        contentDiv.style.overflow = "hidden";
        contentDiv.style.height = "55px"; // Adjust this value to match initial height
        button.style.display = "inline-block";
      } else {
        button.style.display = "none";
      }
    });
  });

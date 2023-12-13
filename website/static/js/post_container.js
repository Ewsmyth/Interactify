// Function to store the scroll position
function storeScrollPosition() {
    sessionStorage.setItem('scrollPosition', window.scrollY);
}

// Store the scroll position when the user scrolls
window.addEventListener('scroll', storeScrollPosition);

// Function to restore the scroll position
function restoreScrollPosition() {
    const scrollPosition = sessionStorage.getItem('scrollPosition');
    if (scrollPosition) {
        window.scrollTo(0, scrollPosition);
    }
}

$(document).ready(function() {
    $(".cmnt-list").hide(); // Hide comments by default on page load
  
    $(".toggle-comments-btn").on("click", function() {
      var commentList = $(this).siblings(".cmnt-list");
      commentList.toggle(); // Toggle display of comments
  
      if (commentList.is(":visible")) {
        $(this).text("Hide Comments");
      } else {
        $(this).text("View Comments");
      }
    });
  });
   
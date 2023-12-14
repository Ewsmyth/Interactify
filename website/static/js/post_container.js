function viewComments(button) {
  var commentsList = button.nextElementSibling; // Get the sibling element containing comments
  if (commentsList.style.display === "none" || commentsList.style.display === "") {
      commentsList.style.display = "block";
  } else {
      commentsList.style.display = "none";
  }
}

// Function to save scroll position
function saveScrollPosition(postId) {
  localStorage.setItem(`scrollPosition_${postId}`, window.scrollY);
}

// Function to restore scroll position
function restoreScrollPosition(postId) {
  const scrollPosition = localStorage.getItem(`scrollPosition_${postId}`);
  if (scrollPosition) {
      window.scrollTo(0, parseInt(scrollPosition));
      localStorage.removeItem(`scrollPosition_${postId}`); // Remove the stored position after restoring
  }
}

// Call saveScrollPosition() whenever a comment is submitted
// For example, if you have a form with class "comment-form":
$('.comment-form').submit(function() {
  const postId = $(this).closest('.post-container').data('post-id');
  saveScrollPosition(postId);
});

// Call restoreScrollPosition() when the page loads for each post
$('.post-container').each(function() {
  const postId = $(this).data('post-id');
  restoreScrollPosition(postId);
});

// Attach an event listener to handle scroll position saving on post like
$('.like-btn').click(function() {
  const postId = $(this).closest('.post-container').data('post-id');
  saveScrollPosition(postId);
  // Additionally, you might want to trigger the actual like action here
  // For example, using AJAX to send the like request to the server
});


$(document).ready(function() {
  $('.delete-post-form').submit(function(event) {
      event.preventDefault(); // Prevent the default form submission
      const confirmation = confirm("Are you sure you want to delete this post?");
      if (confirmation) {
          // Submit the form if the user confirms deletion
          $(this).unbind('submit').submit();
      }
  });
});
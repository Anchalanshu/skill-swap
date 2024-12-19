// Select the buttons
const likeBtn = document.querySelector('.like-btn-custom');
const commentBtn = document.querySelector('.comment-btn');
const shareBtn = document.querySelector('.share-btn');
const joinBtn = document.querySelector('.join-btn');
const commentSection = document.querySelector('.comment-section'); // Select the comment box section



// Like button toggle functionality
document.querySelectorAll('.like-btn').forEach((likeBtn) => {
    let isClicked = false;
    likeBtn.addEventListener('click', () => {
        if (isClicked) {
            // Revert to the original background color and text color
            likeBtn.style.background = ''; // Reset the background
            likeBtn.style.color = ''; // Reset the text color
            likeBtn.style.transform = 'scale(1.0)'; /* Slight zoom effect */
            isClicked = false;
        } else {
            // Change to the new background color and text color
            likeBtn.style.background = 'linear-gradient(135deg,rgb(0, 84, 84),rgb(0, 129, 129))'; // New color
            likeBtn.style.color = 'white'; // Change text color to white
            likeBtn.style.transform = 'scale(1.10)'; /* Slight zoom effect */
            isClicked = true;
        }
    });
});

// Comment button toggle functionality
document.querySelectorAll('.comment-btn').forEach((button, index) => {
    button.addEventListener('click', () => {
        // Select the corresponding comment section
        const commentSection = document.querySelectorAll('.comment-section')[index];
        
        // Toggle the visibility of the comment section
        if (commentSection.style.display === 'block') {
            commentSection.style.display = 'none';
        } else {
            commentSection.style.display = 'block';
            // Focus on the textarea inside the comment section
            commentSection.querySelector('.comment-box').focus();
        }
    });
});

// Handling comment submission and clearing comment box
document.querySelectorAll('.comment-box').forEach((commentBox) => {
    commentBox.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();

            // Show the "Comment Posted" message
            const messageDiv = document.createElement('div');
            messageDiv.textContent = "Comment Posted.! 🎉";
            messageDiv.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: #ffffff;
                padding: 20px 40px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
                font-size: 18px;
                font-weight: bold;
                z-index: 1;
            `;

            // Append the message to the body
            document.body.appendChild(messageDiv);

            // Clear the comment box
            commentBox.value = '';

            // Remove the message after 1 second
            setTimeout(() => {
                messageDiv.remove();
            }, 1000);
        }
    });
});

// Share button functionality
document.querySelectorAll('.share-btn').forEach((shareBtn) => {
    shareBtn.addEventListener('click', () => {
        // Simulate copying the link (using the browser's Clipboard API)
        navigator.clipboard.writeText(window.location.href).then(() => {
            alert('Link copied!');
        }).catch((err) => {
            console.error('Failed to copy: ', err);
        });
    });
});

// Join Project button functionality
document.querySelectorAll('.join-btn').forEach((joinBtn) => {
    joinBtn.addEventListener('click', () => {
        // Toggle the 'clicked' class to change the button appearance
        joinBtn.classList.toggle('clicked');
        
        // Toggle the text content between 'Request To Project' and 'View Project'
        if (joinBtn.classList.contains('clicked')) {
            joinBtn.textContent = 'View Project';
        } else {
            joinBtn.textContent = 'Request Sent.!';
        }
    });
});



document.addEventListener("DOMContentLoaded", function() {
    // Follow button logic (toggle between Follow and Following)
    const followButtons = document.querySelectorAll(".follow-btn");

    followButtons.forEach(function(followButton) {
        followButton.addEventListener("click", function() {
            // Check if the button is currently in "Following" state
            if (followButton.classList.contains("following")) {
                // If it's in "Following", revert it to "Follow"
                followButton.classList.remove("following");
                followButton.innerHTML = "Follow +👤"; // Reset text to original
                followButton.style.backgroundColor = "#0073b1"; // Reset color
            } else {
                // If it's in "Follow", change to "Following"
                followButton.classList.add("following");
                followButton.innerHTML = "Following ✅"; // Change text to "Following"
                followButton.style.backgroundColor = "#28a745"; // Change color (Green for following)
            }
        });
    });

    const messageButtons = document.querySelectorAll(".message-btn");
    messageButtons.forEach(button => {
        button.addEventListener("click", () => {
            const modalId = button.getAttribute("data-modal");
            const modal = document.getElementById(modalId);
            modal.style.display = "block";
        });
    });
    
    // Close modal
    const closeButtons = document.querySelectorAll(".close-btn");
    closeButtons.forEach(button => {
        button.addEventListener("click", () => {
            const modalId = button.getAttribute("data-modal");
            const modal = document.getElementById(modalId);
            modal.style.display = "none";
        });
    });
    
    // Send message logic
    const sendMessageButtons = document.querySelectorAll(".sendMessageBtn");
    sendMessageButtons.forEach(button => {
        button.addEventListener("click", () => {
            const inputId = button.getAttribute("data-input");
            const messageInput = document.getElementById(inputId);
            const message = messageInput.value.trim();
            
            if (message !== "") {
                alert("Message sent: " + message); // Fixed alert message
                const modal = button.closest(".modal");
                modal.style.display = "none"; // Close modal
            } else {
                alert("Please enter a message.");
            }
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener("click", (event) => {
        const modals = document.querySelectorAll(".modal");
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    });
});


function toggleJoinText(button) {
    // Change button text to 'View Project' and color to light blue
    button.innerText = 'View Project';
    button.classList.add('clicked');
}

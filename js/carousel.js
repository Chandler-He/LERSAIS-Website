// This function initializes the carousel
function initCarousel() {
    // Get all carousel items
    const carouselItems = document.querySelectorAll('.carousel-item');
    
    // If no items found, exit
    if (carouselItems.length === 0) return;
    
    // Track current slide index (start with 0)
    let currentIndex = 0;
    
    // Function to show the next slide
    function showNextSlide() {
        // Remove active class from current slide
        carouselItems[currentIndex].classList.remove('active');
        
        // Move to next slide (loop back to first slide if at the end)
        currentIndex = (currentIndex + 1) % carouselItems.length;
        
        // Add active class to new current slide
        carouselItems[currentIndex].classList.add('active');
    }
    
    // Set up automatic rotation every 8 seconds
    setInterval(showNextSlide, 6000);
}

// Wait for DOM content to be loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if header is already loaded
    if (document.querySelectorAll('.carousel-item').length > 0) {
        initCarousel();
    } else {
        // If header is not yet loaded, wait a bit and check again
        let checkInterval = setInterval(function() {
            if (document.querySelectorAll('.carousel-item').length > 0) {
                clearInterval(checkInterval);
                initCarousel();
            }
        }, 100); // Check every 100ms
        
        // Stop checking after 10 seconds to prevent infinite checking
        setTimeout(function() {
            clearInterval(checkInterval);
        }, 10000);
    }
});
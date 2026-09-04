# header.html
```html
<!DOCTYPE html>
<div class="hero-container">
    <!-- Logo and Title Section -->
    <div class="header-content">
        <div class="logo-container">
            <img src="images/pitt_logo.svg" alt="University of Pittsburgh logo" class="pitt-logo">
        </div>
        <div class="title-container">
            <p class="subtitle">School of Computing and Information</p>
            <h1 class="main-title">Laboratory of Education and Research on Security Assured Information Systems</h1>
        </div>
    </div>


    <!-- Hero Image/Carousel Section -->
    <div class="hero-carousel" id="hero-carousel">
        <div class="carousel-items">
            <div class="carousel-item active">
                <img src="images/cathey.jpg" alt="University of Pittsburgh">
            </div>
            <div class="carousel-item">
                <img src="images/lersais1.jpg" alt="Leaders and Researchers">
            </div>
            <div class="carousel-item">
                <img src="images/joshi.jpeg" alt="Keynote">
            </div>
        </div>
        <!-- <button class="carousel-control prev" aria-label="Previous slide">‹</button>
        <button class="carousel-control next" aria-label="Next slide">›</button> -->
    </div>
     <!-- Navigation Bar -->
     <nav class="main-navbar">
        <ul class="nav-links">
            <li><a href="index.html" class="nav-link">Home</a></li>
            <li><a href="people.html" class="nav-link">People</a></li>
            <li><a href="#research.html" class="nav-link">Research</a></li>
            <li><a href="#conference.html" class="nav-link">Conference</a></li>
            <li><a href="#gallery.html" class="nav-link">Gallery</a></li>
            <li><a href="#news.html" class="nav-link">News</a></li>
            <li><a href="#education.html" class="nav-link">Education</a></li>
        </ul>
    </nav>
</div>
```
# footer.html
```html
<!DOCTYPE html>
<footer id="footer">
    <div class="container-fluid">
        <div class="row-fluid">
            <div class="span5">
                <h3>Contact Information</h3>
                <p><b>Office Hours: </b>Monday-Friday (9:00am - 5:00pm, U.S. EST)</p>
                <p>Want to join Lersais? contact:</p>
                <a href="jjoshi@pitt.edu">James Joshi (Director): jjoshi@pitt.edu</a>
                <br>
                <br>
                <p>This Webiste is developed by <a href="https://sites.pitt.edu/~peh53/" target="_blank">Peilin He</a>.
                    All Rights Reserved ®.</p>
            </div>
            <div class="span2">
                <a href="#"><img src="thumbs/logo.png" alt="research-lab-logo" style="width: 70%; margin-top: 10%;"></a>
            </div>
            <div class="span5">
                <h3>Address</h3>
                <p>
                    Informal Science Building, Room 410<br>
                    135 N Bellefield Ave.
                    <br>

                    Pittsburgh, PA, USA, 15213

                </p>
                <a href="http://maps.google.com/" target="_blank">Show Map</a>
            </div>
        </div>
    </div>
</footer>
```
# js/include-header.js
```javascript
document.addEventListener('DOMContentLoaded', function() {
  // Find all elements with data-include attribute
  const includes = document.querySelectorAll('[data-include]');

  // Process each include
  includes.forEach(element => {
    const file = element.getAttribute('data-include');

    // Fetch the file content
    fetch(file)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to load ${file}: ${response.status}`);
        }
        return response.text();
      })
      .then(html => {
        // Insert the content into the element
        element.innerHTML = html;

        // Dispatch event to notify content was loaded
        const event = new CustomEvent('contentLoaded');
        element.dispatchEvent(event);
      })
      .catch(error => {
        console.error(`Error including ${file}:`, error);
        element.innerHTML = `<p>Error loading content: ${error.message}</p>`;
      });
  });
});
```
# js/sidebar.js
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const sidebar = document.querySelector('.sidebar');
    const header = document.getElementById('header-container');
    const navItems = document.querySelectorAll('.sidebar li a');

    if (!sidebar) return;

    // Store initial position
    const sidebarOffset = getOffset(sidebar).top;
    const sidebarWidth = sidebar.offsetWidth;
    const sidebarParent = sidebar.parentElement;

    // Handle scrolling
    window.addEventListener('scroll', function() {
        // Current scroll position
        const scrollPos = window.scrollY || document.documentElement.scrollTop;
        // Header height (if available)
        const headerHeight = header ? header.offsetHeight : 0;

        // Fixed sidebar after header
        if (scrollPos > headerHeight) {
            // Apply fixed position
            sidebar.classList.add('sidebar-fixed');
            sidebar.style.position = 'fixed';
            sidebar.style.top = '100px';
            sidebar.style.width = sidebarWidth + 'px';
        } else {
            // Reset to normal flow
            sidebar.classList.remove('sidebar-fixed');
            sidebar.style.position = '';
            sidebar.style.top = '';
            sidebar.style.width = '';
        }

        // Stop at footer if present
        const footer = document.querySelector('footer') || document.getElementById('footer');
        if (footer && sidebar.classList.contains('sidebar-fixed')) {
            const footerTop = getOffset(footer).top;
            const sidebarBottom = scrollPos + sidebar.offsetHeight + 30;

            if (sidebarBottom > footerTop) {
                sidebar.style.top = (footerTop - sidebarBottom + 30) + 'px';
            }
        }
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        if (sidebar.classList.contains('sidebar-fixed')) {
            sidebar.style.width = sidebarParent.offsetWidth + 'px';
        }
    });

    // Highlight active item based on scroll position
    function setActiveNavItem() {
        const scrollPos = window.scrollY + 100; // Add offset for better detection

        // Find all sections
        const sections = document.querySelectorAll('section[id]');

        // Check each section
        sections.forEach(section => {
            const sectionTop = getOffset(section).top;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                // Remove active from all
                navItems.forEach(item => item.parentElement.classList.remove('active'));

                // Add active to current
                const activeLink = document.querySelector(`.sidebar li a[href="#${sectionId}"]`);
                if (activeLink) {
                    activeLink.parentElement.classList.add('active');
                }
            }
        });
    }

    // Add smooth scrolling to nav links
    navItems.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: getOffset(targetElement).top - 80,
                    behavior: 'smooth'
                });

                // Update URL without jumping
                history.pushState(null, null, targetId);
            }
        });
    });

    // Helper function to get element offset
    function getOffset(el) {
        const rect = el.getBoundingClientRect();
        return {
            top: rect.top + window.scrollY,
            left: rect.left + window.scrollX
        };
    }

    // Listen for scroll to update active item
    window.addEventListener('scroll', setActiveNavItem);

    // Initialize by triggering scroll event
    window.dispatchEvent(new Event('scroll'));
});
```
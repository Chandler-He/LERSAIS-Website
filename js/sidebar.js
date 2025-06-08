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
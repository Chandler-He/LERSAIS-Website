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
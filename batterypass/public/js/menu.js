document.addEventListener('DOMContentLoaded', function() {
    // Sidebar item click handler
    const sidebarItems = document.querySelectorAll('.nav-link');
    
    sidebarItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all sidebar items
            sidebarItems.forEach(i => i.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Hide all section content
            const sectionContents = document.querySelectorAll('.main-content');
            sectionContents.forEach(section => section.classList.add('d-none'));
            
            // Show the selected section content
            const sectionId = this.getAttribute('data-section') + '-section';
            document.getElementById(sectionId).classList.remove('d-none');
        });
    });
});
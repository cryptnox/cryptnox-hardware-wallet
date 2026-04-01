// Version selector — move into sidebar below logo, above search
document.addEventListener('DOMContentLoaded', function () {
    var container = document.getElementById('version-selector-container');
    if (!container) return;
    var searchArea = document.querySelector('.wy-side-nav-search');
    var searchForm = searchArea && searchArea.querySelector('[role="search"]');
    if (searchArea && searchForm) {
        searchArea.insertBefore(container, searchForm);
        container.style.display = 'block';
    }
    var select = document.getElementById('version-select');
    if (select) {
        select.addEventListener('change', function () {
            if (this.value) window.location.href = this.value;
        });
    }
});

// Add smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for internal links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add copy button to code blocks
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        const button = document.createElement('button');
        button.textContent = 'Copy';
        button.className = 'copy-button';
        button.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: #007bff;
            color: white;
            border: none;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            cursor: pointer;
            font-size: 0.8rem;
        `;
        
        button.addEventListener('click', function() {
            navigator.clipboard.writeText(block.textContent);
            button.textContent = 'Copied!';
            setTimeout(() => {
                button.textContent = 'Copy';
            }, 2000);
        });
        
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        block.parentNode.parentNode.insertBefore(wrapper, block.parentNode);
        wrapper.appendChild(block.parentNode);
        wrapper.appendChild(button);
    });
});

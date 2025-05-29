document.addEventListener('DOMContentLoaded', function() {
    // Terminal cursor blinking animation
    const cursor = document.querySelector('.cursor');
    setInterval(() => {
        cursor.style.opacity = cursor.style.opacity === '0' ? '1' : '0';
    }, 600);

    // Simulate typing in the terminal
    setTimeout(simulateTyping, 2000);

    // Add terminal typing sounds
    const typingSound = new Audio('audio/typing.mp3');
    typingSound.volume = 0.2;

    // Tab functionality for installation section
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(`${tabId}-content`).classList.add('active');
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Header scroll effect
    const header = document.querySelector('header');
    let lastScrollTop = 0;

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop) {
            // Scrolling down
            header.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            header.style.transform = 'translateY(0)';
        }
        
        if (scrollTop <= 0) {
            // At the top
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });

    // Add animation to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.transform = 'translateY(0)';
                entry.target.style.opacity = '1';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    featureCards.forEach(card => {
        card.style.transform = 'translateY(20px)';
        card.style.opacity = '0';
        card.style.transition = 'transform 0.5s ease, opacity 0.5s ease, box-shadow 0.3s ease';
        observer.observe(card);
    });
});

// Function to simulate typing in the terminal
function simulateTyping() {
    const prompts = [
        'Tell me about Linux file permissions',
        'How does a neural network work?',
        'Write a hello world in Python',
        'What are the main features of Docker?'
    ];
    
    const randomPrompt = prompts[Math.floor(Math.random() * prompts.length)];
    const promptElement = document.querySelector('.prompt');
    const terminal = document.querySelector('.terminal-content');
    
    // Clear existing prompt content
    while (promptElement.childNodes.length > 0) {
        promptElement.removeChild(promptElement.lastChild);
    }
    
    // Add the "> " prefix
    promptElement.appendChild(document.createTextNode('> '));
    
    let i = 0;
    const typeInterval = setInterval(() => {
        if (i < randomPrompt.length) {
            promptElement.appendChild(document.createTextNode(randomPrompt[i]));
            i++;
        } else {
            clearInterval(typeInterval);
            
            // After typing is complete, simulate AI response
            setTimeout(() => {
                // Create a new line for AI response
                const responseLine = document.createElement('div');
                responseLine.className = 'line';
                responseLine.textContent = 'AI: Processing query...';
                terminal.appendChild(responseLine);
                
                // Scroll to bottom of terminal
                terminal.scrollTop = terminal.scrollHeight;
                
                // Create a new prompt line after response
                setTimeout(() => {
                    const newPromptLine = document.createElement('div');
                    newPromptLine.className = 'line prompt';
                    newPromptLine.innerHTML = '> <span class="cursor">_</span>';
                    terminal.appendChild(newPromptLine);
                    
                    // Scroll to bottom of terminal
                    terminal.scrollTop = terminal.scrollHeight;
                    
                    // Restart the typing animation after a delay
                    setTimeout(simulateTyping, 4000);
                }, 1500);
            }, 800);
        }
    }, 100);
}
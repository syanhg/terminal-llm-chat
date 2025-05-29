document.addEventListener('DOMContentLoaded', function() {
    const inputEl = document.getElementById('input');
    const outputEl = document.getElementById('output');
    const terminal = document.querySelector('.terminal');
    
    let inputBuffer = '';
    let commandHistory = [];
    let historyIndex = -1;
    
    const commands = {
        help: () => {
            return `Available commands:
/help - Display this help message
/clear - Clear the terminal
/model - Show current model (GPT-4)
/theme - Change theme (green, amber, blue, matrix)
/about - About Terminal LLM Chat`;
        },
        clear: () => {
            outputEl.innerHTML = '';
            return '';
        },
        model: () => {
            return 'Current model: GPT-4';
        },
        theme: (args) => {
            const themes = {
                green: '#0f0',
                amber: '#FFB000',
                blue: '#00bfff',
                matrix: '#00FF41'
            };
            
            if (args && themes[args]) {
                document.documentElement.style.setProperty('--terminal-color', themes[args]);
                document.body.style.color = themes[args];
                document.querySelectorAll('.ascii-art, .cursor').forEach(el => {
                    el.style.color = themes[args];
                    if (el.classList.contains('cursor')) {
                        el.style.backgroundColor = themes[args];
                    }
                });
                return `Theme changed to ${args}`;
            } else {
                return `Available themes: ${Object.keys(themes).join(', ')}`;
            }
        },
        about: () => {
            return `Terminal LLM Chat v1.0.0
A terminal-based interface for large language models.
GitHub: https://github.com/syanhg/terminal-llm-chat`;
        }
    };
    
    function processCommand(cmd) {
        if (!cmd) return '';
        
        if (cmd.startsWith('/')) {
            const parts = cmd.slice(1).split(' ');
            const command = parts[0];
            const args = parts.slice(1).join(' ');
            
            if (commands[command]) {
                return commands[command](args);
            } else {
                return `Unknown command: ${command}. Type /help for available commands.`;
            }
        } else {
            // Simulate AI response
            return simulateResponse(cmd);
        }
    }
    
    function simulateResponse(input) {
        const responses = [
            "I'm a simulated terminal AI interface. In the real app, this would connect to GPT-4 or other LLMs.",
            "This is just a demo interface. The actual Terminal LLM Chat app connects to real AI models via API.",
            "In the full application, I would process your request and return an AI-generated response.",
            "The real Terminal LLM Chat app allows you to chat with AI models directly from your terminal.",
            "This is a static demo. Install the actual Terminal LLM Chat for full functionality!"
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    function handleInput(e) {
        if (e.key === 'Enter') {
            // Process command
            const command = inputBuffer;
            inputBuffer = '';
            inputEl.textContent = '';
            
            // Add to history
            if (command) {
                commandHistory.push(command);
                historyIndex = commandHistory.length;
            }
            
            // Display command
            outputEl.innerHTML += `<div class="line">> ${command}</div>`;
            
            // Process and display response
            const response = processCommand(command);
            if (response) {
                outputEl.innerHTML += `<div class="line">${response}</div>`;
            }
            
            // Scroll to bottom
            terminal.scrollTop = terminal.scrollHeight;
            
        } else if (e.key === 'ArrowUp') {
            // Navigate history up
            e.preventDefault();
            if (historyIndex > 0) {
                historyIndex--;
                inputBuffer = commandHistory[historyIndex];
                inputEl.textContent = inputBuffer;
            }
        } else if (e.key === 'ArrowDown') {
            // Navigate history down
            e.preventDefault();
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                inputBuffer = commandHistory[historyIndex];
                inputEl.textContent = inputBuffer;
            } else if (historyIndex === commandHistory.length - 1) {
                historyIndex = commandHistory.length;
                inputBuffer = '';
                inputEl.textContent = '';
            }
        } else if (e.key === 'Backspace') {
            // Handle backspace
            e.preventDefault();
            if (inputBuffer.length > 0) {
                inputBuffer = inputBuffer.slice(0, -1);
                inputEl.textContent = inputBuffer;
            }
        } else if (e.key === 'Tab') {
            // Tab completion
            e.preventDefault();
            // Simplified tab completion could be added here
        } else if (e.key.length === 1) {
            // Add character to input
            inputBuffer += e.key;
            inputEl.textContent = inputBuffer;
        }
    }
    
    // Event listeners
    document.addEventListener('keydown', handleInput);
    
    // Focus on terminal by default
    terminal.focus();
    
    // Add mobile support with a hidden input field
    if (/Mobi|Android/i.test(navigator.userAgent)) {
        // Create hidden input for mobile
        const mobileInput = document.createElement('input');
        mobileInput.type = 'text';
        mobileInput.style.position = 'absolute';
        mobileInput.style.opacity = '0';
        mobileInput.style.height = '0';
        document.body.appendChild(mobileInput);
        
        // Focus the hidden input when terminal is clicked
        terminal.addEventListener('click', () => {
            mobileInput.focus();
        });
        
        // Handle mobile input
        mobileInput.addEventListener('input', (e) => {
            inputBuffer = e.target.value;
            inputEl.textContent = inputBuffer;
        });
        
        mobileInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const command = inputBuffer;
                inputBuffer = '';
                mobileInput.value = '';
                inputEl.textContent = '';
                
                // Add to history
                if (command) {
                    commandHistory.push(command);
                    historyIndex = commandHistory.length;
                }
                
                // Display command
                outputEl.innerHTML += `<div class="line">> ${command}</div>`;
                
                // Process and display response
                const response = processCommand(command);
                if (response) {
                    outputEl.innerHTML += `<div class="line">${response}</div>`;
                }
                
                // Scroll to bottom
                terminal.scrollTop = terminal.scrollHeight;
            }
        });
    }
});
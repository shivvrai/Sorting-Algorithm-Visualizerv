class SortingVisualizer {
    constructor() {
    this.apiUrl = window.location.origin;
    this.currentArray = [];
    this.isRunning = false;
    this.isPaused = false;           
    this.currentAlgorithm = 'bubble';
    this.speed = 1;
    this.lastTrialResults = null;
    this.allSteps = [];              
    this.currentStepIndex = 0;       
    
    this.init();
}


    init() {
        this.setupEventListeners();
        this.generateArray('random');
        this.loadAlgorithmInfo('bubble');
    }

    setupEventListeners() {
        
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchTab(e.target.closest('.tab').dataset.mode);
            });
        });

document.getElementById('runTrialBtn').addEventListener('click', () => this.runTimeTrial());

        // Algorithm selection
        document.getElementById('algorithmSelect').addEventListener('change', (e) => {
            this.currentAlgorithm = e.target.value;
            this.loadAlgorithmInfo(e.target.value);
        });

        // Control buttons
        document.getElementById('startBtn').addEventListener('click', () => this.start());
        document.getElementById('pauseBtn').addEventListener('click', () => this.pause());
        document.getElementById('resetBtn').addEventListener('click', () => this.reset());

        // Array size slider
         document.getElementById('stepBackBtn')?.addEventListener('click', () => this.stepBackward());
    document.getElementById('stepForwardBtn')?.addEventListener('click', () => this.stepForward());
    
        document.getElementById('sizeSlider').addEventListener('input', (e) => {
            document.getElementById('sizeValue').textContent = e.target.value;
            this.generateArray('random');
        });

        // Speed slider
        document.getElementById('speedSlider').addEventListener('input', (e) => {
            this.speed = parseFloat(e.target.value);
            document.getElementById('speedLabel').textContent = this.speed + 'x';
        });

        // Preset buttons
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.generateArray(e.target.closest('.preset-btn').dataset.preset);
            });
        });

        // Array input
        document.getElementById('arrayInput').addEventListener('change', (e) => {
            const input = e.target.value;
            if (input.trim()) {
                this.currentArray = input.split(',').map(n => parseInt(n.trim())).filter(n => !isNaN(n));
                this.renderBars();
            }
        });

        // Export buttons
        document.getElementById('exportJSON').addEventListener('click', () => this.exportResults('json'));
        document.getElementById('exportCSV').addEventListener('click', () => this.exportResults('csv'));
    }

   switchTab(mode) {
    // Hide all modes with fade out
    document.querySelectorAll('[id$="Mode"]').forEach(el => {
        el.style.opacity = '0';
        setTimeout(() => {
            el.classList.add('hidden');
        }, 150);
    });
    
    // Show target mode with fade in
    setTimeout(() => {
        const targetMode = document.getElementById(mode + 'Mode');
        targetMode.classList.remove('hidden');
        setTimeout(() => {
            targetMode.style.opacity = '1';
        }, 10);
    }, 150);
    
    // Update active tab
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    const targetTab = document.querySelector(`[data-mode="${mode}"]`);
    if (targetTab) {
        targetTab.closest('.tab').classList.add('active');
    }
}


    generateArray(type) {
        const size = parseInt(document.getElementById('sizeSlider').value);
        this.currentArray = [];

        for (let i = 0; i < size; i++) {
            this.currentArray.push(Math.floor(Math.random() * 100) + 1);
        }

        if (type === 'sorted') {
            this.currentArray.sort((a, b) => a - b);
        } else if (type === 'reversed') {
            this.currentArray.sort((a, b) => b - a);
        } else if (type === 'nearly') {
            this.currentArray.sort((a, b) => a - b);
            // Swap a few elements
            for (let i = 0; i < Math.floor(size * 0.1); i++) {
                let idx1 = Math.floor(Math.random() * size);
                let idx2 = Math.floor(Math.random() * size);
                [this.currentArray[idx1], this.currentArray[idx2]] = [this.currentArray[idx2], this.currentArray[idx1]];
            }
        }

        document.getElementById('arrayInput').value = this.currentArray.join(', ');
        this.renderBars();
        this.updateStats(size, 0, 0, 0);
    }

    renderBars(highlightIndices = [], highlightClass = '') {
        const container = document.getElementById('barsContainer');
        container.innerHTML = '';
        
        if (this.currentArray.length === 0) return;
        
        const maxValue = Math.max(...this.currentArray);
        
        this.currentArray.forEach((value, index) => {
            const bar = document.createElement('div');
            bar.className = 'bar';
            bar.style.height = (value / maxValue * 350) + 'px';
            
            
            bar.setAttribute('data-value', value);
            bar.innerHTML = `<span class="bar-number">${value}</span>`;
            
            if (highlightIndices.includes(index)) {
                bar.classList.add(highlightClass);
            }
            
            container.appendChild(bar);
        });
    }

    updateStats(arraySize, currentStep, comparisons, swaps) {
        document.getElementById('arraySizeStat').textContent = arraySize;
        document.getElementById('currentStepStat').textContent = currentStep;
        document.getElementById('comparisonsStat').textContent = comparisons;
        document.getElementById('swapsStat').textContent = swaps;
    }

    async loadAlgorithmInfo(algorithm) {
        try {
            const response = await fetch(`${this.apiUrl}/api/algorithm-info/${algorithm}`);
            const data = await response.json();
            
           
            document.getElementById('algoDescription').textContent = data.description;
            document.getElementById('timeBest').textContent = data.time_complexity.best;
            document.getElementById('timeAvg').textContent = data.time_complexity.average;
            document.getElementById('timeWorst').textContent = data.time_complexity.worst;
            document.getElementById('spaceComplexity').textContent = data.space_complexity;
            
            document.getElementById('algoProperties').innerHTML = `
                <span class="property-badge">${data.stable ? 'Stable' : 'Unstable'}</span>
                <span class="property-badge">${data.in_place ? 'In-place' : 'Not in-place'}</span>
            `;
            
            document.getElementById('algoHowItWorks').textContent = data.how_it_works;
            document.getElementById('realWorldUses').innerHTML = data.real_world_uses.map(use => `<li>${use}</li>`).join('');
            document.getElementById('whenToUse').innerHTML = data.when_to_use.map(item => `<li>${item}</li>`).join('');
            document.getElementById('advantages').innerHTML = data.advantages.map(adv => `<li>${adv}</li>`).join('');
            document.getElementById('disadvantages').innerHTML = data.disadvantages.map(dis => `<li>${dis}</li>`).join('');
            document.getElementById('whenNotToUse').innerHTML = data.when_not_to_use.map(item => `<li>${item}</li>`).join('');
            
           
            const codeResponse = await fetch(`${this.apiUrl}/api/algorithm-code/${algorithm}`);
            const codeData = await codeResponse.json();
            document.getElementById('algoCode').textContent = codeData.code;
            document.getElementById('algoCodeExplanation').textContent = codeData.explanation;
            
        } catch (error) {
            console.error('Error loading algorithm info:', error);
        }
    }

    async start() {
    if (this.isRunning && !this.isPaused) return;
    
   
    if (this.isPaused && this.allSteps.length > 0) {
        this.isPaused = false;
        this.isRunning = true;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('pauseBtn').disabled = false;
        document.getElementById('stepBackBtn').disabled = true;
        document.getElementById('stepForwardBtn').disabled = true;
        
        
        await this.continueVisualization();
        return;
    }
    
    this.isRunning = true;
    this.isPaused = false;
    document.getElementById('startBtn').disabled = true;
    document.getElementById('pauseBtn').disabled = false;
    document.getElementById('stepBackBtn').disabled = true;
    document.getElementById('stepForwardBtn').disabled = true;
    
    try {
        const response = await fetch(`${this.apiUrl}/api/sort`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                array: this.currentArray,
                algorithm: this.currentAlgorithm
            })
        });
        
        const data = await response.json();
        
        
        this.allSteps = data.steps;
        this.currentStepIndex = 0;
        
        // Start visualization
        await this.continueVisualization();
        
    } catch (error) {
        console.error('Error during sorting:', error);
        alert('Error: ' + error.message);
        this.isRunning = false;
        document.getElementById('startBtn').disabled = false;
        document.getElementById('pauseBtn').disabled = true;
    }
}
async continueVisualization() {
    const totalSteps = this.allSteps.length;
    
    for (let i = this.currentStepIndex; i < totalSteps && this.isRunning; i++) {
        if (this.isPaused) {
            this.currentStepIndex = i;
            return;
        }
        
        const step = this.allSteps[i];
        this.currentArray = step.array;
        
        const highlightClass = step.type === 'comparing' ? 'comparing' :
                             step.type === 'swapping' ? 'swapping' :
                             step.type === 'sorted' ? 'sorted' : 'pivot';
        
        this.renderBars(step.indices, highlightClass);
        document.getElementById('stepDescription').textContent = step.description;
        
        // Get final stats from last step
        const finalStep = this.allSteps[totalSteps - 1];
        this.updateStats(
            this.currentArray.length,
            i + 1,
            finalStep.total_comparisons || 0,
            finalStep.total_swaps || 0
        );
        
        const progress = ((i + 1) / totalSteps) * 100;
        document.getElementById('progressBar').style.width = progress + '%';
        
        this.currentStepIndex = i;
        await this.sleep(100 / this.speed);
    }
    
    // Finished
    this.isRunning = false;
    this.isPaused = false;
    document.getElementById('startBtn').disabled = false;
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('stepBackBtn').disabled = true;
    document.getElementById('stepForwardBtn').disabled = true;
}


    pause() {
    console.log('Pause clicked - enabling step buttons');
    this.isPaused = true;
    this.isRunning = false;
    
    // Update pause/start buttons
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('startBtn').disabled = false;
    document.getElementById('startBtn').innerHTML = '<i class="fas fa-play"></i> Continue';
    
    //  Enable step buttons with multiple methods
    const stepBackBtn = document.getElementById('stepBackBtn');
    const stepForwardBtn = document.getElementById('stepForwardBtn');
    
    if (stepBackBtn) {
        stepBackBtn.disabled = false;
        stepBackBtn.removeAttribute('disabled');
        stepBackBtn.classList.remove('disabled');
        console.log('Step back button enabled:', !stepBackBtn.disabled);
    } else {
        console.error('stepBackBtn element NOT FOUND');
    }
    
    if (stepForwardBtn) {
        stepForwardBtn.disabled = false;
        stepForwardBtn.removeAttribute('disabled');
        stepForwardBtn.classList.remove('disabled');
        console.log('Step forward button enabled:', !stepForwardBtn.disabled);
    } else {
        console.error('stepForwardBtn element NOT FOUND');
    }
}




    reset() {
    this.isRunning = false;
    this.isPaused = false;
    this.allSteps = [];
    this.currentStepIndex = 0;
    
    this.generateArray('random');
    document.getElementById('startBtn').disabled = false;
    document.getElementById('startBtn').innerHTML = '<i class="fas fa-play"></i> Start';
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('stepBackBtn').disabled = true;
    document.getElementById('stepForwardBtn').disabled = true;
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('stepDescription').textContent = 'Ready to visualize! Click Start to begin sorting.';
}
stepBackward() {
    if (!this.isPaused || this.currentStepIndex <= 0) return;
    
    this.currentStepIndex--;
    const step = this.allSteps[this.currentStepIndex];
    
    this.currentArray = step.array;
    const highlightClass = step.type === 'comparing' ? 'comparing' :
                         step.type === 'swapping' ? 'swapping' :
                         step.type === 'sorted' ? 'sorted' : 'pivot';
    
    this.renderBars(step.indices, highlightClass);
    document.getElementById('stepDescription').textContent = step.description;
    
    const progress = ((this.currentStepIndex + 1) / this.allSteps.length) * 100;
    document.getElementById('progressBar').style.width = progress + '%';
    
    const finalStep = this.allSteps[this.allSteps.length - 1];
    this.updateStats(
        this.currentArray.length,
        this.currentStepIndex + 1,
        finalStep.total_comparisons || 0,
        finalStep.total_swaps || 0
    );
}

stepForward() {
    if (!this.isPaused || this.currentStepIndex >= this.allSteps.length - 1) return;
    
    this.currentStepIndex++;
    const step = this.allSteps[this.currentStepIndex];
    
    this.currentArray = step.array;
    const highlightClass = step.type === 'comparing' ? 'comparing' :
                         step.type === 'swapping' ? 'swapping' :
                         step.type === 'sorted' ? 'sorted' : 'pivot';
    
    this.renderBars(step.indices, highlightClass);
    document.getElementById('stepDescription').textContent = step.description;
    
    const progress = ((this.currentStepIndex + 1) / this.allSteps.length) * 100;
    document.getElementById('progressBar').style.width = progress + '%';
    
    const finalStep = this.allSteps[this.allSteps.length - 1];
    this.updateStats(
        this.currentArray.length,
        this.currentStepIndex + 1,
        finalStep.total_comparisons || 0,
        finalStep.total_swaps || 0
    );
}


    async exportResults(format) {
    // Check if we have trial results
    if (!this.lastTrialResults) {
        // Auto-run time trial and switch to Time Trial tab
        const runTrial = confirm('No time trial results yet. Run time trial now?');
        if (runTrial) {
            // Switch to Time Trial tab with animation
            this.switchTab('compare');
            
            // Wait a moment for tab animation
            await new Promise(resolve => setTimeout(resolve, 300));
            
            // Run time trial
            const results = await this.runTimeTrial();
            
            if (!results) {
                alert('Failed to run time trial. Please try again.');
                return;
            }
        } else {
            return;
        }
    }
    
    try {
        let content, filename, mimeType;
        
        if (format === 'json') {
            // Export as JSON
            content = JSON.stringify(this.lastTrialResults, null, 2);
            filename = `sorting-trial-${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
            mimeType = 'application/json';
        } else if (format === 'csv') {
            // Export as CSV
            let csv = 'Algorithm,Time (ms),Space Complexity,Comparisons,Swaps,Steps\n';
            
            this.lastTrialResults.results.forEach(result => {
                const timeMs = (result.execution_time_us / 1000).toFixed(3);
                csv += `${result.algorithm},${timeMs},${result.space_complexity},${result.comparisons},${result.swaps},${result.total_steps}\n`;
            });
            
            csv += `\nArray Size: ${this.lastTrialResults.array_size}\n`;
            csv += `Fastest Algorithm: ${this.lastTrialResults.fastest}\n`;
            csv += `Timestamp: ${this.lastTrialResults.timestamp}\n`;
            
            content = csv;
            filename = `sorting-trial-${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.csv`;
            mimeType = 'text/csv';
        }
        
        // Create download link
        const blob = new Blob([content], { type: mimeType });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        // Show success message
        alert(`Exported successfully: ${filename}`);
        
    } catch (error) {
        console.error('Error exporting results:', error);
        alert('Error exporting results: ' + error.message);
    }
}

    async runTimeTrial() {
    const resultsDiv = document.getElementById('comparisonResults');
    
    if (!this.currentArray || this.currentArray.length === 0) {
        resultsDiv.innerHTML = `
            <div style="color: var(--accent-orange); padding: 2rem; text-align: center; background: var(--bg-secondary); border-radius: 8px;">
                <h4>No Array Available</h4>
                <p>Please go to the <strong>Visualize</strong> tab and generate or input an array first.</p>
            </div>
        `;
        return null;
    }
    
    resultsDiv.innerHTML = '<div style="text-align: center; padding: 2rem;"><i class="fas fa-spinner fa-spin"></i> Running time trial...</div>';
    
    try {
        const response = await fetch(`${this.apiUrl}/api/time-trial`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                array: this.currentArray
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Store results
        this.lastTrialResults = {
            array: this.currentArray.slice(),
            array_size: data.array_size,
            results: data.results,
            fastest: data.fastest,
            timestamp: new Date().toISOString()
        };
        
        // Display results
        this.displayTrialResults(data);
        
        return this.lastTrialResults;
        
    } catch (error) {
        console.error('Error running time trial:', error);
        resultsDiv.innerHTML = `
            <div style="color: var(--accent-orange); padding: 2rem; text-align: center; background: var(--bg-secondary); border-radius: 8px;">
                <h4>⚠️ Error Running Time Trial</h4>
                <p>${error.message}</p>
            </div>
        `;
        return null;
    }
}
displayTrialResults(data) {
    const resultsDiv = document.getElementById('comparisonResults');
    
    let html = '<div class="trial-results">';
    html += `<h4 style="display: flex; align-items: center; gap: 0.5rem;">
        <span>🏆</span> Performance Comparison - Array Size: <strong>${data.array_size} elements</strong>
    </h4>`;
    html += `<p style="color: var(--text-secondary); margin: 0.5rem 0 1.5rem 0; font-size: 0.95rem;">
        Testing array: [${this.currentArray.slice(0, 10).join(', ')}${this.currentArray.length > 10 ? ', ...' : ''}]
    </p>`;
    html += '<div class="results-grid">';
    
    data.results.forEach((result, index) => {
        const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '🏅';
        const timeMs = result.execution_time_us / 1000;
        
        html += `
            <div class="result-card">
                <div class="result-rank">${medal} #${index + 1}</div>
                <h5>${result.algorithm.charAt(0).toUpperCase() + result.algorithm.slice(1)} Sort</h5>
                <div class="result-stats">
                    <div class="stat-item">
                        <span class="stat-label">⏱️ Time:</span>
                        <span class="stat-value">${timeMs.toFixed(3)}ms</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">💾 Space:</span>
                        <span class="stat-value">${result.space_complexity || 'N/A'}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">🔄 Comparisons:</span>
                        <span class="stat-value">${result.comparisons ? result.comparisons.toLocaleString() : '0'}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">↔️ Swaps:</span>
                        <span class="stat-value">${result.swaps ? result.swaps.toLocaleString() : '0'}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">📊 Steps:</span>
                        <span class="stat-value">${result.total_steps ? result.total_steps.toLocaleString() : '0'}</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    
    if (data.fastest) {
        html += `<div style="text-align: center; margin-top: 1.5rem; padding: 1rem; background: var(--bg-secondary); border-radius: 8px;">
            <strong>🏆 Fastest Algorithm:</strong> ${data.fastest.charAt(0).toUpperCase() + data.fastest.slice(1)} Sort
        </div>`;
    }
    
    html += '</div>';
    resultsDiv.innerHTML = html;
}



    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SortingVisualizer();
});

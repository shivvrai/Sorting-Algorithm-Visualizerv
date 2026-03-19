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
        
        // Update education tab content
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
        
        // ✅ CORRECT: Declare variables INSIDE the function with proper indentation
        const algorithmName = algorithm.charAt(0).toUpperCase() + algorithm.slice(1);
        const algorithmQuery = algorithmName + ' Sort';
        
        const dynamicLinks = [
            {
                title: `${algorithmQuery} - GeeksforGeeks`,
                url: `https://www.geeksforgeeks.org/${algorithm}-sort/`,
                icon: 'fab fa-google'
            },
            {
                title: `${algorithmQuery} Tutorial - YouTube`,
                url: `https://www.youtube.com/results?search_query=${encodeURIComponent(algorithmQuery + ' algorithm tutorial')}`,
                icon: 'fab fa-youtube'
            },
            {
                title: `Visualize ${algorithmQuery} - VisuAlgo`,
                url: `https://visualgo.net/en/sorting?slide=1`,
                icon: 'fas fa-chart-bar'
            },
            {
                title: `${algorithmQuery} - Wikipedia`,
                url: `https://en.wikipedia.org/wiki/${algorithmName}_sort`,
                icon: 'fab fa-wikipedia-w'
            }
        ];
        
        // Render dynamic links
        const linksContainer = document.getElementById('algoLinks');
        if (linksContainer) {
            linksContainer.innerHTML = dynamicLinks.map(link => `
                <a href="${link.url}" target="_blank" rel="noopener noreferrer" class="external-link">
                    <i class="${link.icon}"></i> ${link.title}
                </a>
            `).join('');
        }
        
        // Load code
        const codeResponse = await fetch(`${this.apiUrl}/api/algorithm-code/${algorithm}`);
        const codeData = await codeResponse.json();
        document.getElementById('algoCode').textContent = codeData.code;
        document.getElementById('algoCodeExplanation').textContent = codeData.explanation;
        
    } catch (error) {
        console.error('Error loading algorithm info:', error);
    }
}


    async start() {
    if (this.isRunning) return;
    
    this.isRunning = true;
    document.getElementById('startBtn').disabled = true;
    document.getElementById('pauseBtn').disabled = false;
    
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
        
        // Visualize steps
        for (let i = 0; i < data.steps.length && this.isRunning; i++) {
            const step = data.steps[i];
            this.currentArray = step.array;
            
            const highlightClass = step.type === 'comparing' ? 'comparing' :
                                 step.type === 'swapping' ? 'swapping' :
                                 step.type === 'sorted' ? 'sorted' : 'pivot';
            
            this.renderBars(step.indices, highlightClass);
            document.getElementById('stepDescription').textContent = step.description;
            
            this.updateStats(
                this.currentArray.length,
                i + 1,
                data.total_comparisons,
                data.total_swaps
            );
            
            const progress = ((i + 1) / data.steps.length) * 100;
            document.getElementById('progressBar').style.width = progress + '%';
            
            await this.sleep(100 / this.speed);
        }
        
        // Only show completion message if NOT paused
        if (this.isRunning) {
            const sortedIndices = Array.from({length: this.currentArray.length}, (_, i) => i);
            this.renderBars(sortedIndices, 'sorted');
            document.getElementById('stepDescription').textContent = 'Sorting completed!';
        }
        // If paused, the step description remains unchanged
        
    } catch (error) {
        console.error('Error during sorting:', error);
        alert('Error: ' + error.message);
    }
    
    this.isRunning = false;
    document.getElementById('startBtn').disabled = false;
    document.getElementById('pauseBtn').disabled = true;
}


async continueVisualization() {
    const totalSteps = this.allSteps.length;
    
    // ✅ Ensure we're actually animating
    for (let i = this.currentStepIndex; i < totalSteps; i++) {
        // Check if paused or stopped
        if (this.isPaused || !this.isRunning) {
            this.currentStepIndex = i;
            return;
        }
        
        const step = this.allSteps[i];
        this.currentArray = step.array;
        
        // Determine highlight class
        const highlightClass = step.type === 'comparing' ? 'comparing' :
                       step.type === 'swapping' ? 'swapping' :
                       step.type === 'sorted' ? 'sorted' :
                       step.type === 'pivot' ? 'pivot' :
                       step.type === 'done' ? 'sorted' : '';

        
        // ✅ Render bars with animation
        this.renderBars(step.indices || [], highlightClass);
        document.getElementById('stepDescription').textContent = step.description || 'Sorting...';
        
        // Get final stats from last step
        const finalStep = this.allSteps[totalSteps - 1];
        this.updateStats(
    this.currentArray.length,
    i + 1,
    step.total_comparisons || finalStep.total_comparisons || 0,
    step.total_swaps || finalStep.total_swaps || 0
);

        
        // Update progress bar
        const progress = ((i + 1) / totalSteps) * 100;
        document.getElementById('progressBar').style.width = progress + '%';
        
        this.currentStepIndex = i;
        
        // ✅ Wait based on speed (100ms base / speed multiplier)
        await this.sleep(100 / this.speed);
    }
    
    // ✅ After completion - show all bars as sorted
    const sortedIndices = Array.from({length: this.currentArray.length}, (_, i) => i);
    this.renderBars(sortedIndices, 'sorted');
    document.getElementById('stepDescription').textContent = `${this.currentAlgorithm.charAt(0).toUpperCase() + this.currentAlgorithm.slice(1)} sort completed!`;
    
    // ✅ Reset state
    this.isRunning = false;
    this.isPaused = false;
    document.getElementById('startBtn').disabled = false;
    document.getElementById('startBtn').innerHTML = '<i class="fas fa-play"></i> Start';
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('stepBackBtn').disabled = true;
    document.getElementById('stepForwardBtn').disabled = true;
}



    pause() {
    this.isRunning = false;
    document.getElementById('pauseBtn').disabled = true;
}





   reset() {
    this.isRunning = false;
    this.generateArray('random');
    document.getElementById('startBtn').disabled = false;
    document.getElementById('pauseBtn').disabled = true;
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


// ============================================
// GRAPH ALGORITHMS VISUALIZER
// ============================================

class GraphVisualizer {
    constructor() {
        this.apiUrl = window.location.origin;
        this.canvas = document.getElementById('graphCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.nodes = {};       // { 'A': {x, y}, 'B': {x, y}, ... }
        this.edges = [];       // [{from, to, weight}, ...]
        this.directed = false;
        this.nextLabel = 0;    // 0→A, 1→B, ...
        this.nodeRadius = 22;

        // Interaction state
        this.mode = 'vertex';  // 'vertex' | 'edge' | 'delete'
        this.dragging = null;  // node label being dragged to create edge
        this.dragLine = null;  // {x,y} current mouse during drag
        this.movingNode = null; // node being repositioned

        // Edge weight modal state
        this.pendingEdge = null; // {from, to} waiting for weight input
        this.editingEdgeIndex = -1; // index of edge being edited

        // Algorithm animation
        this.animating = false;
        this.nodeColors = {};  // override colors per node
        this.edgeColors = {};  // override colors per edge key
        this.speed = 1;
        this.canvasW = 800;
        this.canvasH = 500;

        this.setupEvents();
        this.loadAlgoInfo();
        this.setMode('vertex');

        // Listen for the Graphs tab to become visible
        const graphsTab = document.querySelector('[data-mode="graphs"]');
        if (graphsTab) {
            graphsTab.addEventListener('click', () => {
                setTimeout(() => this.resizeCanvas(), 200);
            });
        }
    }

    getLabel(index) {
        return String.fromCharCode(65 + index);
    }

    resizeCanvas() {
        const w = this.canvas.offsetWidth;
        const h = this.canvas.offsetHeight;
        if (w > 0 && h > 0) {
            this.canvasW = w;
            this.canvasH = h;
            const dpr = window.devicePixelRatio || 1;
            this.canvas.width = w * dpr;
            this.canvas.height = h * dpr;
            this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            this.drawGraph();
        }
    }

    setupEvents() {
        // Mode buttons
        document.getElementById('addVertexModeBtn').addEventListener('click', () => this.setMode('vertex'));
        document.getElementById('addEdgeModeBtn').addEventListener('click', () => this.setMode('edge'));
        document.getElementById('deleteModBtn').addEventListener('click', () => this.setMode('delete'));
        document.getElementById('clearGraphBtn').addEventListener('click', () => this.clearGraph());

        // Directed/undirected toggle
        document.getElementById('undirectedBtn').addEventListener('click', () => this.setDirected(false));
        document.getElementById('directedBtn').addEventListener('click', () => this.setDirected(true));

        // Presets
        document.getElementById('presetSmall').addEventListener('click', () => this.loadPreset('small'));
        document.getElementById('presetMedium').addEventListener('click', () => this.loadPreset('medium'));
        document.getElementById('presetWeighted').addEventListener('click', () => this.loadPreset('weighted'));
        document.getElementById('presetTree').addEventListener('click', () => this.loadPreset('tree'));

        // Run / Reset
        document.getElementById('runGraphAlgoBtn').addEventListener('click', () => this.runAlgorithm());
        document.getElementById('resetGraphAlgoBtn').addEventListener('click', () => this.resetColors());

        // Speed
        const slider = document.getElementById('graphSpeedSlider');
        slider.addEventListener('input', () => {
            this.speed = parseFloat(slider.value);
            document.getElementById('graphSpeedLabel').textContent = this.speed + 'x';
        });

        // Algo select → load info + toggle target node
        document.getElementById('graphAlgoSelect').addEventListener('change', () => {
            this.loadAlgoInfo();
            this.toggleTargetNode();
        });

        // Canvas mouse events
        this.canvas.addEventListener('mousedown', (e) => this.onMouseDown(e));
        this.canvas.addEventListener('mousemove', (e) => this.onMouseMove(e));
        this.canvas.addEventListener('mouseup', (e) => this.onMouseUp(e));
        this.canvas.addEventListener('mouseleave', () => this.onMouseLeave());

        // Double-click to edit edge weight
        this.canvas.addEventListener('dblclick', (e) => this.onDoubleClick(e));

        // Edge weight modal buttons
        document.getElementById('edgeWeightConfirm').addEventListener('click', () => this.confirmEdgeWeight());
        document.getElementById('edgeWeightCancel').addEventListener('click', () => this.cancelEdgeWeight());
        document.getElementById('edgeWeightInput').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') this.confirmEdgeWeight();
            if (e.key === 'Escape') this.cancelEdgeWeight();
        });

        // Error notification close
        document.getElementById('graphErrorClose').addEventListener('click', () => this.hideGraphError());

        // Education sub-tabs
        document.querySelectorAll('.edu-sub-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.edu-sub-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                const eduTab = tab.getAttribute('data-edu-tab');
                const sortingContent = document.querySelector('.education-grid');
                const sortingCode = document.getElementById('sortingCodeSection');
                const graphContent = document.getElementById('graphEducationContent');
                if (eduTab === 'sorting') {
                    sortingContent.style.display = '';
                    sortingCode.style.display = '';
                    graphContent.style.display = 'none';
                } else {
                    sortingContent.style.display = 'none';
                    sortingCode.style.display = 'none';
                    graphContent.style.display = '';
                    this.loadGraphEducationInfo();
                }
            });
        });

        // Graph education algo select
        const graphEduSelect = document.getElementById('graphEduAlgoSelect');
        if (graphEduSelect) {
            graphEduSelect.addEventListener('change', () => this.loadGraphEducationInfo());
        }

        // Initial target node toggle
        this.toggleTargetNode();
    }

    getMousePos(e) {
        const rect = this.canvas.getBoundingClientRect();
        return { x: e.clientX - rect.left, y: e.clientY - rect.top };
    }

    getNodeAt(pos) {
        for (const [label, node] of Object.entries(this.nodes)) {
            const dx = pos.x - node.x;
            const dy = pos.y - node.y;
            if (dx * dx + dy * dy <= this.nodeRadius * this.nodeRadius) return label;
        }
        return null;
    }

    setMode(mode) {
        this.mode = mode;
        const indicator = document.getElementById('graphModeIndicator');
        const modeBtns = document.querySelectorAll('.graph-build-btns .btn');
        modeBtns.forEach(b => b.classList.remove('active-mode'));

        if (mode === 'vertex') {
            indicator.innerHTML = '<i class="fas fa-plus-circle"></i> Click canvas to add a vertex';
            document.getElementById('addVertexModeBtn').classList.add('active-mode');
        } else if (mode === 'edge') {
            indicator.innerHTML = '<i class="fas fa-link"></i> Drag from one node to another to add an edge';
            document.getElementById('addEdgeModeBtn').classList.add('active-mode');
        } else if (mode === 'delete') {
            indicator.innerHTML = '<i class="fas fa-trash"></i> Click a node or edge to delete';
            document.getElementById('deleteModBtn').classList.add('active-mode');
        }
    }

    setDirected(val) {
        this.directed = val;
        document.getElementById('undirectedBtn').classList.toggle('active', !val);
        document.getElementById('directedBtn').classList.toggle('active', val);
        this.drawGraph();
    }

    // ---- Mouse Handlers ----

    onMouseDown(e) {
        if (this.animating) return;
        this.resizeCanvas();
        const pos = this.getMousePos(e);
        const node = this.getNodeAt(pos);

        if (this.mode === 'vertex') {
            if (!node) {
                const label = this.getLabel(this.nextLabel++);
                this.nodes[label] = { x: pos.x, y: pos.y };
                this.updateStartNodeSelect();
                this.drawGraph();
            } else {
                // Start moving existing node
                this.movingNode = node;
            }
        } else if (this.mode === 'edge') {
            if (node) {
                this.dragging = node;
                this.dragLine = pos;
            }
        } else if (this.mode === 'delete') {
            if (node) {
                this.deleteNode(node);
            } else {
                this.deleteEdgeAt(pos);
            }
        }
    }

    onMouseMove(e) {
        const pos = this.getMousePos(e);
        if (this.dragging) {
            this.dragLine = pos;
            this.drawGraph();
            // Draw temporary edge line
            const from = this.nodes[this.dragging];
            this.ctx.beginPath();
            this.ctx.moveTo(from.x, from.y);
            this.ctx.lineTo(pos.x, pos.y);
            this.ctx.strokeStyle = '#94a3b8';
            this.ctx.lineWidth = 2;
            this.ctx.setLineDash([6, 4]);
            this.ctx.stroke();
            this.ctx.setLineDash([]);
        } else if (this.movingNode) {
            this.nodes[this.movingNode] = { x: pos.x, y: pos.y };
            this.drawGraph();
        }
    }

    onMouseUp(e) {
        const pos = this.getMousePos(e);
        if (this.dragging) {
            const target = this.getNodeAt(pos);
            if (target && target !== this.dragging) {
                // Check for duplicate
                const exists = this.edges.some(e =>
                    (e.from === this.dragging && e.to === target) ||
                    (!this.directed && e.from === target && e.to === this.dragging)
                );
                if (!exists) {
                    this.pendingEdge = { from: this.dragging, to: target };
                    this.editingEdgeIndex = -1;
                    this.showEdgeWeightModal(`${this.dragging} → ${target}`, 1);
                }
            }
            this.dragging = null;
            this.dragLine = null;
            this.drawGraph();
        }
        if (this.movingNode) {
            this.movingNode = null;
        }
    }

    onMouseLeave() {
        this.dragging = null;
        this.dragLine = null;
        this.movingNode = null;
        this.drawGraph();
    }

    deleteNode(label) {
        delete this.nodes[label];
        this.edges = this.edges.filter(e => e.from !== label && e.to !== label);
        delete this.nodeColors[label];
        this.updateStartNodeSelect();
        this.drawGraph();
    }

    deleteEdgeAt(pos) {
        let minDist = 15;
        let found = -1;
        for (let i = 0; i < this.edges.length; i++) {
            const e = this.edges[i];
            const a = this.nodes[e.from];
            const b = this.nodes[e.to];
            if (!a || !b) continue;
            const dist = this.pointToSegmentDist(pos, a, b);
            if (dist < minDist) {
                minDist = dist;
                found = i;
            }
        }
        if (found >= 0) {
            this.edges.splice(found, 1);
            this.drawGraph();
        }
    }

    pointToSegmentDist(p, a, b) {
        const dx = b.x - a.x, dy = b.y - a.y;
        const len2 = dx * dx + dy * dy;
        if (len2 === 0) return Math.hypot(p.x - a.x, p.y - a.y);
        let t = ((p.x - a.x) * dx + (p.y - a.y) * dy) / len2;
        t = Math.max(0, Math.min(1, t));
        return Math.hypot(p.x - (a.x + t * dx), p.y - (a.y + t * dy));
    }

    clearGraph() {
        this.nodes = {};
        this.edges = [];
        this.nextLabel = 0;
        this.nodeColors = {};
        this.edgeColors = {};
        this.updateStartNodeSelect();
        this.drawGraph();
    }

    resetColors() {
        this.nodeColors = {};
        this.edgeColors = {};
        this.animating = false;
        document.getElementById('graphStepDescription').textContent = 'Colors reset. Ready to run another algorithm.';
        this.drawGraph();
    }

    updateStartNodeSelect() {
        const sel = document.getElementById('startNodeSelect');
        const labels = Object.keys(this.nodes).sort();
        sel.innerHTML = labels.length
            ? labels.map(l => `<option value="${l}">${l}</option>`).join('')
            : '<option value="">— add vertices first —</option>';
        this.updateTargetNodeSelect();
    }

    updateTargetNodeSelect() {
        const sel = document.getElementById('targetNodeSelect');
        if (!sel) return;
        const labels = Object.keys(this.nodes).sort();
        sel.innerHTML = '<option value="">— none (all nodes) —</option>' +
            labels.map(l => `<option value="${l}">${l}</option>`).join('');
    }

    toggleTargetNode() {
        const algo = document.getElementById('graphAlgoSelect').value;
        const group = document.getElementById('targetNodeGroup');
        if (group) {
            group.style.display = algo === 'dijkstra' ? '' : 'none';
        }
    }

    // ---- Styled Error Notification ----

    showGraphError(title, message, reason = '', type = 'error') {
        const overlay = document.getElementById('graphErrorOverlay');
        const icon = document.getElementById('graphErrorIcon');
        document.getElementById('graphErrorTitle').textContent = title;
        document.getElementById('graphErrorMessage').textContent = message;
        document.getElementById('graphErrorReason').textContent = reason;
        icon.className = 'graph-error-icon' + (type === 'warning' ? ' warning' : '');
        overlay.style.display = 'flex';
    }

    hideGraphError() {
        document.getElementById('graphErrorOverlay').style.display = 'none';
    }

    // ---- Edge Weight Modal ----

    showEdgeWeightModal(label, defaultWeight) {
        const modal = document.getElementById('edgeWeightModal');
        const input = document.getElementById('edgeWeightInput');
        const labelEl = document.getElementById('edgeWeightLabel');
        labelEl.textContent = `Set weight for edge ${label}`;
        input.value = defaultWeight;
        modal.style.display = 'flex';
        setTimeout(() => input.focus(), 50);
    }

    confirmEdgeWeight() {
        const input = document.getElementById('edgeWeightInput');
        const weight = parseFloat(input.value) || 1;
        const modal = document.getElementById('edgeWeightModal');
        modal.style.display = 'none';

        if (this.editingEdgeIndex >= 0) {
            // Editing existing edge
            this.edges[this.editingEdgeIndex].weight = weight;
            this.editingEdgeIndex = -1;
        } else if (this.pendingEdge) {
            // Creating new edge
            this.edges.push({ from: this.pendingEdge.from, to: this.pendingEdge.to, weight });
            this.pendingEdge = null;
        }
        this.drawGraph();
    }

    cancelEdgeWeight() {
        document.getElementById('edgeWeightModal').style.display = 'none';
        this.pendingEdge = null;
        this.editingEdgeIndex = -1;
    }

    onDoubleClick(e) {
        if (this.animating) return;
        const pos = this.getMousePos(e);
        // Check if double-click is near an edge
        let minDist = 15;
        let found = -1;
        for (let i = 0; i < this.edges.length; i++) {
            const edge = this.edges[i];
            const a = this.nodes[edge.from];
            const b = this.nodes[edge.to];
            if (!a || !b) continue;
            const dist = this.pointToSegmentDist(pos, a, b);
            if (dist < minDist) {
                minDist = dist;
                found = i;
            }
        }
        if (found >= 0) {
            const edge = this.edges[found];
            this.editingEdgeIndex = found;
            this.pendingEdge = null;
            this.showEdgeWeightModal(`${edge.from} → ${edge.to}`, edge.weight);
        }
    }

    // ---- Presets ----

    loadPreset(type) {
        this.clearGraph();
        this.resizeCanvas();
        const W = this.canvasW;
        const H = this.canvasH;
        const cx = W / 2, cy = H / 2;

        if (type === 'small') {
            this.nodes = {
                A: {x: cx-120, y: cy-80},
                B: {x: cx+120, y: cy-80},
                C: {x: cx, y: cy+80},
                D: {x: cx-200, y: cy+40}
            };
            this.edges = [
                {from:'A', to:'B', weight:1},
                {from:'B', to:'C', weight:1},
                {from:'A', to:'C', weight:1},
                {from:'A', to:'D', weight:1}
            ];
            this.nextLabel = 4;
        } else if (type === 'medium') {
            this.nodes = {
                A: {x: cx-180, y: cy-120},
                B: {x: cx, y: cy-140},
                C: {x: cx+180, y: cy-100},
                D: {x: cx-140, y: cy+40},
                E: {x: cx+60, y: cy+20},
                F: {x: cx+180, y: cy+100},
                G: {x: cx-40, y: cy+140}
            };
            this.edges = [
                {from:'A', to:'B', weight:1}, {from:'B', to:'C', weight:1},
                {from:'A', to:'D', weight:1}, {from:'B', to:'E', weight:1},
                {from:'C', to:'F', weight:1}, {from:'D', to:'G', weight:1},
                {from:'E', to:'F', weight:1}, {from:'D', to:'E', weight:1},
                {from:'G', to:'E', weight:1}
            ];
            this.nextLabel = 7;
        } else if (type === 'weighted') {
            this.nodes = {
                A: {x: cx-200, y: cy-80},
                B: {x: cx-60, y: cy-140},
                C: {x: cx+120, y: cy-80},
                D: {x: cx-140, y: cy+80},
                E: {x: cx+40, y: cy+60},
                F: {x: cx+200, y: cy+40}
            };
            this.edges = [
                {from:'A', to:'B', weight:4}, {from:'A', to:'D', weight:2},
                {from:'B', to:'C', weight:5}, {from:'B', to:'E', weight:10},
                {from:'C', to:'F', weight:3}, {from:'D', to:'E', weight:7},
                {from:'E', to:'F', weight:1}, {from:'B', to:'D', weight:1}
            ];
            this.nextLabel = 6;
        } else if (type === 'tree') {
            this.nodes = {
                A: {x: cx, y: 60},
                B: {x: cx-160, y: 160},
                C: {x: cx+160, y: 160},
                D: {x: cx-240, y: 280},
                E: {x: cx-80, y: 280},
                F: {x: cx+80, y: 280},
                G: {x: cx+240, y: 280}
            };
            this.edges = [
                {from:'A', to:'B', weight:1}, {from:'A', to:'C', weight:1},
                {from:'B', to:'D', weight:1}, {from:'B', to:'E', weight:1},
                {from:'C', to:'F', weight:1}, {from:'C', to:'G', weight:1}
            ];
            this.nextLabel = 7;
        }

        this.updateStartNodeSelect();
        this.drawGraph();
    }

    // ---- Drawing ----

    drawGraph() {
        const W = this.canvasW;
        const H = this.canvasH;
        this.ctx.clearRect(0, 0, W, H);

        // Draw edges
        for (const edge of this.edges) {
            this.drawEdge(edge);
        }

        // Draw nodes
        for (const [label, pos] of Object.entries(this.nodes)) {
            this.drawNode(label, pos);
        }
    }

    drawNode(label, pos) {
        const ctx = this.ctx;
        const r = this.nodeRadius;
        const color = this.nodeColors[label] || '#64748b';

        // Shadow
        ctx.shadowColor = 'rgba(0,0,0,0.12)';
        ctx.shadowBlur = 8;
        ctx.shadowOffsetY = 3;

        // Circle
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, r, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.shadowColor = 'transparent';

        // White border
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 3;
        ctx.stroke();

        // Label
        ctx.font = 'bold 14px Inter, sans-serif';
        ctx.fillStyle = '#fff';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(label, pos.x, pos.y);
    }

    drawEdge(edge) {
        const ctx = this.ctx;
        const from = this.nodes[edge.from];
        const to = this.nodes[edge.to];
        if (!from || !to) return;

        const key = edge.from + '-' + edge.to;
        const reverseKey = edge.to + '-' + edge.from;
        const color = this.edgeColors[key] || this.edgeColors[reverseKey] || '#cbd5e1';
        const lineWidth = color !== '#cbd5e1' ? 3 : 2;

        const dx = to.x - from.x;
        const dy = to.y - from.y;
        const dist = Math.hypot(dx, dy);
        if (dist === 0) return;
        const ux = dx / dist, uy = dy / dist;

        // Start/end at edge of circles
        const sx = from.x + ux * this.nodeRadius;
        const sy = from.y + uy * this.nodeRadius;
        const ex = to.x - ux * this.nodeRadius;
        const ey = to.y - uy * this.nodeRadius;

        ctx.beginPath();
        ctx.moveTo(sx, sy);
        ctx.lineTo(ex, ey);
        ctx.strokeStyle = color;
        ctx.lineWidth = lineWidth;
        ctx.stroke();

        // Arrow for directed
        if (this.directed) {
            const arrowLen = 12;
            const arrowAngle = Math.PI / 7;
            const angle = Math.atan2(ey - sy, ex - sx);
            ctx.beginPath();
            ctx.moveTo(ex, ey);
            ctx.lineTo(ex - arrowLen * Math.cos(angle - arrowAngle), ey - arrowLen * Math.sin(angle - arrowAngle));
            ctx.moveTo(ex, ey);
            ctx.lineTo(ex - arrowLen * Math.cos(angle + arrowAngle), ey - arrowLen * Math.sin(angle + arrowAngle));
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.stroke();
        }

        // Weight label — always show
        {
            const mx = (sx + ex) / 2;
            const my = (sy + ey) / 2;
            // Offset perpendicular
            const offX = -uy * 14;
            const offY = ux * 14;
            ctx.font = 'bold 12px Inter, sans-serif';
            ctx.fillStyle = '#2563eb';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            // Background pill
            const tw = ctx.measureText(edge.weight.toString()).width + 8;
            ctx.fillStyle = '#eff6ff';
            ctx.beginPath();
            ctx.roundRect(mx + offX - tw/2, my + offY - 10, tw, 20, 6);
            ctx.fill();
            ctx.strokeStyle = '#bfdbfe';
            ctx.lineWidth = 1;
            ctx.stroke();

            ctx.fillStyle = '#2563eb';
            ctx.fillText(edge.weight.toString(), mx + offX, my + offY);
        }
    }

    // ---- Build adjacency list ----

    buildAdjList() {
        const adj = {};
        for (const label of Object.keys(this.nodes)) {
            adj[label] = {};
        }
        for (const e of this.edges) {
            adj[e.from][e.to] = e.weight;
            if (!this.directed) {
                adj[e.to][e.from] = e.weight;
            }
        }
        return adj;
    }

    // ---- Run Algorithm ----

    async runAlgorithm() {
        if (this.animating) return;
        const algo = document.getElementById('graphAlgoSelect').value;
        const start = document.getElementById('startNodeSelect').value;

        if (Object.keys(this.nodes).length === 0) {
            this.showGraphError(
                'No Graph Found',
                'Please add some vertices and edges before running an algorithm.',
                '', 'warning'
            );
            return;
        }
        if (!start) {
            this.showGraphError(
                'No Start Node',
                'Please select a start node from the dropdown.',
                '', 'warning'
            );
            return;
        }

        // ---- Negative weight validation per algorithm ----
        const negativeEdges = this.edges.filter(e => e.weight < 0);
        if (negativeEdges.length > 0) {
            const negList = negativeEdges.map(e => `${e.from} → ${e.to} (weight: ${e.weight})`).join(', ');

            if (algo === 'dijkstra') {
                this.showGraphError(
                    'Negative Weights Not Allowed',
                    `Dijkstra's algorithm does not support negative edge weights.`,
                    `Dijkstra uses a greedy approach — it assumes that once a node is visited with the shortest distance, ` +
                    `no shorter path exists. Negative weights violate this assumption and can produce incorrect results. ` +
                    `Use Bellman-Ford algorithm for graphs with negative weights.\n\nNegative edges found: ${negList}`,
                    'error'
                );
                return;
            }

            if (algo === 'prim') {
                this.showGraphError(
                    'Negative Weights Not Allowed',
                    `Prim's algorithm does not support negative edge weights.`,
                    `Prim's MST algorithm uses a priority queue to greedily pick the minimum-weight edge. ` +
                    `Negative weights can cause the algorithm to select suboptimal edges and produce an incorrect ` +
                    `minimum spanning tree. Remove negative weights to proceed.\n\nNegative edges found: ${negList}`,
                    'error'
                );
                return;
            }
        }

        this.animating = true;
        this.resetColors();
        this.animating = true; // resetColors sets it false
        const btn = document.getElementById('runGraphAlgoBtn');
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running...';

        try {
            const graph = this.buildAdjList();
            const payload = { graph, algorithm: algo, start, directed: this.directed };

            // Include target for Dijkstra
            if (algo === 'dijkstra') {
                const target = document.getElementById('targetNodeSelect').value;
                if (target) payload.target = target;
            }

            const response = await fetch(`${this.apiUrl}/api/graph-solve`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                let errMsg = 'API error';
                try {
                    const err = await response.json();
                    errMsg = err.detail || errMsg;
                } catch {
                    errMsg = `Server error (${response.status})`;
                }
                throw new Error(errMsg);
            }

            const data = await response.json();
            await this.animateSteps(data.steps);

        } catch (err) {
            this.showGraphError(
                'Algorithm Error',
                err.message,
                'An error occurred while running the algorithm. Please check your graph and try again.',
                'error'
            );
        }

        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-play"></i> Run Algorithm';
        this.animating = false;
    }

    async animateSteps(steps) {
        const descEl = document.getElementById('graphStepDescription');

        for (const step of steps) {
            if (!this.animating) break;

            // Update description
            descEl.textContent = step.description || '';

            // Color visited nodes
            if (step.visited) {
                for (const v of step.visited) {
                    this.nodeColors[v] = '#22c55e'; // green
                }
            }

            // Color queued nodes
            if (step.queue) {
                for (const q of step.queue) {
                    if (!step.visited || !step.visited.includes(q)) {
                        this.nodeColors[q] = '#8b5cf6'; // purple
                    }
                }
            }

            // Current node
            if (step.current) {
                this.nodeColors[step.current] = '#f59e0b'; // amber
            }

            // Active edges
            if (step.edges) {
                for (const [a, b] of step.edges) {
                    if (a && b) {
                        const key = a + '-' + b;
                        this.edgeColors[key] = '#f59e0b';
                    }
                }
            }

            // MST edges (red)
            if (step.mst_edges) {
                for (const [a, b] of step.mst_edges) {
                    const key = a + '-' + b;
                    const reverseKey = b + '-' + a;
                    this.edgeColors[key] = '#ef4444';
                    this.edgeColors[reverseKey] = '#ef4444';
                }
            }

            // Relaxed / added edges → highlight
            if (step.type === 'relax' || step.type === 'add_edge') {
                if (step.edges) {
                    for (const [a, b] of step.edges) {
                        if (a && b) {
                            this.edgeColors[a + '-' + b] = '#22c55e';
                        }
                    }
                }
            }

            // Rejected edges → dim
            if (step.type === 'reject_edge') {
                if (step.edges) {
                    for (const [a, b] of step.edges) {
                        if (a && b) {
                            this.edgeColors[a + '-' + b] = '#e2e8f0';
                        }
                    }
                }
            }

            // Shortest path highlighting (Dijkstra with target)
            if (step.type === 'done' && step.path && step.path_edges) {
                // Highlight shortest path nodes in blue
                for (const node of step.path) {
                    this.nodeColors[node] = '#3b82f6';
                }
                // Highlight shortest path edges in blue
                for (const [a, b] of step.path_edges) {
                    this.edgeColors[a + '-' + b] = '#3b82f6';
                    this.edgeColors[b + '-' + a] = '#3b82f6';
                }
            }

            this.drawGraph();
            await new Promise(r => setTimeout(r, 600 / this.speed));
        }
    }

    // ---- Algorithm Info ----

    async loadAlgoInfo() {
        const algo = document.getElementById('graphAlgoSelect').value;
        const infoDiv = document.getElementById('graphAlgoInfo');
        try {
            const resp = await fetch(`${this.apiUrl}/api/graph-algorithm-info/${algo}`);
            const info = await resp.json();
            infoDiv.innerHTML = `
                <div class="algo-name">${info.name}</div>
                <div>${info.description}</div>
                <div class="algo-complexity">
                    <span>Time: <strong>${info.time_complexity}</strong></span>
                    <span>Space: <strong>${info.space_complexity}</strong></span>
                </div>
            `;
        } catch {
            infoDiv.innerHTML = '';
        }
    }

    // ---- Graph Education Info ----

    async loadGraphEducationInfo() {
        const algo = document.getElementById('graphEduAlgoSelect').value;
        try {
            const [infoResp, codeResp] = await Promise.all([
                fetch(`${this.apiUrl}/api/graph-algorithm-info/${algo}`),
                fetch(`${this.apiUrl}/api/graph-algorithm-code/${algo}`)
            ]);
            const info = await infoResp.json();
            const codeData = await codeResp.json();

            // Fill the education section
            document.getElementById('graphAlgoDescription').textContent = info.description || '';
            document.getElementById('graphTimeComplexity').textContent = info.time_complexity || '';
            document.getElementById('graphSpaceComplexity').textContent = info.space_complexity || '';
            document.getElementById('graphHowItWorks').textContent = info.how_it_works || '';

            // Code explanation
            const codeExpEl = document.getElementById('graphCodeExplanation');
            if (info.code_explanation) {
                const ce = info.code_explanation;
                codeExpEl.innerHTML = `
                    <div class="code-explanation-card">
                        <strong>Algorithm</strong>
                        <p>${ce.algorithm || ''}</p>
                    </div>
                    <div class="code-explanation-card">
                        <strong>Key Insight</strong>
                        <p>${ce.key_insight || ''}</p>
                    </div>
                    <div class="code-explanation-card">
                        <strong>Data Structure</strong>
                        <p>${ce.data_structure || ''}</p>
                    </div>
                `;
            } else {
                codeExpEl.innerHTML = '';
            }

            // Lists
            document.getElementById('graphRealWorldUses').innerHTML =
                (info.real_world_uses || []).map(u => `<li>${u}</li>`).join('');
            document.getElementById('graphWhenToUse').innerHTML =
                (info.when_to_use || []).map(u => `<li>${u}</li>`).join('');
            document.getElementById('graphAdvantages').innerHTML =
                (info.advantages || []).map(a => `<li>${a}</li>`).join('');
            document.getElementById('graphDisadvantages').innerHTML =
                (info.disadvantages || []).map(d => `<li>${d}</li>`).join('');
            document.getElementById('graphWhenNotToUse').innerHTML =
                (info.when_not_to_use || []).map(w => `<li>${w}</li>`).join('');

            // Resources
            const resources = info.resources || {};
            const linksEl = document.getElementById('graphAlgoLinks');
            const algoName = info.name || algo;
            linksEl.innerHTML = `
                ${resources.geeksforgeeks ? `<a href="${resources.geeksforgeeks}" target="_blank" rel="noopener noreferrer" class="external-link"><i class="fab fa-google"></i> ${algoName} — GeeksforGeeks</a>` : ''}
                ${resources.youtube ? `<a href="${resources.youtube}" target="_blank" rel="noopener noreferrer" class="external-link"><i class="fab fa-youtube"></i> ${algoName} Tutorial — YouTube</a>` : ''}
                ${resources.visualgo ? `<a href="${resources.visualgo}" target="_blank" rel="noopener noreferrer" class="external-link"><i class="fas fa-chart-bar"></i> Visualize ${algoName} — VisuAlgo</a>` : ''}
            `;

            // Code
            document.getElementById('graphAlgoCode').textContent = codeData.code || '';

        } catch (error) {
            console.error('Error loading graph education info:', error);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SortingVisualizer();
    new GraphVisualizer();
});

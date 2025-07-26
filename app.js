/**
 * Flora & Fauna Data Collection Frontend
 * Modern JavaScript application with Supabase integration
 */

class FloraFaunaApp {
    constructor() {
        this.supabase = null;
        this.allData = [];
        this.filteredData = [];
        this.currentFilter = 'all';
        this.searchQuery = '';
        
        this.init();
    }

    async init() {
        this.setupEventListeners();
        await this.initializeSupabase();
        await this.loadData();
        this.updateStatistics();
    }

    setupEventListeners() {
        // Mobile menu toggle
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        
        mobileMenuBtn?.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    // Close mobile menu if open
                    mobileMenu.classList.add('hidden');
                }
            });
        });

        // CTA buttons
        document.getElementById('explore-data-btn')?.addEventListener('click', () => {
            document.getElementById('data').scrollIntoView({
                behavior: 'smooth'
            });
        });

        document.getElementById('streamlit-app-btn')?.addEventListener('click', () => {
            // In a real deployment, this would redirect to the Streamlit app
            window.open('/app.py', '_blank');
        });

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.handleFilterChange(e.target.dataset.filter);
                this.updateFilterButtons(e.target);
            });
        });

        // Search input
        const searchInput = document.getElementById('search-input');
        searchInput?.addEventListener('input', (e) => {
            this.searchQuery = e.target.value.toLowerCase();
            this.filterAndDisplayData();
        });

        // Retry button
        document.getElementById('retry-btn')?.addEventListener('click', () => {
            this.loadData();
        });

        // Configuration modal
        document.getElementById('save-config')?.addEventListener('click', () => {
            this.saveSupabaseConfig();
        });

        document.getElementById('cancel-config')?.addEventListener('click', () => {
            this.hideConfigModal();
        });
    }

    async initializeSupabase() {
        // Try to get credentials from localStorage first
        const savedUrl = localStorage.getItem('supabase_url');
        const savedKey = localStorage.getItem('supabase_key');

        if (savedUrl && savedKey) {
            await this.connectToSupabase(savedUrl, savedKey);
        } else {
            // Try default/demo configuration
            const demoUrl = 'https://your-project.supabase.co';
            const demoKey = 'your-anon-key';
            
            if (demoUrl !== 'https://your-project.supabase.co') {
                await this.connectToSupabase(demoUrl, demoKey);
            } else {
                this.showConfigModal();
            }
        }
    }

    async connectToSupabase(url, key) {
        try {
            this.supabase = supabase.createClient(url, key);
            
            // Test connection
            const { data, error } = await this.supabase
                .from('data_entries')
                .select('id')
                .limit(1);

            if (error) {
                throw error;
            }

            this.updateConnectionStatus(true);
        } catch (error) {
            console.error('Supabase connection error:', error);
            this.updateConnectionStatus(false);
            this.showConfigModal();
        }
    }

    showConfigModal() {
        const modal = document.getElementById('config-modal');
        modal?.classList.remove('hidden');
    }

    hideConfigModal() {
        const modal = document.getElementById('config-modal');
        modal?.classList.add('hidden');
    }

    async saveSupabaseConfig() {
        const url = document.getElementById('supabase-url').value.trim();
        const key = document.getElementById('supabase-key').value.trim();

        if (!url || !key) {
            alert('Please provide both URL and key');
            return;
        }

        // Save to localStorage
        localStorage.setItem('supabase_url', url);
        localStorage.setItem('supabase_key', key);

        // Connect to Supabase
        await this.connectToSupabase(url, key);
        
        if (this.supabase) {
            this.hideConfigModal();
            await this.loadData();
            this.updateStatistics();
        }
    }

    updateConnectionStatus(connected) {
        const indicator = document.getElementById('status-indicator');
        const text = document.getElementById('status-text');

        if (connected) {
            indicator?.classList.remove('bg-red-500');
            indicator?.classList.add('bg-green-500');
            if (text) text.textContent = 'Connected';
        } else {
            indicator?.classList.remove('bg-green-500');
            indicator?.classList.add('bg-red-500');
            if (text) text.textContent = 'Disconnected';
        }
    }

    async loadData() {
        if (!this.supabase) {
            this.showError('Supabase not connected. Please check your configuration.');
            return;
        }

        this.showLoading();

        try {
            const { data, error } = await this.supabase
                .from('data_entries')
                .select('*')
                .order('timestamp', { ascending: false });

            if (error) {
                throw error;
            }

            this.allData = data || [];
            this.filterAndDisplayData();
            
        } catch (error) {
            console.error('Error loading data:', error);
            this.showError(`Failed to load data: ${error.message}`);
        }
    }

    showLoading() {
        document.getElementById('loading-state')?.classList.remove('hidden');
        document.getElementById('data-grid')?.classList.add('hidden');
        document.getElementById('error-state')?.classList.add('hidden');
        document.getElementById('empty-state')?.classList.add('hidden');
    }

    showError(message) {
        document.getElementById('loading-state')?.classList.add('hidden');
        document.getElementById('data-grid')?.classList.add('hidden');
        document.getElementById('error-state')?.classList.remove('hidden');
        document.getElementById('empty-state')?.classList.add('hidden');
        
        const errorState = document.getElementById('error-state');
        const errorText = errorState?.querySelector('p');
        if (errorText) {
            errorText.textContent = message;
        }
    }

    handleFilterChange(filter) {
        this.currentFilter = filter;
        this.filterAndDisplayData();
    }

    updateFilterButtons(activeButton) {
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active', 'bg-nature-green', 'text-white');
            btn.classList.add('bg-gray-200', 'text-gray-700');
        });
        
        activeButton.classList.add('active', 'bg-nature-green', 'text-white');
        activeButton.classList.remove('bg-gray-200', 'text-gray-700');
    }

    filterAndDisplayData() {
        // Filter by type
        let filtered = this.currentFilter === 'all' 
            ? this.allData 
            : this.allData.filter(item => item.entry_type === this.currentFilter);

        // Filter by search query
        if (this.searchQuery) {
            filtered = filtered.filter(item => 
                item.title?.toLowerCase().includes(this.searchQuery) ||
                item.content?.toLowerCase().includes(this.searchQuery) ||
                item.location_name?.toLowerCase().includes(this.searchQuery)
            );
        }

        this.filteredData = filtered;
        this.displayData();
    }

    displayData() {
        const grid = document.getElementById('data-grid');
        const loading = document.getElementById('loading-state');
        const error = document.getElementById('error-state');
        const empty = document.getElementById('empty-state');

        // Hide all states first
        [loading, error, empty].forEach(el => el?.classList.add('hidden'));

        if (this.filteredData.length === 0) {
            empty?.classList.remove('hidden');
            grid?.classList.add('hidden');
            return;
        }

        grid?.classList.remove('hidden');
        
        if (grid) {
            grid.innerHTML = this.filteredData.map(item => this.createDataCard(item)).join('');
        }
    }

    createDataCard(item) {
        const timestamp = new Date(item.timestamp).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });

        const typeIcon = this.getTypeIcon(item.entry_type);
        const location = item.location_name || 'Unknown location';

        return `
            <div class="bg-white rounded-xl shadow-lg overflow-hidden card-hover fade-in">
                <div class="relative">
                    ${this.createMediaPreview(item)}
                    <div class="absolute top-4 left-4">
                        <span class="bg-black bg-opacity-50 text-white px-3 py-1 rounded-full text-sm">
                            ${typeIcon} ${item.entry_type.charAt(0).toUpperCase() + item.entry_type.slice(1)}
                        </span>
                    </div>
                </div>
                <div class="p-6">
                    <h3 class="text-xl font-semibold mb-3 text-gray-800">${this.escapeHtml(item.title || 'Untitled')}</h3>
                    
                    ${item.content ? `
                        <p class="text-gray-600 mb-4 line-clamp-3">${this.escapeHtml(item.content.substring(0, 150))}${item.content.length > 150 ? '...' : ''}</p>
                    ` : ''}
                    
                    <div class="flex items-center justify-between text-sm text-gray-500 mb-4">
                        <div class="flex items-center space-x-2">
                            <i class="fas fa-calendar"></i>
                            <span>${timestamp}</span>
                        </div>
                        ${item.location_lat && item.location_lng ? `
                            <div class="flex items-center space-x-2">
                                <i class="fas fa-map-marker-alt"></i>
                                <span>${this.escapeHtml(location)}</span>
                            </div>
                        ` : ''}
                    </div>
                    
                    <div class="flex space-x-3">
                        ${item.file_url ? `
                            <a href="${item.file_url}" target="_blank" 
                               class="flex-1 bg-nature-green text-white text-center py-2 px-4 rounded-lg hover:bg-green-600 transition-colors">
                                <i class="fas fa-external-link-alt mr-2"></i>View
                            </a>
                        ` : ''}
                        <button onclick="app.viewDetails('${item.id}')" 
                                class="flex-1 bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors">
                            <i class="fas fa-info-circle mr-2"></i>Details
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    createMediaPreview(item) {
        const placeholderImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjNmNGY2Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5YTNhZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPk5vIEltYWdlIEF2YWlsYWJsZTwvdGV4dD48L3N2Zz4=';

        switch (item.entry_type) {
            case 'image':
                return `
                    <div class="aspect-w-16 aspect-h-9 bg-gray-100">
                        <img src="${item.file_url || placeholderImage}" 
                             alt="${this.escapeHtml(item.title)}"
                             class="w-full h-48 object-cover"
                             onerror="this.src='${placeholderImage}'">
                    </div>
                `;
            case 'video':
                return `
                    <div class="aspect-w-16 aspect-h-9 bg-gray-900 flex items-center justify-center h-48">
                        <i class="fas fa-play-circle text-6xl text-white opacity-75"></i>
                    </div>
                `;
            case 'audio':
                return `
                    <div class="aspect-w-16 aspect-h-9 bg-gradient-to-r from-purple-400 to-pink-400 flex items-center justify-center h-48">
                        <i class="fas fa-music text-6xl text-white"></i>
                    </div>
                `;
            case 'text':
                return `
                    <div class="aspect-w-16 aspect-h-9 bg-gradient-to-r from-blue-400 to-indigo-400 flex items-center justify-center h-48">
                        <i class="fas fa-file-text text-6xl text-white"></i>
                    </div>
                `;
            default:
                return `
                    <div class="aspect-w-16 aspect-h-9 bg-gray-400 flex items-center justify-center h-48">
                        <i class="fas fa-file text-6xl text-white"></i>
                    </div>
                `;
        }
    }

    getTypeIcon(type) {
        const icons = {
            'image': '🖼️',
            'video': '🎥',
            'audio': '🎵',
            'text': '📝'
        };
        return icons[type] || '📄';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async updateStatistics() {
        if (!this.supabase) return;

        try {
            // Get total records count
            const { count: totalCount, error: countError } = await this.supabase
                .from('data_entries')
                .select('*', { count: 'exact', head: true });

            if (countError) throw countError;

            // Get unique species count (using title as proxy for species)
            const { data: speciesData, error: speciesError } = await this.supabase
                .from('data_entries')
                .select('title');

            if (speciesError) throw speciesError;

            const uniqueSpecies = new Set(speciesData?.map(item => item.title?.toLowerCase()) || []).size;

            // Get unique locations count
            const { data: locationData, error: locationError } = await this.supabase
                .from('data_entries')
                .select('location_name')
                .not('location_name', 'is', null);

            if (locationError) throw locationError;

            const uniqueLocations = new Set(locationData?.map(item => item.location_name) || []).size;

            // Update UI
            this.animateCountUp('total-records', totalCount || 0);
            this.animateCountUp('species-count', uniqueSpecies);
            this.animateCountUp('locations-count', uniqueLocations);

        } catch (error) {
            console.error('Error updating statistics:', error);
            // Set default values on error
            document.getElementById('total-records').textContent = '0';
            document.getElementById('species-count').textContent = '0';
            document.getElementById('locations-count').textContent = '0';
        }
    }

    animateCountUp(elementId, targetValue) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const duration = 2000;
        const startValue = 0;
        const increment = targetValue / (duration / 16);
        let currentValue = startValue;

        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= targetValue) {
                element.textContent = targetValue.toLocaleString();
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(currentValue).toLocaleString();
            }
        }, 16);
    }

    async viewDetails(itemId) {
        const item = this.allData.find(data => data.id.toString() === itemId);
        if (!item) return;

        // Create and show detailed modal (you could expand this)
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4';
        modal.innerHTML = `
            <div class="bg-white rounded-xl max-w-2xl w-full max-h-96 overflow-y-auto">
                <div class="p-6">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-2xl font-bold">${this.escapeHtml(item.title || 'Untitled')}</h3>
                        <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700">
                            <i class="fas fa-times text-xl"></i>
                        </button>
                    </div>
                    
                    <div class="space-y-4">
                        <div>
                            <label class="font-semibold text-gray-700">Type:</label>
                            <span class="ml-2">${this.getTypeIcon(item.entry_type)} ${item.entry_type.charAt(0).toUpperCase() + item.entry_type.slice(1)}</span>
                        </div>
                        
                        ${item.content ? `
                            <div>
                                <label class="font-semibold text-gray-700">Content:</label>
                                <p class="mt-2 text-gray-600 whitespace-pre-wrap">${this.escapeHtml(item.content)}</p>
                            </div>
                        ` : ''}
                        
                        <div>
                            <label class="font-semibold text-gray-700">Date:</label>
                            <span class="ml-2">${new Date(item.timestamp).toLocaleString()}</span>
                        </div>
                        
                        ${item.location_name ? `
                            <div>
                                <label class="font-semibold text-gray-700">Location:</label>
                                <span class="ml-2">${this.escapeHtml(item.location_name)}</span>
                                ${item.location_lat && item.location_lng ? `
                                    <div class="text-sm text-gray-500 mt-1">
                                        Coordinates: ${item.location_lat.toFixed(6)}, ${item.location_lng.toFixed(6)}
                                    </div>
                                ` : ''}
                            </div>
                        ` : ''}
                        
                        ${item.file_url ? `
                            <div>
                                <a href="${item.file_url}" target="_blank" 
                                   class="inline-flex items-center bg-nature-green text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors">
                                    <i class="fas fa-external-link-alt mr-2"></i>View File
                                </a>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    }
}

// Initialize the application
const app = new FloraFaunaApp();

// Export for global access
window.app = app;
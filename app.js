// Flora & Fauna Data Collection - Frontend JavaScript
// Advanced Supabase Integration with Professional UI/UX

class FloraFaunaApp {
    constructor() {
        this.supabase = null;
        this.currentData = [];
        this.filteredData = [];
        this.currentFilter = 'all';
        this.searchQuery = '';
        this.isConnected = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadSupabaseConfig();
    }

    setupEventListeners() {
        // Mobile menu toggle
        document.getElementById('mobile-menu-btn')?.addEventListener('click', () => {
            const mobileMenu = document.getElementById('mobile-menu');
            mobileMenu.classList.toggle('hidden');
        });

        // Navigation smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setActiveFilter(e.target);
                this.currentFilter = e.target.dataset.filter;
                this.filterData();
            });
        });

        // Search functionality
        const searchInput = document.getElementById('search-input');
        searchInput?.addEventListener('input', (e) => {
            this.searchQuery = e.target.value.toLowerCase();
            this.filterData();
        });

        // Button actions
        document.getElementById('explore-data-btn')?.addEventListener('click', () => {
            document.getElementById('data').scrollIntoView({ behavior: 'smooth' });
        });

        document.getElementById('streamlit-app-btn')?.addEventListener('click', () => {
            // You can replace this with your actual Streamlit app URL
            window.open('/streamlit', '_blank');
        });

        // Retry button
        document.getElementById('retry-btn')?.addEventListener('click', () => {
            this.loadData();
        });

        // Config modal
        document.getElementById('save-config')?.addEventListener('click', () => {
            this.saveSupabaseConfig();
        });

        document.getElementById('cancel-config')?.addEventListener('click', () => {
            this.hideConfigModal();
        });
    }

    setActiveFilter(activeBtn) {
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active', 'bg-nature-green', 'text-white');
            btn.classList.add('bg-gray-200', 'text-gray-700');
        });
        
        activeBtn.classList.remove('bg-gray-200', 'text-gray-700');
        activeBtn.classList.add('active', 'bg-nature-green', 'text-white');
    }

    async loadSupabaseConfig() {
        // Try to load config from localStorage first
        const savedUrl = localStorage.getItem('supabase_url');
        const savedKey = localStorage.getItem('supabase_key');

        if (savedUrl && savedKey) {
            await this.initializeSupabase(savedUrl, savedKey);
        } else {
            // Show config modal if no saved config
            this.showConfigModal();
        }
    }

    async initializeSupabase(url, key) {
        try {
            this.supabase = supabase.createClient(url, key);
            
            // Test connection
            const { data, error } = await this.supabase.from('multimedia_data').select('count', { count: 'exact', head: true });
            
            if (error && error.code !== 'PGRST116') { // PGRST116 is "relation does not exist"
                throw error;
            }

            this.isConnected = true;
            this.updateConnectionStatus(true);
            this.loadData();
            this.hideConfigModal();
            
        } catch (error) {
            console.error('Supabase connection failed:', error);
            this.updateConnectionStatus(false);
            this.showError('Failed to connect to Supabase: ' + error.message);
        }
    }

    async saveSupabaseConfig() {
        const url = document.getElementById('supabase-url').value.trim();
        const key = document.getElementById('supabase-key').value.trim();

        if (!url || !key) {
            alert('Please enter both Supabase URL and Anon Key');
            return;
        }

        // Save to localStorage
        localStorage.setItem('supabase_url', url);
        localStorage.setItem('supabase_key', key);

        await this.initializeSupabase(url, key);
    }

    showConfigModal() {
        document.getElementById('config-modal').classList.remove('hidden');
    }

    hideConfigModal() {
        document.getElementById('config-modal').classList.add('hidden');
    }

    updateConnectionStatus(connected) {
        const indicator = document.getElementById('status-indicator');
        const text = document.getElementById('status-text');
        
        if (connected) {
            indicator.classList.remove('bg-red-500');
            indicator.classList.add('bg-green-500');
            text.textContent = 'Connected';
        } else {
            indicator.classList.remove('bg-green-500');
            indicator.classList.add('bg-red-500');
            text.textContent = 'Disconnected';
        }
    }

    async loadData() {
        if (!this.supabase) {
            this.showError('Supabase not initialized');
            return;
        }

        this.showLoading();

        try {
            // Load multimedia data
            const { data, error } = await this.supabase
                .from('multimedia_data')
                .select('*')
                .order('created_at', { ascending: false })
                .limit(50);

            if (error) {
                throw error;
            }

            this.currentData = data || [];
            this.filteredData = [...this.currentData];
            
            this.updateStats();
            this.renderData();
            this.hideLoading();

        } catch (error) {
            console.error('Error loading data:', error);
            this.showError('Error loading data: ' + error.message);
            this.hideLoading();
        }
    }

    async updateStats() {
        try {
            // Get total records count
            const { count: totalCount } = await this.supabase
                .from('multimedia_data')
                .select('*', { count: 'exact', head: true });

            // Get unique species count
            const { data: speciesData } = await this.supabase
                .from('multimedia_data')
                .select('species_name')
                .not('species_name', 'is', null);

            const uniqueSpecies = new Set(speciesData?.map(item => item.species_name) || []);

            // Get unique locations count
            const { data: locationData } = await this.supabase
                .from('multimedia_data')
                .select('location')
                .not('location', 'is', null);

            const uniqueLocations = new Set(locationData?.map(item => item.location) || []);

            // Animate counters
            this.animateCounter('total-records', totalCount || 0);
            this.animateCounter('species-count', uniqueSpecies.size);
            this.animateCounter('locations-count', uniqueLocations.size);

        } catch (error) {
            console.error('Error updating stats:', error);
        }
    }

    animateCounter(elementId, targetValue) {
        const element = document.getElementById(elementId);
        if (!element) return;

        let current = 0;
        const increment = targetValue / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= targetValue) {
                current = targetValue;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current).toLocaleString();
        }, 30);
    }

    filterData() {
        let filtered = [...this.currentData];

        // Apply filter
        if (this.currentFilter !== 'all') {
            filtered = filtered.filter(item => {
                const type = this.getDataType(item);
                return type === this.currentFilter;
            });
        }

        // Apply search
        if (this.searchQuery) {
            filtered = filtered.filter(item =>
                (item.species_name?.toLowerCase().includes(this.searchQuery)) ||
                (item.common_name?.toLowerCase().includes(this.searchQuery)) ||
                (item.location?.toLowerCase().includes(this.searchQuery)) ||
                (item.description?.toLowerCase().includes(this.searchQuery))
            );
        }

        this.filteredData = filtered;
        this.renderData();
    }

    getDataType(item) {
        if (item.file_path) {
            const ext = item.file_path.split('.').pop()?.toLowerCase();
            if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext)) return 'image';
            if (['mp4', 'webm', 'mov', 'avi'].includes(ext)) return 'video';
            if (['mp3', 'wav', 'ogg', 'm4a'].includes(ext)) return 'audio';
        }
        return 'text';
    }

    renderData() {
        const dataGrid = document.getElementById('data-grid');
        const emptyState = document.getElementById('empty-state');

        if (this.filteredData.length === 0) {
            dataGrid.classList.add('hidden');
            emptyState.classList.remove('hidden');
            return;
        }

        emptyState.classList.add('hidden');
        dataGrid.classList.remove('hidden');

        dataGrid.innerHTML = this.filteredData.map(item => this.createDataCard(item)).join('');
    }

    createDataCard(item) {
        const type = this.getDataType(item);
        const typeIcons = {
            image: '🖼',
            video: '🎥',
            audio: '🎵',
            text: '📝'
        };

        const formatDate = (dateString) => {
            return new Date(dateString).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        };

        const getMediaPreview = () => {
            if (!item.file_path) return '';
            
            if (type === 'image') {
                return `<img src="${item.file_path}" alt="${item.species_name}" class="w-full h-48 object-cover rounded-t-xl">`;
            } else if (type === 'video') {
                return `<video class="w-full h-48 object-cover rounded-t-xl" controls><source src="${item.file_path}" type="video/mp4"></video>`;
            } else if (type === 'audio') {
                return `<div class="w-full h-48 bg-gradient-to-br from-blue-100 to-purple-100 rounded-t-xl flex items-center justify-center">
                    <audio controls class="w-full mx-4"><source src="${item.file_path}" type="audio/mpeg"></audio>
                </div>`;
            }
            return `<div class="w-full h-48 bg-gradient-to-br from-green-100 to-blue-100 rounded-t-xl flex items-center justify-center">
                <i class="fas fa-file-text text-4xl text-gray-500"></i>
            </div>`;
        };

        return `
            <div class="bg-white rounded-xl shadow-lg overflow-hidden card-hover">
                ${getMediaPreview()}
                <div class="p-6">
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-sm font-medium text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                            ${typeIcons[type]} ${type.charAt(0).toUpperCase() + type.slice(1)}
                        </span>
                        <span class="text-xs text-gray-400">${formatDate(item.created_at)}</span>
                    </div>
                    
                    <h3 class="text-xl font-bold text-gray-800 mb-2">
                        ${item.species_name || 'Unknown Species'}
                    </h3>
                    
                    ${item.common_name ? `<p class="text-sm text-gray-600 mb-2"><strong>Common Name:</strong> ${item.common_name}</p>` : ''}
                    
                    ${item.location ? `<p class="text-sm text-gray-600 mb-2"><i class="fas fa-map-marker-alt mr-1"></i> ${item.location}</p>` : ''}
                    
                    ${item.description ? `<p class="text-sm text-gray-700 mb-4 line-clamp-3">${item.description}</p>` : ''}
                    
                    <div class="flex justify-between items-center">
                        <div class="flex items-center space-x-2">
                            ${item.latitude && item.longitude ? 
                                `<button onclick="app.showOnMap(${item.latitude}, ${item.longitude})" class="text-blue-500 hover:text-blue-700 text-sm">
                                    <i class="fas fa-map mr-1"></i>View on Map
                                </button>` : ''
                            }
                        </div>
                        <button onclick="app.viewDetails('${item.id}')" class="bg-nature-green text-white px-4 py-2 rounded-lg text-sm hover:bg-green-600 transition-colors">
                            View Details
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    showOnMap(lat, lng) {
        // Open Google Maps with the coordinates
        window.open(`https://www.google.com/maps?q=${lat},${lng}`, '_blank');
    }

    viewDetails(id) {
        const item = this.currentData.find(data => data.id === id);
        if (item) {
            // Create a detailed view modal or navigate to a detail page
            alert(`Details for ${item.species_name}:\n\nLocation: ${item.location}\nDescription: ${item.description}`);
        }
    }

    showLoading() {
        document.getElementById('loading-state').classList.remove('hidden');
        document.getElementById('error-state').classList.add('hidden');
        document.getElementById('data-grid').classList.add('hidden');
        document.getElementById('empty-state').classList.add('hidden');
    }

    hideLoading() {
        document.getElementById('loading-state').classList.add('hidden');
    }

    showError(message) {
        document.getElementById('error-state').classList.remove('hidden');
        document.getElementById('loading-state').classList.add('hidden');
        document.getElementById('data-grid').classList.add('hidden');
        document.getElementById('empty-state').classList.add('hidden');
        
        // Update error message if needed
        const errorElement = document.querySelector('#error-state p');
        if (errorElement) {
            errorElement.textContent = message;
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new FloraFaunaApp();
});

// Add CSS for line clamping (truncating text)
const style = document.createElement('style');
style.textContent = `
    .line-clamp-3 {
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
`;
document.head.appendChild(style);
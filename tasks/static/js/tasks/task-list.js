// static/js/tasks/task-list.js
'use strict';

/**
 * Task List Manager - Handles AJAX pagination and loading states
 */
class TaskListManager {
    constructor() {
        this.loadingDelay = 900; // Reduced from 1000ms for better UX
        this.currentRequests = new Map(); // Track ongoing requests
        this.init();
    }

    /**
     * Initialize event listeners and setup
     */
    init() {
        this.bindEvents();
        this.setupErrorHandling();
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Use event delegation for pagination links
        document.addEventListener('click', (e) => {
            if (e.target.matches('.pagination-link, .pagination-link *')) {
                e.preventDefault();
                const link = e.target.closest('.pagination-link');
                this.handlePaginationClick(link);
            }
        });

        // Handle browser back/forward buttons
        window.addEventListener('popstate', async (e) => {
            if (e.state && e.state.section && e.state.page) {
                await this.loadSection(e.state.section, e.state.page, false);
            }
        });
    }

    /**
     * Handle pagination link clicks
     * @param {HTMLElement} link - The clicked pagination link
     */
    handlePaginationClick(link) {
        if (!link) return;

        const section = link.dataset.section;
        const page = link.dataset.page;

        if (!section || !page) {
            console.error('Missing section or page data in pagination link');
            return;
        }

        // Prevent rapid clicking
        if (link.disabled) return;
        
        this.loadSection(section, page, true);
    }

    /**
     * Show loading spinner for a section
     * @param {string} section - Section identifier
     */
    showSpinner(section) {
        const loader = document.getElementById(`${section}-loader-container`);
        const content = document.getElementById(`${section}-content`);
        
        if (loader) {
            loader.style.display = 'flex';
            loader.setAttribute('aria-hidden', 'false');
        }
        if (content) {
            content.style.opacity = '0.5';
            content.setAttribute('aria-busy', 'true');
        }

        // Disable pagination links in this section
        this.disablePaginationLinks(section, true);
    }

    /**
     * Hide loading spinner for a section
     * @param {string} section - Section identifier
     */
    hideSpinner(section) {
        const loader = document.getElementById(`${section}-loader-container`);
        const content = document.getElementById(`${section}-content`);
        
        if (loader) {
            loader.style.display = 'none';
            loader.setAttribute('aria-hidden', 'true');
        }
        if (content) {
            content.style.opacity = '';
            content.removeAttribute('aria-busy');
        }

        // Re-enable pagination links
        this.disablePaginationLinks(section, false);
    }

    /**
     * Disable/enable pagination links in a section
     * @param {string} section - Section identifier
     * @param {boolean} disable - Whether to disable or enable
     */
    disablePaginationLinks(section, disable) {
        const sectionEl = document.getElementById(`tasks-${section}-section`);
        if (!sectionEl) return;

        const links = sectionEl.querySelectorAll('.pagination-link');
        links.forEach(link => {
            link.disabled = disable;
            if (disable) {
                link.style.pointerEvents = 'none';
                link.style.opacity = '0.6';
            } else {
                link.style.pointerEvents = '';
                link.style.opacity = '';
            }
        });
    }

    /**
     * Load a specific section with pagination
     * @param {string} section - Section identifier
     * @param {number} page - Page number
     * @param {boolean} updateHistory - Whether to update browser history
     */
    async loadSection(section, page, updateHistory = true) {
        // Cancel any existing request for this section
        if (this.currentRequests.has(section)) {
            this.currentRequests.get(section).abort();
        }

        // Create new AbortController for this request
        const controller = new AbortController();
        this.currentRequests.set(section, controller);

        try {
            this.showSpinner(section);

            // Add a small delay for better UX (prevents flashing on fast networks)
            await new Promise(resolve => setTimeout(resolve, this.loadingDelay));

            const response = await this.fetchSectionData(section, page, controller.signal);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            // Update the DOM
            const sectionContainer = document.getElementById(`${section}-content`);
            if (sectionContainer && data.html) {
                sectionContainer.innerHTML = data.html;
                
                // Update browser history
                if (updateHistory) {
                    this.updateHistory(section, page);
                }
                
                // Announce to screen readers
                this.announceUpdate(section, page);
            }

        } catch (error) {
            if (error.name === 'AbortError') {
                console.log(`Request for ${section} was cancelled`);
                return;
            }
            
            console.error(`Failed to load ${section} section:`, error);
            this.handleLoadError(section, error.message);
            
        } finally {
            this.hideSpinner(section);
            this.currentRequests.delete(section);
        }
    }

    /**
     * Fetch section data from server
     * @param {string} section - Section identifier
     * @param {number} page - Page number
     * @param {AbortSignal} signal - AbortController signal
     * @returns {Promise<Response>}
     */
    fetchSectionData(section, page, signal) {
        const url = new URL('/tasks/', window.location.origin);
        url.searchParams.set('section', section);
        url.searchParams.set(`${section}_page`, page.toString());

        return fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
            },
            signal,
        });
    }

    /**
     * Update browser history
     * @param {string} section - Section identifier  
     * @param {number} page - Page number
     */
    updateHistory(section, page) {
        const url = new URL(window.location);
        url.searchParams.set(`${section}_page`, page.toString());
        
        const state = { section, page };
        window.history.pushState(state, '', url);
    }

    /**
     * Announce updates to screen readers
     * @param {string} section - Section identifier
     * @param {number} page - Page number
     */
    announceUpdate(section, page) {
        const message = `${section} section updated to page ${page}`;
        
        // Create or update live region for announcements
        let liveRegion = document.getElementById('task-list-announcements');
        if (!liveRegion) {
            liveRegion = document.createElement('div');
            liveRegion.id = 'task-list-announcements';
            liveRegion.setAttribute('aria-live', 'polite');
            liveRegion.setAttribute('aria-atomic', 'true');
            liveRegion.style.position = 'absolute';
            liveRegion.style.left = '-10000px';
            liveRegion.style.width = '1px';
            liveRegion.style.height = '1px';
            liveRegion.style.overflow = 'hidden';
            document.body.appendChild(liveRegion);
        }
        
        liveRegion.textContent = message;
    }

    /**
     * Handle loading errors
     * @param {string} section - Section identifier
     * @param {string} errorMessage - Error message
     */
    handleLoadError(section, errorMessage) {
        const sectionContainer = document.getElementById(`tasks-${section}-section`);
        if (!sectionContainer) return;

        const errorHtml = `
            <div class="alert alert-danger" role="alert">
                <h4 class="alert-heading">Loading Error</h4>
                <p>Failed to load ${section} tasks: ${errorMessage}</p>
                <button type="button" class="btn btn-outline-danger btn-sm" 
                        onclick="taskListManager.retryLoad('${section}')">
                    Try Again
                </button>
            </div>
        `;
        
        const contentDiv = sectionContainer.querySelector(`#${section}-content`);
        if (contentDiv) {
            contentDiv.innerHTML = errorHtml;
        }
    }

    /**
     * Retry loading a section
     * @param {string} section - Section identifier
     */
    async retryLoad(section) {
        // Get current page from URL or default to 1
        const urlParams = new URLSearchParams(window.location.search);
        const page = urlParams.get(`${section}_page`) || 1;

        await this.loadSection(section, page, false);
    }

    /**
     * Setup global error handling
     */
    setupErrorHandling() {
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.taskListManager = new TaskListManager();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.taskListManager) {
        // Cancel any ongoing requests
        window.taskListManager.currentRequests.forEach(controller => {
            controller.abort();
        });
    }
});
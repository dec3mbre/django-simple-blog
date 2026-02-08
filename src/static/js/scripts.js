/**
 * Dev/Blog - Main Scripts
 * Handles mobile menu, article filtering, and profile tabs.
 */

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initArticleSearch();
    initProfileTabs();
    initShareButton();
    initSubscribeForm();
});

/**
 * Mobile Menu Toggle
 * Looks for #menu-toggle and #mobile-menu
 */
function initMobileMenu() {
    // Try to find the generic menu elements first
    let toggle = document.getElementById('menu-toggle');
    let menu = document.getElementById('mobile-menu');

    // Fallback for articles page if generic IDs aren't found (though we plan to standardize)
    if (!toggle) {
        toggle = document.getElementById('menu-toggle-articles');
        menu = document.getElementById('mobile-menu-articles');
    }

    if (!toggle || !menu) return;

    const openIcon = toggle.querySelector('.menu-open');
    const closeIcon = toggle.querySelector('.menu-close');

    toggle.addEventListener('click', () => {
        const isHidden = menu.classList.toggle('hidden');
        toggle.setAttribute('aria-expanded', !isHidden);

        // Update icons if they exist
        if (openIcon && closeIcon) {
            openIcon.classList.toggle('hidden', !isHidden);
            closeIcon.classList.toggle('hidden', isHidden);
        }
    });
}

/**
 * Article Search and Filtering
 * Handles search input and tag matching on articles.html
 */
function initArticleSearch() {
    const searchInput = document.getElementById('search-input');
    const tagFilters = document.querySelectorAll('.tag-filter');
    const articlesGrid = document.getElementById('articles-grid');
    const articles = document.querySelectorAll('.article-card');
    const resultsCount = document.getElementById('results-count');
    const emptyState = document.getElementById('empty-state');

    if (!searchInput || !articlesGrid) return;

    let activeTag = 'all';

    function filterArticles() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        let visibleCount = 0;

        articles.forEach(article => {
            const title = article.dataset.title ? article.dataset.title.toLowerCase() : '';
            const desc = article.dataset.desc ? article.dataset.desc.toLowerCase() : '';
            const tags = article.dataset.tags ? article.dataset.tags.split(',') : [];

            const matchesSearch = !searchTerm || title.includes(searchTerm) || desc.includes(searchTerm);
            const matchesTag = activeTag === 'all' || tags.includes(activeTag);

            if (matchesSearch && matchesTag) {
                article.classList.remove('hidden');
                visibleCount++;
            } else {
                article.classList.add('hidden');
            }
        });

        if (resultsCount) resultsCount.textContent = visibleCount;

        if (emptyState) emptyState.classList.toggle('hidden', visibleCount > 0);
        if (articlesGrid) articlesGrid.classList.toggle('hidden', visibleCount === 0);
    }

    searchInput.addEventListener('input', filterArticles);

    tagFilters.forEach(filter => {
        filter.addEventListener('click', () => {
            tagFilters.forEach(f => f.classList.remove('active'));
            filter.classList.add('active');
            activeTag = filter.dataset.tag;
            filterArticles();
        });
    });
}

/**
 * Profile Tabs
 * Handles tab switching on profile.html
 */
function initProfileTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');

    if (tabs.length === 0) return;

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetId = tab.dataset.tab;
            const targetContent = document.getElementById('tab-' + targetId);

            if (!targetContent) return;

            // Update tab styles
            tabs.forEach(t => {
                t.classList.remove('text-white', 'border-emerald-400');
                t.classList.add('text-white/50', 'border-transparent');
            });
            tab.classList.remove('text-white/50', 'border-transparent');
            tab.classList.add('text-white', 'border-emerald-400');

            // Show/hide content
            contents.forEach(c => c.classList.add('hidden'));
            targetContent.classList.remove('hidden');
        });
    });
}

/**
 * Share Button
 * Uses Web Share API or falls back to clipboard copy
 */
function initShareButton() {
    const btn = document.querySelector('[data-share]');
    if (!btn) return;

    btn.addEventListener('click', async () => {
        const originalText = btn.textContent;
        try {
            if (navigator.share) {
                await navigator.share({ title: document.title, url: location.href });
            } else {
                await navigator.clipboard.writeText(location.href);
                btn.textContent = 'Скопировано!';
                btn.classList.add('text-emerald-300');
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.classList.remove('text-emerald-300');
                }, 2000);
            }
        } catch (err) {
            // User cancelled share or clipboard failed
        }
    });
}

/**
 * Subscribe Form
 * Sends email to backend via fetch and provides visual feedback
 */
function initSubscribeForm() {
    const form = document.getElementById('subscribe-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = form.querySelector('button[type="submit"]');
        const emailInput = form.querySelector('input[name="email"]');
        const originalText = btn.textContent;
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]');

        btn.disabled = true;
        btn.textContent = 'Отправка...';

        try {
            const formData = new FormData();
            formData.append('email', emailInput.value);
            if (csrfToken) formData.append('csrfmiddlewaretoken', csrfToken.value);

            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();

            btn.textContent = data.ok ? 'Готово ✓' : data.error || 'Ошибка';
            btn.classList.add('border-emerald-400/50', 'text-emerald-200');

            setTimeout(() => {
                btn.textContent = originalText;
                btn.classList.remove('border-emerald-400/50', 'text-emerald-200');
                btn.disabled = false;
                if (data.ok) form.reset();
            }, 2500);
        } catch {
            btn.textContent = 'Ошибка сети';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.disabled = false;
            }, 2500);
        }
    });
}

/**
 * CodeSphere Theme Scripts
 * Vanilla JavaScript for Table of Contents spy, keyboard accessibility, and copy-code functionality.
 */
document.addEventListener('DOMContentLoaded', () => {
  // 1. Automatic Heading Anchor IDs & TOC Generation if TOC container exists
  const articleContent = document.querySelector('.entry-content');
  const tocList = document.querySelector('.toc-list');

  if (articleContent && tocList) {
    const headings = articleContent.querySelectorAll('h2, h3');
    if (headings.length > 0) {
      tocList.innerHTML = '';
      headings.forEach((heading, index) => {
        if (!heading.id) {
          heading.id = heading.textContent
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/(^-|-$)/g, '') || `section-${index + 1}`;
        }

        const li = document.createElement('li');
        li.className = heading.tagName.toLowerCase() === 'h3' ? 'toc-subitem' : 'toc-item';
        
        const a = document.createElement('a');
        a.href = `#${heading.id}`;
        a.textContent = heading.textContent;
        li.appendChild(a);
        tocList.appendChild(li);
      });
    } else {
      const tocWrapper = document.querySelector('.toc-sidebar');
      if (tocWrapper) {
        tocWrapper.style.display = 'none';
      }
    }
  }

  // 2. Active TOC Link Highlighting via IntersectionObserver
  const tocLinks = document.querySelectorAll('.toc-list a');
  if (tocLinks.length > 0 && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          tocLinks.forEach((link) => {
            if (link.getAttribute('href') === `#${id}`) {
              link.classList.add('active');
              link.style.fontWeight = '700';
              link.style.color = 'var(--accent-primary)';
            } else {
              link.classList.remove('active');
              link.style.fontWeight = 'normal';
              link.style.color = '';
            }
          });
        }
      });
    }, { rootMargin: '0px 0px -70% 0px' });

    document.querySelectorAll('.entry-content h2, .entry-content h3').forEach((heading) => {
      observer.observe(heading);
    });
  }

  // 3. Code Block Copy Button
  document.querySelectorAll('pre').forEach((pre) => {
    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-code-btn';
    copyBtn.innerText = 'Copy';
    copyBtn.setAttribute('aria-label', 'Copy code to clipboard');
    copyBtn.style.cssText = 'position:absolute;top:0.5rem;right:0.5rem;font-size:0.75rem;padding:0.25rem 0.5rem;background:var(--bg-tertiary);border:1px solid var(--border-color);border-radius:4px;cursor:pointer;color:var(--text-secondary);';
    pre.style.position = 'relative';
    pre.appendChild(copyBtn);

    copyBtn.addEventListener('click', () => {
      const code = pre.querySelector('code') ? pre.querySelector('code').innerText : pre.innerText;
      navigator.clipboard.writeText(code).then(() => {
        copyBtn.innerText = 'Copied!';
        setTimeout(() => { copyBtn.innerText = 'Copy'; }, 2000);
      });
    });
  });
});

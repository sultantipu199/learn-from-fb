// Facebook Video Learning Series Interactive App

let lessonsData = [];
let currentFilter = 'ALL';
let currentSearch = '';
let currentSort = 'asc';

// Load lessons
async function initApp() {
  try {
    let response = await fetch('lessons_data.json');
    if (!response.ok) {
      response = await fetch('../data/lessons_data.json');
    }
    if (response.ok) {
      lessonsData = await response.json();
    } else {
      throw new Error('Fetch failed');
    }
  } catch (e) {
    console.warn('Direct fetch failed, falling back to embedded dataset or localStorage', e);
    const saved = localStorage.getItem('fb_lessons_data');
    if (saved) {
      lessonsData = JSON.parse(saved);
    } else {
      // Fallback sample data will be loaded from generate_lessons output if needed
      lessonsData = defaultLessons;
    }
  }

  // Load custom added lessons from localStorage
  const extra = localStorage.getItem('fb_custom_lessons');
  if (extra) {
    try {
      const extraLessons = JSON.parse(extra);
      extraLessons.forEach(el => {
        if (!lessonsData.some(l => l.lesson_id === el.lesson_id)) {
          lessonsData.push(el);
        }
      });
    } catch(err) {
      console.error(err);
    }
  }

  setupEventListeners();
  renderApp();
}

function setupEventListeners() {
  // Search
  document.getElementById('search-input').addEventListener('input', (e) => {
    currentSearch = e.target.value.toLowerCase().trim();
    renderLessons();
  });

  // Filter Buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.dataset.level;
      renderLessons();
    });
  });

  // Sort
  document.getElementById('sort-select').addEventListener('change', (e) => {
    currentSort = e.target.value;
    renderLessons();
  });

  // Copy All for Google Docs
  document.getElementById('btn-copy-all').addEventListener('click', copyAllForGoogleDocs);

  // Download Markdown
  document.getElementById('btn-download-md').addEventListener('click', downloadMarkdownFile);

  // Modal handlers
  const modal = document.getElementById('add-modal');
  document.getElementById('btn-open-add-modal').addEventListener('click', () => {
    modal.classList.add('open');
  });
  document.getElementById('btn-close-modal').addEventListener('click', () => {
    modal.classList.remove('open');
  });
  document.getElementById('btn-cancel-modal').addEventListener('click', () => {
    modal.classList.remove('open');
  });

  // Mobile QR Code Modal handlers
  const mobileModal = document.getElementById('mobile-qr-modal');
  const openMobileModal = () => {
    if (mobileModal) mobileModal.classList.add('open');
  };
  const closeMobileModal = () => {
    if (mobileModal) mobileModal.classList.remove('open');
  };

  const btnOpenMobile = document.getElementById('btn-open-mobile-modal');
  if (btnOpenMobile) btnOpenMobile.addEventListener('click', openMobileModal);

  const btnCloseMobile = document.getElementById('btn-close-mobile-modal');
  if (btnCloseMobile) btnCloseMobile.addEventListener('click', closeMobileModal);

  const btnBannerQr = document.getElementById('btn-banner-qr');
  if (btnBannerQr) btnBannerQr.addEventListener('click', openMobileModal);

  // Close modals when clicking backdrop
  window.addEventListener('click', (e) => {
    if (e.target === modal) modal.classList.remove('open');
    if (e.target === mobileModal) mobileModal.classList.remove('open');
  });

  // Banner Copy Button
  const btnBannerCopy = document.getElementById('btn-banner-copy');
  if (btnBannerCopy) {
    btnBannerCopy.addEventListener('click', () => {
      const url = document.getElementById('banner-public-link').href;
      navigator.clipboard.writeText(url).then(() => {
        showToast('মোবাইল লিঙ্ক কপি করা হয়েছে! মেসেঞ্জারে পাঠিয়ে ফোনে ওপেন করুন।');
      }).catch(() => fallbackCopyText(url));
    });
  }

  // QR Modal Copy Buttons
  const btnCopyPub = document.getElementById('btn-copy-mobile-public');
  if (btnCopyPub) {
    btnCopyPub.addEventListener('click', () => {
      const input = document.getElementById('mobile-public-url-input');
      navigator.clipboard.writeText(input.value).then(() => {
        showToast('পাবলিক মোবাইল লিঙ্ক কপি করা হয়েছে!');
      }).catch(() => fallbackCopyText(input.value));
    });
  }

  const btnCopyLoc = document.getElementById('btn-copy-mobile-local');
  if (btnCopyLoc) {
    btnCopyLoc.addEventListener('click', () => {
      const input = document.getElementById('mobile-local-url-input');
      navigator.clipboard.writeText(input.value).then(() => {
        showToast('ওয়াইফাই লোকাল লিঙ্ক কপি করা হয়েছে!');
      }).catch(() => fallbackCopyText(input.value));
    });
  }

  // Mobile Bottom Navigation Bar Events
  const navTop = document.getElementById('nav-top');
  if (navTop) {
    navTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  const navSearch = document.getElementById('nav-search');
  if (navSearch) {
    navSearch.addEventListener('click', () => {
      const searchBox = document.getElementById('search-input');
      if (searchBox) {
        searchBox.focus();
        searchBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  }

  const navToc = document.getElementById('nav-toc');
  if (navToc) {
    navToc.addEventListener('click', () => {
      const details = document.querySelector('.toc-accordion details');
      if (details) {
        details.open = !details.open;
        details.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  const navCopy = document.getElementById('nav-copy');
  if (navCopy) {
    navCopy.addEventListener('click', copyAllForGoogleDocs);
  }

  const navMobileLink = document.getElementById('nav-mobile-link');
  if (navMobileLink) {
    navMobileLink.addEventListener('click', openMobileModal);
  }

  // Add Lesson Form
  document.getElementById('add-lesson-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const newLesson = {
      lesson_id: Date.now(),
      lesson_number: String(lessonsData.length + 1).padStart(2, '0'),
      title: document.getElementById('new-title').value,
      title_en: document.getElementById('new-title-en').value || 'New Facebook Lesson',
      video_url: document.getElementById('new-url').value || 'https://www.facebook.com/mdshouvikurrahman',
      original_post_url: 'https://www.facebook.com/share/14nc19UVKkk/',
      posted_date: new Date().toISOString().split('T')[0],
      duration: '20 মিনিট',
      views: 'New',
      engagement_level: 'HIGH',
      learning_level: document.getElementById('new-level').value,
      topic: 'New Added Topic',
      original_caption: 'নতুন সংযোজিত ফেসবুক ভিডিও লেসন',
      key_learning_points: document.getElementById('new-points').value.split(',').map(s => s.trim()).filter(Boolean),
      detailed_summary: document.getElementById('new-summary').value,
      key_takeaways: ['১. নিয়মিত অনুশীলন ও প্র্যাকটিক্যাল প্রয়োগ নিশ্চিত করুন।'],
      speaker_quotes: 'জ্ঞান অর্জনই যথেষ্ট নয়, প্রয়োগই আসল সাফল্য।',
      added_value_notes: 'নতুন ভিডিওটির নোটস ও বিস্তারিত টিপস সংরক্ষণ করা হয়েছে।',
      related_lessons: []
    };

    lessonsData.push(newLesson);
    
    // Save to localStorage
    const extra = JSON.parse(localStorage.getItem('fb_custom_lessons') || '[]');
    extra.push(newLesson);
    localStorage.setItem('fb_custom_lessons', JSON.stringify(extra));

    modal.classList.remove('open');
    document.getElementById('add-lesson-form').reset();
    showToast('নতুন লেসন সফলভাবে যুক্ত হয়েছে!');
    renderApp();
  });
}

function renderApp() {
  updateStats();
  renderTOC();
  renderLessons();
}

function updateStats() {
  document.getElementById('stat-total').innerText = lessonsData.length;
  
  // Calculate completed from localStorage
  const completedKeys = Object.keys(localStorage).filter(k => k.startsWith('lesson_done_') && localStorage.getItem(k) === 'true');
  document.getElementById('stat-completed').innerText = `${completedKeys.length} / ${lessonsData.length}`;
}

function renderTOC() {
  const tocContainer = document.getElementById('toc-container');
  tocContainer.innerHTML = '';

  lessonsData.forEach(l => {
    const a = document.createElement('a');
    a.href = `#lesson-${l.lesson_number}`;
    a.className = 'toc-item';
    a.innerHTML = `
      <span><strong>L-${l.lesson_number}:</strong> ${l.title}</span>
      <span class="toc-badge">${l.learning_level}</span>
    `;
    tocContainer.appendChild(a);
  });
}

function renderLessons() {
  const container = document.getElementById('lessons-list');
  container.innerHTML = '';

  let filtered = lessonsData.filter(l => {
    // Level filter
    if (currentFilter !== 'ALL' && l.learning_level !== currentFilter) {
      return false;
    }
    // Search filter
    if (currentSearch) {
      const haystack = (l.title + ' ' + l.title_en + ' ' + l.topic + ' ' + l.detailed_summary + ' ' + l.key_learning_points.join(' ')).toLowerCase();
      if (!haystack.includes(currentSearch)) {
        return false;
      }
    }
    return true;
  });

  // Sort
  filtered.sort((a, b) => {
    if (currentSort === 'asc') {
      return parseInt(a.lesson_number) - parseInt(b.lesson_number);
    } else {
      return parseInt(b.lesson_number) - parseInt(a.lesson_number);
    }
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--text-muted); background: var(--bg-card); border-radius: var(--radius-md);">
        <h3>কোনো লেসন পাওয়া যায়নি!</h3>
        <p>আপনার সার্চ টার্ম পরিবর্তন করে পুনরায় চেষ্টা করুন।</p>
      </div>
    `;
    return;
  }

  filtered.forEach(l => {
    const isCompleted = localStorage.getItem(`lesson_done_${l.lesson_id}`) === 'true';
    const savedNotes = localStorage.getItem(`lesson_notes_${l.lesson_id}`) || '';

    const card = document.createElement('article');
    card.className = `lesson-card ${isCompleted ? 'completed' : ''}`;
    card.id = `lesson-${l.lesson_number}`;

    const levelClass = l.learning_level.toLowerCase();

    card.innerHTML = `
      <div class="card-header">
        <div class="card-left">
          <span class="lesson-num-badge">LESSON ${l.lesson_number}</span>
          <h2 class="lesson-title">${l.title}</h2>
          <div class="lesson-subtitle">${l.title_en}</div>
        </div>
        <div class="card-actions-top">
          <button class="btn-status-toggle ${isCompleted ? 'is-done' : ''}" onclick="toggleLessonDone(${l.lesson_id})">
            ${isCompleted ? '✓ সম্পন্ন হয়েছে' : '○ সম্পন্ন হিসেবে চিহ্নিত করুন'}
          </button>
          <button class="btn-copy-card" onclick="copySingleLesson(${l.lesson_id})" title="এই লেসনটি কপি করুন">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            কপি
          </button>
        </div>
      </div>

      <!-- Metadata Chips -->
      <div class="meta-chips">
        <span class="meta-chip level-badge ${levelClass}">লেভেল: ${l.learning_level}</span>
        <span class="meta-chip">⏱️ ${l.duration}</span>
        <span class="meta-chip">📅 ${l.posted_date}</span>
        <span class="meta-chip">👁️ ${l.views} ভিউ</span>
        <span class="meta-chip">🎯 ${l.topic}</span>
        <a href="${l.video_url}" target="_blank" rel="noopener" class="meta-chip" style="color: #38bdf8; text-decoration: none;">
          🔗 ভিডিও দেখুন
        </a>
      </div>

      <!-- Caption -->
      <div class="caption-quote">
        "${l.original_caption}"
      </div>

      <!-- Key Learning Points -->
      <div class="card-section">
        <div class="section-heading">🎯 মূল শিক্ষণীয় বিষয়সমূহ:</div>
        <ul class="key-points-list">
          ${l.key_learning_points.map(pt => `<li>${pt}</li>`).join('')}
        </ul>
      </div>

      <!-- Detailed Summary -->
      <div class="card-section">
        <div class="section-heading">📚 বক্তার বিস্তারিত বক্তব্য ও সারসংক্ষেপ:</div>
        <div class="summary-text">${l.detailed_summary}</div>
      </div>

      <!-- Key Takeaways -->
      <div class="takeaways-box">
        <div class="section-heading" style="color: #38bdf8; margin-bottom: 6px;">💡 বাস্তব টেকওয়ে ও অ্যাকশন পয়েন্ট:</div>
        <ul>
          ${l.key_takeaways.map(tk => `<li>${tk}</li>`).join('')}
        </ul>
      </div>

      <!-- Quote -->
      <div class="quote-box">
        💬 <strong>বক্তার গোল্ডেন বাণী:</strong> "${l.speaker_quotes}"
      </div>

      <!-- Added Value Notes -->
      <div class="value-add-box">
        🚀 <strong>সংযুক্ত বিশেষজ্ঞ পরামর্শ ও গাইডলাইন:</strong> ${l.added_value_notes}
      </div>

      <!-- Notes Area -->
      <div class="user-notes-section">
        <label style="font-size: 0.85rem; color: var(--text-dim); display: block; margin-bottom: 5px;">
          📌 আপনার ব্যক্তিগত নোটস (স্বয়ংক্রিয়ভাবে সেভ হবে):
        </label>
        <textarea class="notes-textarea" placeholder="এই লেসনটি দেখার পর আপনার নিজস্ব পর্যবেক্ষণ এখানে লিখে রাখুন..." oninput="saveLessonNotes(${l.lesson_id}, this.value)">${savedNotes}</textarea>
      </div>
    `;

    container.appendChild(card);
  });
}

// Toggle lesson completed
window.toggleLessonDone = function(id) {
  const current = localStorage.getItem(`lesson_done_${id}`) === 'true';
  localStorage.setItem(`lesson_done_${id}`, (!current).toString());
  updateStats();
  renderLessons();
  showToast(!current ? 'লেসনটি সম্পন্ন হিসেবে চিহ্নিত হয়েছে!' : 'লেসনটি পুনরায় সক্রিয় করা হয়েছে।');
};

// Save user notes
window.saveLessonNotes = function(id, text) {
  localStorage.setItem(`lesson_notes_${id}`, text);
};

// Copy single lesson
window.copySingleLesson = function(id) {
  const l = lessonsData.find(x => x.lesson_id === id);
  if (!l) return;

  const text = `
───────────────────────────────────────────────────────────
LESSON ${l.lesson_number}: ${l.title}
Sub-Topic: ${l.title_en}
Level: ${l.learning_level} | Duration: ${l.duration} | Posted: ${l.posted_date}
Video URL: ${l.video_url}
Speaker: Tipu Sultan (ICT CARE)
───────────────────────────────────────────────────────────

🎯 KEY LEARNING POINTS:
${l.key_learning_points.map(p => `• ${p}`).join('\n')}

📚 DETAILED SUMMARY:
${l.detailed_summary}

💡 KEY TAKEAWAYS:
${l.key_takeaways.join('\n')}

💬 GOLDEN QUOTE:
"${l.speaker_quotes}"

🚀 ADDED VALUE & PRACTICAL TIPS:
${l.added_value_notes}
───────────────────────────────────────────────────────────
`;

  navigator.clipboard.writeText(text).then(() => {
    showToast(`Lesson ${l.lesson_number} কপি করা হয়েছে! Google Doc-এ পেস্ট করতে পারবেন।`);
  }).catch(() => {
    fallbackCopyText(text);
  });
};

// Copy all for Google Docs
function copyAllForGoogleDocs() {
  let doc = `═══════════════════════════════════════════════════════════\n`;
  doc += `📚 FACEBOOK VIDEO LEARNING SERIES : ENGR. TIPU SULTAN\n`;
  doc += `   অনলাইন উদ্যোক্তা ও এফ-কমার্স স্পেশাল মাস্টারক্লাস\n`;
  doc += `═══════════════════════════════════════════════════════════\n`;
  doc += `Total Lessons: ${lessonsData.length}\n`;
  doc += `Source URL: https://www.facebook.com/share/14nc19UVKkk/\n\n`;

  doc += `TABLE OF CONTENTS:\n`;
  lessonsData.forEach(l => {
    doc += `• Lesson ${l.lesson_number}: ${l.title} [${l.learning_level}]\n`;
  });
  doc += `\n═══════════════════════════════════════════════════════════\n\n`;

  lessonsData.forEach(l => {
    doc += `───────────────────────────────────────────────────────────\n`;
    doc += `LESSON ${l.lesson_number}: ${l.title}\n`;
    doc += `English Sub-Topic: ${l.title_en}\n`;
    doc += `───────────────────────────────────────────────────────────\n`;
    doc += `📺 Video URL: ${l.video_url}\n`;
    doc += `📅 Posted: ${l.posted_date} | Duration: ${l.duration} | Level: ${l.learning_level}\n\n`;
    doc += `📝 Caption: "${l.original_caption}"\n\n`;
    doc += `🎯 KEY LEARNING POINTS:\n`;
    l.key_learning_points.forEach(p => doc += `  • ${p}\n`);
    doc += `\n📚 DETAILED SUMMARY:\n${l.detailed_summary}\n\n`;
    doc += `💡 KEY TAKEAWAYS:\n`;
    l.key_takeaways.forEach(t => doc += `  ${t}\n`);
    doc += `\n💬 GOLDEN QUOTE: "${l.speaker_quotes}"\n`;
    doc += `🚀 ADDED VALUE: ${l.added_value_notes}\n\n`;
    doc += `📌 NOTES:\n[Personal Notes]\n`;
    doc += `───────────────────────────────────────────────────────────\n\n`;
  });

  navigator.clipboard.writeText(doc).then(() => {
    showToast('সম্পূর্ণ ২৭টি লেসন গুগল ডক ফরম্যাটে কপি হয়েছে!');
  }).catch(() => {
    fallbackCopyText(doc);
  });
}

function fallbackCopyText(text) {
  const ta = document.createElement('textarea');
  ta.value = text;
  document.body.appendChild(ta);
  ta.select();
  document.execCommand('copy');
  document.body.removeChild(ta);
  showToast('কপি করা হয়েছে!');
}

function downloadMarkdownFile() {
  let md = "# 📚 FACEBOOK VIDEO LEARNING SERIES : ENGR. TIPU SULTAN\n\n";
  lessonsData.forEach(l => {
    md += `## LESSON ${l.lesson_number}: ${l.title}\n`;
    md += `*${l.title_en}*\n\n`;
    md += `- **Video URL:** ${l.video_url}\n`;
    md += `- **Posted:** ${l.posted_date} | **Duration:** ${l.duration} | **Level:** ${l.learning_level}\n\n`;
    md += `### 🎯 মূল শিক্ষণীয় পয়েন্ট:\n`;
    l.key_learning_points.forEach(p => md += `- ${p}\n`);
    md += `\n### 📚 বিস্তারিত সারসংক্ষেপ:\n${l.detailed_summary}\n\n`;
    md += `### 💡 টেকওয়ে ও সিদ্ধান্ত:\n`;
    l.key_takeaways.forEach(t => md += `${t}\n`);
    md += `\n> *"${l.speaker_quotes}"*\n\n`;
    md += `**সংযুক্ত পরামর্শ:** ${l.added_value_notes}\n\n---\n\n`;
  });

  const blob = new Blob([md], { type: 'text/markdown;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'MASTER_FACEBOOK_LESSONS_GOOGLE_DOC.md';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast('Markdown ফাইল ডাউনলোড সম্পন্ন হয়েছে!');
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.innerText = msg;
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}

// Fallback embedded lessons dataset
const defaultLessons = [
  {
    lesson_id: 1,
    lesson_number: "01",
    title: "অনলাইন উদ্যোক্তা হিসেবে যাত্রার মানসিকতা ও বাস্তব প্রস্তুতি",
    title_en: "Online Entrepreneur Mindset & Real Preparation",
    video_url: "https://www.facebook.com/mdshouvikurrahman/videos/lesson01-entrepreneur-mindset",
    original_post_url: "https://www.facebook.com/share/14nc19UVKkk/",
    posted_date: "2026-01-10",
    duration: "18 মিনিট 45 সেকেন্ড",
    views: "48.5K",
    engagement_level: "HIGH",
    learning_level: "BEGINNER",
    topic: "Entrepreneurship Foundation & Mindset",
    original_caption: "একটি ফেসবুক পেইজ খুলেই পণ্য বিক্রি শুরু করলেই উদ্যোক্তা হওয়া যায় না। ব্যবসায় নামার আগে আপনার মানসিক প্রস্তুতি ও ব্যবসায়িক শৃঙ্খলা কেমন হওয়া উচিত?",
    key_learning_points: [
      "উদ্যোক্তা বনাম সাধারণ বিক্রেতার পার্থক্য অনুধাবন করা।",
      "প্রথম কয়েক মাসের অনিশ্চয়তা সামলানোর মানসিক স্থিতিস্থাপকতা (Mental Resilience) তৈরি।",
      "ব্যবসায়িক পুঁজিতে অপ্রয়োজনীয় অপচয় বন্ধ করে প্রাথমিক বাজেট পরিকল্পনা।"
    ],
    detailed_summary: "এই ভিডিওতে ইঞ্জিনিয়ার টিপু সুলতান অনলাইন উদ্যোক্তা হিসেবে আত্মপ্রকাশ করার প্রাথমিক মানসিক ভিত্তি নিয়ে অত্যন্ত গুরুত্বপূর্ণ দিকনির্দেশনা দিয়েছেন। তিনি আলোচনা করেন যে, বেশিরভাগ মানুষ হুজুগে ফেসবুক পেইজ খুলে পণ্য পোস্ট করা শুরু করে এবং বিক্রি না হলে হতাশ হয়ে ব্যবসা বন্ধ করে দেয়।",
    key_takeaways: [
      "১. ব্যক্তিগত ব্যাংক অ্যাকাউন্ট এবং ব্যবসার ক্যাশ কখনও একসাথে মেলাবেন না।",
      "২. প্রোডাক্ট নিয়ে অতিরিক্ত আবেগপ্রবণ না হয়ে কাস্টমারের মতামত ও বাজার চাহিদাকে সর্বোচ্চ অগ্রাধিকার দিন।"
    ],
    speaker_quotes: "পেইজ খোলা কোনো ব্যবসা নয়, পেইজের পেছনে একটি কার্যকর সিস্টেম দাঁড় করানোই আসল ব্যবসা।",
    added_value_notes: "অতিরিক্ত পরামর্শ: নতুন উদ্যোক্তাদের জন্য 'বুস্টট্র্যাপিং' (Bootstrapping) মেথডোলজি অত্যন্ত কার্যকর।",
    related_lessons: ["Lesson 02", "Lesson 03"]
  }
];

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', initApp);

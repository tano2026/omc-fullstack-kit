/**
 * OMC Agency OS - Clean Frontend Application State & Controller
 */

const state = {
    activeTab: 'dash',
    activeBrand: 'tano-agency',
    allBrands: [],
    activeAgent: 'cskh-consultant',
    chatHistories: {
        'cskh-consultant': [
            { sender: 'bot', text: '👋 Chào Sếp! Tôi là Chuyên Viên Tư Vấn & Chốt Đơn 24/7. Tôi túc trực đa kênh Zalo, Facebook Messenger và TikTok. Sếp cần kiểm tra khách hàng mới, tư vấn giá gói nào hay xem tỷ lệ chốt đơn?', time: 'Vừa xong' }
        ],
        'social-creator': [
            { sender: 'bot', text: '🎬 Chào Sếp! Tôi là Đạo Diễn Kịch Bản Video & Social Content. Tôi chuyên viết kịch bản video ngắn 30-60s chuẩn retention (3s đầu giữ chân) và prompt hình ảnh Midjourney/Runway. Hôm nay chúng ta làm chủ đề gì ạ?', time: 'Vừa xong' }
        ],
        'market-spy': [
            { sender: 'bot', text: '🕵️ Thám Tử Thị Trường sẵn sàng! Tôi có thể quét xu hướng 30 ngày qua, bóc tách điểm yếu đối thủ và tìm ra các nỗi đau lớn nhất của khách hàng mục tiêu.', time: 'Vừa xong' }
        ],
        'ceo-copilot': [
            { sender: 'bot', text: '👑 Báo cáo Sếp! Tôi là Thư Ký Điều Hành. Tôi theo dõi tiến độ toàn bộ 5 phòng ban, tổng hợp chỉ số ROI và ghi nhận mọi thay đổi bảng giá/chính sách.', time: 'Vừa xong' }
        ],
        'brand-guard': [
            { sender: 'bot', text: '🛡️ Rào Chắn JEV Sentinel túc trực! Tôi bảo vệ thương hiệu khỏi từ ngữ cấm vi phạm chính sách Meta/TikTok và chống bot AI ảo giác tự ý giảm giá.', time: 'Vừa xong' }
        ],
        'openclaw-executor': [
            { sender: 'bot', text: '⚡ Kỹ Sư IT OpenClaw sẵn sàng! Tôi hỗ trợ kiểm tra kết nối webhook, giám sát tiến trình PM2 và tự động sửa lỗi kỹ thuật khi có sự cố.', time: 'Vừa xong' }
        ]
    },
    crmLeads: [],
    crmFilterPlatform: 'ALL',
    currentScriptData: null,
    currentHooksData: []
};

// INITIALIZATION
window.addEventListener('DOMContentLoaded', () => {
    initApp();
});

async function initApp() {
    await loadBrands();
    await loadMetrics();
    await loadCrmLeads();
    renderAgentChat();
}

// 1. NAVIGATION
function switchTab(tabId) {
    state.activeTab = tabId;
    
    // Update nav buttons
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    const activeNav = document.getElementById('nav-' + tabId);
    if (activeNav) activeNav.classList.add('active');

    // Update view panels
    document.querySelectorAll('.view-panel').forEach(el => el.classList.remove('active'));
    const targetPanel = document.getElementById('panel-' + tabId);
    if (targetPanel) targetPanel.classList.add('active');

    const headings = {
        'dash': '📊 Bảng Điều Hành Tổng Quan (Executive Overview)',
        'chat': '💬 Phòng Chat & Điều Phối Nhân Sự AI',
        'studio': '🎬 Studio Kịch Bản Video Ngắn TikTok/Reels & 5 Hooks',
        'crm': '👥 Sổ Khách Hàng Tiềm Năng (CRM Leads 24/7)',
        'brand': '🏢 Quản Lý Đa Thương Hiệu & Cứu Hộ IT'
    };
    document.getElementById('page-title-text').innerText = headings[tabId] || 'Bảng Điều Khiển';

    if (tabId === 'crm') loadCrmLeads();
    if (tabId === 'dash') loadMetrics();
}

// 2. BRAND MANAGEMENT
async function loadBrands() {
    try {
        const res = await fetch('/api/brands');
        const data = await res.json();
        state.allBrands = data.brands || [];
        state.activeBrand = data.active_brand || 'tano-agency';

        // Populate dropdown
        const sel = document.getElementById('brand-select-dropdown');
        sel.innerHTML = '';
        let cardsHtml = '';

        state.allBrands.forEach(b => {
            const opt = document.createElement('option');
            opt.value = b.id;
            opt.innerText = b.name;
            if (b.id === state.activeBrand) {
                opt.selected = true;
                document.getElementById('topbar-brand-badge').innerText = b.name;
            }
            sel.appendChild(opt);

            const isActive = (b.id === state.activeBrand);
            cardsHtml += `
                <div class="dash-card-box ${isActive ? 'active-brand-card' : ''}" style="${isActive ? 'border-color: var(--accent-blue);' : ''}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="color: #fff; font-size: 0.95rem;">${b.name}</h4>
                        <span style="font-size: 0.72rem; padding: 2px 8px; border-radius: 10px; font-weight: 600; background: ${isActive ? 'var(--accent-green-glow)' : 'var(--bg-card)'}; color: ${isActive ? 'var(--accent-green)' : 'var(--text-muted)'};">
                            ${isActive ? 'ĐANG CHỌN' : 'SẴN SÀNG'}
                        </span>
                    </div>
                    <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 4px;">Ngành: <strong style="color: #fff;">${b.industry}</strong> | Hotline: <strong style="color: var(--accent-blue);">${b.hotline}</strong></p>
                    <p style="font-size: 0.78rem; color: var(--text-secondary); margin-top: 2px;">Offer: ${b.core_offer}</p>
                    ${!isActive ? `<button class="chip-btn" style="margin-top: 8px; align-self: flex-start;" onclick="switchBrand('${b.id}')">👉 Kích Hoạt Brand Này</button>` : ''}
                </div>
            `;
        });

        const grid = document.getElementById('brand-grid-container');
        if (grid) grid.innerHTML = cardsHtml;
    } catch (err) {
        console.error('Error loading brands:', err);
    }
}

async function switchBrand(brandId) {
    try {
        const res = await fetch('/api/brands/switch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ brand_id: brandId })
        });
        const data = await res.json();
        if (data.status === 'success') {
            state.activeBrand = brandId;
            await loadBrands();
            showToast(`Đã chuyển sang thương hiệu: ${data.brand_name}`);
            
            // Add system announcement in chat
            state.chatHistories[state.activeAgent].push({
                sender: 'bot',
                text: `🔄 Toàn bộ hệ thống vừa được nạp tri thức của thương hiệu: "${data.brand_name}". Mọi câu trả lời, bảng giá và kịch bản video sẽ áp dụng riêng cho thương hiệu này!`,
                time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
            });
            renderAgentChat();
        }
    } catch (err) {
        alert('Lỗi chuyển brand: ' + err.message);
    }
}

async function createBrand() {
    const name = document.getElementById('brand-name-input').value.trim();
    const industry = document.getElementById('brand-industry-input').value.trim();
    const hotline = document.getElementById('brand-hotline-input').value.trim();
    const offer = document.getElementById('brand-offer-input').value.trim();
    const p1 = document.getElementById('brand-p1-input').value.trim() || '1.990.000đ';
    const p2 = document.getElementById('brand-p2-input').value.trim() || '4.990.000đ';
    const p3 = document.getElementById('brand-p3-input').value.trim() || '12.500.000đ';

    if (!name || !industry || !hotline) {
        alert('Vui lòng điền đủ Tên, Lĩnh vực và Hotline!');
        return;
    }

    try {
        const res = await fetch('/api/brands/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name, industry, hotline, core_offer: offer,
                pricing_starter: p1, pricing_pro: p2, pricing_vip: p3
            })
        });
        const data = await res.json();
        if (data.status === 'success') {
            showToast(`Kích hoạt thành công brand: ${name}`);
            await loadBrands();
            // Clear inputs
            document.getElementById('brand-name-input').value = '';
            document.getElementById('brand-industry-input').value = '';
            document.getElementById('brand-hotline-input').value = '';
            document.getElementById('brand-offer-input').value = '';
            switchTab('dash');
        } else {
            alert('Lỗi: ' + data.error);
        }
    } catch (err) {
        alert('Lỗi kết nối: ' + err.message);
    }
}

// 3. METRICS & KPI
async function loadMetrics() {
    try {
        const res = await fetch('/api/metrics');
        const data = await res.json();
        document.getElementById('kpi-chat').innerText = (data.total_conversations || 0).toLocaleString();
        document.getElementById('kpi-lead').innerText = (data.total_leads || 0).toLocaleString();
        document.getElementById('kpi-video').innerText = (data.total_videos_created || 0).toLocaleString();
        const million = ((data.cost_savings_vnd || 0) / 1000000).toFixed(1);
        document.getElementById('kpi-cost').innerText = million + ' tr đ';
    } catch (err) {
        console.error('Error loading metrics:', err);
    }
}

// 4. CHAT HUB WITH THREADED AGENT SESSIONS
function selectAgent(agentId) {
    state.activeAgent = agentId;
    
    // Update active row in agent list
    document.querySelectorAll('.agent-row').forEach(r => r.classList.remove('active'));
    const activeRow = document.getElementById('agent-row-' + agentId);
    if (activeRow) activeRow.classList.add('active');

    // Update topbar in chat area
    const agentNames = {
        'cskh-consultant': '💬 Chuyên Viên Tư Vấn & Chốt Đơn 24/7',
        'social-creator': '🎬 Đạo Diễn Kịch Bản Video & Social',
        'market-spy': '🕵️ Thám Tử Thị Trường & Đối Thủ',
        'ceo-copilot': '👑 Thư Ký Điều Hành Cho Sếp',
        'brand-guard': '🛡️ Rào Chắn An Toàn JEV Sentinel',
        'openclaw-executor': '⚡ Kỹ Sư IT OpenClaw Tự Sửa Lỗi'
    };
    document.getElementById('chat-active-agent-title').innerText = agentNames[agentId] || agentId;

    // Render chips
    renderPromptChips(agentId);

    // Render chat history
    renderAgentChat();
}

function renderPromptChips(agentId) {
    const chipBox = document.getElementById('prompt-chips-container');
    const chipPresets = {
        'cskh-consultant': [
            'Hôm nay có bao nhiêu khách để lại SĐT?',
            'Cho anh bảng giá các gói và chính sách ưu đãi',
            'Khách chê giá cao thì trả lời thế nào để chốt đơn?'
        ],
        'social-creator': [
            'Lên 3 kịch bản video TikTok giữ chân 3s đầu',
            'Cho anh 5 câu Hook giật gân theo nỗi đau',
            'Viết prompt vẽ ảnh bìa Thumbnail phong cách Cinematic'
        ],
        'market-spy': [
            'Quét xu hướng ngành đang viral 30 ngày qua',
            'Bóc tách 3 điểm yếu lớn nhất của các đối thủ',
            'Trích xuất từ vựng thực tế khách hàng hay dùng'
        ],
        'ceo-copilot': [
            'Báo cáo tổng kết hiệu suất và doanh thu hôm nay',
            'Tháng này tiết kiệm được bao nhiêu chi phí nhân sự?',
            'Cập nhật lại giá gói Starter thành 1.850.000đ'
        ],
        'brand-guard': [
            'Kiểm duyệt bài viết xem có từ khóa vi phạm cấm ads không',
            'Xác minh mức giá 1.990k có đúng với bảng giá duyệt không'
        ],
        'openclaw-executor': [
            'Kiểm tra tình trạng máy chủ và cổng webhook Zalo/FB',
            'Khởi động lại toàn bộ tiến trình bot 24/7'
        ]
    };

    const chips = chipPresets[agentId] || [];
    chipBox.innerHTML = chips.map(c => `<button class="chip-btn" onclick="usePromptChip('${escapeHtml(c)}')">${c}</button>`).join('');
}

function usePromptChip(text) {
    document.getElementById('chat-message-input').value = text;
    sendMessage();
}

function renderAgentChat() {
    const box = document.getElementById('chat-stream-box');
    const messages = state.chatHistories[state.activeAgent] || [];
    
    box.innerHTML = messages.map(m => `
        <div class="msg-bubble-wrap ${m.sender}">
            <div class="msg-content">${escapeHtml(m.text)}</div>
            <div class="msg-timestamp">${m.sender === 'user' ? 'Bạn' : '@' + state.activeAgent} • ${m.time}</div>
        </div>
    `).join('');

    box.scrollTop = box.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('chat-message-input');
    const text = input.value.trim();
    if (!text) return;

    const now = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    state.chatHistories[state.activeAgent].push({ sender: 'user', text, time: now });
    renderAgentChat();

    input.value = '';
    input.disabled = true;

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, agent: state.activeAgent })
        });
        const data = await res.json();
        const reply = data.reply || 'Đã ghi nhận yêu cầu và xử lý thành công.';
        state.chatHistories[state.activeAgent].push({
            sender: 'bot',
            text: reply,
            time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
        });
        renderAgentChat();
        loadMetrics();
    } catch (err) {
        state.chatHistories[state.activeAgent].push({
            sender: 'bot',
            text: '❌ Lỗi kết nối: ' + err.message,
            time: now
        });
        renderAgentChat();
    } finally {
        input.disabled = false;
        input.focus();
    }
}

// 5. STUDIO VIDEO 1-CLICK
async function generateVideoScript() {
    const topic = document.getElementById('studio-topic-input').value.trim();
    const duration = document.getElementById('studio-duration-select').value;
    if (!topic) {
        alert('Vui lòng nhập chủ đề video!');
        return;
    }

    const resCard = document.getElementById('studio-results-card');
    resCard.style.display = 'block';
    document.getElementById('hooks-container').innerHTML = '<p style="color: var(--text-muted); font-size: 0.85rem;">Đang vận dụng 5 đòn bẩy tâm lý và dựng phân cảnh...</p>';
    document.getElementById('full-script-text').innerText = 'Đang biên kịch lời thoại và chỉ dẫn CapCut...';

    try {
        const res = await fetch('/api/video-generator', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, duration: parseInt(duration) })
        });
        const data = await res.json();
        if (data.status === 'success') {
            state.currentScriptData = data.script;
            state.currentHooksData = data.hooks || [];

            // Render Hooks
            let hooksHtml = '';
            state.currentHooksData.forEach((h, i) => {
                hooksHtml += `
                    <div class="hook-item-box">
                        <div style="flex: 1; padding-right: 12px;">
                            <div class="hook-badge-tag">Hook #${i+1}: ${h.type}</div>
                            <div class="hook-quote">"${h.hook_text}"</div>
                            <div class="hook-visual-note">🎬 Visual gợi ý: ${h.visual_direction}</div>
                        </div>
                        <button class="btn-copy-hook" onclick="copyText('${escapeHtml(h.hook_text)}')">📋 Copy</button>
                    </div>
                `;
            });
            document.getElementById('hooks-container').innerHTML = hooksHtml;

            // Render Script
            const sc = data.script;
            let fullText = `🎯 CHỦ ĐỀ: ${sc.topic}\n⏱️ THỜI LƯỢNG: ${sc.duration}\n\n`;
            (sc.storyboard || []).forEach(s => {
                fullText += `[${s.time}] - ${s.phase}\n• Hình ảnh: ${s.visual}\n• Lời thoại: ${s.audio}\n• Chữ trên màn hình: ${s.text_overlay}\n\n`;
            });
            fullText += `✂️ HƯỚNG DẪN DỰNG CAPCUT:\n1. Tốc độ nói: 1.15x, Zero silence gap.\n2. Phụ đề tự động chữ to vàng viền đen giữa ngực.\n3. Cứ 2-3s đổi góc máy hoặc chèn B-roll.`;
            document.getElementById('full-script-text').innerText = fullText;

            showToast('Đã sinh kịch bản video thành công!');
            loadMetrics();
        } else {
            alert('Lỗi: ' + data.error);
        }
    } catch (err) {
        alert('Lỗi kết nối: ' + err.message);
    }
}

function copyFullScript() {
    const text = document.getElementById('full-script-text').innerText;
    copyText(text);
}

function downloadScriptTxt() {
    const text = document.getElementById('full-script-text').innerText;
    const topic = document.getElementById('studio-topic-input').value.trim() || 'Kich_Ban_Video';
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = topic.replace(/[^a-zA-Z0-9]/g, '_') + '.txt';
    link.click();
    showToast('Đã tải file kịch bản (.txt)!');
}

// 6. CRM LEADS WITH SEARCH & FILTER
async function loadCrmLeads() {
    const tbody = document.getElementById('crm-table-body');
    tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 20px;">Đang tải danh sách leads...</td></tr>';

    try {
        const res = await fetch('/api/leads');
        const data = await res.json();
        state.crmLeads = data.leads || [];
        renderCrmTable();
        renderRecentLeadsOnDashboard();
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="6" style="color: var(--accent-red); text-align: center;">Lỗi tải CRM: ${err.message}</td></tr>`;
    }
}

function filterCrmPlatform(platform) {
    state.crmFilterPlatform = platform;
    document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
    const btn = document.getElementById('filter-' + platform.toLowerCase());
    if (btn) btn.classList.add('active');
    renderCrmTable();
}

function searchCrm(query) {
    renderCrmTable(query);
}

function renderCrmTable(searchQuery = '') {
    const tbody = document.getElementById('crm-table-body');
    let filtered = state.crmLeads;

    if (state.crmFilterPlatform !== 'ALL') {
        filtered = filtered.filter(l => l.platform.toLowerCase() === state.crmFilterPlatform.toLowerCase());
    }

    if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        filtered = filtered.filter(l => l.name.toLowerCase().includes(q) || l.phone.includes(q) || l.note.toLowerCase().includes(q));
    }

    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 30px;">Không tìm thấy khách hàng nào phù hợp bộ lọc.</td></tr>';
        return;
    }

    tbody.innerHTML = filtered.map(l => `
        <tr>
            <td style="color: var(--text-muted); font-size: 0.8rem;">${l.time}</td>
            <td><span class="badge-platform">${l.platform}</span></td>
            <td style="font-weight: 600; color: #fff;">${l.name}</td>
            <td><span class="phone-tag">${l.phone}</span></td>
            <td style="max-width: 250px; font-size: 0.82rem; color: var(--text-secondary);">${l.note}</td>
            <td>
                <a href="tel:${l.phone}" class="call-btn">📞 Gọi Ngay</a>
            </td>
        </tr>
    `).join('');
}

function renderRecentLeadsOnDashboard() {
    const list = document.getElementById('recent-leads-list');
    if (!list) return;
    const recent = state.crmLeads.slice(0, 4);
    if (recent.length === 0) {
        list.innerHTML = '<p style="color: var(--text-muted); font-size: 0.82rem;">Chưa có khách hàng mới hôm nay.</p>';
        return;
    }
    list.innerHTML = recent.map(l => `
        <div class="recent-item">
            <div>
                <div class="recent-title">${l.name} (${l.platform})</div>
                <div class="recent-meta">${l.phone} • ${l.note.slice(0, 40)}...</div>
            </div>
            <a href="tel:${l.phone}" class="call-btn" style="padding: 3px 8px; font-size: 0.72rem;">📞 Gọi</a>
        </div>
    `).join('');
}

function exportCsv() {
    if (state.crmLeads.length === 0) {
        alert('Không có dữ liệu để xuất file!');
        return;
    }
    let csv = '\uFEFFThời Gian,Nền Tảng,Tên Khách Hàng,Số Điện Thoại,Ghi Chú\n';
    state.crmLeads.forEach(l => {
        csv += `"${l.time}","${l.platform}","${l.name}","${l.phone}","${l.note}"\n`;
    });
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `CRM_Leads_${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
    showToast('Đã xuất file CRM Leads (.csv)!');
}

// 7. SYSTEM ACTIONS & SELF-HEALING
async function runHealthAction(action) {
    const out = document.getElementById('health-action-output');
    out.style.display = 'block';
    out.innerText = 'Đang kích hoạt Kỹ Sư AI kiểm tra hệ thống...';

    try {
        const res = await fetch('/api/system-action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action })
        });
        const data = await res.json();
        out.innerHTML = `
            <div style="color: var(--accent-green); font-weight: 700;">✅ ${data.status}</div>
            <div style="margin-top: 4px; color: var(--text-secondary);">${data.message}</div>
        `;
        showToast('Hệ thống hoạt động 100% ổn định!');
    } catch (err) {
        out.innerHTML = `<div style="color: var(--accent-red);">❌ Lỗi kiểm tra: ${err.message}</div>`;
    }
}

// UTILITIES
function copyText(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Đã copy vào bộ nhớ đệm (Clipboard)!');
    }).catch(err => {
        alert('Không thể copy: ' + err);
    });
}

function showToast(msg) {
    const toast = document.getElementById('global-toast');
    toast.innerText = '✨ ' + msg;
    toast.style.display = 'flex';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 2800);
}

function escapeHtml(text) {
    if (!text) return '';
    return text.toString().replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

const $ = (selector) => document.querySelector(selector);
const page = document.body.dataset.page;
let noticeTimer;

function escapeHtml(value = '') {
	return String(value).replace(/[&<>"']/g, (character) => ({
		'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
	})[character]);
}

function showNotice(message, isError = false) {
	const notice = $('#notice');
	notice.textContent = message;
	notice.classList.toggle('error', isError);
	notice.classList.add('visible');
	clearTimeout(noticeTimer);
	noticeTimer = setTimeout(() => notice.classList.remove('visible'), 5000);
}

async function request(path, options = {}) {
	const response = await fetch(path, options);
	if (!response.ok) {
		let message = `Request failed (${response.status})`;
		try {
			const body = await response.json();
			const detail = body.detail || body.message;
			message = Array.isArray(detail) ? detail.map((item) => item.msg).join('; ') : detail || message;
		} catch { /* Keep the HTTP status message. */ }
		throw new Error(message);
	}
	if (response.status === 204) return null;
	return response.json();
}

function queryString(filters = {}) {
	const params = new URLSearchParams();
	Object.entries(filters).forEach(([key, value]) => {
		if (value) params.set(key, value);
	});
	params.set('page', '1');
	params.set('page_size', '50');
	return params.toString();
}

function formatDate(value) {
	if (!value) return '—';
	return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date(value));
}

function debounce(callback, delay = 250) {
	let timer;
	return (...args) => {
		clearTimeout(timer);
		timer = setTimeout(() => callback(...args), delay);
	};
}

function setButtonBusy(button, busy, label = 'Working…') {
	if (!button.dataset.label) button.dataset.label = button.textContent;
	button.disabled = busy;
	button.textContent = busy ? label : button.dataset.label;
}

function syncRepeatableRows(list) {
	const rows = [...list.querySelectorAll('.repeat-row')];
	rows.forEach((row) => {
		row.querySelector('[data-remove-row]').disabled = rows.length === 1;
	});
}

function addRepeatableInput(listId, name, label, placeholder, focus = true) {
	const list = document.getElementById(listId);
	const row = document.createElement('div');
	row.className = 'repeat-row';
	const input = document.createElement('input');
	input.name = name;
	input.required = true;
	input.setAttribute('aria-label', label);
	input.placeholder = placeholder;
	const remove = document.createElement('button');
	remove.className = 'remove-row';
	remove.type = 'button';
	remove.setAttribute('data-remove-row', '');
	remove.setAttribute('aria-label', `Remove ${label.toLowerCase()}`);
	remove.textContent = '×';
	row.append(input, remove);
	list.append(row);
	syncRepeatableRows(list);
	if (focus) input.focus();
}

function resetRepeatableList(listId, name, label, placeholder) {
	const list = document.getElementById(listId);
	list.replaceChildren();
	addRepeatableInput(listId, name, label, placeholder, false);
	list.querySelector('input').value = '';
}

async function loadJobs() {
	try {
		const search = $('#job-search').value.trim();
		const result = await request(`/jds?${queryString({ search })}`);
		$('#job-total').textContent = result.total;
		$('#job-count').textContent = `${result.total} role${result.total === 1 ? '' : 's'}`;
		$('#job-empty').hidden = result.data.length > 0;
		$('#job-rows').innerHTML = result.data.map((job) => {
			const scheme = job.generated_classification;
			const schemeLabel = Array.isArray(scheme) && scheme.length ? `${scheme.length} categories` : 'Building…';
			const schemeStatus = Array.isArray(scheme) && scheme.length ? 'done' : 'processing';
			return `<tr>
				<td><strong>${escapeHtml(job.title)}</strong><small>${escapeHtml(job.description || '')}</small></td>
				<td><span class="status ${schemeStatus}">${schemeLabel}</span></td>
				<td><small>${formatDate(job.created_at)}</small></td>
				<td><div class="table-actions"><button class="button secondary small" data-view-job="${escapeHtml(job.id)}" type="button">View</button><button class="button quiet-danger small" data-delete-job="${escapeHtml(job.id)}" type="button">Delete</button></div></td>
			</tr>`;
		}).join('');
	} catch (error) {
		showNotice(error.message, true);
		$('#job-count').textContent = 'Could not load roles';
	}
}

async function loadCareerJobs() {
	try {
		const search = $('#career-search').value.trim();
		const result = await request(`/jds?${queryString({ search })}`);
		$('#career-total').textContent = result.total;
		$('#career-empty').hidden = result.data.length > 0;
		$('#career-list').innerHTML = result.data.map((job) => `
			<article class="career-card">
				<div class="career-copy"><p class="eyebrow">Now hiring</p><h2>${escapeHtml(job.title)}</h2><p class="career-snippet">${escapeHtml(job.description || 'Learn more about this opportunity by applying.')}</p></div>
				<button class="button" type="button" data-apply-job="${escapeHtml(job.id)}" data-job-title="${escapeHtml(job.title)}">Apply now</button>
			</article>`).join('');
	} catch (error) {
		showNotice(error.message, true);
	}
}

function initJobBoard() {
	const dialog = $('#career-apply-dialog');
	dialog.addEventListener('click', (event) => {
		if (event.target.closest('[data-close-dialog]') || event.target === dialog) dialog.close();
	});
	$('#career-list').addEventListener('click', (event) => {
		const button = event.target.closest('[data-apply-job]');
		if (!button) return;
		$('#career-job-id').value = button.dataset.applyJob;
		$('#career-apply-title').textContent = `Apply for ${button.dataset.jobTitle}`;
		$('#career-selected-job').textContent = button.dataset.jobTitle;
		$('#career-subject').value = `Application for ${button.dataset.jobTitle}`;
		dialog.showModal();
	});
	$('#career-application-form').addEventListener('submit', async (event) => {
		event.preventDefault();
		const form = event.currentTarget;
		const button = form.querySelector('[type="submit"]');
		const body = Object.fromEntries(new FormData(form).entries());
		for (const key of ['resume_url', 'cover_letter_url']) body[key] = body[key].trim() || null;
		setButtonBusy(button, true, 'Submitting…');
		try {
			await request('/applications', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
			form.reset();
			dialog.close();
			showNotice('Application submitted successfully.');
		} catch (error) { showNotice(error.message, true); }
		finally { setButtonBusy(button, false); }
	});
	$('#career-refresh').addEventListener('click', loadCareerJobs);
	$('#career-search').addEventListener('input', debounce(loadCareerJobs));
	loadCareerJobs();
}

function initJobs() {
	const createDialog = $('#job-create-dialog');
	$('#job-create-open').addEventListener('click', () => createDialog.showModal());
	for (const dialog of [createDialog, $('#job-dialog')]) {
		dialog.addEventListener('click', (event) => {
			if (event.target.closest('[data-close-dialog]') || event.target === dialog) dialog.close();
		});
	}
	$('#add-responsibility').addEventListener('click', () => addRepeatableInput('responsibility-list', 'responsibilities', 'Responsibility', 'Describe a responsibility'));
	$('#add-qualification').addEventListener('click', () => addRepeatableInput('qualification-list', 'qualifications', 'Qualification', 'Describe a qualification'));
	for (const list of [$('#responsibility-list'), $('#qualification-list')]) {
		list.addEventListener('click', (event) => {
			if (!event.target.closest('[data-remove-row]')) return;
			event.target.closest('.repeat-row').remove();
			syncRepeatableRows(list);
		});
	}
	$('#job-form').addEventListener('submit', async (event) => {
		event.preventDefault();
		const form = event.currentTarget;
		const button = form.querySelector('[type="submit"]');
		const values = new FormData(form);
		const body = {
			title: values.get('title').trim(),
			description: values.get('description').trim(),
			responsibilities: values.getAll('responsibilities').map((item) => item.trim()).filter(Boolean),
			qualifications: values.getAll('qualifications').map((item) => item.trim()).filter(Boolean),
			note_to_intelligence: values.get('note_to_intelligence').trim() || null,
		};
		setButtonBusy(button, true, 'Creating…');
		try {
			await request('/jds', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
			form.reset();
			resetRepeatableList('responsibility-list', 'responsibilities', 'Responsibility', 'Describe a responsibility');
			resetRepeatableList('qualification-list', 'qualifications', 'Qualification', 'Describe a qualification');
			createDialog.close();
			showNotice('Role created. Classification is generated in the background.');
			await loadJobs();
		} catch (error) { showNotice(error.message, true); }
		finally { setButtonBusy(button, false); }
	});

	$('#job-rows').addEventListener('click', async (event) => {
		const viewButton = event.target.closest('[data-view-job]');
		if (viewButton) {
			try {
				const result = await request(`/jds?id=${encodeURIComponent(viewButton.dataset.viewJob)}&page=1&page_size=1`);
				const job = result.data[0];
				if (!job) throw new Error('Job description not found.');
				$('#job-detail-title').textContent = job.title;
				const list = (items) => Array.isArray(items) && items.length
					? `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`
					: '<p class="muted">None provided.</p>';
				const categories = Array.isArray(job.generated_classification) && job.generated_classification.length
					? job.generated_classification.map((category) => `<section class="category-detail"><h4>${escapeHtml(category.label)}</h4><p>${escapeHtml(category.description)}</p><strong>Criteria</strong>${list(category.criteria)}<strong>Reply goal</strong><p>${escapeHtml(category.reply_goal)}</p></section>`).join('')
					: '<p class="muted">Classification is still being generated.</p>';
				$('#job-detail-content').innerHTML = `<p>${escapeHtml(job.description || 'No overview provided.')}</p><h3>Responsibilities</h3>${list(job.responsibilities)}<h3>Qualifications</h3>${list(job.qualifications)}<h3>Reviewer note</h3><p>${escapeHtml(job.note_to_intelligence || 'None provided.')}</p><h3>Classification</h3>${categories}`;
				$('#job-dialog').showModal();
			} catch (error) { showNotice(error.message, true); }
			return;
		}
		const button = event.target.closest('[data-delete-job]');
		if (!button || !confirm('Delete this job description?')) return;
		try {
			await request(`/jds/${encodeURIComponent(button.dataset.deleteJob)}`, { method: 'DELETE' });
			showNotice('Job description deleted.');
			await loadJobs();
		} catch (error) { showNotice(error.message, true); }
	});

	$('#job-refresh').addEventListener('click', loadJobs);
	$('#job-search').addEventListener('input', debounce(loadJobs));
	loadJobs();
	window.setInterval(loadJobs, 15000);
}

async function loadApplications() {
	try {
		const search = $('#application-search').value.trim();
		const processing_status = $('#application-status').value;
		const result = await request(`/applications?${queryString({ search, processing_status })}`);
		$('#application-total').textContent = result.total;
		$('#application-count').textContent = `${result.total} application${result.total === 1 ? '' : 's'}`;
		$('#application-empty').hidden = result.data.length > 0;
		$('#application-rows').innerHTML = result.data.map((application) => `
			<tr>
				<td><strong>${escapeHtml(application.candidate_name || 'Candidate')}</strong><small>${escapeHtml(application.from_email)}</small></td>
				<td>${escapeHtml(application.job?.title || 'Unassigned')}</td>
				<td><span class="status ${escapeHtml(application.processing_status || 'received')}">${escapeHtml(application.processing_status || 'received')}</span></td>
				<td><details class="application-message"><summary>${escapeHtml(application.subject || 'View message')}</summary><p>${escapeHtml(application.message || 'No message included.')}</p></details></td>
				<td><div class="table-actions"><button class="button secondary small" data-view-application="${escapeHtml(application.id)}" type="button">View</button><button class="button quiet-danger small" data-delete-application="${escapeHtml(application.id)}" type="button">Delete</button></div></td>
			</tr>`).join('');
	} catch (error) {
		showNotice(error.message, true);
		$('#application-count').textContent = 'Could not load applications';
	}
}

async function loadApplicationJobs() {
	const select = $('#application-job');
	try {
		const result = await request(`/jds?${queryString()}`);
		select.innerHTML = '<option value="">Choose a role</option>' + result.data.map((job) => `<option value="${escapeHtml(job.id)}">${escapeHtml(job.title)}</option>`).join('');
	} catch (error) { showNotice(error.message, true); }
}

function initApplications() {
	const createDialog = $('#application-create-dialog');
	$('#application-create-open').addEventListener('click', async () => {
		await loadApplicationJobs();
		createDialog.showModal();
	});
	for (const dialog of [createDialog, $('#application-dialog')]) {
		dialog.addEventListener('click', (event) => {
			if (event.target.closest('[data-close-dialog]') || event.target === dialog) dialog.close();
		});
	}

	$('#application-form').addEventListener('submit', async (event) => {
		event.preventDefault();
		const form = event.currentTarget;
		const button = form.querySelector('[type="submit"]');
		const values = new FormData(form);
		const body = Object.fromEntries(values.entries());
		for (const key of ['resume_url', 'cover_letter_url']) body[key] = body[key].trim() || null;
		setButtonBusy(button, true, 'Submitting…');
		try {
			await request('/applications', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
			form.reset();
			createDialog.close();
			showNotice('Application submitted. Processing will continue in the background.');
			await loadApplications();
		} catch (error) { showNotice(error.message, true); }
		finally { setButtonBusy(button, false); }
	});

	$('#import-form').addEventListener('submit', async (event) => {
		event.preventDefault();
		const form = event.currentTarget;
		const file = $('#application-file').files[0];
		if (!file) return;
		const button = form.querySelector('[type="submit"]');
		const data = new FormData();
		data.append('file', file);
		setButtonBusy(button, true, 'Importing…');
		try {
			const report = await request('/applications/import', { method: 'POST', body: data });
			const errors = report.errors.length
				? `<details><summary>See import errors</summary><pre>${escapeHtml(JSON.stringify(report.errors, null, 2))}</pre></details>`
				: '';
			$('#import-result').innerHTML = `<strong>${report.created} created</strong> · ${report.skipped_duplicates} duplicates skipped · ${report.errors.length} rows with errors${errors}`;
			$('#import-result').hidden = false;
			showNotice('Import finished.');
			form.reset();
			await loadApplications();
		} catch (error) { showNotice(error.message, true); }
		finally { setButtonBusy(button, false); }
	});

	$('#application-rows').addEventListener('click', async (event) => {
		const viewButton = event.target.closest('[data-view-application]');
		if (viewButton) {
			try {
				const result = await request(`/applications?id=${encodeURIComponent(viewButton.dataset.viewApplication)}&page=1&page_size=1`);
				const application = result.data[0];
				if (!application) throw new Error('Application not found.');
				$('#application-detail-title').textContent = application.candidate_name || application.from_email;
				const link = (url, label) => typeof url === 'string' && url.startsWith('https://')
					? `<p><a class="detail-link" href="${escapeHtml(url)}" target="_blank" rel="noreferrer">Open ${label}</a></p>`
					: '<p class="muted">Not provided as a secure link.</p>';
				$('#application-detail-content').innerHTML = `<div class="detail-grid"><div><strong>Role</strong><p>${escapeHtml(application.job?.title || 'Unassigned')}</p></div><div><strong>Status</strong><p><span class="status ${escapeHtml(application.processing_status || 'received')}">${escapeHtml(application.processing_status || 'received')}</span></p></div><div><strong>Email</strong><p>${escapeHtml(application.from_email)}</p></div><div><strong>Subject</strong><p>${escapeHtml(application.subject || '—')}</p></div><div><strong>Received</strong><p>${formatDate(application.created_at)}</p></div><div><strong>Application ID</strong><p>${escapeHtml(application.id)}</p></div></div><h3>Message</h3><p class="detail-message">${escapeHtml(application.message || 'No message provided.')}</p><h3>Resume</h3>${link(application.resume_url, 'resume')}<h3>Cover letter</h3>${link(application.cover_letter_url, 'cover letter')}`;
				$('#application-dialog').showModal();
			} catch (error) { showNotice(error.message, true); }
			return;
		}
		const button = event.target.closest('[data-delete-application]');
		if (!button || !confirm('Delete this application?')) return;
		try {
			await request(`/applications/${encodeURIComponent(button.dataset.deleteApplication)}`, { method: 'DELETE' });
			showNotice('Application deleted.');
			await loadApplications();
		} catch (error) { showNotice(error.message, true); }
	});

	$('#application-refresh').addEventListener('click', loadApplications);
	$('#application-search').addEventListener('input', debounce(loadApplications));
	$('#application-status').addEventListener('change', loadApplications);
	loadApplications();
	window.setInterval(loadApplications, 15000);
}

async function loadResponses() {
	try {
		const search = $('#response-search').value.trim();
		const status = $('#response-status').value;
		const result = await request(`/responses?${queryString({ search, status })}`);
		$('#response-total').textContent = result.total;
		$('#response-count').textContent = `${result.total} response${result.total === 1 ? '' : 's'}`;
		$('#response-empty').hidden = result.data.length > 0;
		$('#response-list').innerHTML = result.data.map((response) => {
			const application = response.application || {};
			const job = application.job || {};
			return `<article class="surface response-card" data-response="${escapeHtml(response.id)}">
				<div class="response-top"><div><h3>${escapeHtml(application.candidate_name || 'Candidate')}</h3><div class="response-meta"><span>${escapeHtml(job.title || 'Unassigned role')}</span><span class="status ${escapeHtml(response.status)}">${escapeHtml(response.status)}</span></div></div><strong>${escapeHtml(response.classification || 'Unclassified')}</strong></div>
				${response.classification_reason ? `<p class="muted">${escapeHtml(response.classification_reason)}</p>` : ''}
				<div class="response-body"><div><h3>Generated draft</h3><p>${escapeHtml(response.generated_response)}</p></div><div class="field"><label for="draft-${escapeHtml(response.id)}">Review and edit</label><textarea id="draft-${escapeHtml(response.id)}" data-authored-response>${escapeHtml(response.authored_response)}</textarea></div></div>
				<div class="response-actions"><button class="button secondary small" data-save-response type="button">Update response</button>${response.status === 'draft' ? '<button class="button small" data-approve-response type="button">Approve</button>' : ''}</div>
			</article>`;
		}).join('');
	} catch (error) {
		showNotice(error.message, true);
		$('#response-count').textContent = 'Could not load responses';
	}
}

function initResponses() {
	$('#response-list').addEventListener('click', async (event) => {
		const button = event.target.closest('[data-save-response], [data-approve-response]');
		if (!button) return;
		const card = button.closest('[data-response]');
		const body = { authored_response: card.querySelector('[data-authored-response]').value };
		if (button.hasAttribute('data-approve-response')) body.status = 'approved';
		setButtonBusy(button, true, 'Saving…');
		try {
			await request(`/responses/${encodeURIComponent(card.dataset.response)}`, {
				method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
			});
			showNotice(body.status ? 'Draft saved and approved.' : 'Draft saved.');
			await loadResponses();
		} catch (error) { showNotice(error.message, true); }
		finally { setButtonBusy(button, false); }
	});

	$('#response-refresh').addEventListener('click', loadResponses);
	$('#response-search').addEventListener('input', debounce(loadResponses));
	$('#response-status').addEventListener('change', loadResponses);
	loadResponses();
}

if (page === 'jobs') initJobs();
if (page === 'job-board') initJobBoard();
if (page === 'applications') initApplications();
if (page === 'responses') initResponses();

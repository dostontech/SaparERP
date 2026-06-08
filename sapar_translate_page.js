frappe.pages["sapar-translate"].on_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Translation Tool",
		single_column: true,
	});

	// ── State ────────────────────────────────────────────────────────────────
	var state = {
		lang: "uz",
		filter: "all",
		search: "",
		page: 1,
		page_length: 80,
		dirty: {},
	};

	// ── Inject styles once ────────────────────────────────────────────────────
	if (!document.getElementById("sapar-translate-css")) {
		var style = document.createElement("style");
		style.id = "sapar-translate-css";
		style.textContent = `
			#st-wrap { padding: 0 4px 24px; }
			#st-toolbar {
				display: flex; align-items: center; gap: 10px;
				flex-wrap: wrap; padding: 12px 0 14px;
				border-bottom: 1px solid #eee; margin-bottom: 14px;
			}
			#st-toolbar label { font-size:11px; font-weight:700; color:#888; text-transform:uppercase; margin:0; }
			#st-toolbar select, #st-toolbar input[type=text] {
				border:1px solid #d1d8dd; border-radius:5px; padding:6px 10px;
				font-size:13px; outline:none; background:#fff; height:32px;
			}
			#st-toolbar select:focus, #st-toolbar input[type=text]:focus { border-color:var(--primary-color,#5e64ff); }
			.st-btn { height:32px; padding:0 14px; border-radius:5px; border:none; cursor:pointer; font-size:13px; font-weight:500; }
			.st-btn-primary { background:var(--primary-color,#5e64ff); color:#fff; }
			.st-btn-primary:hover { opacity:.9; }
			.st-btn-primary:disabled { opacity:.45; cursor:default; }
			.st-btn-default { background:#fff; border:1px solid #d1d8dd; color:#333; }
			.st-btn-default:hover { background:#f5f7fa; }
			#st-stats { margin-left:auto; font-size:12px; color:#666; white-space:nowrap; }
			#st-stats strong { color:#333; }
			#st-table table { width:100%; border-collapse:collapse; font-size:13px; }
			#st-table thead th {
				background:#f8f9fa; border-bottom:2px solid #e2e8f0;
				padding:9px 12px; text-align:left;
				font-size:11px; font-weight:700; color:#777; text-transform:uppercase; letter-spacing:.4px;
			}
			#st-table tbody tr { border-bottom:1px solid #f0f2f5; }
			#st-table tbody tr:hover { background:#f8f9ff; }
			#st-table tbody tr.st-dirty { background:#fffde7; }
			#st-table td { padding:7px 12px; vertical-align:middle; }
			#st-table td.st-src { color:#555; max-width:380px; word-break:break-word; line-height:1.5; }
			#st-table td.st-src .st-ctx { font-size:11px; color:#bbb; margin-top:2px; }
			.st-inp {
				width:100%; border:none; background:transparent;
				font-size:13px; color:#222; padding:3px 0; outline:none; line-height:1.5;
			}
			.st-inp:focus { border-bottom:2px solid var(--primary-color,#5e64ff); padding-bottom:1px; }
			.st-badge { display:inline-block; padding:2px 7px; border-radius:10px; font-size:11px; font-weight:600; }
			.st-badge.empty { background:#fff3cd; color:#856404; }
			.st-badge.done  { background:#d4edda; color:#155724; }
			.st-del { background:none; border:none; color:#ccc; cursor:pointer; font-size:15px; padding:2px 6px; border-radius:3px; }
			.st-del:hover { color:#e74c3c; background:#fef3f2; }
			#st-pager { display:flex; align-items:center; justify-content:center; gap:6px; padding:16px 0; }
			#st-pager button { width:30px; height:30px; border:1px solid #d1d8dd; background:#fff; border-radius:5px; cursor:pointer; font-size:13px; }
			#st-pager button.st-pg-active { background:var(--primary-color,#5e64ff); color:#fff; border-color:var(--primary-color,#5e64ff); }
			#st-pager button:hover:not(.st-pg-active):not(:disabled) { background:#f5f7fa; }
			#st-pager .st-pg-info { font-size:12px; color:#666; margin:0 8px; }
		`;
		document.head.appendChild(style);
	}

	// ── Build HTML skeleton ───────────────────────────────────────────────────
	$(page.main).html(`
		<div id="st-wrap">
			<div id="st-toolbar">
				<label>Language</label>
				<select id="st-lang">
					<option value="uz">O'zbekcha (uz)</option>
					<option value="ru">Русский (ru)</option>
					<option value="en">English (en)</option>
				</select>
				<label>Show</label>
				<select id="st-filter">
					<option value="all">All strings</option>
					<option value="empty">Untranslated only</option>
					<option value="done">Translated only</option>
				</select>
				<input type="text" id="st-search" placeholder="Search…" style="min-width:200px">
				<button class="st-btn st-btn-default" id="st-add-btn">+ Add</button>
				<button class="st-btn st-btn-primary" id="st-save-btn" disabled>Save Changes</button>
				<span id="st-stats"></span>
			</div>
			<div id="st-table"><div style="text-align:center;padding:50px;color:#aaa">Loading…</div></div>
			<div id="st-pager"></div>
		</div>
	`);

	// ── Toolbar events ────────────────────────────────────────────────────────
	$("#st-lang").on("change", function () {
		if (Object.keys(state.dirty).length) {
			frappe.confirm("You have unsaved changes. Switch language?", function () {
				state.lang = $("#st-lang").val();
				state.dirty = {};
				state.page = 1;
				load();
			}, function () {
				$("#st-lang").val(state.lang);
			});
		} else {
			state.lang = $(this).val();
			state.page = 1;
			load();
		}
	});

	$("#st-filter").on("change", function () {
		state.filter = $(this).val();
		state.page = 1;
		load();
	});

	var search_timer;
	$("#st-search").on("input", function () {
		clearTimeout(search_timer);
		var val = $(this).val();
		search_timer = setTimeout(function () {
			state.search = val;
			state.page = 1;
			load();
		}, 350);
	});

	$("#st-save-btn").on("click", save_all);
	$("#st-add-btn").on("click", show_add_dialog);

	// ── Load ──────────────────────────────────────────────────────────────────
	function load() {
		$("#st-table").html('<div style="text-align:center;padding:50px;color:#aaa">Loading…</div>');
		$("#st-pager").empty();

		frappe.call({
			method: "frappe.core.page.sapar_translate.sapar_translate.get_translations",
			args: {
				language: state.lang,
				search: state.search,
				only_empty: state.filter === "empty" ? 1 : 0,
				only_done: state.filter === "done" ? 1 : 0,
				page: state.page,
				page_length: state.page_length,
			},
			callback: function (r) {
				if (r.message) {
					render_table(r.message.rows);
					render_stats(r.message);
					render_pager(r.message.total);
				}
			},
		});
	}

	// ── Table ─────────────────────────────────────────────────────────────────
	function render_table(rows) {
		if (!rows || !rows.length) {
			$("#st-table").html('<div style="text-align:center;padding:60px;color:#aaa;font-size:14px">No strings found.</div>');
			return;
		}

		var html = `<table>
			<thead><tr>
				<th style="width:45%">Source Text (English)</th>
				<th>Translation</th>
				<th style="width:70px">Status</th>
				<th style="width:44px"></th>
			</tr></thead><tbody>`;

		rows.forEach(function (r) {
			var cur = state.dirty[r.name] !== undefined ? state.dirty[r.name] : (r.translated_text || "");
			var is_dirty = state.dirty[r.name] !== undefined;
			var badge = cur
				? '<span class="st-badge done">✓</span>'
				: '<span class="st-badge empty">—</span>';
			html += `<tr class="${is_dirty ? "st-dirty" : ""}" data-name="${frappe.utils.escape_html(r.name)}">
				<td class="st-src">${frappe.utils.escape_html(r.source_text)}${r.context ? `<div class="st-ctx">${frappe.utils.escape_html(r.context)}</div>` : ""}</td>
				<td><input class="st-inp" type="text" data-name="${frappe.utils.escape_html(r.name)}" value="${frappe.utils.escape_html(cur)}" placeholder="Enter translation…"></td>
				<td>${badge}</td>
				<td><button class="st-del" data-name="${frappe.utils.escape_html(r.name)}" title="Delete">✕</button></td>
			</tr>`;
		});
		html += "</tbody></table>";
		$("#st-table").html(html);

		// Input change
		$("#st-table .st-inp").on("input", function () {
			var name = $(this).data("name");
			var orig_row = rows.find(function(x){ return x.name === name; });
			var orig = orig_row ? (orig_row.translated_text || "") : "";
			var val = $(this).val();
			var $row = $(this).closest("tr");
			if (val !== orig) {
				state.dirty[name] = val;
				$row.addClass("st-dirty");
			} else {
				delete state.dirty[name];
				$row.removeClass("st-dirty");
			}
			$row.find("td:nth-child(3)").html(val
				? '<span class="st-badge done">✓</span>'
				: '<span class="st-badge empty">—</span>');
			$("#st-save-btn").prop("disabled", Object.keys(state.dirty).length === 0);
			update_dirty_count();
		});

		// Delete
		$("#st-table .st-del").on("click", function () {
			var name = $(this).data("name");
			frappe.confirm("Delete this translation?", function () {
				frappe.call({
					method: "frappe.core.page.sapar_translate.sapar_translate.delete_translation",
					args: { name: name },
					callback: function () {
						delete state.dirty[name];
						load();
						frappe.show_alert({ message: "Deleted", indicator: "red" }, 2);
					},
				});
			});
		});
	}

	// ── Save ──────────────────────────────────────────────────────────────────
	function save_all() {
		var updates = Object.entries(state.dirty).map(function (pair) {
			return { name: pair[0], translated_text: pair[1] };
		});
		if (!updates.length) return;
		$("#st-save-btn").prop("disabled", true).text("Saving…");
		frappe.call({
			method: "frappe.core.page.sapar_translate.sapar_translate.save_batch",
			args: { updates: JSON.stringify(updates) },
			callback: function (r) {
				state.dirty = {};
				$("#st-save-btn").prop("disabled", true).text("Save Changes");
				load();
				frappe.show_alert({ message: (r.message || updates.length) + " saved", indicator: "green" }, 3);
			},
		});
	}

	// ── Stats ─────────────────────────────────────────────────────────────────
	function render_stats(data) {
		var pct = data.total_lang ? Math.round((data.done / data.total_lang) * 100) : 0;
		$("#st-stats").html(
			`Showing <strong>${data.total}</strong> &bull; ` +
			`<strong>${data.done}/${data.total_lang}</strong> translated (${pct}%)`
		);
	}

	function update_dirty_count() {
		var n = Object.keys(state.dirty).length;
		var existing = $("#st-stats").text().split("·").slice(0, 2).join("·");
		if (n) {
			if (!$("#st-dirty-count").length)
				$("#st-stats").append(` &bull; <span id="st-dirty-count" style="color:#e67e22"><strong>${n}</strong> unsaved</span>`);
			else
				$("#st-dirty-count strong").text(n);
		} else {
			$("#st-dirty-count").remove();
		}
	}

	// ── Pager ─────────────────────────────────────────────────────────────────
	function render_pager(total) {
		var pages = Math.ceil(total / state.page_length);
		if (pages <= 1) { $("#st-pager").hide(); return; }
		$("#st-pager").show();
		var html = `<button ${state.page === 1 ? "disabled" : ""} data-p="${state.page - 1}">‹</button>`;
		for (var p = Math.max(1, state.page - 3); p <= Math.min(pages, state.page + 3); p++) {
			html += `<button class="${p === state.page ? "st-pg-active" : ""}" data-p="${p}">${p}</button>`;
		}
		html += `<button ${state.page === pages ? "disabled" : ""} data-p="${state.page + 1}">›</button>`;
		html += `<span class="st-pg-info">Page ${state.page} of ${pages} &bull; ${total} total</span>`;
		$("#st-pager").html(html).find("button[data-p]").on("click", function () {
			state.page = parseInt($(this).data("p"));
			load();
			$(page.main).get(0).scrollTop = 0;
		});
	}

	// ── Add dialog ────────────────────────────────────────────────────────────
	function show_add_dialog() {
		var d = new frappe.ui.Dialog({
			title: "Add Translation",
			fields: [
				{ fieldname: "source_text", fieldtype: "Small Text", label: "Source Text (English)", reqd: 1 },
				{ fieldname: "translated_text", fieldtype: "Small Text", label: "Translation (" + state.lang + ")", reqd: 1 },
				{ fieldname: "context", fieldtype: "Data", label: "Context (optional)" },
			],
			primary_action_label: "Add",
			primary_action: function (vals) {
				frappe.call({
					method: "frappe.core.page.sapar_translate.sapar_translate.add_translation",
					args: {
						language: state.lang,
						source_text: vals.source_text,
						translated_text: vals.translated_text,
						context: vals.context || "",
					},
					callback: function () {
						d.hide();
						load();
						frappe.show_alert({ message: "Translation added", indicator: "green" }, 3);
					},
				});
			},
		});
		d.show();
	}

	// ── Initial load ──────────────────────────────────────────────────────────
	load();
};

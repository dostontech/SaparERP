// SaparERP – Navbar language switcher (EN / O'Z / RU)
// Targets Frappe v16 desktop-navbar structure:
//   header.desktop-navbar > div.flex > [notifications, avatar]
(function () {
	"use strict";

	var LANGS = [
		{ code: "en", label: "EN", full: "English" },
		{ code: "uz", label: "O'Z", full: "O'zbekcha" },
		{ code: "ru", label: "RU", full: "Русский" },
	];

	function currentCode() {
		return (frappe.boot && frappe.boot.lang) ? frappe.boot.lang : "en";
	}

	function currentLabel() {
		var match = LANGS.find(function (l) { return l.code === currentCode(); });
		return match ? match.label : "EN";
	}

	window.saparSetLang = function (code) {
		frappe.call({
			method: "frappe.client.set_value",
			args: { doctype: "User", name: frappe.session.user, fieldname: "language", value: code },
			callback: function () { location.reload(); },
		});
	};

	function inject() {
		if (!frappe.session || frappe.session.user === "Guest") return;
		if (document.getElementById("sapar-lang-switcher")) return;

		// Frappe v16 desktop navbar right-side container
		var $container = $("header.desktop-navbar > div.flex");
		if (!$container.length) {
			// fallback: any flex div inside the desktop navbar
			$container = $("header.desktop-navbar .flex").first();
		}
		if (!$container.length) return;

		var items = LANGS.map(function (l) {
			var active = currentCode() === l.code ? " style=\"font-weight:700\"" : "";
			return "<li><a class=\"dropdown-item\" href=\"#\" onclick=\"event.preventDefault();saparSetLang('" + l.code + "')\"" + active + ">" + l.full + "</a></li>";
		}).join("");

		var $btn = $([
			"<div id=\"sapar-lang-switcher\" class=\"dropdown\" style=\"display:flex;align-items:center;\">",
			"  <button class=\"btn-reset nav-link text-muted dropdown-toggle\" data-toggle=\"dropdown\" style=\"font-weight:700;font-size:11px;letter-spacing:1px;padding:4px 8px;border:1px solid var(--border-color,#d1d8dd);border-radius:4px;\">",
			currentLabel(),
			"  </button>",
			"  <div class=\"dropdown-menu dropdown-menu-right\" style=\"min-width:130px;\">",
			"    <ul class=\"list-unstyled mb-0\">",
			items,
			"    </ul>",
			"  </div>",
			"</div>",
		].join(""));

		// Insert before .desktop-notifications
		var $notif = $container.find(".desktop-notifications");
		if ($notif.length) {
			$btn.insertBefore($notif);
		} else {
			$container.prepend($btn);
		}
	}

	function tryInject() {
		// Retry until the desktop-navbar is in the DOM
		if ($("header.desktop-navbar").length) {
			inject();
		} else {
			setTimeout(tryInject, 300);
		}
	}

	$(document).on("toolbar_setup", function () { setTimeout(inject, 200); });
	$(document).on("page-change", function () {
		$("#sapar-lang-switcher").remove();
		setTimeout(inject, 300);
	});

	frappe.ready(function () { setTimeout(tryInject, 500); });

	// ── Remove unwanted user-menu items ───────────────────────────────────
	var HIDDEN_MENU_LABELS = ["Frappe Support", "Delete Demo Data"];

	function removeUnwantedMenuItems() {
		document.querySelectorAll(".dropdown-menu a, .user-info-menu a").forEach(function (a) {
			var text = (a.textContent || "").trim();
			var href = a.href || "";
			if (
				HIDDEN_MENU_LABELS.indexOf(text) !== -1 ||
				href.indexOf("discuss.frappe.io") !== -1
			) {
				var li = a.closest("li") || a.parentElement;
				if (li) li.style.display = "none";
			}
		});
	}

	// Re-run whenever the DOM changes (menus open/close)
	new MutationObserver(removeUnwantedMenuItems)
		.observe(document.body, { childList: true, subtree: true });

})();

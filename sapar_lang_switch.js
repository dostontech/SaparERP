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
	// CSS fallback for href-based items (catches even before JS runs)
	var _style = document.createElement("style");
	_style.textContent =
		'a[href*="discuss.frappe"]{display:none!important;}' +
		'li:has(a[href*="discuss.frappe"]){display:none!important;}';
	(document.head || document.documentElement).appendChild(_style);

	var HIDDEN_LABELS = ["Frappe Support", "About", "Reset Desktop Layout"];

	function removeUnwantedMenuItems() {
		document.querySelectorAll(".dropdown-menu li, .user-menu li").forEach(function (li) {
			var el = li.querySelector("a, button") || li;
			var text = (el.textContent || "").trim();
			var href = (el.getAttribute && el.getAttribute("href")) || "";
			if (
				HIDDEN_LABELS.indexOf(text) !== -1 ||
				href.indexOf("discuss.frappe") !== -1
			) {
				li.style.display = "none";
			}
		});
	}

	// Hook into Bootstrap dropdown open events
	$(document).on("show.bs.dropdown shown.bs.dropdown", function () {
		setTimeout(removeUnwantedMenuItems, 30);
		setTimeout(removeUnwantedMenuItems, 150);
	});
	// Hook into Frappe page/toolbar events
	$(document).on("toolbar_setup page-change", function () {
		setTimeout(removeUnwantedMenuItems, 300);
	});
	// MutationObserver as safety net
	new MutationObserver(function (mutations) {
		for (var i = 0; i < mutations.length; i++) {
			if (mutations[i].addedNodes.length) {
				removeUnwantedMenuItems();
				break;
			}
		}
	}).observe(document.body, { childList: true, subtree: true });

})();

import html
import json
import os

ORANGE = "#ff6a00"
BLUE = "#1e6fe0"
GREEN = "#0a9a5c"

SHOW_ON_SCREEN = False

BANNER_SCRIPT = """
(function () {
    if (window.top !== window) { return; }
    var title = TITLE_HERE;
    var description = DESCRIPTION_HERE;
    var knownBug = KNOWN_BUG_HERE;
    function addBanner() {
        if (!document.documentElement || document.getElementById("qa-banner")) { return; }
        var bar = document.createElement("div");
        bar.id = "qa-banner";
        bar.style.cssText = "position:fixed;left:0;right:0;bottom:0;z-index:2147483646;box-sizing:border-box;padding:8px 14px;background:rgba(20,20,20,0.93);border-top:4px solid #ff6a00;color:#fff;font-family:Arial,sans-serif;pointer-events:none;";
        var line1 = document.createElement("div");
        line1.textContent = title;
        line1.style.cssText = "font-size:18px;font-weight:bold;line-height:24px;";
        var line2 = document.createElement("div");
        line2.textContent = description;
        line2.style.cssText = "font-size:14px;line-height:19px;color:#ddd;";
        bar.appendChild(line1);
        bar.appendChild(line2);
        if (knownBug) {
            var line3 = document.createElement("div");
            line3.textContent = knownBug;
            line3.style.cssText = "font-size:14px;line-height:19px;font-weight:bold;color:#ffb74d;";
            bar.appendChild(line3);
        }
        document.documentElement.appendChild(bar);
    }
    var timer = setInterval(function () {
        if (document.documentElement) { addBanner(); clearInterval(timer); }
    }, 20);
    document.addEventListener("DOMContentLoaded", addBanner);
    window.addEventListener("load", addBanner);
})();
"""

HIGHLIGHT_SCRIPT = """
(els, args) => {
    var label = args[0];
    var color = args[1];
    var limit = args[2];
    var shown = 0;
    for (var i = 0; i < els.length && shown < limit; i++) {
        var el = els[i];
        if (shown === 0) { el.scrollIntoView({block: "center", inline: "nearest", behavior: "instant"}); }
        var rect = el.getBoundingClientRect();
        var left = Math.max(rect.left, 0);
        var top = Math.max(rect.top, 0);
        var right = Math.min(rect.right, window.innerWidth);
        var bottom = Math.min(rect.bottom, window.innerHeight);
        if (rect.width === 0 || rect.height === 0 || right <= left || bottom <= top) { continue; }
        var hidden = !el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true});
        var shade = hidden ? "#777777" : color;
        var box = document.createElement("div");
        box.className = "qa-mark";
        box.style.cssText = "position:fixed;z-index:2147483647;pointer-events:none;box-sizing:border-box;border:4px " + (hidden ? "dashed" : "solid") + " " + shade + ";background:" + (hidden ? "transparent" : color + "33") + ";border-radius:6px;";
        box.style.left = (left - 4) + "px";
        box.style.top = (top - 4) + "px";
        box.style.width = (right - left + 8) + "px";
        box.style.height = (bottom - top + 8) + "px";
        document.documentElement.appendChild(box);
        if (shown === 0) {
            var chip = document.createElement("div");
            chip.className = "qa-mark";
            chip.textContent = (label.length > 45 ? label.slice(0, 45) + "..." : label) + (hidden ? "  (HIDDEN: you cannot see it on the page)" : "");
            chip.style.cssText = "position:fixed;z-index:2147483647;pointer-events:none;padding:3px 9px;border-radius:5px;color:#fff;font:bold 17px Arial,sans-serif;white-space:nowrap;background:" + shade + ";";
            chip.style.left = Math.max(left - 4, 4) + "px";
            chip.style.top = (top - 4 > 38 ? top - 38 : bottom + 8) + "px";
            document.documentElement.appendChild(chip);
            if (chip.offsetLeft + chip.offsetWidth > window.innerWidth - 4) {
                chip.style.left = Math.max(window.innerWidth - chip.offsetWidth - 4, 4) + "px";
            }
            if (label.indexOf("CLICK") === 0 && !hidden) {
                var dot = document.createElement("div");
                dot.className = "qa-mark";
                dot.style.cssText = "position:fixed;z-index:2147483647;pointer-events:none;width:26px;height:26px;border-radius:50%;border:3px solid #fff;background:" + color + ";";
                dot.style.left = ((left + right) / 2 - 13) + "px";
                dot.style.top = ((top + bottom) / 2 - 13) + "px";
                document.documentElement.appendChild(dot);
                dot.animate([{transform: "scale(0.4)", opacity: 1}, {transform: "scale(1.6)", opacity: 0.3}], {duration: 450, iterations: 2});
            }
        }
        shown++;
    }
    return shown > 0;
}
"""

REMOVE_MARKS_SCRIPT = """
document.querySelectorAll(".qa-mark").forEach(function (e) { e.remove(); })
"""

NOTE_SCRIPT = """
(args) => {
    var text = args[0];
    var seconds = args[1];
    var bar = document.getElementById("qa-banner");
    var holder = document.getElementById("qa-notes");
    if (!holder) {
        holder = document.createElement("div");
        holder.id = "qa-notes";
        holder.style.cssText = "position:fixed;right:12px;z-index:2147483645;pointer-events:none;display:flex;flex-direction:column;align-items:flex-end;gap:6px;max-width:85vw;";
        document.documentElement.appendChild(holder);
    }
    holder.style.bottom = (bar ? bar.offsetHeight + 10 : 10) + "px";
    var note = document.createElement("div");
    note.textContent = text;
    note.style.cssText = "background:#fff8e1;color:#222;border:2px solid #ff6a00;border-radius:6px;padding:6px 10px;font:14px Arial,sans-serif;box-shadow:0 2px 8px rgba(0,0,0,0.3);";
    holder.appendChild(note);
    setTimeout(function () { note.remove(); }, seconds * 1000);
}
"""


CARD_HTML = """
<body style="margin:0;background:#141414;color:#fff;font-family:Arial,sans-serif;display:flex;flex-direction:column;justify-content:center;min-height:100vh;padding:0 7%;box-sizing:border-box;">
<div style="color:#ff6a00;font-size:20px;font-weight:bold;letter-spacing:3px;">NEXT TEST</div>
<div style="font-size:36px;font-weight:bold;margin:14px 0;line-height:44px;">TITLE_HERE</div>
<div style="font-size:22px;color:#dddddd;line-height:30px;">DESCRIPTION_HERE</div>
<div style="font-size:20px;color:#ffb74d;font-weight:bold;margin-top:22px;">KNOWN_BUG_HERE</div>
</body>
"""


def show_test_banner(page, request):
    global SHOW_ON_SCREEN
    SHOW_ON_SCREEN = os.getenv("CI") != "true" and request.config.getoption("headed")
    if not SHOW_ON_SCREEN:
        return
    title = getattr(request.function, "__allure_display_name__", request.node.name)
    if hasattr(request.node, "callspec"):
        title = title.format(**request.node.callspec.params)
    description = ""
    mark = request.node.get_closest_marker("allure_description")
    if mark:
        description = "What it checks: " + mark.args[0]
    known_bug = ""
    xfail_mark = request.node.get_closest_marker("xfail")
    if xfail_mark:
        known_bug = "EXPECTED TO FAIL. " + xfail_mark.kwargs.get("reason", "")
    script = BANNER_SCRIPT.replace("TITLE_HERE", json.dumps(title))
    script = script.replace("DESCRIPTION_HERE", json.dumps(description))
    script = script.replace("KNOWN_BUG_HERE", json.dumps(known_bug))
    page.add_init_script(script)
    card = CARD_HTML.replace("TITLE_HERE", html.escape(title))
    card = card.replace("DESCRIPTION_HERE", html.escape(description))
    card = card.replace("KNOWN_BUG_HERE", html.escape(known_bug))
    try:
        page.set_content(card)
        page.wait_for_timeout(2500)
    except Exception:
        pass


def highlight(page, locator, label, color, limit=1):
    if not SHOW_ON_SCREEN:
        return
    try:
        drawn = page.locator(locator).evaluate_all(HIGHLIGHT_SCRIPT, [label, color, limit])
        if drawn:
            page.wait_for_timeout(700)
        page.evaluate(REMOVE_MARKS_SCRIPT)
    except Exception:
        pass


def show_note(page, text, seconds=4):
    if not SHOW_ON_SCREEN:
        return
    text = str(text)
    if len(text) > 120:
        text = text[:120] + "..."
    try:
        page.evaluate(NOTE_SCRIPT, [text, seconds])
    except Exception:
        pass


def pause_after_test(page):
    if not SHOW_ON_SCREEN:
        return
    try:
        page.wait_for_timeout(1200)
    except Exception:
        pass

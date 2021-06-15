$(document).ready(function() {
    $("#inputLT").click((event) => {
        lt = $("#inputLocalTimezone").get(0)
        lt.disabled = lt.disabled ? false : true
        lt.required = lt.required ? false : true
        $('#labelILT')[0].innerHTML = lt.disabled ? "Local Timezone" : 'Local Timezone<i class="req"></i>'
    })

    // Ripped off Stackoverflow
    window.copyToClipboard = (text) => {
        if (window.clipboardData && window.clipboardData.setData) {
            // Internet Explorer-specific code path to prevent textarea being shown while dialog is visible.
            return window.clipboardData.setData("Text", text);

        } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
            var textarea = document.createElement("textarea");
            textarea.textContent = text;
            textarea.style.position = "fixed"; // Prevent scrolling to bottom of page in Microsoft Edge.
            document.body.appendChild(textarea);
            textarea.select();
            try {
                return document.execCommand("copy"); // Security exception may be thrown by some browsers.
            } catch (ex) {
                console.warn("Copy to clipboard failed.", ex);
                return false;
            } finally {
                document.body.removeChild(textarea);
            }
        }
    }

    // Change border color
    window.changeBorderColor = (elements, color) => {
        elements.forEach(element => {
            $(element).css({
                "border-color": color
            })
        })
    }
})
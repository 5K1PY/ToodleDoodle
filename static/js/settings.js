$(function() {
    var $this = $(this);

    const TRANSPOSE_TABLES_TAG = 'transpose-tables';
    const INTERVAL_MODE_TAG = 'interval-mode';
    const WEIGHTS_TAG = 'weights';
    const BUTTON_TAG = 'buttons';
    const SETTINGS = {
        't': TRANSPOSE_TABLES_TAG,
        'i': INTERVAL_MODE_TAG,
        'w': WEIGHTS_TAG,
        'b': BUTTON_TAG
    };
 
    if (getCookie(TRANSPOSE_TABLES_TAG) === 'true') {
        $this.find(`#${TRANSPOSE_TABLES_TAG}`).click();
    }

    if (getCookie(INTERVAL_MODE_TAG) === 'true') {
        $this.find(`#${INTERVAL_MODE_TAG}`).click();
    }

    if (getCookie(WEIGHTS_TAG) === 'true') {
        $this.find(`#${WEIGHTS_TAG}`).click();
    }

    if (getCookie(BUTTON_TAG) === 'true' || getCookie(BUTTON_TAG) === undefined) {
        $this.find(`#${BUTTON_TAG}`).click();
    }

    $this.find(`#${TRANSPOSE_TABLES_TAG}`).change(() => toggleCookie(TRANSPOSE_TABLES_TAG));
    $this.find(`#${INTERVAL_MODE_TAG}`).change(() => toggleCookie(INTERVAL_MODE_TAG));
    $this.find(`#${WEIGHTS_TAG}`).change(() => toggleCookie(WEIGHTS_TAG));
    $this.find(`#${BUTTON_TAG}`).change(() => toggleCookie(BUTTON_TAG));
    // cookies
    function getCookie(cname) {
        var cookies = document.cookie;
        var parts = cookies.split(`${cname}=`);
        if (parts.length > 1) {
            return parts[1].split(';')[0];
        } else {
            return undefined;
        }
    }
    function setCookie(cname, val) {
        document.cookie = `${cname}=${val}; path=/`;
    }
    function toggleCookie(cname) {
        var val = getCookie(cname);
        if (val === 'true') {
            setCookie(cname, 'false');
        } else {
            setCookie(cname, 'true');
        }
    }

    // add shortcuts
    $this.keypress(function(e) {
        if (e.target.tagName === 'INPUT' && e.target.type === 'text') {
            return;
        }
        var key = String.fromCharCode(e.keyCode || e.which);
        if (key == 's') {
            $this.find('#show-settings').click();
        }
        for (const bound_key in SETTINGS) {
            if (key == bound_key) {
                $this.find(`#${SETTINGS[bound_key]}`).click();
            }
        }
    });
});

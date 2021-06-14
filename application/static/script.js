$(document).ready(function () {
    $("#inputLT").click((event) => {
        lt = $("#inputLocalTimezone").get(0)
        lt.disabled = lt.disabled ? false : true
        lt.required = lt.required ? false : true
        $('#labelILT')[0].innerHTML = lt.disabled ? "Local Timezone" : 'Local Timezone<i class="req"></i>'
    })

})
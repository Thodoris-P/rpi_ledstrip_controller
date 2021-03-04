function toggle(item)
{
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send("toggle=" + item.checked);
}

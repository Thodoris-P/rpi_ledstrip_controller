function getSliderValue()
{
    var value = document.getElementById("brightness").value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send("brightness=" + value);
}
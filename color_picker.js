function initColorPicker()
{
    var canvasEl = document.getElementById('colorCanvas');
    var canvasContext = canvasEl.getContext('2d');

    var image = new Image(250, 250);
    image.onload = () => canvasContext.drawImage(image, 0, 0, image.width, image.height); 
    image.src = "color_picker.png";

    canvasEl.onclick = function(mouseEvent) 
    {
        var checkbox = document.getElementById('cb-toggle');
        if(!checkbox.checked)
        {
            return;
        }
        
        var imgData = canvasContext.getImageData(mouseEvent.offsetX, mouseEvent.offsetY, 1, 1);
        var rgba = imgData.data;

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send("color=" + rgba[0] + "," + rgba[1] + "," + rgba[2]);
    }
}
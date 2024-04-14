import QtQuick 2.15
import QtMultimedia 5.15

Item {
    id: videoItem
    width: 800
    height: 600

    VideoOutput {
        id: videoOutput
        anchors.fill: parent
        source: videoItem

        onStatusChanged: {
            if (videoOutput.status === VideoOutput.Loading) {
                console.log("Loading video output...");
            } else if (videoOutput.status === VideoOutput.Ready) {
                console.log("Video output ready");
            } else if (videoOutput.status === VideoOutput.Error) {
                console.error("Video output error:", videoOutput.errorString());
            }
        }
    }

    function updateFrame(frame) {
        var image = new Image();
        image.setData(frame.data, frame.cols, frame.rows, Image.Format_RGB888);
        videoOutput.source = image;
    }
}
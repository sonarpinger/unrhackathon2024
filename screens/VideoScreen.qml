// display frame from cv2

import QtQuick 6.5
import QtQuick.Controls 6.5

Rectangle {
    width: 100
    height: 100
    color: "red"
    Frame {
        id: bigframe
        x: 10
        y: 10
        width: 80
        height: 80
        color: "blue"
    }
    Image {
        id: image
        x: 10
        y: 10
        width: 80
        height: 80
        source: frame
    }

    function updateFrame(frame) {
        image.source = frame
    }
}
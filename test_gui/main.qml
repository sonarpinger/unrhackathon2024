import QtQuick 2.15
import QtQuick.Controls 2.15
import "./screens"

ApplicationWindow {
    visible: true
    width: 800
    height: 600

    StackView {
        id: stackView
        initialItem: Component {
            Rectangle {
                color: "lightblue"
                Text {
                    text: "First Screen"
                    anchors.centerIn: parent
                }
            }
        }
        anchors.fill: parent
    }

    StackView {
        id: videoStackView
        anchors.fill: parent
        visible: false
    }

    Connections {
        target: video
        onNew_frame: {
            videoScreen.updateFrame(new_frame);
        }
    }

    Timer {
        interval: 1000
        repeat: false
        onTriggered: {
            stackView.pop();
            var videoScreen = videoStackView.push(videoScreenComponent.createObject(videoStackView));
            videoScreen.visible = true;
        }
    }

    Component {
        id: videoScreenComponent
        VideoScreen {} // Create an instance of VideoScreen
    }
}
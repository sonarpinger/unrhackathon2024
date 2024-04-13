

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick 6.5
import QtQuick.Controls 6.5
import UntitledProject

Rectangle {
    id: rectangle
    width: Constants.width
    height: Constants.height
    color: "#764abc"
    radius: 0
    border.color: "#6a23dc"
    border.width: 0

    Column {
        id: column
        x: 433
        y: 340
        width: 200
        height: 1043
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 23
        anchors.rightMargin: 1469
        topPadding: 0
        spacing: 215
        anchors.verticalCenterOffset: 0

        Label {
            id: label
            color: "#ffffff"
            text: qsTr("High Score: ")
            font.letterSpacing: -6.4
            font.wordSpacing: -19.7
            font.pointSize: 63
            font.family: "VT323"
        }

        Label {
            id: label1
            color: "#ffffff"
            text: qsTr("Score: ")
            font.pointSize: 63
            font.family: "VT323"
        }

        Label {
            id: label2
            color: "#ffffff"
            text: qsTr("Dance: ")
            font.pointSize: 63
            font.family: "VT323"
        }
    }

    Frame {
        id: frame
        x: 480
        y: -1
        width: 1440
        height: 1080
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.topMargin: 0
        anchors.bottomMargin: 0

        Frame {
            id: frame1
            x: 788
            y: 588
            width: 640
            height: 480
            anchors.right: parent.right
            anchors.rightMargin: -12
        }
    }

    states: [
        State {
            name: "clicked"
        }
    ]
}


/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick 6.5
import QtQuick.Controls 6.5

Rectangle {
    id: rectangle
    width: Constants.width
    height: Constants.height
    color: "#764abc"
    radius: 0
    border.color: "#6a23dc"
    border.width: 16

    Column {
        id: column
        x: 433
        y: 340
        width: 200
        height: 758
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 82
        anchors.rightMargin: 1352
        spacing: 215
        anchors.verticalCenterOffset: 0

        Button {
            id: button
            width: 440
            height: 109
            opacity: 1
            visible: true
            text: qsTr("BATTLE MODE")
            font.letterSpacing: 4.3
            font.wordSpacing: -6.4
            font.pointSize: 41
            font.family: "VT323"
            display: AbstractButton.TextOnly
            checkable: false
            z: 1
            clip: false
            layer.enabled: true
            highlighted: false
            flat: false
        }

        Button {
            id: button1
            width: 440
            height: 109
            opacity: 1
            visible: true
            text: qsTr("PRACTICE MODE")
            font.letterSpacing: 0.4
            z: 1
            layer.enabled: true
            highlighted: false
            font.wordSpacing: -8.8
            font.pointSize: 41
            font.family: "VT323"
            flat: false
            display: AbstractButton.TextOnly
            clip: false
            checkable: false
            onClicked: {
                // screenLoader.source = "screens/PracticeMode.qml"
                screenLoader.source = "screens/VideoScreen.qml"
            }
        }

        Button {
            id: button2
            width: 440
            height: 109
            opacity: 1
            visible: true
            text: qsTr("ABOUT")
            font.letterSpacing: 4.3
            z: 1
            layer.enabled: true
            highlighted: false
            font.wordSpacing: -6.4
            font.pointSize: 41
            font.family: "VT323"
            flat: false
            display: AbstractButton.TextOnly
            clip: false
            checkable: false
        }
    }

    Image {
        id: pixelearf
        x: 914
        y: 140
        width: 868
        height: 917
        anchors.verticalCenter: parent.verticalCenter
        source: "../assets/images/pixelearf.png"
        anchors.verticalCenterOffset: 1
        fillMode: Image.PreserveAspectFit

        Text {
            id: text2
            x: 222
            y: 731
            color: "#f5e2ff"
            text: qsTr("PLANET")
            font.letterSpacing: 10
            font.pixelSize: 130
            anchors.horizontalCenterOffset: 16
            font.family: "VT323"
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            id: text3
            x: 207
            y: 28
            color: "#f5e2ff"
            text: qsTr("DANCE")
            font.letterSpacing: 10
            font.pixelSize: 130
            font.kerning: true
            renderType: Text.QtRendering
            anchors.horizontalCenterOffset: 16
            font.family: "VT323"
            anchors.horizontalCenter: pixelearf.horizontalCenter
        }
    }

    states: [
        State {
            name: "clicked"
        }
    ]
}

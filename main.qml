// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick 6.5
import QtQuick.Controls 6.5
// import guiqmls

Window {
    width: 1920
    height: 1080

    visible: true
    title: "Planet Dance"

    FontLoader {
        id: customFontLoader
        source: "file:///C:/Users/brandonramirez/Documents/unrhackathon2024/assets/font/VT323-Regular.ttf"
    }

    Loader {
        id: screenLoader
        anchors.fill: parent
        source: "./screens/main_menu.ui.qml"
    }
}
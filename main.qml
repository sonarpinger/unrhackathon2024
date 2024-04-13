// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick 6.5
import guiqmls

Window {
    width: mainScreen.width
    height: mainScreen.height

    visible: true
    title: "Planet Dance"

    Screen01 {
        id: mainScreen
    }

    Screen01 {
        id: mainScreen1
        border.width: 0
    }

}
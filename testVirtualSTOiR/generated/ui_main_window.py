/********************************************************************************
** Form generated from reading UI file 'main_window.ui'
**
** Created by: Qt User Interface Compiler version 5.11.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAIN_WINDOW_H
#define UI_MAIN_WINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *Load;
    QAction *ZoomIn;
    QAction *ZoomOut;
    QAction *actionOpenReestr;
    QAction *actionSchema;
    QAction *actionUpdate;
    QAction *actionEditorMode;
    QAction *actionAddSensorPoint;
    QWidget *centralwidget;
    QVBoxLayout *verticalLayout;
    QScrollArea *scrollArea;
    QWidget *scrollAreaWidgetContents;
    QLabel *schema_label;
    QStatusBar *statusbar;
    QMenuBar *menubar;
    QMenu *Schema;
    QMenu *View;
    QToolBar *toolBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(727, 600);
        Load = new QAction(MainWindow);
        Load->setObjectName(QStringLiteral("Load"));
        ZoomIn = new QAction(MainWindow);
        ZoomIn->setObjectName(QStringLiteral("ZoomIn"));
        ZoomOut = new QAction(MainWindow);
        ZoomOut->setObjectName(QStringLiteral("ZoomOut"));
        actionOpenReestr = new QAction(MainWindow);
        actionOpenReestr->setObjectName(QStringLiteral("actionOpenReestr"));
        actionSchema = new QAction(MainWindow);
        actionSchema->setObjectName(QStringLiteral("actionSchema"));
        actionUpdate = new QAction(MainWindow);
        actionUpdate->setObjectName(QStringLiteral("actionUpdate"));
        actionEditorMode = new QAction(MainWindow);
        actionEditorMode->setObjectName(QStringLiteral("actionEditorMode"));
        actionEditorMode->setCheckable(true);
        actionAddSensorPoint = new QAction(MainWindow);
        actionAddSensorPoint->setObjectName(QStringLiteral("actionAddSensorPoint"));
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QStringLiteral("centralwidget"));
        verticalLayout = new QVBoxLayout(centralwidget);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        scrollArea = new QScrollArea(centralwidget);
        scrollArea->setObjectName(QStringLiteral("scrollArea"));
        scrollArea->setWidgetResizable(false);
        scrollAreaWidgetContents = new QWidget();
        scrollAreaWidgetContents->setObjectName(QStringLiteral("scrollAreaWidgetContents"));
        scrollAreaWidgetContents->setGeometry(QRect(0, 0, 116, 80));
        schema_label = new QLabel(scrollAreaWidgetContents);
        schema_label->setObjectName(QStringLiteral("schema_label"));
        schema_label->setGeometry(QRect(20, 30, 58, 18));
        scrollArea->setWidget(scrollAreaWidgetContents);

        verticalLayout->addWidget(scrollArea);

        MainWindow->setCentralWidget(centralwidget);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QStringLiteral("statusbar"));
        MainWindow->setStatusBar(statusbar);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QStringLiteral("menubar"));
        menubar->setGeometry(QRect(0, 0, 727, 30));
        Schema = new QMenu(menubar);
        Schema->setObjectName(QStringLiteral("Schema"));
        View = new QMenu(menubar);
        View->setObjectName(QStringLiteral("View"));
        MainWindow->setMenuBar(menubar);
        toolBar = new QToolBar(MainWindow);
        toolBar->setObjectName(QStringLiteral("toolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, toolBar);
        MainWindow->insertToolBarBreak(toolBar);

        menubar->addAction(Schema->menuAction());
        menubar->addAction(View->menuAction());
        Schema->addAction(Load);
        View->addAction(ZoomIn);
        View->addAction(ZoomOut);
        toolBar->addAction(actionOpenReestr);
        toolBar->addAction(actionSchema);
        toolBar->addAction(actionUpdate);
        toolBar->addAction(actionEditorMode);
        toolBar->addAction(actionAddSensorPoint);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "\320\241\320\242\320\236\320\270\320\240 \320\241\321\205\320\265\320\274\320\260", nullptr));
        Load->setText(QApplication::translate("MainWindow", "\320\227\320\260\320\263\321\200\321\203\320\267\320\270\321\202\321\214", nullptr));
        ZoomIn->setText(QApplication::translate("MainWindow", "\320\243\320\262\320\265\320\273\320\270\321\207\320\270\321\202\321\214", nullptr));
        ZoomOut->setText(QApplication::translate("MainWindow", "\320\243\320\274\320\265\320\275\321\214\321\210\320\270\321\202\321\214", nullptr));
        actionOpenReestr->setText(QApplication::translate("MainWindow", "\320\240\320\265\320\265\321\201\321\202\321\200 \320\276\320\261\320\276\321\200\321\203\320\264\320\276\320\262\320\260\320\275\320\270\321\217 \320\232\320\230\320\237\320\270\320\220", nullptr));
        actionSchema->setText(QApplication::translate("MainWindow", "\320\241\321\205\320\265\320\274\320\260", nullptr));
        actionUpdate->setText(QApplication::translate("MainWindow", "\320\236\320\261\320\275\320\276\320\262\320\270\321\202\321\214", nullptr));
        actionEditorMode->setText(QApplication::translate("MainWindow", "\320\240\320\265\320\266\320\270\320\274 \321\200\320\265\320\264\320\260\320\272\321\202\320\276\321\200\320\260", nullptr));
        actionAddSensorPoint->setText(QApplication::translate("MainWindow", "\320\224\320\276\320\261\320\260\320\262\320\270\321\202\321\214 \320\264\320\260\321\202\321\207\320\270\320\272", nullptr));
        schema_label->setText(QString());
        Schema->setTitle(QApplication::translate("MainWindow", "\320\241\321\205\320\265\320\274\320\260", nullptr));
        View->setTitle(QApplication::translate("MainWindow", "\320\237\321\200\320\276\321\201\320\274\320\276\321\202\321\200", nullptr));
        toolBar->setWindowTitle(QApplication::translate("MainWindow", "toolBar", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAIN_WINDOW_H

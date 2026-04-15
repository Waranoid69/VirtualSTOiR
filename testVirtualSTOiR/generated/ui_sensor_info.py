/********************************************************************************
** Form generated from reading UI file 'sensor_info.ui'
**
** Created by: Qt User Interface Compiler version 5.11.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SENSOR_INFO_H
#define UI_SENSOR_INFO_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>

QT_BEGIN_NAMESPACE

class Ui_SensorInfo
{
public:
    QVBoxLayout *verticalLayout;
    QFormLayout *formLayout;
    QLabel *lbl_tag;
    QLabel *lbl_description;
    QLabel *lbl_model_info;
    QLabel *lbl_last_check;
    QLabel *lbl_status;
    QHBoxLayout *horizontalLayout;
    QPushButton *btn_close;
    QPushButton *btn_edit;
    QSpacerItem *horizontalSpacer;

    void setupUi(QDialog *SensorInfo)
    {
        if (SensorInfo->objectName().isEmpty())
            SensorInfo->setObjectName(QStringLiteral("SensorInfo"));
        SensorInfo->resize(448, 220);
        verticalLayout = new QVBoxLayout(SensorInfo);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        formLayout = new QFormLayout();
        formLayout->setObjectName(QStringLiteral("formLayout"));
        lbl_tag = new QLabel(SensorInfo);
        lbl_tag->setObjectName(QStringLiteral("lbl_tag"));
        QFont font;
        font.setFamily(QStringLiteral("Noto Sans"));
        font.setPointSize(15);
        font.setBold(true);
        font.setWeight(75);
        lbl_tag->setFont(font);

        formLayout->setWidget(0, QFormLayout::LabelRole, lbl_tag);

        lbl_description = new QLabel(SensorInfo);
        lbl_description->setObjectName(QStringLiteral("lbl_description"));
        QFont font1;
        font1.setFamily(QStringLiteral("Noto Sans"));
        font1.setPointSize(13);
        font1.setBold(true);
        font1.setWeight(75);
        lbl_description->setFont(font1);
        lbl_description->setWordWrap(true);

        formLayout->setWidget(1, QFormLayout::LabelRole, lbl_description);

        lbl_model_info = new QLabel(SensorInfo);
        lbl_model_info->setObjectName(QStringLiteral("lbl_model_info"));
        lbl_model_info->setFont(font1);

        formLayout->setWidget(2, QFormLayout::LabelRole, lbl_model_info);

        lbl_last_check = new QLabel(SensorInfo);
        lbl_last_check->setObjectName(QStringLiteral("lbl_last_check"));
        lbl_last_check->setFont(font1);

        formLayout->setWidget(3, QFormLayout::LabelRole, lbl_last_check);

        lbl_status = new QLabel(SensorInfo);
        lbl_status->setObjectName(QStringLiteral("lbl_status"));
        lbl_status->setFont(font1);

        formLayout->setWidget(4, QFormLayout::LabelRole, lbl_status);


        verticalLayout->addLayout(formLayout);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        btn_close = new QPushButton(SensorInfo);
        btn_close->setObjectName(QStringLiteral("btn_close"));

        horizontalLayout->addWidget(btn_close);

        btn_edit = new QPushButton(SensorInfo);
        btn_edit->setObjectName(QStringLiteral("btn_edit"));

        horizontalLayout->addWidget(btn_edit);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);


        verticalLayout->addLayout(horizontalLayout);


        retranslateUi(SensorInfo);

        QMetaObject::connectSlotsByName(SensorInfo);
    } // setupUi

    void retranslateUi(QDialog *SensorInfo)
    {
        SensorInfo->setWindowTitle(QApplication::translate("SensorInfo", "\320\230\320\275\321\204\320\276\321\200\320\274\320\260\321\206\320\270\321\217 \320\276 \320\264\320\260\321\202\321\207\320\270\320\272\320\265", nullptr));
        lbl_tag->setText(QApplication::translate("SensorInfo", "\320\232\320\276\320\264 \320\277\320\260\321\200\320\260\320\274\320\265\321\202\321\200\320\260 (TAG):", nullptr));
        lbl_description->setText(QApplication::translate("SensorInfo", "\320\235\320\260\320\270\320\274\320\265\320\275\320\276\320\262\320\260\320\275\320\270\320\265:", nullptr));
        lbl_model_info->setText(QApplication::translate("SensorInfo", "\320\234\320\276\320\264\320\265\320\273\321\214 / \320\237\321\200\320\276\320\270\320\267\320\262\320\276\320\264\320\270\321\202\320\265\320\273\321\214:", nullptr));
        lbl_last_check->setText(QApplication::translate("SensorInfo", "\320\237\320\276\321\201\320\273\320\265\320\264\320\275\321\217\321\217 \320\277\320\276\320\262\320\265\321\200\320\272\320\260:", nullptr));
        lbl_status->setText(QApplication::translate("SensorInfo", "\320\241\321\202\320\260\321\202\321\203\321\201 \320\276\320\261\320\276\321\200\321\203\320\264\320\276\320\262\320\260\320\275\320\270\321\217:", nullptr));
        btn_close->setText(QApplication::translate("SensorInfo", "\320\227\320\260\320\272\321\200\321\213\321\202\321\214", nullptr));
        btn_edit->setText(QApplication::translate("SensorInfo", "\320\240\320\265\320\264\320\260\320\272\321\202\320\270\321\200\320\276\320\262\320\260\321\202\321\214", nullptr));
    } // retranslateUi

};

namespace Ui {
    class SensorInfo: public Ui_SensorInfo {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SENSOR_INFO_H

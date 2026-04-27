/********************************************************************************
** Form generated from reading UI file 'registry.ui'
**
** Created by: Qt User Interface Compiler version 5.11.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_REGISTRY_H
#define UI_REGISTRY_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QTableView>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Registry
{
public:
    QVBoxLayout *verticalLayout_2;
    QGroupBox *groupBox;
    QHBoxLayout *horizontalLayout;
    QLabel *label;
    QLineEdit *lineEdit;
    QPushButton *btn_search;
    QTableView *equipment_table;
    QVBoxLayout *verticalLayout;
    QLabel *label_2;
    QHBoxLayout *horizontalLayout_2;
    QPushButton *btn_add;
    QPushButton *pushButton;
    QSpacerItem *horizontalSpacer;

    void setupUi(QWidget *Registry)
    {
        if (Registry->objectName().isEmpty())
            Registry->setObjectName(QStringLiteral("Registry"));
        Registry->resize(623, 437);
        verticalLayout_2 = new QVBoxLayout(Registry);
        verticalLayout_2->setObjectName(QStringLiteral("verticalLayout_2"));
        groupBox = new QGroupBox(Registry);
        groupBox->setObjectName(QStringLiteral("groupBox"));
        QFont font;
        font.setPointSize(12);
        font.setItalic(true);
        groupBox->setFont(font);
        horizontalLayout = new QHBoxLayout(groupBox);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        label = new QLabel(groupBox);
        label->setObjectName(QStringLiteral("label"));

        horizontalLayout->addWidget(label);

        lineEdit = new QLineEdit(groupBox);
        lineEdit->setObjectName(QStringLiteral("lineEdit"));

        horizontalLayout->addWidget(lineEdit);

        btn_search = new QPushButton(groupBox);
        btn_search->setObjectName(QStringLiteral("btn_search"));

        horizontalLayout->addWidget(btn_search);


        verticalLayout_2->addWidget(groupBox);

        equipment_table = new QTableView(Registry);
        equipment_table->setObjectName(QStringLiteral("equipment_table"));
        equipment_table->setAlternatingRowColors(true);
        equipment_table->setSortingEnabled(true);

        verticalLayout_2->addWidget(equipment_table);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        label_2 = new QLabel(Registry);
        label_2->setObjectName(QStringLiteral("label_2"));
        QFont font1;
        font1.setPointSize(14);
        label_2->setFont(font1);

        verticalLayout->addWidget(label_2);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName(QStringLiteral("horizontalLayout_2"));
        btn_add = new QPushButton(Registry);
        btn_add->setObjectName(QStringLiteral("btn_add"));

        horizontalLayout_2->addWidget(btn_add);

        pushButton = new QPushButton(Registry);
        pushButton->setObjectName(QStringLiteral("pushButton"));

        horizontalLayout_2->addWidget(pushButton);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer);


        verticalLayout->addLayout(horizontalLayout_2);


        verticalLayout_2->addLayout(verticalLayout);


        retranslateUi(Registry);

        QMetaObject::connectSlotsByName(Registry);
    } // setupUi

    void retranslateUi(QWidget *Registry)
    {
        Registry->setWindowTitle(QApplication::translate("Registry", "\320\240\320\265\320\265\321\201\321\202\321\200 \320\276\320\261\320\276\321\200\321\203\320\264\320\276\320\262\320\260\320\275\320\270\321\217 \320\232\320\230\320\237\320\270\320\220", nullptr));
        groupBox->setTitle(QApplication::translate("Registry", "\320\244\320\270\320\273\321\214\321\202\321\200\321\213 \320\270 \320\277\320\276\320\270\321\201\320\272", nullptr));
        label->setText(QApplication::translate("Registry", "\320\237\320\276\320\270\321\201\320\272 \320\277\320\276 TAG", nullptr));
        btn_search->setText(QApplication::translate("Registry", "\320\235\320\260\320\271\321\202\320\270", nullptr));
        label_2->setText(QApplication::translate("Registry", "\320\222\321\201\320\265\320\263\320\276 \320\267\320\260\320\277\320\270\321\201\320\265\320\271 \320\262 \320\261\320\260\320\267\320\265 : 0", nullptr));
        btn_add->setText(QApplication::translate("Registry", "\320\224\320\276\320\261\320\260\320\262\320\270\321\202\321\214 \320\275\320\276\320\262\321\213\320\271 \320\277\321\200\320\270\320\261\320\276\321\200", nullptr));
        pushButton->setText(QApplication::translate("Registry", "\320\241\320\276\321\205\321\200\320\260\320\275\320\270\321\202\321\214 \320\270\320\267\320\274\320\265\320\275\320\265\320\275\320\270\321\217", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Registry: public Ui_Registry {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_REGISTRY_H

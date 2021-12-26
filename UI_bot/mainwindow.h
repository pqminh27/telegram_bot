#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QFile>
#include <QtSql>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_sendButton_clicked();
    void on_pushButton_clicked();
    void on_removeButton_clicked();

private:
    Ui::MainWindow *ui;
    QSqlQueryModel* m_model;
    QSqlDatabase m_db;
    QStringList receiverList;
};
#endif // MAINWINDOW_H

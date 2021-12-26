#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QString>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    m_db = QSqlDatabase::addDatabase("QPSQL");
    m_db.setDatabaseName("fn1131_2021");
    m_db.setHostName("195.19.32.74");
    m_db.setPort(5432);
    m_db.setUserName("student");
    m_db.setPassword("bmstu");

    if(m_db.open()) {
        m_model = new QSqlQueryModel(this);
        QString command = "SELECT name, chat_id FROM bot_users";
        m_model->setQuery(command,m_db);
        ui->userTableView->setModel(m_model);
    }
    else {
        qDebug() << "Error while connecting to database server";
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_sendButton_clicked()
{
    QSqlQuery msg;
    foreach(auto receiver, static_cast<QStringListModel*>(ui->receiverListView->model())->stringList()) {
        qDebug() << receiver;
        QString command = "INSERT INTO bot_users_msg(receiver_name,msg,state) VALUES('"+receiver+"'::text, '"
                +ui->msgEdit->toPlainText() + "'::text, 'queued'::STATE_MSG)";
        msg.exec(command);
        if(msg.lastError().isValid()) {
            ui->errorLabel->setText("Error: "+msg.lastError().text());
        }
        else ui->errorLabel->setText("Message sending: success");
    }
}

void MainWindow::on_pushButton_clicked() {
    auto receiverListIndex = ui->userTableView->selectionModel()->selectedIndexes();
    foreach(auto idx, receiverListIndex) {
    QModelIndex name_idx = ui->userTableView->model()->index(idx.row(),0);
        if(!receiverList.contains(ui->userTableView->model()->data(name_idx).toString()))
            receiverList << ui->userTableView->model()->data(name_idx).toString();
    }
    ui->receiverListView->setModel(new QStringListModel(receiverList));
}

void MainWindow::on_removeButton_clicked() {
    auto removeReceiverListIndex = ui->receiverListView->selectionModel()->selectedIndexes();
    foreach(auto idx, removeReceiverListIndex) {
        auto name_idx = ui->receiverListView->model()->index(idx.row(),idx.column());
        auto name_ = ui->receiverListView->model()->data(name_idx).toString();
        receiverList.removeAll(name_);
    }
    ui->receiverListView->setModel(new QStringListModel(receiverList));
}

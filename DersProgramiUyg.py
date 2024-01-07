import sys
from PyQt5.QtWidgets import QApplication,QMessageBox,QHBoxLayout, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDialog
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

conn = sqlite3.connect('ders_programi.db')  #https://derslik.kerteriz.net/python-dersleri/veritabani-islemleri/python-sqlite-veritabani

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dersler (
        Hoca_ID INTEGER,
        Ders_Adı TEXT,
        Gün TEXT,
        Saat TEXT,
        Sınıf TEXT,
        CONSTRAINT unique_kisit UNIQUE (Gün, Saat, Sınıf)
    )
''')

conn.commit()

conn.close()

class DersSilDialog(QDialog):  #https://build-system.fman.io/pyqt5-tutorial
    def __init__(self, parent=None, secili_satir=None):
        super().__init__(parent)

        self.secili_satir = secili_satir

        self.setWindowTitle('Ders Silme')
        self.layout = QVBoxLayout()

        self.label_silme_onay = QLabel(f"Dersi silmek istediğinizden emin misiniz?\nDers: {secili_satir[1]}, Gün: {secili_satir[2]}, Saat: {secili_satir[3]}, Sınıf: {secili_satir[4]}")

        self.button_sil = QPushButton('Dersi Sil', self)
        self.button_sil.clicked.connect(self.ders_sil)

        self.layout.addWidget(self.label_silme_onay)
        self.layout.addWidget(self.button_sil)

        self.setLayout(self.layout)

    def ders_sil(self):
        try:
            conn = sqlite3.connect('ders_programi.db')
            cursor = conn.cursor()

            cursor.execute("DELETE FROM Dersler WHERE Gün=? AND Saat=? AND Sınıf=?", (self.secili_satir[2], self.secili_satir[3], self.secili_satir[4]))

            conn.commit()
            QMessageBox.information(self, 'Başarı', 'Ders silindi.')

        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Hata: {e}')

        finally:
            conn.close()

        self.accept()

class DersGuncelleDialog(QDialog):  #https://build-system.fman.io/pyqt5-tutorial
    def __init__(self, parent=None, secili_satir=None):
        super().__init__(parent)

        self.secili_satir = secili_satir

        self.setWindowTitle('Ders Güncelleme')
        self.layout = QVBoxLayout()

        self.label_hoca_id = QLabel('Yeni Hoca ID:')
        self.edit_hoca_id = QLineEdit(self)

        self.label_ders_adi = QLabel('Yeni Ders Adı:')
        self.edit_ders_adi = QLineEdit(self)

        self.label_gun = QLabel('Yeni Gün:')
        self.edit_gun = QLineEdit(self)

        self.label_saat = QLabel('Yeni Saat:')
        self.edit_saat = QLineEdit(self)

        self.label_sinif = QLabel('Yeni Sınıf:')
        self.edit_sinif = QLineEdit(self)

        self.button_guncelle = QPushButton('Dersi Güncelle', self)
        self.button_guncelle.clicked.connect(self.ders_guncelle)

        self.layout.addWidget(self.label_hoca_id)
        self.layout.addWidget(self.edit_hoca_id)
        self.layout.addWidget(self.label_ders_adi)
        self.layout.addWidget(self.edit_ders_adi)
        self.layout.addWidget(self.label_gun)
        self.layout.addWidget(self.edit_gun)
        self.layout.addWidget(self.label_saat)
        self.layout.addWidget(self.edit_saat)
        self.layout.addWidget(self.label_sinif)
        self.layout.addWidget(self.edit_sinif)
        self.layout.addWidget(self.button_guncelle)

        self.setLayout(self.layout)

        if secili_satir:
            self.edit_hoca_id.setText(str(secili_satir[0]))
            self.edit_ders_adi.setText(secili_satir[1])
            self.edit_gun.setText(secili_satir[2])
            self.edit_saat.setText(secili_satir[3])
            self.edit_sinif.setText(secili_satir[4])

    def ders_guncelle(self):
        hoca_id = int(self.edit_hoca_id.text())
        ders_adi = self.edit_ders_adi.text()
        gun = self.edit_gun.text()
        saat = self.edit_saat.text()
        sinif = self.edit_sinif.text()

        try:
            conn = sqlite3.connect('ders_programi.db')
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE Dersler SET Hoca_ID=?, Ders_Adı=?, Gün=?, Saat=?, Sınıf=? WHERE Gün=? AND Saat=? AND Sınıf=?",
                (hoca_id, ders_adi, gun, saat, sinif, self.secili_satir[2], self.secili_satir[3], self.secili_satir[4]))

            conn.commit()
            QMessageBox.information(self, 'Başarı', 'Ders güncellendi.')

        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Hata: {e}')

        finally:
            conn.close()

        self.accept()

class DersEkleUygulamasi(QWidget):  #https://build-system.fman.io/pyqt5-tutorial
    def __init__(self, ders_programi_uygulamasi):
        super().__init__()

        self.ders_programi_uygulamasi = ders_programi_uygulamasi

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Ders Ekleme Uygulaması')

        self.label_hoca_id = QLabel('Hoca ID:')
        self.edit_hoca_id = QLineEdit(self)

        self.label_ders_adi = QLabel('Ders Adı:')
        self.edit_ders_adi = QLineEdit(self)

        self.label_gun = QLabel('Gün:')
        self.edit_gun = QLineEdit(self)

        self.label_saat = QLabel('Saat:')
        self.edit_saat = QLineEdit(self)

        self.label_sinif = QLabel('Sınıf:')
        self.edit_sinif = QLineEdit(self)

        self.button_ekle = QPushButton('Ders Ekle', self)
        self.button_ekle.clicked.connect(self.ders_ekle)


        vbox = QVBoxLayout()
        vbox.addWidget(self.label_hoca_id)
        vbox.addWidget(self.edit_hoca_id)
        vbox.addWidget(self.label_ders_adi)
        vbox.addWidget(self.edit_ders_adi)
        vbox.addWidget(self.label_gun)
        vbox.addWidget(self.edit_gun)
        vbox.addWidget(self.label_saat)
        vbox.addWidget(self.edit_saat)
        vbox.addWidget(self.label_sinif)
        vbox.addWidget(self.edit_sinif)
        vbox.addWidget(self.button_ekle)

        self.setLayout(vbox)

    def ders_ekle(self):  #https://derslik.kerteriz.net/python-dersleri/veritabani-islemleri/python-sqlite-veritabani
        hoca_id = int(self.edit_hoca_id.text())
        ders_adi = self.edit_ders_adi.text()
        gun = self.edit_gun.text()
        saat = self.edit_saat.text()
        sinif = self.edit_sinif.text()

        conn = sqlite3.connect('ders_programi.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Dersler WHERE Hoca_ID = ? AND Gün = ? AND Saat = ?", (hoca_id, gun, saat))
        ayni_hoca_sayisi = cursor.fetchone()[0]

        if ayni_hoca_sayisi == 0:
            cursor.execute("SELECT COUNT(*) FROM Dersler WHERE Gün = ? AND Saat = ? AND Sınıf = ?", (gun, saat, sinif))
            ayni_sinif_zaman = cursor.fetchone()[0]

            if ayni_sinif_zaman == 0:
                cursor.execute("INSERT INTO Dersler (Hoca_ID, Ders_Adı, Gün, Saat, Sınıf) VALUES (?, ?, ?, ?, ?)",
                               (hoca_id, ders_adi, gun, saat, sinif))
                conn.commit()
                QMessageBox.information(self, 'Başarı', f'{ders_adi} dersi eklendi.')
                self.ders_programi_uygulamasi.guncelle_ders_programi()
            else:
                QMessageBox.warning(self, 'Hata', 'Bu saat ve gün için bu sınıfta ders zaten var.')
        else:
            QMessageBox.warning(self, 'Hata', 'Bu saat ve gün için bu öğretmenin başka bir dersi zaten var.')

        conn.close()

        self.ders_programi_uygulamasi.guncelle_ders_programi()

    def sil_secili_ders(self):
        secili_satir = self.table.currentItem().row() if self.table.currentItem() else None

        if secili_satir is not None:
            secili_veri = [self.table.item(secili_satir, i).text() for i in range(self.table.columnCount())]
            dialog = DersSilDialog(self, secili_veri)

            if dialog.exec_() == QDialog.Accepted:
                self.guncelle_ders_programi()

class DersProgramiUygulamasi(QWidget): #https://build-system.fman.io/pyqt5-tutorial
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Ders Programı')

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Hoca ID', 'Ders Adı', 'Gün', 'Saat', 'Sınıf'])

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.canvas)

        self.button_guncelle_secili = QPushButton('Güncelle', self)
        self.button_guncelle_secili.clicked.connect(self.guncelle_secili_ders)
        self.layout.addWidget(self.button_guncelle_secili)

        self.button_sil_secili = QPushButton('Sil', self)
        self.button_sil_secili.clicked.connect(self.sil_secili_ders)

        hbox = QHBoxLayout()
        hbox.addWidget(self.button_guncelle_secili)
        hbox.addWidget(self.button_sil_secili)

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.canvas)
        self.layout.addLayout(hbox)

        self.setLayout(self.layout)

        self.guncelle_ders_programi()
        # Ders Ekleme Butonu
        self.button_ders_ekle = QPushButton('Ders Ekle', self)
        self.button_ders_ekle.clicked.connect(self.toggle_ders_ekle_uygulamasi)

        self.layout.addWidget(self.button_ders_ekle)

        self.ders_ekle_uygulamasi = DersEkleUygulamasi(self)
        self.ders_ekle_uygulamasi.hide()

    def toggle_ders_ekle_uygulamasi(self):
        if self.ders_ekle_uygulamasi.isHidden():
            self.ders_ekle_uygulamasi.show()
        else:
            self.ders_ekle_uygulamasi.hide()

    def guncelle_secili_ders(self):
        secili_satir = self.table.currentItem().row() if self.table.currentItem() else None

        if secili_satir is not None:
            secili_veri = [self.table.item(secili_satir, i).text() for i in range(self.table.columnCount())]

            dialog = DersGuncelleDialog(self, secili_veri)

            if dialog.exec_() == QDialog.Accepted:
                
                self.guncelle_ders_programi()

    def guncelle_ders_programi(self):
        conn = sqlite3.connect('ders_programi.db')
        cursor = conn.cursor()

        cursor.execute("SELECT Hoca_ID, Ders_Adı, Gün, Saat, Sınıf FROM Dersler")
        dersler = cursor.fetchall()

        conn.close()

        self.table.setRowCount(0)

        for satir_numarasi, satir_verisi in enumerate(dersler):
            self.table.insertRow(satir_numarasi)
            for sutun_numarasi, veri in enumerate(satir_verisi):
                self.table.setItem(satir_numarasi, sutun_numarasi, QTableWidgetItem(str(veri)))

        self.cizgeyi_guncelle(dersler)

    def cizgeyi_guncelle(self, dersler): #https://matplotlib.org/stable/gallery/text_labels_and_annotations/font_file.html#sphx-glr-gallery-text-labels-and-annotations-font-file-py
        self.ax.clear()

        gunler = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma','---']

        for gun in gunler:
            saatler = [f"{i}:00" if i != 18 else '---' for i in range(8, 19)]
            for saat in saatler:
                ders_var_mi = any(ders[2] == gun and ders[3] == saat for ders in dersler)

                if ders_var_mi:
                    renk = 'red'
                    hoca_id = next((ders[0] for ders in dersler if ders[2] == gun and ders[3] == saat), "")
                    self.ax.text(gunler.index(gun) + 0.5, saatler.index(saat) + 0.5, str(hoca_id),
                                 ha='center', va='center', color='white', fontsize=8)
                else:
                    renk = 'green'

                self.ax.add_patch(plt.Rectangle((gunler.index(gun), saatler.index(saat)), 0.6, 0.6, fill=True, color=renk))

        self.ax.set_xticks(range(len(gunler)))
        self.ax.set_yticks(range(len(saatler)))    #https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html#sphx-glr-gallery-images-contours-and-fields-image-annotated-heatmap-py
        self.ax.set_xticklabels(gunler)
        self.ax.set_yticklabels(saatler)

        self.ax.set_xlabel('Gün')
        self.ax.set_ylabel('Saat')

        self.canvas.draw()
    def sil_secili_ders(self):
        secili_satir = self.table.currentItem().row() if self.table.currentItem() else None

        if secili_satir is not None:
            secili_veri = [self.table.item(secili_satir, i).text() for i in range(self.table.columnCount())]
            dialog = DersSilDialog(self, secili_veri)

            if dialog.exec_() == QDialog.Accepted:
                self.guncelle_ders_programi()
if __name__ == '__main__':
    app = QApplication(sys.argv)

    ders_programi_uygulamasi = DersProgramiUygulamasi()
    ders_programi_uygulamasi.show()

    ders_ekle_uygulamasi = DersEkleUygulamasi(ders_programi_uygulamasi)
    ders_ekle_uygulamasi.show()

    sys.exit(app.exec_())
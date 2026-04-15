from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class SensorInfoDialog(QDialog):
    def __init__(self, sensor_data: dict, parent=None):
        super().__init__(parent)
        loadUi("ui/sensor_info.ui", self)

        self.lbl_tag.setText(f"Код параметра (TAG):   {sensor_data.get('TAG', '—')}")
        self.lbl_description.setText(f"Наименование:   {sensor_data.get('Наименование', '—')}")
        self.lbl_model_info.setText(
            f"Модель / Производитель:   "
            f"{sensor_data.get('Модель', '—')} / {sensor_data.get('Производитель', '—')}"
        )
        self.lbl_last_check.setText(f"Последняя поверка:   {sensor_data.get('Дата_поверки', '—')}")
        self.lbl_status.setText(f"Статус оборудования:   {sensor_data.get('Статус', '—')}")

        self.btn_close.clicked.connect(self.close)
        self.btn_edit.clicked.connect(self._open_in_registry)

        self._tag = sensor_data.get("TAG", "")

    def _open_in_registry(self):
        """Сигнал родительскому окну — открыть реестр и выделить строку."""
        self.parent_open_registry_tag = self._tag
        self.accept()
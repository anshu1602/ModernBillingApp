
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QFrame,
    QSplitter,
    QSpacerItem,
    QSizePolicy,
    QComboBox,
)
from PySide6.QtGui import QFont, QLinearGradient
from PySide6.QtCore import Qt, QSize
import mysql.connector
from datetime import datetime

class ModernBillingApp(QMainWindow):
    """A modern billing system application with a GUI built using PySide6."""

    # Constants for styling
    COLORS = {
        "primary": "#3498db",  # Blue
        "secondary": "#2ecc71",  # Green
        "accent": "#9b59b6",  # Purple
        "danger": "#e74c3c",  # Red
        "warning": "#f39c12",  # Orange
        "background": "#f9f9f9",  # Light Gray
        "card": "#ffffff",  # White
        "text": "#2c3e50",  # Dark Blue Gray
        "text_light": "#7f8c8d",  # Gray
        "border": "#ecf0f1",  # Very Light Gray
    }

    # Database configuration
    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "1234",
        "database": "billing_db",
    }

    def __init__(self):
        """Initialize the main window and its components."""
        super().__init__()
        self.setWindowTitle("Elegant Billing System")
        self.setGeometry(100, 100, 1000, 700)

        # Initialize input widgets as instance attributes
        self.name_input = None
        self.phone_input = None
        self.item_input = None
        self.quantity_input = None
        self.price_input = None
        self.payment_method = None

        self._setup_styles()
        self._initialize_database()
        self._setup_ui()
        self.show()

    def _setup_styles(self):
        """Set up the application-wide stylesheet."""
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: %(background)s;
            }
            QLabel {
                color: %(text)s;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid %(border)s;
                border-radius: 5px;
                background-color: white;
                selection-background-color: %(primary)s;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid %(primary)s;
            }
            QPushButton {
                padding: 10px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid %(border)s;
                border-radius: 5px;
                background-color: white;
                selection-background-color: %(primary)s;
                font-size: 14px;
                min-height: 40px;
            }
            QComboBox:focus {
                border: 2px solid %(primary)s;
            }
            QComboBox::drop-down {
                border: 0px;
                width: 30px;
            }
            QTableWidget {
                alternate-background-color: #f5f5f5;
                gridline-color: %(border)s;
                selection-background-color: #e0f2fe;
                selection-color: %(text)s;
                border: none;
                border-radius: 8px;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid %(border)s;
            }
            QHeaderView::section {
                background-color: %(primary)s;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            """ % self.COLORS
        )

    def _setup_ui(self):
        """Set up the main layout and widgets."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.create_header()
        self.create_content_area()
        self.create_footer()

    def _initialize_database(self):
        """Initialize the database connection and create tables if they don't exist."""
        try:
            self.connection = mysql.connector.connect(**self.DB_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS billing_db")
                self.cursor.execute("USE billing_db")
                self.cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS customers (
                        customer_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        phone VARCHAR(20) DEFAULT NULL
                    )
                    """
                )
                self.cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS bills (
                        bill_id INT AUTO_INCREMENT PRIMARY KEY,
                        customer_id INT,
                        item VARCHAR(100) NOT NULL,
                        quantity INT NOT NULL,
                        price DECIMAL(10, 2) NOT NULL,
                        payment_method VARCHAR(50) DEFAULT 'Cash',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                    )
                    """
                )
                print("Database connection successful")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Cannot connect to database: {e}")
            sys.exit(1)

    def create_header(self):
        """Create the header section with title and date."""
        header_container = QWidget()
        header_container.setFixedHeight(80)
        header_container.setStyleSheet(
            f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                      stop:0 {self.COLORS['primary']},
                                      stop:1 {self.COLORS['accent']});
            border-radius: 10px;
            margin-bottom: 10px;
            """
        )

        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(20, 0, 20, 0)

        app_title = QLabel("Elegant Billing System")
        app_title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        app_title.setStyleSheet("color: white;")
        header_layout.addWidget(app_title)

        current_date = QLabel(datetime.now().strftime("%B %d, %Y"))
        current_date.setFont(QFont("Segoe UI", 12))
        current_date.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        current_date.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        header_layout.addWidget(current_date)

        self.main_layout.addWidget(header_container)

    def create_content_area(self):
        """Create the main content area with form and table."""
        content_container = QSplitter(Qt.Horizontal)
        self.create_billing_form(content_container)
        self.create_bills_table(content_container)
        content_container.setSizes([350, 650])
        self.main_layout.addWidget(content_container, 1)

    def create_footer(self):
        """Create the footer section with status and version."""
        footer = QFrame()
        footer.setFrameShape(QFrame.StyledPanel)
        footer.setStyleSheet(
            f"""
            background-color: {self.COLORS['background']};
            border-radius: 5px;
            padding: 10px;
            """
        )
        footer.setFixedHeight(40)

        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(10, 0, 10, 0)

        status_label = QLabel("Ready")
        status_label.setStyleSheet(f"color: {self.COLORS['text_light']};")
        footer_layout.addWidget(status_label)

        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignRight)
        version_label.setStyleSheet(f"color: {self.COLORS['text_light']};")
        footer_layout.addWidget(version_label)

        self.main_layout.addWidget(footer)

    def create_billing_form(self, parent):
        """Create the billing form widget."""
        form_container = QWidget()
        form_container.setStyleSheet(
            f"""
            background-color: {self.COLORS['card']};
            border-radius: 10px;
            padding: 0px;
            """
        )

        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(20)

        # Form title
        title_layout = QHBoxLayout()
        form_icon = QLabel("📝")
        form_icon.setFont(QFont("Segoe UI", 20))
        title_layout.addWidget(form_icon)

        form_title = QLabel("New Transaction")
        form_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        form_title.setStyleSheet(f"color: {self.COLORS['primary']};")
        title_layout.addWidget(form_title)
        title_layout.addStretch()
        form_layout.addLayout(title_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"background-color: {self.COLORS['border']}; margin: 0 0 10px 0;")
        form_layout.addWidget(separator)

        # Form fields
        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(15)
        self._add_form_field(fields_layout, "Customer Name", self.name_input)
        self._add_form_field(fields_layout, "Phone Number", self.phone_input)
        self._add_form_field(fields_layout, "Item", self.item_input)
        self._add_quantity_price_fields(fields_layout)
        self._add_payment_method(fields_layout)

        form_layout.addLayout(fields_layout)
        form_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        form_layout.addLayout(self._create_action_buttons())
        parent.addWidget(form_container)

    def _add_form_field(self, layout, label_text, input_widget):
        """Add a labeled input field to the layout."""
        field_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setFont(QFont("Segoe UI", 12))
        field_layout.addWidget(label)
        if input_widget is None:
            input_widget = QLineEdit()
            setattr(self, f"{label_text.lower().replace(' ', '_')}_input", input_widget)
        input_widget.setPlaceholderText(f"Enter {label_text.lower()}")
        input_widget.setMinimumHeight(40)
        field_layout.addWidget(input_widget)
        layout.addLayout(field_layout)

    def _add_quantity_price_fields(self, layout):
        """Add quantity and price fields in a horizontal layout."""
        qty_price_layout = QHBoxLayout()
        self._add_form_field(qty_price_layout, "Quantity", self.quantity_input)
        self._add_form_field(qty_price_layout, "Price (₹)", self.price_input)
        layout.addLayout(qty_price_layout)

    def _add_payment_method(self, layout):
        """Add payment method dropdown to the layout."""
        payment_layout = QVBoxLayout()
        self.payment_label = QLabel("Payment Method")
        self.payment_label.setFont(QFont("Segoe UI", 12))
        payment_layout.addWidget(self.payment_label)
        if self.payment_method is None:
            self.payment_method = QComboBox()
            self.payment_method.addItems(["Cash", "Credit Card", "Debit Card", "Scanner", "UPI"])
            self.payment_method.setMinimumHeight(40)
        payment_layout.addWidget(self.payment_method)
        layout.addLayout(payment_layout)

    def _create_action_buttons(self):
        """Create and return the action buttons layout."""
        button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear")
        self.clear_button.setStyleSheet(
            f"""
            background-color: {self.COLORS['text_light']};
            color: white;
            min-width: 100px;
            """
        )
        self.clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_button)

        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(
            f"""
            background-color: {self.COLORS['secondary']};
            color: white;
            min-width: 100px;
            """
        )
        self.save_button.clicked.connect(self.save_bill)
        button_layout.addWidget(self.save_button)
        return button_layout

    def create_bills_table(self, parent):
        """Create the bills table widget."""
        table_container = QWidget()
        table_container.setStyleSheet(
            f"""
            background-color: {self.COLORS['card']};
            border-radius: 10px;
            """
        )

        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(20, 20, 20, 20)
        table_layout.setSpacing(15)

        # Table header
        header_layout = QHBoxLayout()
        table_icon = QLabel("🧾")
        table_icon.setFont(QFont("Segoe UI", 20))
        header_layout.addWidget(table_icon)

        table_title = QLabel("Recent Transactions")
        table_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        table_title.setStyleSheet(f"color: {self.COLORS['primary']};")
        header_layout.addWidget(table_title)

        header_layout.addStretch()
        refresh_button = QPushButton("Refresh")
        refresh_button.setStyleSheet(
            f"""
            background-color: {self.COLORS['primary']};
            color: white;
            padding: 5px 15px;
            """
        )
        refresh_button.clicked.connect(self.view_bills)
        header_layout.addWidget(refresh_button)
        table_layout.addLayout(header_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"background-color: {self.COLORS['border']}; margin: 0 0 10px 0;")
        table_layout.addWidget(separator)

        # Table setup
        self.bills_table = QTableWidget()
        self.bills_table.setColumnCount(8)
        self.bills_table.setHorizontalHeaderLabels(
            ["ID", "Customer", "Phone", "Item", "Qty", "Price", "Payment", "Total"]
        )
        self.bills_table.setAlternatingRowColors(True)
        self.bills_table.verticalHeader().setVisible(False)
        self.bills_table.setShowGrid(False)
        self.bills_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.bills_table.setSortingEnabled(True)

        # Configure column widths
        header = self.bills_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)

        self.bills_table.verticalHeader().setDefaultSectionSize(40)
        table_layout.addWidget(self.bills_table)

        # Summary section
        summary_frame = QFrame()
        summary_frame.setStyleSheet(
            f"""
            background-color: {self.COLORS['background']};
            border-radius: 5px;
            padding: 10px;
            """
        )

        summary_layout = QHBoxLayout(summary_frame)
        self.transactions_label = QLabel("Total Transactions: 0")
        self.transactions_label.setFont(QFont("Segoe UI", 11))
        summary_layout.addWidget(self.transactions_label)

        summary_layout.addStretch()
        self.revenue_label = QLabel("Total Revenue: ₹0.00")
        self.revenue_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.revenue_label.setStyleSheet(f"color: {self.COLORS['secondary']};")
        summary_layout.addWidget(self.revenue_label)

        table_layout.addWidget(summary_frame)
        parent.addWidget(table_container)
        self.view_bills()

    def save_bill(self):
        """Save a new bill to the database."""
        data = {
            "name": self.name_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "item": self.item_input.text().strip(),
            "quantity": self.quantity_input.text().strip(),
            "price": self.price_input.text().strip(),
            "payment_method": self.payment_method.currentText(),
        }

        if not all([data["name"], data["item"], data["quantity"], data["price"]]):
            QMessageBox.warning(self, "Input Required", "Please fill all required fields before saving!")
            return

        try:
            quantity_val = int(data["quantity"])
            price_val = float(data["price"])
            if quantity_val <= 0 or price_val <= 0:
                QMessageBox.warning(self, "Invalid Input", "Quantity and Price must be positive values!")
                return

            try:
                self.cursor.execute("INSERT INTO customers (name, phone) VALUES (%s, %s)", (data["name"], data["phone"]))
                self.connection.commit()
                customer_id = self.cursor.lastrowid

                self.cursor.execute(
                    """
                    INSERT INTO bills (customer_id, item, quantity, price, payment_method)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (customer_id, data["item"], quantity_val, price_val, data["payment_method"]),
                )
                self.connection.commit()

                self.show_success_message("Transaction saved successfully!")
                self.clear_form()
                self.view_bills()
            except mysql.connector.Error as e:
                self.connection.rollback()
                QMessageBox.critical(self, "Database Error", f"Could not save transaction: {e}")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for quantity and price!")

    def view_bills(self):
        """Retrieve and display all bills in the table."""
        try:
            self.cursor.execute(
                """
                SELECT b.bill_id, c.name, c.phone, b.item, b.quantity, b.price, b.payment_method, b.price * b.quantity as total
                FROM bills b
                JOIN customers c ON b.customer_id = c.customer_id
                ORDER BY b.bill_id DESC
                """
            )
            bills = self.cursor.fetchall()

            self.bills_table.setRowCount(0)
            total_revenue = 0

            for row_index, bill in enumerate(bills):
                self.bills_table.insertRow(row_index)
                self._add_table_item(row_index, 0, str(bill[0]), Qt.AlignCenter)
                self._add_table_item(row_index, 1, str(bill[1]))
                self._add_table_item(row_index, 2, str(bill[2] if bill[2] else ""))
                self._add_table_item(row_index, 3, str(bill[3]))
                self._add_table_item(row_index, 4, str(bill[4]), Qt.AlignCenter)
                self._add_table_item(row_index, 5, f"₹{bill[5]:.2f}", Qt.AlignRight | Qt.AlignVCenter)
                self._add_table_item(row_index, 6, str(bill[6]), Qt.AlignCenter)
                self._add_table_item(
                    row_index, 7, f"₹{bill[7]:.2f}", Qt.AlignRight | Qt.AlignVCenter, QFont("Segoe UI", 9, QFont.Bold)
                )
                total_revenue += bill[7]

            self.transactions_label.setText(f"Total Transactions: {len(bills)}")
            self.revenue_label.setText(f"Total Revenue: ₹{total_revenue:.2f}")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Could not retrieve transactions: {e}")

    def _add_table_item(self, row, col, text, alignment=Qt.AlignLeft, font=None):
        """Add an item to the table with specified alignment and font."""
        item = QTableWidgetItem(text)
        item.setTextAlignment(alignment)
        if font:
            item.setFont(font)
        self.bills_table.setItem(row, col, item)

    def clear_form(self):
        """Clear all input fields and reset the form."""
        for widget in [self.name_input, self.phone_input, self.item_input, self.quantity_input, self.price_input]:
            widget.clear()
        self.payment_method.setCurrentIndex(0)  # Reset to "Cash"
        self.name_input.setFocus()

    def show_success_message(self, message):
        """Display a success message box."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Success")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet(
            f"""
            QMessageBox {
                background-color: {self.COLORS['card']};
                color: {self.COLORS['text']};
            }
            QPushButton {
                background-color: {self.COLORS['primary']};
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            """
        )
        msg.exec()

    def closeEvent(self, event):
        """Handle window close event to clean up database connections."""
        if hasattr(self, "connection") and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernBillingApp()
    sys.exit(app.exec())
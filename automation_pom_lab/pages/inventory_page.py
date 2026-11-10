from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page Object untuk halaman Inventori/Katalog Produk Saucedemo."""

    # Relative XPath Selectors
    ADD_BACKPACK_BTN = (
        By.XPATH,
        "//button[contains(@data-test, 'add-to-cart-sauce-labs-backpack')]",
    )
    CART_BADGE = (By.XPATH, "//span[contains(@class, 'shopping_cart_badge')]")
    BURGER_MENU_BTN = (By.XPATH, "//button[@id='react-burger-menu-btn']")
    LOGOUT_LINK = (By.XPATH, "//a[@id='logout_sidebar_link']")

    def __init__(self, driver):
        super().__init__(driver)

    def add_backpack_to_cart(self):
        """Menambahkan produk Sauce Labs Backpack ke keranjang."""
        self.click(self.ADD_BACKPACK_BTN)

    def get_cart_badge_count(self) -> str:
        """Mengambil teks angka jumlah barang dari badge keranjang belanja."""
        return self.get_text(self.CART_BADGE)

    def logout(self):
        """Membuka menu samping lalu klik Logout setelah animasi selesai."""
        self.click(self.BURGER_MENU_BTN)
        logout_elem = self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))
        logout_elem.click()
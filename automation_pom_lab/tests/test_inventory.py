import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestInventory:
    """Kumpulan kasus uji fungsional untuk halaman inventori produk."""

    def test_add_to_cart_flow(self, driver):
        """TC-INV-01: Verifikasi penambahan produk ke keranjang."""
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory_page.add_backpack_to_cart()

        actual_badge_text = inventory_page.get_cart_badge_count()
        assert actual_badge_text == "1", (
            f"Jumlah keranjang tidak sesuai. Diharapkan '1', tetapi "
            f"diterima '{actual_badge_text}'"
        )

    def test_sort_name_za(self, driver):
        """TC-INV-03: Verifikasi pengurutan produk berdasarkan nama Z ke A."""
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory_page.select_sort_option("za")

        first_product = inventory_page.get_first_product_name()
        assert first_product == "Test.allTheThings() T-Shirt (Red)", (
            f"Sorting Z-A gagal. Produk pertama adalah '{first_product}'"
        )

    def test_sort_price_low_to_high(self, driver):
        """TC-INV-04: Verifikasi pengurutan produk harga terendah ke tertinggi."""
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory_page.select_sort_option("lohi")

        first_product = inventory_page.get_first_product_name()
        assert first_product == "Sauce Labs Onesie", (
            f"Sorting Low-to-High gagal. Produk pertama adalah '{first_product}'"
        )

    def test_verify_inventory_page_loaded(self, driver):
        """TC-INV-05: Verifikasi halaman katalog produk berhasil diakses sempurna."""
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        assert login_page.is_dashboard_displayed() is True, (
            "Halaman inventori produk gagal dimuat!"
        )

    def test_logout_flow(self, driver):
        """TC-INV-02: Verifikasi alur pengakhiran sesi (Logout)."""
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory_page.logout()

        WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/"))
        actual_url = login_page.get_current_url()

        assert actual_url.rstrip("/") == "https://www.saucedemo.com", (
            f"URL setelah logout tidak sesuai. Berada di '{actual_url}'"
        )
        assert login_page.find_element(login_page.LOGIN_BUTTON).is_displayed(), (
            "Tombol login tidak tampil setelah proses logout!"
        )
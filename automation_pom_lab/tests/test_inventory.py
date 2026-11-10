import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestInventory:
    """Kumpulan kasus uji fungsional untuk halaman inventori produk."""

    def test_add_to_cart_flow(self, driver):
        """Kasus Uji 1 (Add to Cart Flow):

        Lakukan login sebagai standard_user, tambahkan produk Backpack ke
        keranjang belanja, dan validasi bahwa badge keranjang belanja
        menunjukkan teks "1".
        """
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        # 1. Login sebagai standard_user
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        # 2. Tambahkan Backpack ke keranjang
        inventory_page.add_backpack_to_cart()

        # 3. Assertion: Validasi badge keranjang belanja menampilkan teks "1"
        actual_badge_text = inventory_page.get_cart_badge_count()
        assert actual_badge_text == "1", (
            f"Jumlah keranjang tidak sesuai. Diharapkan '1', tetapi "
            f"diterima '{actual_badge_text}'"
        )

    def test_logout_flow(self, driver):
        """Kasus Uji 2 (Logout Flow):

        Setelah berada di halaman inventori, klik menu burger, pilih Logout, dan
        gunakan Assertion untuk membuktikan bahwa pengguna berhasil dialihkan
        kembali ke URL utama login serta tombol login kembali tampil.
        """
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        # 1. Login terlebih dahulu untuk masuk ke inventori
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        # 2. Eksekusi alur Logout
        inventory_page.logout()

        # 3. Wait & Assertions
        # Menunggu proses redirect URL selesai (memastikan URL bukan inventory.html lagi)
        WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/"))

        actual_url = login_page.get_current_url()

        # Assertion 1: Validasi URL kembali dialihkan ke alamat utama login
        assert actual_url.rstrip("/") == "https://www.saucedemo.com", (
            f"URL setelah logout tidak sesuai. Berada di '{actual_url}'"
        )

        # Assertion 2: Validasi respons DOM (tombol login kembali tampil)
        assert login_page.find_element(login_page.LOGIN_BUTTON).is_displayed(), (
            "Tombol login tidak tampil setelah proses logout!"
        )
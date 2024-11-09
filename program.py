import json
import pwinput
from prettytable import PrettyTable
from datetime import datetime
import os

# buka file JSON
json_path = r"C:\Users\user\DDS 1\data.json"

# prsing data JSON
with open(json_path, "r") as jsondatabase:
    data = json.load(jsondatabase)

def simpan_json(data):
    with open("data.json", "w") as sondatabase:
        json.dump(data, sondatabase, indent=4)

#Keluar program
def keluar_program():
    print("\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("Terima Kasih sudah menggunakan aplikasi kami!")
    print("====Kami Tunggu Kedatangan Kakak Lagi ^w^====")
    exit()

#Menu Utama
def menu_utama():
    while True:
        try:
            print("\n^^^^^^^^PROGRAM SEWA KONSOL GAME^^^^^^^^^")
            print("=========+++=+= Menu Utama =+=+++========")
            print("1. Registrasi")
            print("2. Masuk")
            print("3. Keluar")
            pilihan = int(input("Silahkan pilih menu (1-3): "))
            print("=========================================")
            if pilihan == 1:
                registrasi_user()
            elif pilihan == 2:
                masuk_user()
            elif pilihan == 3:
                keluar_program()
            else:
                print("Masukkan angka yang sesuai ya kak")
        except ValueError:
            print("Silahkan masukkan angka ya.")
        except KeyboardInterrupt:
            print("\nKakak salah input, silahkan mengulangi")

#Registrasi
def registrasi_user():
    while True:
        try:
            print("\n============ Registrasi ================")
            username = input("Masukkan username (huruf): ")
            password = pwinput.pwinput("Masukkan password: ").strip()
            print("========================================")
            for user in data["user"]:
                if user["username"] == username:
                    print("Username sudah terdaftar. Silahkan coba username lain.")
                    break
                elif not username.isalpha():
                    print("Kesalahan pada username. Silahkan coba lagi.")
                    break
                elif not password:
                    print("Password tidak boleh kosong. Silahkan coba lagi.")
                    break
            else:
                for admin in data["admin"]:
                    if admin["username"] == username:
                        print("Username sudah terdaftar. Silahkan coba username lain.")
                        break
                else:
                    data["user"].append({"username": username, "pw": password, "saldo": 0})
                    simpan_json(data)
                    print("Registrasi berhasil!")
                    menu_utama()
                    return
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nKakak salah input, silahkan mengulang")


#Login
def masuk_user():
    while True:
        try:
            print("\n=============== Login ==================")
            username = input("Masukkan username: ")
            password = pwinput.pwinput("Masukkan password: ")
            print("========================================")
            for user in data["user"]:
                if user["username"] == username and user["pw"] == password:
                    print(f"Selamat datang, User {username}!")
                    menu_user(user)
                    return  
            for admin in data["admin"]:
                if admin["username"] == username and admin["pw"] == password:
                    print(f"Selamat datang, Admin {username}!")
                    menu_admin()
                    return
            print("Username atau password kakak salah. \nKembali ke menu utama.")
            return
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nKakak salah input, silahkan mengulang")



#Fungsi Read
def tampil_produk():
    tabel = PrettyTable()
    tabel.field_names = ["nomor", "Produk", "Harga sewa/hari", "Status Barang"]
    tabel.clear_rows()
    for produk in data["produk"]:
        tabel.add_row([produk["nomor"], produk["nama"], produk["harga"], produk["status barang"]])
    print(tabel)

#Menu admin
def menu_admin():
    while True:
        print("\n****** Menu Admin *****")
        print("1. Tambah produk")
        print("2. Tampilkan produk")
        print("3. Ubah syarat produk")
        print("4. Hapus produk")
        print("5. Logout")
        print("***********************")
        try:
            pilih = int(input("Masukkan pilihan admin: "))
            if pilih == 1:
                tambah_produk()
            elif pilih == 2:
                tampil_produk()
            elif pilih == 3:
                ubah_produk()
            elif pilih == 4:
                hapus_produk()
            elif pilih == 5:
                print("Logout berhasil")
                menu_utama()
                return
            else:
                print("Masukkan angka yang sesuai ya min")
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nAdmin salah input, silahkan mengulang")

#Fungsi Create
def tambah_produk():
    tampil_produk()
    while True:
        try:
            print("\n======================== Tambahkan Produk =========================")
            nomor = str(len(data["produk"]) + 1) 
            nama = input("Masukkan nama produk: ")
            harga = int(input("Masukkan harga sewa per hari (IDR): "))
            status = int(input("Pilih status barang \n1. Tersedia \n2. Tidak Tersedia: "))
            print("====================================================================")
            if status == 1:
                status = "Tersedia"
            elif status == 2:
                status = "Tidak Tersedia"
            else:
                print("Pilih 1 atau 2 aja ya min")
                tambah_produk()
                return
            tambahan = {
                "nomor": nomor,
                "nama": nama,
                "harga": harga,
                "status barang": status
            }
            data["produk"].append(tambahan)
            simpan_json(data)
            print("\nProduk berhasil ditambahkan!")
            tampil_produk() 
            while True:
                pilih = input("\nApakah ingin menambah produk lagi? (y/n): ")
                if pilih.lower() == 'n':
                    menu_admin()
                    return
                elif pilih.lower() == 'y':
                    break
                else:
                    ("Input 'y' atau 'n" )
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nAdmin salah input, silahkan mengulang")

#Fungsi update produk
def ubah_produk():
    tampil_produk()    
    while True:
        try:
            print("\n=================== Perbarui Produk ===================")
            nomor = int(input("Masukkan Nomor produk yang ingin dirubah: "))
            if 0 < nomor <= len(data["produk"]):
                produk = data["produk"][nomor - 1]
                print("Apa yang ingin admin perbarui?")
                print("1. Nama Produk")
                print("2. Harga Sewa")
                pilihan = int(input("Masukkan pilihan (1/2): "))
                if pilihan == 1:
                    nama_baru = input("Masukkan nama produk baru: ")
                    if nama_baru.strip() == "":
                        print("Nama produk tidak boleh kosong!")
                        continue
                    produk["nama"] = nama_baru
                    print("Nama produk berhasil diperbarui!")
                elif pilihan == 2:
                    harga_baru = int(input("Masukkan harga sewa baru (IDR): "))
                    if harga_baru <= 0:
                            print("Harga sewa harus lebih besar dari 0.")
                            continue
                    produk["harga"] = harga_baru
                    print("Harga produk berhasil diperbarui!")
                else:
                    print("Masukkan angka yang sesuai")
                    continue
                simpan_json(data)
                tampil_produk()
                while True:
                    pilih = input("\nApakah ingin memperbarui produk lagi? (y/n): ")
                    if pilih.lower() == 'n':
                        menu_admin()
                        return
                    elif pilih.lower() == 'y':
                        break
                    else:
                        ("Input 'y' atau 'n'" )
            else:
                print("Produk tidak tersedia")
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nAdmin salah input, silahkan mengulang")

#Fungsi delete
def hapus_produk():
    tampil_produk()
    while True:
        try:
            print("\n==================== Hapus Produk =======================")
            nomor = int(input("\nMasukkan nomor produk yang ingin dihapus: "))
            if 1 <= nomor <= len(data["produk"]):
                index = nomor - 1
                produk_dihapus = data["produk"][index]

                while True:
                    yakin = input(f"Yakin ingin menghapus produk '{produk_dihapus['nama']}'? (y/n): ")
                    if yakin.lower() == 'y':
                        data["produk"].pop(index)
                        print(f"Produk '{produk_dihapus['nama']}' berhasil dihapus!")
                        for i, produk in enumerate(data["produk"], start=1):
                            produk["nomor"] = i
                        simpan_json(data)
                        tampil_produk()
                        break
                    elif yakin.lower() == 'n':
                        print(f"Penghapusan produk '{produk_dihapus['nama']}' dibatalkan.")
                        break
                    else:
                        print("Input 'y' atau 'n'")

                while True:
                    pilih = input("\nApakah ingin hapus produk lagi? (y/n): ")
                    if pilih.lower() == 'n':
                        menu_admin()
                        return
                    elif pilih.lower() == 'y':
                        break
                    else:
                        print("Input 'y' atau 'n'")
            else:
                print("Nomor produk tidak valid.")
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("Admin salah input, silahkan mengulang")

#Menu user
def menu_user(user):
    while True:
        try:
            print("\n~~~~~~~~Menu User~~~~~~~~")
            print("1. Sewa Produk")
            print("2. Cek Akun E-Money")
            print("3. Kembalikan Produk")
            print("4. Cek barang yang disewa")
            print("5. Log out")
            pilihan = int(input("Pilih menu (1-5): "))
            if pilihan == 1:
                sewa_produk(user)
            elif pilihan == 2:
                akun_emoney(user)
            elif pilihan == 3:
                kembalikan_produk(user)
            elif pilihan == 4:
                lihat_sewa(user)
            elif pilihan == 5:
                menu_utama()
            else:
                print("Masukkan angka yang sesuai ya kak")
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nKakak salah input, silahkan mengulang")

#Proses transaksi
def sewa_produk(user):
    while True:
        try:
            print("\n~~~~~~~~~~~~~~~~Ayo Pilih~~~~~~~~~~~~~~~~~")
            print("Pilih opsi pengurutan produk:")
            print("1. Berdasarkan Nama (A-Z)")
            print("2. Berdasarkan Harga (Termurah-Termahal)")
            print("3. Berdasarkan Ketersediaan")
            print("4. Pilih Produk Tanpa Urut")
            pilihan_sort = int(input("Masukkan pilihan (1-4): "))
            produk_urut = data["produk"][:]
            
            if pilihan_sort == 1:
                produk_urut = sorted(data["produk"], key=lambda x: x["nama"])
            elif pilihan_sort == 2:
                produk_urut = sorted(data["produk"], key=lambda x: x["harga"])
            elif pilihan_sort == 3:
                produk_urut = sorted(data["produk"], key=lambda x: x["status barang"])
            elif pilihan_sort == 4:
                produk_urut = data["produk"]
            else:
                print("Pilihan tidak valid. Ulangi ya kak")
                continue

            tabel = PrettyTable()
            tabel.field_names = ["Nomor", "Produk", "Harga sewa/hari", "Status Barang"]
            tabel.clear_rows()
            for idx, produk in enumerate(produk_urut, start=1):
                tabel.add_row([idx, produk["nama"], produk["harga"], produk["status barang"]])
            print(tabel)

            jumlah_pinjaman = sum(1 for transaksi in data["transaksi"] if transaksi["username"] == user["username"])
            if jumlah_pinjaman >= 2:
                print("Kakak sudah menyewa maksimal 2 produk. Kembali ke menu user.")
                return

            while True:
                try:
                    nomor_produk = int(input("Masukkan nomor produk yang ingin disewa: "))
                    if 1 <= nomor_produk <= len(produk_urut):
                        produk_ditemukan = produk_urut[nomor_produk - 1]
                        break
                    else:
                        print("Nomor produk tidak ditemukan. Silakan masukkan nomor yang benar ya kak.")
                except ValueError:
                    print("Input harus berupa angka. Silakan coba lagi.")

            hari_sewa = int(input("Masukkan jumlah hari sewa: "))

            if produk_ditemukan["status barang"] == "tersedia":
                biaya_sewa = produk_ditemukan["harga"] * hari_sewa
                if user["saldo"] >= biaya_sewa:
                    user["saldo"] -= biaya_sewa
                    tanggal_sewa = datetime.now().strftime("%Y-%m-%d")
                    data["transaksi"].append({
                        "username": user["username"],
                        "produk": produk_ditemukan["nama"],
                        "harga": produk_ditemukan["harga"],
                        "hari_sewa": hari_sewa,
                        "biaya_total": biaya_sewa,
                        "tanggal_sewa": tanggal_sewa
                    })
                    produk_ditemukan["status barang"] = "tidak tersedia"
                    simpan_json(data)
                    print(f"\nTransaksi berhasil! Kakak telah menyewa {produk_ditemukan['nama']} selama {hari_sewa} hari dengan biaya total Rp {biaya_sewa}.")

                    print("\n============ INVOICE ============")
                    print("       RENTAL KONSOL GAME")
                    print("==================================")
                    print(f"  Nama Pelanggan   : {user['username']}")
                    print("==================================")
                    print(f"  Produk           : {produk_ditemukan['nama']}")
                    print(f"  Lama Sewa        : {hari_sewa} hari")
                    print(f"  Biaya per Hari   : Rp {produk_ditemukan['harga']}")
                    print("----------------------------------")
                    print(f"  Total Biaya      : Rp {biaya_sewa}")
                    print("==================================")
                    print(f"  Tanggal Sewa     : {tanggal_sewa}")
                    print("==================================")
                    print("  Terima kasih telah menggunakan")
                    print("      layanan rental kami!")
                    print("==================================")
                    while True:
                        pilih = input("\nApakah kakak ingin menyewa produk lagi? (y/n): ")
                        if pilih.lower() == 'n':
                            menu_user(user)
                            return
                        elif pilih.lower() == 'y':
                            break
                        else:
                            print("Input 'y' atau 'n'")
                else:
                    print("Saldo Kakak tidak cukup.")
                    akun_emoney(user)
            else:
                print("Produk tidak tersedia untuk disewa.")
                return
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nKakak salah input, silahkan mengulang")


def kembalikan_produk(user):
    while True:
        print("\n=== Pengembalian Produk ===")
        transaksi_user = [transaksi for transaksi in data["transaksi"] if transaksi["username"] == user["username"]]
        if not transaksi_user:
            print("Kakak tidak memiliki produk yang disewa.")
            menu_user(user)
            return 
        
        tabel = PrettyTable()
        tabel.field_names = ["Nomor", "Produk", "Tanggal Sewa", "Hari Sewa"]
        tabel.clear_rows()
        for idx, transaksi in enumerate(transaksi_user, start=1):
            tabel.add_row([idx, transaksi["produk"], transaksi["tanggal_sewa"], transaksi["hari_sewa"]])
        print(tabel)
        try:
            nomor_produk = int(input("Masukkan nomor produk yang ingin dikembalikan: "))
            if 1 <= nomor_produk <= len(transaksi_user):
                produk_dikembalikan = transaksi_user[nomor_produk - 1]
                tanggal_sewa = datetime.strptime(produk_dikembalikan["tanggal_sewa"], "%Y-%m-%d")
                tanggal_kembali = datetime.now()
                selisih_hari = (tanggal_kembali - tanggal_sewa).days
                
                denda_per_hari = 3000
                total_denda = 0
                keterlambatan = 0
                if selisih_hari > produk_dikembalikan["hari_sewa"]:
                    keterlambatan = selisih_hari - produk_dikembalikan["hari_sewa"]
                    total_denda = keterlambatan * denda_per_hari
                    print(f"Terdapat keterlambatan {keterlambatan} hari. Denda yang harus dibayar: Rp {total_denda}.")
                    konfirmasi_denda = input("Apakah kakak ingin membayar denda? (y/n): ")
                    if konfirmasi_denda.lower() != 'y':
                        print("Pengembalian dibatalkan.")
                        break

                if total_denda > 0:
                    if user["saldo"] >= total_denda:
                        user["saldo"] -= total_denda
                        print(f"Sisa saldo kakak: Rp {user['saldo']}.")
                    else:
                        print("Saldo tidak cukup untuk membayar denda.")
                        akun_emoney(user)
                        return
                for produk in data["produk"]:
                    if produk["nama"] == produk_dikembalikan["produk"]:
                        produk["status barang"] = "tersedia"
                        break
                data["transaksi"].remove(produk_dikembalikan)
                
                simpan_json(data)
                print(f"Produk '{produk_dikembalikan['produk']}' berhasil dikembalikan!")
                
                while True:
                    pilih = input("\nApakah kakak ingin mengembalikan produk lagi? (y/n): ")
                    if pilih.lower() == 'n':
                        menu_user(user)
                        return
                    elif pilih.lower() == 'y':
                        break
                    else:
                        print("Input 'y' atau 'n'")
            else:
                print("Nomor produk tidak valid.")
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nKakak salah input, silahkan mengulang")


#Akun e-money
def akun_emoney(user):
    while True:
        try:
            print("\n=== Menu Akun E-Money ===")
            print("1. Cek Saldo")
            print("2. Isi Saldo")
            print("3. Kembali ke Menu User")
            pilihan = int(input("Pilih menu (1-3): "))
            if pilihan == 1:
                cek_saldo(user)
            elif pilihan == 2:
                isi_saldo(user)
            elif pilihan == 3:
                menu_user(user)
            else:
                print("Pilihan tidak valid.")
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nKakak salah input, silahkan mengulang")

#cek saldo
def cek_saldo(user):
    print(f"\n=== Cek Saldo ===")
    saldo = "{:,.0f}".format(user['saldo']).replace(',', '.')
    print(f"Saldo kakak: Rp {saldo}")

#Isi saldo
def isi_saldo(user):
    while True:
        try:
            jumlah = int(input("Masukkan jumlah saldo yang ingin diisi: Rp "))
            user['saldo'] += jumlah
            simpan_json(data)
            print(f"Saldo kakak berhasil diisi. Saldo sekarang: Rp {user['saldo']}")
            return
        except ValueError:
            print("Sepertinya ada kesalahan, silahkan masukkan lagi.")
        except KeyboardInterrupt:
            print("\nKakak salah input, silahkan mengulang")

def lihat_sewa(user):
    print("\n=== Produk Yang Disewa ===")
    transaksi_user = [transaksi for transaksi in data["transaksi"] if transaksi["username"] == user["username"]]
    if not transaksi_user:
        print("Kakak tidak memiliki produk yang disewa.")
        return
    
    tabel = PrettyTable()
    tabel.field_names = ["Nomor", "Produk", "Tanggal Sewa", "Hari Sewa"]
    tabel.clear_rows()
    for idx, transaksi in enumerate(transaksi_user, start=1):
        tabel.add_row([idx, transaksi["produk"], transaksi["tanggal_sewa"], transaksi["hari_sewa"]])
    print(tabel)

#Menu
menu_utama()
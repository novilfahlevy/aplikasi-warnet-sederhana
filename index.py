from prettytable import PrettyTable
import csv

# Simulasi database
database = {
  'pengguna': [
    { 'username': 'admin', 'password': 'admin' },
    { 'username': 'novil', 'password': '12345' }
  ],
  'PC': ['1', '2', '3', '4', '5', '6'],
  'billing': [
    { 'PC': '1', 'dari': '12:00', 'sampai': '14:00', 'harga': 3000 }
  ]
}

# Pilih tabel dari database
def select(table) :
  return database.get(table)

# Masukan data ke database
def insert(table, data) :
  database.get(table).append(data)

def saldo() :
  jumlah = 0

  billing = select('billing')
  for i in range(len(billing)) :
    jumlah += billing[i].get('harga')

  return jumlah

# Login, jika berhasil akan mereturn True
def login() :
  login_berhasil = False

  while login_berhasil == False :
    username = input('Username : ')
    password = input('Password : ')

    for user in select('pengguna') :
      if user.get('username') == username and user.get('password') == password :
        login_berhasil = True
        return login_berhasil
    
    print('Username atau password yang anda masukan salah\n')

# Daftar menu, sekaligus me-return menu yang diinput
def daftar_menu() :
  print('\nMenu')
  print('[1] Daftar PC')
  print('[2] Daftar Billing')
  print('[3] Tambah Billing')
  print('[4] Hapus Billing')
  print('[5] Tambah Akun')
  print('[6] Laporan')
  print('[7] Selesai')
  print('[8] Logout')
  print(f'Saldo Rp {saldo()}')

  menu = int(input('Masukan menu yang ingin dipilih : '))
  print()
  return menu

# Daftar PC
def daftar_PC() :
  print('Daftar PC :')

  table = PrettyTable()
  table.field_names = ['No', 'PC', 'Status']

  pc = select('PC');
  for i in range(len(pc)) :
    if pc[i] not in PC_tersedia() :
      table.add_row([i + 1, f'PC {pc[i]}', 'Billed'])
    else :
      table.add_row([i + 1, f'PC {pc[i]}', 'Free'])

  print(table)

# Daftar billing
def daftar_billing() :
  print('Daftar Billing :')

  table = PrettyTable()
  table.field_names = ['No', 'PC', 'Waktu', 'Harga']

  billing = select('billing');
  for i in range(len(billing)) :
    pc = billing[i].get('PC')
    dari = billing[i].get('dari')
    sampai = billing[i].get('sampai')
    harga = billing[i].get('harga')

    table.add_row([i + 1, f'PC {pc}', f'{dari}-{sampai}', f'Rp {harga}'])

  print(table)

# Daftar PC yang tersedia, dengan membandingkan tabel PC dan billing
def PC_tersedia() :
  pc_terpakai = list(map(lambda billing: billing.get('PC'), select('billing')))
  return list(filter(lambda pc: pc not in pc_terpakai, select('PC')))

# Tambah billing
def tambah_billing() :
  table_PC_tersedia = PrettyTable()
  table_PC_tersedia.field_names = ['No', 'PC']

  pc_tersedia = PC_tersedia()
  for i in range(len(pc_tersedia)) :
    table_PC_tersedia.add_row([i + 1, f'PC {pc_tersedia[i]}'])

  print('PC yang tersedia : ')
  print(table_PC_tersedia)

  pc = int(input('PC (No) : '))
  dari = input('Dari jam : ')
  sampai = input('Sampai jam : ')
  harga = int(input('Harga : '))

  # Jika nomor PC salah, coba lagi
  if pc - 1 < len(pc_tersedia) :
    insert('billing', { 'PC': pc_tersedia[pc - 1], 'dari': dari, 'sampai': sampai, 'harga': harga })
    print('Billing berhasil ditambah')
  else :
    print('Mohon pilih PC yang tersedia\n')
    return tambah_billing()

# Hapus billing
def hapus_billing() :
  daftar_billing()

  billing = int(input('Pilih billing yang ingin dihapus (No) : '))

  # Jika nomor billing salah, coba lagi
  if billing - 1 < len(database['billing']) :
    del database['billing'][billing - 1]
    print('Billing berhasil dihapus\n')
  else :
    print('Mohon pilih billing yang tersedia\n')
    return hapus_billing()

# Tambah akun (register)
def tambah_akun() :
  print('Tambah Akun Baru')
  username = input('Username : ')
  password = input('Password : ')

  for user in select('pengguna') :
    if user.get('username') == username :
      print('Username sudah ada\n')
      return tambah_akun()
  
  print('Pengguna berhasil ditambahkan')
  insert('pengguna', { 'username': username, 'password': password })

def laporan() :
  # sumber https://www.codegrepper.com/code-examples/python/save+list+in+csv+file+python

  with open('laporan.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
      
    write.writerow(['PC', 'Waktu', 'Harga'])
    write.writerows(
      list(
        map(lambda b: ['PC ' + b.get('PC'), b.get('dari') + '-' + b.get('sampai'), b.get('harga')], select('billing'))
      )
    )

def app() :
  if login() : # Jika berhasil login
    aplikasi_selesai = False

    while aplikasi_selesai == False :
      menu = daftar_menu()

      if menu == 1 :
        daftar_PC()
      elif menu == 2 :
        daftar_billing()
      elif menu == 3 :
        tambah_billing()
      elif menu == 4 :
        hapus_billing()
      elif menu == 5 :
        tambah_akun()
      elif menu == 6 :
        laporan()
      elif menu == 7 :
        aplikasi_selesai = True
      elif menu == 8 :
        return app()
      else :
        print('Masukan pilihan yang tersedia')
  
  print('Sampai nanti ^^')

app()

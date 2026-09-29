-- =========================================================
-- DATABASE LOGIKA FUZZY
-- DOMAIN USIA 0 - 150 TAHUN
-- =========================================================

CREATE DATABASE IF NOT EXISTS logika_fuzzy;

USE logika_fuzzy;


-- =========================================================
-- 1. TABEL DOMAIN USIA BAYI
-- Parameter: (0, 0, 5, 6)
-- =========================================================

CREATE TABLE IF NOT EXISTS tb_domain_usia_bayi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batas_bawah INT NOT NULL,
    batas_atas INT NOT NULL,
    fungsi VARCHAR(100) NOT NULL
);

INSERT INTO tb_domain_usia_bayi
(batas_bawah, batas_atas, fungsi)
VALUES
(0, 5, '1'),
(5, 6, 'trapesium_down_bayi'),
(6, 150, '0');


-- =========================================================
-- 2. TABEL DOMAIN USIA ANAK
-- Parameter: (5, 6, 11, 12)
-- =========================================================

CREATE TABLE IF NOT EXISTS tb_domain_usia_anak (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batas_bawah INT NOT NULL,
    batas_atas INT NOT NULL,
    fungsi VARCHAR(100) NOT NULL
);

INSERT INTO tb_domain_usia_anak
(batas_bawah, batas_atas, fungsi)
VALUES
(0, 5, '0'),
(5, 6, 'trapesium_up_anak'),
(6, 11, '1'),
(11, 12, 'trapesium_down_anak'),
(12, 150, '0');


-- =========================================================
-- 3. TABEL DOMAIN USIA REMAJA
-- Parameter: (9, 10, 19, 20)
-- =========================================================

CREATE TABLE IF NOT EXISTS tb_domain_usia_remaja (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batas_bawah INT NOT NULL,
    batas_atas INT NOT NULL,
    fungsi VARCHAR(100) NOT NULL
);

INSERT INTO tb_domain_usia_remaja
(batas_bawah, batas_atas, fungsi)
VALUES
(0, 9, '0'),
(9, 10, 'trapesium_up_remaja'),
(10, 19, '1'),
(19, 20, 'trapesium_down_remaja'),
(20, 150, '0');


-- =========================================================
-- 4. TABEL DOMAIN USIA PEMUDA
-- Parameter: (14, 15, 24, 25)
-- =========================================================

CREATE TABLE IF NOT EXISTS tb_domain_usia_pemuda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batas_bawah INT NOT NULL,
    batas_atas INT NOT NULL,
    fungsi VARCHAR(100) NOT NULL
);

INSERT INTO tb_domain_usia_pemuda
(batas_bawah, batas_atas, fungsi)
VALUES
(0, 14, '0'),
(14, 15, 'trapesium_up_pemuda'),
(15, 24, '1'),
(24, 25, 'trapesium_down_pemuda'),
(25, 150, '0');


-- =========================================================
-- 5. TABEL DOMAIN USIA DEWASA
-- Parameter: (19, 20, 65, 66)
-- =========================================================

CREATE TABLE IF NOT EXISTS tb_domain_usia_dewasa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batas_bawah INT NOT NULL,
    batas_atas INT NOT NULL,
    fungsi VARCHAR(100) NOT NULL
);

INSERT INTO tb_domain_usia_dewasa
(batas_bawah, batas_atas, fungsi)
VALUES
(0, 19, '0'),
(19, 20, 'trapesium_up_dewasa'),
(20, 65, '1'),
(65, 66, 'trapesium_down_dewasa'),
(66, 150, '0');


-- =========================================================
-- 6. TABEL DOMAIN USIA LANSIA
-- Parameter: (64, 65, 150, 150)
-- =========================================================

CREATE TABLE IF NOT EXISTS tb_domain_usia_lansia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    batas_bawah INT NOT NULL,
    batas_atas INT NOT NULL,
    fungsi VARCHAR(100) NOT NULL
);

INSERT INTO tb_domain_usia_lansia
(batas_bawah, batas_atas, fungsi)
VALUES
(0, 64, '0'),
(64, 65, 'trapesium_up_lansia'),
(65, 150, '1');


-- =========================================================
-- CEK DATA
-- =========================================================

SELECT * FROM tb_domain_usia_bayi;
SELECT * FROM tb_domain_usia_anak;
SELECT * FROM tb_domain_usia_remaja;
SELECT * FROM tb_domain_usia_pemuda;
SELECT * FROM tb_domain_usia_dewasa;
SELECT * FROM tb_domain_usia_lansia;
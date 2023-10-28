-- query 1 : Berapa rata-rata umur customer jika dilihat dari marital statusnya ?

SELECT 
	CASE 
        WHEN "Marital Status" = '' THEN '(blank)'
        ELSE "Marital Status"
    END AS "Status Pernikahan",
    avg(age) "Rata-Rata Umur",
	ROUND(avg(age), 0) "Rata-Rata Umur (Dibulatkan)" -- rata-ratanya dibulatkan menjadi angka integer 
FROM customer
GROUP BY "Marital Status";

-- query 2 : Berapa rata-rata umur customer jika dilihat dari gender nya ?

SELECT 
	CASE 
        WHEN gender = 0 THEN 'Perempuan'
        WHEN gender = 1 THEN 'Laki-Laki'
        ELSE 'Lainnya'
    END AS "Jenis Kelamin",
    avg(age) "Rata-Rata Umur",
	ROUND(avg(age), 0) "Rata-Rata Umur (Dibulatkan)" -- rata-ratanya dibulatkan menjadi angka integer 
FROM customer
group BY gender;

-- query 3 : Tentukan nama store dengan total quantity terbanyak!

SELECT
    s.StoreName,
    SUM(t.Qty) AS TotalQuantity
FROM Store s
JOIN Transaction t ON s.StoreID = t.StoreID
GROUP BY s.StoreName
ORDER BY TotalQuantity DESC
LIMIT 1;

-- query 4 : Tentukan nama produk terlaris dengan total amount terbanyak!

SELECT
    p.ProductName,
    SUM(t."Total Amount") AS TotalAmount
FROM Product p
JOIN Transaction t ON p.ProductID = t.ProductID
GROUP BY p.ProductName
ORDER BY TotalAmount DESC
LIMIT 1;
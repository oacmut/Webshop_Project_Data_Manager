from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import os
import urllib.request
import pandas as pd


project_folder = "C:/Projektjeim"
if not os.path.exists(project_folder):
    os.makedirs(project_folder)


image_folder = os.path.join(project_folder, "fressnapf_images")
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

service = Service()
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)


start_url = "https://www.fressnapf.hu/"
driver.get(start_url)
print("Kezdőoldal betöltve:", start_url)


time.sleep(4)


last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
print("Kezdőoldal görgetés befejezve")


soup = BeautifulSoup(driver.page_source, "html.parser")


main_categories = []
menu_item = soup.find("li", class_="menu-item-429")
if menu_item:
    print("menu-item-429 megtalálva")
    submenu = menu_item.find("ul", class_="sub-menu")
    if submenu:
        print("Submenu megtalálva")
        links = submenu.find_all("a")
        print(f"Submenu linkek száma: {len(links)}")
        for link in links:
            href = link.get("href", "")
            if href:
                if href.startswith("http"):
                    full_url = href
                else:
                    full_url = "https://www.fressnapf.hu" + href if href.startswith("/") else "https://www.fressnapf.hu/" + href
                slug = full_url.split("/")[-2] if full_url.endswith("/") else full_url.split("/")[-1]
                name = link.get_text(strip=True)  
                main_categories.append({"url": full_url, "slug": slug, "name": name})
                print(f"Fő kategória link: {full_url}, Slug: {slug}, Név: {name}")
    else:
        print("Nem található submenu a menu-item-429 alatt!")
else:
    print("Nem található a menu-item-429 osztályú elem!")

print("Talált fő kategóriák száma:", len(main_categories))
if not main_categories:
    print("Hiba: Nem találtam fő kategóriákat, ellenőrizd az oldal szerkezetét!")

all_subcategory_links = []
subcategory_slugs = []
subcategory_to_main_category = []  
base_url = "https://www.fressnapf.hu"
for main_category in main_categories:
    driver.get(main_category["url"]) 
    print(f"Fő kategória oldal betöltve: {main_category['url']}")

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("Fő kategória görgetés befejezve")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    category_cards = soup.find_all("div", class_=lambda x: x and "category-card" in x)  # Az összes alkategória
    for card in category_cards:
        link = card.find("a")
        if link and "href" in link.attrs:
            href = link["href"]
            if href.startswith("http"):
                full_url = href
            else:
                full_url = base_url + href if href.startswith("/") else base_url + "/" + href
            slug = full_url.split("/")[-2] if full_url.endswith("/") else full_url.split("/")[-1]
            all_subcategory_links.append(full_url)
            subcategory_slugs.append(slug)
            subcategory_to_main_category.append(main_category["slug"]) 
            print(f"Alkategória link: {full_url}, Slug: {slug}, Főkategória: {main_category['slug']}")

print("Összes talált alkategória száma:", len(all_subcategory_links))


main_data = []
categories_data = []
choices_data = [] 
infotabs_data = []
type_properties_data = []
category_tree_data = []
product_counter = 1


if main_categories:
    for main_category in main_categories:
        category_tree_data.append({
            "SLUG": main_category["slug"],
            "PARENT SLUG": "",
            "Category Name": main_category["name"]
        })
else:
    print("Hiba: A Category Tree nem töltődik fel, mert a main_categories üres!")


valid_product_slugs = set()

for idx, subcategory_url in enumerate(all_subcategory_links):
    driver.get(subcategory_url)
    print("Alkategória oldal betöltve:", subcategory_url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("Görgetés befejezve")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    product_links = soup.find_all("a", class_="product_link_normal")
    subcategory_slug = subcategory_slugs[idx] 
    main_category_slug = subcategory_to_main_category[idx]  

    product_type = subcategory_slug.replace(main_category_slug, "").capitalize()

    for i in range(0, len(product_links), 2):
        link = product_links[i]
        title = link.get("title", "Nincs title attribútum")
        if title == "Nincs title attribútum":
            continue

        
        category_short = main_category_slug[:3].upper()
        name_short = "".join([word[:3] for word in title.split()[:2]]).upper()
        sku = f"FRSSNPF-{category_short}-{name_short}-{product_counter:03d}"
        slug = sku.lower()
        product_counter += 1

       
        parent_div = link.find_parent("div", class_="product__inner")
        price = "Nincs ár"
        if parent_div:
            price_tag = parent_div.find("span", class_="price-gross")
            price = price_tag.text.strip().replace(" Ft", "").replace(" ", "") + ",00 Ft" if price_tag else "0,00 Ft"

        
        image_tags = soup.find_all("img", class_=lambda x: x and "product__img" in x and "product-img" in x and "js-main-img")
        image_url = image_tags[i // 2].get("data-src", image_tags[i // 2].get("src", None)) if i // 2 < len(image_tags) else None
        image_name = f"{slug}.jpg"
        image_path = os.path.join(image_folder, image_name)
        if image_url:
            try:
                urllib.request.urlretrieve(image_url, image_path)
                print(f"Kép letöltve: {image_path}")
            except Exception as e:
                print(f"Hiba a kép letöltésekor (URL: {image_url}): {e}")

        main_data.append({
            "SLUG": slug,
            "Active": "YES",
            "Featured": "",
            "SKU": sku,
            "Name": title,
            "Product Type": product_type,
            "MSRP": "0,00 Ft",
            "Cost": "",
            "Price": price,
            "Manufacture": "",
            "Vendor": "",
            "Image": image_name,
            "Description": title,
            "Search Keywords": "",
            "Meta Title": "",
            "Meta Description": "",
            "Meta Keywords": "",
            "Tax Schedule": "",
            "Tax Excempt": "NO",
            "Weight": "0,0000000000",
            "Length": "0,0000000000",
            "Width": "0,0000000000",
            "Height": "0,0000000000",
            "Extra Ship Fee": "0,00 Ft",
            "Ship Mode": "ShipFromSite",
            "Non-Shipping Product": "NO",
            "Ships in a Separate Box": "NO",
            "Allow Reviews": "YES",
            "Minimum Qty": "0",
            "Inventory Mode": "AlwayInStock",
            "Inventory": "0",
            "Stock Out at": "0",
            "Low Stock at": "0",
            "Roles": "",
            "Searchable": "True"
        })


        valid_product_slugs.add(slug)


        categories_data.append({
            "PRODUCT SLUG": slug,
            "CATEGORIES SLUGS": main_category_slug
        })

categories_data = [row for row in categories_data if row["PRODUCT SLUG"] in valid_product_slugs]
print("Categories adatok száma szűrés után:", len(categories_data))

category_tree_data = [row for row in category_tree_data if row["SLUG"] and row["Category Name"]]
print("Category Tree adatok száma szűrés után:", len(category_tree_data))

choices_headers = ["PRODUCT SLUG", "CHOICE", "CHOICE TYPE", "SHARED", "CHOICE ITEMS"]
infotabs_headers = ["PRODUCT SLUG", "Tab Name", "Tab Description"]
type_properties_headers = ["PRODUCT SLUG", "Property Name", "Value"]

excel_path = os.path.join(project_folder, "fressnapf_hotcakes_import.xlsx")
with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
    pd.DataFrame(main_data).to_excel(writer, sheet_name="Main", index=False)
    pd.DataFrame(categories_data).to_excel(writer, sheet_name="Categories", index=False)
    pd.DataFrame(columns=choices_headers).to_excel(writer, sheet_name="Choices", index=False)
    pd.DataFrame(columns=infotabs_headers).to_excel(writer, sheet_name="Info Tabs", index=False)
    pd.DataFrame(columns=type_properties_headers).to_excel(writer, sheet_name="Type Properties", index=False) 
    pd.DataFrame(category_tree_data).to_excel(writer, sheet_name="Category Tree", index=False)
print(f"Excel mentve: {excel_path}")


driver.quit()

# Data Manager role - Fressnapf Scraper Project

Welcome to the **Fressnapf Scraper Project**, a Python-based web scraping solution designed to extract product data from the [Fressnapf Hungary website](https://www.fressnapf.hu/). This project was developed with the help of **Grok 3**, an AI tool by xAI, and serves as part of my university coursework for the **Systems Development and IT Project Management** subject. As the **Data Manager** in my team, I’ve overseen the data collection, cleaning, and preparation process to ensure compatibility with the DNN Hotcakes webshop module.

## Project Overview
The `scraper.py` script automates the extraction of product details (e.g., names, prices, images) across **all categories** on the Fressnapf site. The scraped data is organized into an Excel file tailored for import into the DNN Hotcakes e-commerce platform. This project showcases a practical application of web scraping, data management, and team collaboration.

| **Role**         | **Description**                       |
|-------------------|---------------------------------------|
| **Data Manager**  | I handle data scraping, cleaning, and structuring for the team. |

## Key Features
- Scrapes all product categories, subcategories, and items from Fressnapf.hu.
- Downloads product images and saves them in a designated folder.
- Generates an Excel file with sheets: `Main`, `Categories`, `Choices`, `Info Tabs`, `Type Properties`, and `Category Tree`.
- Handles dynamic content with Selenium scrolling and wait mechanisms.
- Ensures efficient data processing with duplicate prevention.

## Files in the Repository
| **File Name**                  | **Description**                                                                 |
|--------------------------------|---------------------------------------------------------------------------------|
| `scraper.py`                   | The main scraping script, crafted with Grok 3's assistance, covering all categories. |
| `fressnapf_hotcakes_import.xlsx` | The raw Excel output from `scraper.py`, almost ready for DNN Hotcakes import.         |
| `fressnapf_hotcakes_import_tisztitott.xlsx` | Cleaned Excel file, optimized for DNN Hotcakes webshop import.               |
| `bvins.xlsx`                   | Contains `ProductID` mappings and image references for image management.       |
| `image_folder_generator.py`    | Creates image folders and resizes images based on `bvins.xlsx` data.          |

## How It Works
1. **Scraping Process**: `scraper.py` navigates the Fressnapf site, scrolls to load all content, and extracts data from every category. Results are saved to an Excel file.
2. **Image Handling**: Images are downloaded using HTTP requests and stored in the `fressnapf_images` folder. The `image_folder_generator.py` script then organizes and resizes them.
3. **Data Preparation**: The raw Excel file is manually cleaned to produce `fressnapf_hotcakes_import_cleaned.xlsx` for seamless webshop integration.

## Prerequisites
- **Python**
- Required libraries: `selenium`, `beautifulsoup4`, `pandas`, `requests`, `webdriver_manager`
- A compatible web driver (e.g., ChromeDriver)
- Write permissions for `C:/Projektjeim` (adjust the path in the code if needed)
